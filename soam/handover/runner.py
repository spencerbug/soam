"""Fixture-only handover smoke runner with immutable artifacts and exact reproduction."""

import argparse
import json
import resource
import sys
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch

from soam.evaluation.provenance import capture
from soam.handover.data import generate_episode, load_episode
from soam.handover.evaluation import run_episode
from soam.handover.models import HandoverModel
from soam.handover.probes import run_probes
from soam.handover.protocol import (
    DOCUMENT,
    MANIFEST,
    ROOT,
    initialization_seed,
    load_protocol,
    sha256,
)


@dataclass(frozen=True)
class SmokeConfig:
    name: str = "handover-fixture-v1"
    split: str = "fixture"
    seed: int = 11
    episodes_per_condition: int = 1
    threads: int = 1
    max_cpu_seconds: int = 300
    max_rss_gib: int = 8

    def validate(self):
        if self.split != "fixture" or type(self.seed) is not int or self.seed != 11:
            raise ValueError("SOAM-034 runner is fixture-only, seed 11")
        if type(self.episodes_per_condition) is not int or self.episodes_per_condition not in (
            1,
            2,
        ):
            raise ValueError("fixture budget is one or two episodes per condition")
        if type(self.threads) is not int or self.threads != 1:
            raise ValueError("v1 uses one Torch thread")
        if type(self.max_cpu_seconds) is not int or not 0 < self.max_cpu_seconds <= 14400:
            raise ValueError("invalid CPU budget")
        if type(self.max_rss_gib) is not int or not 0 < self.max_rss_gib <= 8:
            raise ValueError("invalid RSS budget")
        return self

    def to_dict(self):
        return asdict(self)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def save_arrays(path, arrays):
    np.savez_compressed(path, **{k: v.detach().cpu().numpy() for k, v in arrays.items()})


def peak_rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == "darwin" else value * 1024


class Budget:
    def __init__(self, config):
        self.config = config
        self.cpu_started = time.process_time()

    def check(self):
        if time.process_time() - self.cpu_started > self.config.max_cpu_seconds:
            raise TimeoutError("smoke CPU budget exhausted")
        if peak_rss_bytes() > self.config.max_rss_gib * 1024**3:
            raise MemoryError("smoke process peak-RSS budget exhausted")


def provenance(config):
    result = capture(ROOT, config)
    for path in (MANIFEST, DOCUMENT):
        result["source_files"][str(path.relative_to(ROOT))] = sha256(path)
    import hashlib

    result["source_sha256"] = hashlib.sha256(
        json.dumps(result["source_files"], sort_keys=True).encode()
    ).hexdigest()
    result.update(
        artifact_schema_version=1,
        protocol_sha256=sha256(DOCUMENT),
        manifest_sha256=sha256(MANIFEST),
        torch_threads=torch.get_num_threads(),
        deterministic_algorithms=torch.are_deterministic_algorithms_enabled(),
        default_dtype=str(torch.get_default_dtype()),
        device="cpu",
        dtype="float32",
        diagnostic_dtype="float64",
        fixture_only=True,
        training_exposure=0,
        development_exposure=0,
        confirmation_exposure=0,
        initialization_seeds={
            name: initialization_seed(config.seed, name)
            for name in ("selector", "G2", "GS24", "GS9")
        },
    )
    return result


def compare_runs(original, repeat):
    original, repeat = Path(original), Path(repeat)
    for filename in ("config.json", "manifest.json", "deterministic.json", "probes.json"):
        if json.loads((original / filename).read_text()) != json.loads(
            (repeat / filename).read_text()
        ):
            raise AssertionError(f"reproduction differs: {filename}")
    before = json.loads((original / "provenance.json").read_text())
    after = json.loads((repeat / "provenance.json").read_text())
    if before["source_sha256"] != after["source_sha256"]:
        raise AssertionError("source fingerprints differ")
    first_files = sorted(p.relative_to(original) for p in original.rglob("*.npz"))
    second_files = sorted(p.relative_to(repeat) for p in repeat.rglob("*.npz"))
    if first_files != second_files:
        raise AssertionError("reproduction array inventory differs")
    count = 0
    for path in first_files:
        with (
            np.load(original / path, allow_pickle=False) as first,
            np.load(repeat / path, allow_pickle=False) as second,
        ):
            if set(first.files) != set(second.files):
                raise AssertionError(f"array names differ: {path}")
            for key in first.files:
                if not np.array_equal(first[key], second[key]):
                    raise AssertionError(f"numeric reproduction differs: {path}:{key}")
                count += 1
    return {
        "exact_numeric_match": True,
        "npz_files": len(first_files),
        "arrays": count,
        "excluded": ["timing", "RSS", "PID", "timestamps", "archive container bytes"],
    }


