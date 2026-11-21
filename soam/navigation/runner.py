"""Finite E0 inventory, source freeze, resource guard, atomic records and exact repeats.

uv run python -m soam.navigation.runner fixture|development|confirmation --output runs/study-e0-v1
"""

import argparse
import hashlib
import json
import resource
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

from soam.evaluation.provenance import capture
from soam.navigation.data import seed
from soam.navigation.engine import development_score, evaluate, fit
from soam.navigation.models import make
from soam.navigation.statistics import summarize

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/protocols/study_e0_v1.json"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class CaptureConfig:
    data: dict
    threads: int = 1

    def to_dict(self):
        return self.data


def rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == "darwin" else value * 1024)


def inventory(config):
    rows = []
    for root in config["development_roots"]:
        for name in config["models"]:
            for rate in [None] if name == "PCA2" else config["rates"]:
                rows.append(
                    {
                        "id": f"development/{root}/{name}/{rate}",
                        "phase": "development",
                        "root": root,
                        "model": name,
                        "rate": rate,
                    }
                )
    for phase, roots in (
        ("confirmation", config["confirmation_roots"]),
        ("repeat", [config["repeat_root"]]),
    ):
        for root in roots:
            for name in config["models"]:
                rows.append(
                    {
                        "id": f"{phase}/{root}/{name}",
                        "phase": phase,
                        "root": root,
                        "model": name,
                        "rate": "selected",
                    }
                )
    return rows


class Run:
    def __init__(self, output, config, phase):
        self.output, self.config, self.phase = output, config, phase
        output.mkdir(parents=True, exist_ok=True)
        self.start_cpu, self.start_wall = time.process_time(), time.monotonic()
        self.ledger_path = output / "ledger.json"
        self.ledger = (
            json.loads(self.ledger_path.read_text())
            if self.ledger_path.exists()
            else {
                "cpu_seconds": 0,
                "wall_seconds": 0,
                "peak_rss_bytes": 0,
                "records": {},
                "commands": [],
            }
        )
        self.previous_cpu, self.previous_wall = (
            self.ledger["cpu_seconds"],
            self.ledger["wall_seconds"],
        )
        self.last_disk_check = 0
        self.artifact_bytes = sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
        self.provenance = capture(ROOT, CaptureConfig(config))
        self.provenance["protocol_sha256"] = digest(ROOT / "docs/STUDY_E0_PROTOCOL.md")
        self.provenance["manifest_sha256"] = digest(MANIFEST)
        if phase != "fixture" and self.provenance["git_status"]:
            raise RuntimeError("Scientific fitting requires a committed clean source tree")
        identity = {
            k: self.provenance[k]
            for k in ("source_sha256", "config_sha256", "protocol_sha256", "manifest_sha256")
        }
        if phase != "fixture":
            if (
                "scientific_identity" in self.ledger
                and self.ledger["scientific_identity"] != identity
            ):
                raise RuntimeError(
                    "Source/protocol changed: use a new reviewed experiment identity"
                )
            self.ledger["scientific_identity"] = identity
        self.ledger["commands"].append(
            {
                "argv": sys.argv,
                "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "provenance": self.provenance,
            }
        )
        self.ledger["inventory"] = inventory(config)
        self.check()
        self.save()
        source = output / ("fixture-source" if phase == "fixture" else "source")
        if not source.exists():
            for relative in self.provenance["source_files"]:
                dest = source / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, dest)
            for relative in ("docs/STUDY_E0_PROTOCOL.md", "docs/protocols/study_e0_v1.json"):
                dest = source / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, dest)

    def check(self):
        limits = self.config["limits"]
        cpu = self.previous_cpu + time.process_time() - self.start_cpu
        wall = self.previous_wall + time.monotonic() - self.start_wall
        if cpu > limits["cpu_seconds"] or wall > limits["wall_seconds"]:
            raise RuntimeError("E0 cumulative execution budget exhausted")
        if rss_bytes() > limits["rss_bytes"]:
            raise RuntimeError("E0 peak RSS limit exceeded")
        if time.monotonic() - self.last_disk_check > 5:
            self.artifact_bytes = sum(
                p.stat().st_size for p in self.output.rglob("*") if p.is_file()
            )
            self.last_disk_check = time.monotonic()
        if self.artifact_bytes > limits["artifact_bytes"]:
            raise RuntimeError("E0 artifact limit exceeded")

    def save(self):
        self.ledger.update(
            cpu_seconds=self.previous_cpu + time.process_time() - self.start_cpu,
            wall_seconds=self.previous_wall + time.monotonic() - self.start_wall,
            peak_rss_bytes=max(self.ledger["peak_rss_bytes"], rss_bytes()),
            artifact_bytes=sum(p.stat().st_size for p in self.output.rglob("*") if p.is_file()),
        )
        write_json(self.ledger_path, self.ledger)

    def trial(self, spec, *, fixture=False):
        ident, name, root = spec["id"], spec["model"], spec["root"]
        old = self.ledger["records"].get(ident)
        if old is not None:
            if old["status"] != "complete":
                raise RuntimeError(f"No automatic retry permitted: {ident}")
            for relative, expected in old["sha256"].items():
                if digest(self.output / relative) != expected:
                    raise RuntimeError(f"Changed completed artifact: {relative}")
            return old
        attempts = sum(r["phase"] != "fixture" for r in self.ledger["records"].values())
        if not fixture and attempts >= self.config["limits"]["scientific_fits"]:
            raise RuntimeError("E0 fit ceiling reached")
        cfg = dict(self.config)
        if fixture:
            cfg["updates"] = 8
        model_seed = seed("fixture" if fixture else "train", root, 0, name + "/initial")
        model = make(name, model_seed)
        record = {
            **spec,
            "model_seed": model_seed,
            "status": "running",
            "provenance": {k: v for k, v in self.provenance.items() if k != "source_files"},
            "actual_config": cfg,
            "resources": model.resources(),
        }
        self.ledger["records"][ident] = record
        self.save()
        print(f"START {ident}", flush=True)
        try:
            fitted = fit(model, root, cfg, spec["rate"], self.check, fixture=fixture)
            trace = np.array(fitted.pop("trace"), dtype=np.float64).reshape(-1, 4)
            record["fitting"] = fitted
            record["loss_diagnostics"] = {
                "last100": float(trace[-100:, 1].mean()) if len(trace) else None,
                "previous100": float(trace[-200:-100, 1].mean()) if len(trace) >= 200 else None,
            }
            record["data_exposure"] = {
                "distinct_training_sequences": cfg["updates"] * cfg["batch"],
                "distinct_clean_training_snapshots": cfg["updates"]
                * cfg["batch"]
                * (cfg["train_horizon"] + 1),
                "training_data_passes": 2 if name == "PCA2" else 1,
                "online_parameter_updates": 0,
                "neural_optimizer_updates": 0 if name == "PCA2" else cfg["updates"],
                "note": "Noisy views share the same physical snapshots; targets are supplied offline to every family.",
            }
            if spec["phase"] == "development":
                record["development_J"] = development_score(model, root, cfg, self.check)
                arrays = {}
            else:
                split = "fixture" if fixture else "confirmation"
                record["evaluation"], arrays = evaluate(model, split, root, cfg, self.check)
            directory = self.output / "trials" / ident
            directory.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), directory / "checkpoint.pt.tmp")
            (directory / "checkpoint.pt.tmp").replace(directory / "checkpoint.pt")
            arrays["fit_trace"] = trace
            np.savez_compressed(directory / "arrays.npz", **arrays)
            record["sha256"] = {
                str(p.relative_to(self.output)): digest(p) for p in directory.iterdir()
            }
            record["status"] = "complete"
            write_json(directory / "record.json", record)
            self.check()
            print(f"DONE {ident} fit_cpu={fitted['cpu_seconds']:.2f}", flush=True)
        except BaseException as error:
            record["status"], record["error"] = "failed", repr(error)
            raise
        finally:
            self.save()
        return record

    def fixture(self):
        rows = [
            self.trial(
                {
                    "id": "fixture/" + name,
                    "phase": "fixture",
                    "root": self.config["fixture_root"],
                    "model": name,
                    "rate": None if name == "PCA2" else self.config["rates"][0],
                },
                fixture=True,
            )
            for name in self.config["models"]
        ]
        neural_step = max(r["fitting"]["steady_update_cpu_seconds"] for r in rows[:-1])
        pca_fit = rows[-1]["fitting"]["cpu_seconds"] * self.config["updates"] / 8
        evaluation = max(r["evaluation"]["inference_cpu_seconds"] for r in rows)
        # Include a conservative per-update data-generation allowance and all evaluation calls.
        raw = (neural_step + 0.001) * self.config["updates"] * 45 + pca_fit * 13 + evaluation * 58
        projected = 2 * (raw + self.ledger["cpu_seconds"])
        wall_ratio = max(
            1,
            *[r["fitting"]["wall_seconds"] / max(r["fitting"]["cpu_seconds"], 1e-6) for r in rows],
            *[
                r["evaluation"]["inference_wall_seconds"]
                / max(r["evaluation"]["inference_cpu_seconds"], 1e-6)
                for r in rows
            ],
        )
        projected_bytes = (
            2 * max(sum((self.output / p).stat().st_size for p in r["sha256"]) for r in rows) * 58
            + self.ledger["artifact_bytes"]
        )
        self.ledger["preflight"] = {
            "projected_cpu_seconds_2x": projected,
            "projected_wall_seconds_2x": projected * wall_ratio,
            "source_sha256": self.provenance["source_sha256"],
            "projected_artifact_bytes_2x": projected_bytes,
            "cpu_limit_fraction": 0.8,
            "pass": projected <= 0.8 * self.config["limits"]["cpu_seconds"]
            and projected * wall_ratio <= 0.8 * self.config["limits"]["wall_seconds"]
            and projected_bytes <= self.config["limits"]["artifact_bytes"],
        }
        self.save()
        print(json.dumps(self.ledger["preflight"]), flush=True)

    def development(self):
        if not self.ledger.get("preflight", {}).get("pass"):
            raise RuntimeError("E0 requires a passing fixture preflight")
        if self.ledger["preflight"]["source_sha256"] != self.provenance["source_sha256"]:
            raise RuntimeError("E0 fixture source no longer matches the scientific source")
        for row in inventory(self.config):
            if row["phase"] == "development":
                self.trial(row)
        choices = {}
        for name in self.config["models"]:
            if name == "PCA2":
                choices[name] = None
                continue
            scores = [
                np.mean(
                    [
                        self.ledger["records"][f"development/{r}/{name}/{rate}"]["development_J"]
                        for r in self.config["development_roots"]
                    ]
                )
                for rate in self.config["rates"]
            ]
            choices[name] = self.config["rates"][int(np.argmin(scores))]
        self.ledger["selection"] = choices
        self.save()
        write_json(self.output / "selection.json", choices)
        self.ledger["selection_sha256"] = digest(self.output / "selection.json")
        self.save()
        print("SELECTION " + json.dumps(choices), flush=True)

    def confirmation(self):
        choices = self.ledger.get("selection")
        if (
            choices is None
            or digest(self.output / "selection.json") != self.ledger["selection_sha256"]
        ):
            raise RuntimeError("E0 requires frozen development selection")
        for row in inventory(self.config):
            if row["phase"] != "development":
                self.trial({**row, "rate": choices[row["model"]]})
        for root in self.config["confirmation_roots"]:
            hashes = {
                self.ledger["records"][f"confirmation/{root}/{name}"]["fitting"][
                    "training_data_sha256"
                ]
                for name in self.config["models"]
            }
            if len(hashes) != 1:
                raise AssertionError("E0 unequal training data exposure across model families")
        checks = {"arrays": 0, "tensors": 0}
        for name in self.config["models"]:
            paths = [
                self.output / "trials" / phase / str(self.config["repeat_root"]) / name
                for phase in ("confirmation", "repeat")
            ]
            with np.load(paths[0] / "arrays.npz") as a, np.load(paths[1] / "arrays.npz") as b:
                if set(a.files) != set(b.files):
                    raise AssertionError("E0 repeat array inventory mismatch")
                for key in a.files:
                    np.testing.assert_array_equal(a[key], b[key], err_msg=name + "/" + key)
                    checks["arrays"] += 1
            a, b = [torch.load(p / "checkpoint.pt", weights_only=True) for p in paths]
            if a.keys() != b.keys():
                raise AssertionError("E0 repeat tensor inventory mismatch")
            for key in a:
                if not torch.equal(a[key], b[key]):
                    raise AssertionError(name + "/" + key + " repeat mismatch")
                checks["tensors"] += 1
        self.ledger["repeat_check"] = checks
        summary = summarize(self.ledger["records"], self.config)
        write_json(self.output / "summary.json", summary)
        self.save()
        print("REPEAT " + json.dumps(checks), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("fixture", "development", "confirmation"))
    parser.add_argument("--output", type=Path, default=ROOT / "runs/study-e0-v1")
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    config = json.loads(MANIFEST.read_text())
    run = Run(args.output.resolve(), config, args.phase)
    try:
        getattr(run, args.phase)()
    finally:
        run.save()


if __name__ == "__main__":
    main()