def run_smoke(config, output, repeat_from=None):
    config.validate()
    manifest = load_protocol()
    torch.set_num_threads(config.threads)
    torch.use_deterministic_algorithms(True)
    if torch.get_default_dtype() != torch.float32:
        raise ValueError("smoke requires default float32")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "packets").mkdir()
    (output / "cells").mkdir()
    repeat_from = Path(repeat_from) if repeat_from else None
    write_json(output / "config.json", config.to_dict())
    write_json(output / "manifest.json", manifest)
    run_provenance = provenance(config)
    write_json(output / "provenance.json", run_provenance)
    status = {
        "artifact_schema_version": 1,
        "status": "running",
        "started_at": datetime.now(UTC).isoformat(),
        "purpose": "engineering fixture coverage; no empirical gate decision",
    }
    write_json(output / "status.json", status)
    rows, deterministic, packets = [], [], {}
    budget = Budget(config)
    started = time.perf_counter()
    try:
        for cell_index, cell in enumerate(manifest["episode_cells"]):
            for episode_index in range(config.episodes_per_condition):
                budget.check()
                condition = cell["condition"]
                oracle = cell["intervention"] == "oracle_full_cue"
                packet_name = f"c{condition}-e{episode_index}-oracle{int(oracle)}.npz"
                if packet_name not in packets:
                    if repeat_from:
                        episode = load_episode(
                            repeat_from / "packets" / packet_name,
                            config.seed,
                            config.split,
                            condition,
                            episode_index,
                        )
                    else:
                        episode = generate_episode(
                            config.seed, config.split, condition, episode_index, oracle
                        )
                    packets[packet_name] = episode
                    save_arrays(output / "packets" / packet_name, episode.arrays())
                episode = packets[packet_name]
                identity = f"cell{cell_index:02d}-e{episode_index}"
                status["active_cell"] = identity
                write_json(output / "status.json", status)
                directory = output / "cells" / identity
                directory.mkdir()
                began = time.perf_counter()
                model = HandoverModel(cell["variant"], config.seed, condition, cell["intervention"])
                if repeat_from:
                    checkpoint = torch.load(
                        repeat_from / "cells" / identity / "checkpoint.pt",
                        map_location="cpu",
                        weights_only=True,
                    )
                    model.load_state_dict(checkpoint, strict=True)
                model.eval()
                initialization_seconds = time.perf_counter() - began
                torch.save(model.state_dict(), directory / "checkpoint.pt")
                result = run_episode(model, episode, cell["mode"], cell["intervention"])
                numeric = {
                    "artifact_schema_version": 1,
                    "id": identity,
                    **cell,
                    "episode": episode_index,
                    "packet_file": packet_name,
                    "packet_fingerprint": episode.fingerprint(),
                    "weights_status": "analytic_supplied" if model.analytic else "unfitted_fixture",
                    "resources": model.resources(),
                    **{k: v for k, v in result.items() if k not in ("arrays", "timings")},
                }
                save_arrays(directory / "trajectories.npz", result["arrays"])
                write_json(
                    directory / "record.json",
                    {
                        **numeric,
                        "timings": {
                            **result["timings"],
                            "initialization_seconds": initialization_seconds,
                        },
                    },
                )
                rows.append({"id": identity, "status": "complete", "timings": result["timings"]})
                deterministic.append(numeric)
                write_json(output / "cells.json", rows)
                write_json(output / "deterministic.json", deterministic)
                print(
                    f"{identity}: {cell['variant']} c{condition} {cell['mode']} "
                    f"{cell['intervention']}",
                    flush=True,
                )
        status["active_cell"] = None
        budget.check()
        probe_started = time.perf_counter()
        probe_rows, probe_arrays = run_probes(config.seed, config.split, cases_per_group=1)
        status["probe_wall_seconds"] = time.perf_counter() - probe_started
        write_json(output / "probes.json", probe_rows)
        save_arrays(output / "probes.npz", probe_arrays)
        budget.check()
        if provenance(config)["source_sha256"] != run_provenance["source_sha256"]:
            raise RuntimeError("source changed during execution")
        if repeat_from:
            write_json(output / "reproduction.json", compare_runs(repeat_from, output))
        write_json(
            output / "artifact-index.json",
            {
                str(p.relative_to(output)): sha256(p)
                for p in sorted(output.rglob("*"))
                if p.is_file() and p.name != "status.json"
            },
        )
        status.update(
            status="complete",
            episode_cells=len(deterministic),
            probe_evaluations=len(probe_rows),
            unique_base_episode_indices=config.episodes_per_condition,
            packet_variants=len(packets),
            trained_models=0,
            empirical_gate_passed=False,
        )
    except Exception as error:
        status.update(
            status="failed",
            error=f"{type(error).__name__}: {error}",
            completed_episode_cells=len(deterministic),
        )
        raise
    finally:
        status.update(
            finished_at=datetime.now(UTC).isoformat(),
            wall_seconds=time.perf_counter() - started,
            cpu_seconds=time.process_time() - budget.cpu_started,
            peak_rss_bytes=peak_rss_bytes(),
        )
        write_json(output / "status.json", status)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/handover-smoke.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeat-from", type=Path)
    args = parser.parse_args()
    config = SmokeConfig(**json.loads(args.config.read_text())).validate()
    run_smoke(config, args.output, args.repeat_from)


if __name__ == "__main__":
    main()
