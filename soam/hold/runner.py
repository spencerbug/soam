"""Bounded E0-HOLD fixture and paired confirmation; no adaptive trial control."""

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import torch

from soam.evaluation.provenance import capture
from soam.hold.statistics import summarize
from soam.hold.training import fit, mapped_root, state_hash
from soam.navigation.data import seed
from soam.navigation.engine import evaluate
from soam.navigation.models import make
from soam.navigation.runner import CaptureConfig, digest, rss_bytes, write_json

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/protocols/study_e0_hold_v1.json"
PROTOCOL = ROOT / "docs/STUDY_E0_HOLD_PROTOCOL.md"


def cells(config):
    return [
        (name, arm)
        for name in config["models"]
        for arm in (["REFERENCE"] if name == "PCA2" else config["arms"])
    ]


def inventory(config, fixture=False):
    phases = (
        [("fixture", [config["fixture_root"]])]
        if fixture
        else [("confirmation", config["confirmation_roots"]), ("repeat", [config["repeat_root"]])]
    )
    return [
        {
            "id": f"{phase}/{root}/{name}/{arm}",
            "phase": phase,
            "root": root,
            "model": name,
            "arm": arm,
        }
        for phase, roots in phases
        for root in roots
        for name, arm in cells(config)
    ]


class Run:
    def __init__(self, output, config, phase):
        self.output, self.config, self.phase = output, config, phase
        output.mkdir(parents=True, exist_ok=True)
        self.start_cpu, self.start_wall = time.process_time(), time.monotonic()
        self.path = output / "ledger.json"
        self.ledger = (
            json.loads(self.path.read_text())
            if self.path.exists()
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
        self.last_disk_check, self.artifact_bytes = 0, 0
        self.provenance = capture(ROOT, CaptureConfig(config))
        self.provenance.update(protocol_sha256=digest(PROTOCOL), manifest_sha256=digest(MANIFEST))
        if self.provenance["git_status"]:
            raise RuntimeError("E0-HOLD requires a clean committed source tree")
        identity = {
            k: self.provenance[k]
            for k in ("source_sha256", "config_sha256", "protocol_sha256", "manifest_sha256")
        }
        if "identity" in self.ledger and identity != self.ledger["identity"]:
            raise RuntimeError("E0-HOLD identity changed; no reuse of this execution")
        self.ledger["identity"] = identity
        self.ledger["inventory"] = inventory(config)
        self.ledger["commands"].append(
            {
                "argv": sys.argv,
                "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "provenance": self.provenance,
            }
        )
        source = output / "source"
        if not source.exists():
            for relative in [
                *self.provenance["source_files"],
                "docs/STUDY_E0_HOLD_PROTOCOL.md",
                "docs/protocols/study_e0_hold_v1.json",
                "docs/STUDY_E0_PROTOCOL.md",
                "docs/protocols/study_e0_v1.json",
            ]:
                dest = source / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, dest)
        self.check()
        self.save()

    def check(self):
        limits = self.config["limits"]
        if self.previous_cpu + time.process_time() - self.start_cpu > limits["cpu_seconds"]:
            raise RuntimeError("E0-HOLD CPU ceiling reached")
        if self.previous_wall + time.monotonic() - self.start_wall > limits["wall_seconds"]:
            raise RuntimeError("E0-HOLD wall ceiling reached")
        if rss_bytes() > limits["rss_bytes"]:
            raise RuntimeError("E0-HOLD RSS ceiling reached")
        if time.monotonic() - self.last_disk_check > 5:
            self.artifact_bytes = sum(
                p.stat().st_size for p in self.output.rglob("*") if p.is_file()
            )
            self.last_disk_check = time.monotonic()
        if self.artifact_bytes > limits["artifact_bytes"]:
            raise RuntimeError("E0-HOLD artifact ceiling reached")

    def save(self):
        self.ledger.update(
            cpu_seconds=self.previous_cpu + time.process_time() - self.start_cpu,
            wall_seconds=self.previous_wall + time.monotonic() - self.start_wall,
            peak_rss_bytes=max(rss_bytes(), self.ledger["peak_rss_bytes"]),
            artifact_bytes=sum(p.stat().st_size for p in self.output.rglob("*") if p.is_file()),
        )
        write_json(self.path, self.ledger)

    def trial(self, row):
        ident = row["id"]
        old = self.ledger["records"].get(ident)
        if old is not None:
            if old["status"] != "complete":
                raise RuntimeError(f"Automatic retry prohibited: {ident}")
            for relative, expected in old["sha256"].items():
                if digest(self.output / relative) != expected:
                    raise RuntimeError(f"Changed payload: {relative}")
            return old
        fixture = row["phase"] == "fixture"
        attempts = sum(
            (r["phase"] == "fixture") == fixture for r in self.ledger["records"].values()
        )
        limit = self.config["limits"]["fixture_fits" if fixture else "scientific_fits"]
        if attempts >= limit:
            raise RuntimeError("E0-HOLD fit-attempt ceiling reached")
        cfg = dict(self.config)
        if fixture:
            cfg["updates"] = 8
        stream_root = mapped_root(row["root"])
        model_seed = seed(
            "fixture" if fixture else "train", stream_root, 0, row["model"] + "/initial"
        )
        model = make(row["model"], model_seed)
        record = {
            **row,
            "stream_root": stream_root,
            "model_seed": model_seed,
            "initial_state_sha256": state_hash(model),
            "status": "running",
            "resources": model.resources(),
            "actual_config": cfg,
            "provenance": {k: v for k, v in self.provenance.items() if k != "source_files"},
        }
        self.ledger["records"][ident] = record
        self.save()
        print("START " + ident, flush=True)
        try:
            fitted = fit(model, stream_root, cfg, row["arm"], self.check, fixture=fixture)
            trace = np.array(fitted.pop("trace"), dtype=np.float64).reshape(-1, 4)
            record["fitting"] = fitted
            record["loss_diagnostics"] = {
                "last100": float(trace[-100:, 1].mean()) if len(trace) else None,
                "previous100": float(trace[-200:-100, 1].mean()) if len(trace) >= 200 else None,
            }
            record["evaluation"], arrays = evaluate(
                model, "fixture" if fixture else "confirmation", stream_root, cfg, self.check
            )
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

    def pairing(self, phase, roots):
        checked = 0
        for root in roots:
            records = [
                self.ledger["records"][f"{phase}/{root}/{n}/{a}"] for n, a in cells(self.config)
            ]
            if len({r["fitting"]["training_data_sha256"] for r in records}) != 1:
                raise AssertionError("Unequal prefix training data across cells")
            for name in self.config["models"][:-1]:
                pair = [r for r in records if r["model"] == name]
                if len({r["initial_state_sha256"] for r in pair}) != 1:
                    raise AssertionError("Unequal initial parameters between horizon arms")
                if (
                    len({r["fitting"]["exposure"]["eligible_stationary_episodes"] for r in pair})
                    != 1
                ):
                    raise AssertionError("Unequal stationary episode selection")
                checked += 1
        return checked

    def fixture(self):
        records = [self.trial(row) for row in inventory(self.config, fixture=True)]
        pairs = self.pairing("fixture", [self.config["fixture_root"]])
        expected = 0
        wall_ratio = 1
        for r in records:
            fitted = r["fitting"]
            if r["model"] == "PCA2":
                fit_cost = fitted["cpu_seconds"] * self.config["updates"] / 8
            else:
                fit_cost = (fitted["steady_update_cpu_seconds"] + 0.001) * self.config["updates"]
            expected += (fit_cost + r["evaluation"]["inference_cpu_seconds"]) * 21
            wall_ratio = max(
                wall_ratio,
                fitted["wall_seconds"] / max(fitted["cpu_seconds"], 1e-6),
                r["evaluation"]["inference_wall_seconds"]
                / max(r["evaluation"]["inference_cpu_seconds"], 1e-6),
            )
        projected = 2 * (expected + self.ledger["cpu_seconds"])
        bytes_est = (
            2
            * max(sum((self.output / p).stat().st_size for p in r["sha256"]) for r in records)
            * 147
            + self.ledger["artifact_bytes"]
        )
        self.ledger["preflight"] = {
            "projected_cpu_seconds_2x": projected,
            "projected_wall_seconds_2x": projected * wall_ratio,
            "projected_artifact_bytes_2x": bytes_est,
            "paired_initializations": pairs,
            "pass": projected <= 0.8 * self.config["limits"]["cpu_seconds"]
            and projected * wall_ratio <= 0.8 * self.config["limits"]["wall_seconds"]
            and bytes_est <= self.config["limits"]["artifact_bytes"],
        }
        self.save()
        print(json.dumps(self.ledger["preflight"]), flush=True)

    def confirmation(self):
        if not self.ledger.get("preflight", {}).get("pass"):
            raise RuntimeError("Passing fixture preflight required before confirmation")
        for row in inventory(self.config):
            self.trial(row)
        pairs = self.pairing("confirmation", self.config["confirmation_roots"])
        pairs += self.pairing("repeat", [self.config["repeat_root"]])
        checks = {"arrays": 0, "tensors": 0, "paired_initializations": pairs}
        for name, arm in cells(self.config):
            paths = [
                self.output / "trials" / p / str(self.config["repeat_root"]) / name / arm
                for p in ("confirmation", "repeat")
            ]
            with np.load(paths[0] / "arrays.npz") as a, np.load(paths[1] / "arrays.npz") as b:
                if set(a.files) != set(b.files):
                    raise AssertionError("Repeated array inventory mismatch")
                for key in a.files:
                    np.testing.assert_array_equal(a[key], b[key], err_msg=f"{name}/{arm}/{key}")
                    checks["arrays"] += 1
            a, b = [torch.load(p / "checkpoint.pt", weights_only=True) for p in paths]
            if a.keys() != b.keys():
                raise AssertionError("Repeated tensor inventory mismatch")
            for key in a:
                if not torch.equal(a[key], b[key]):
                    raise AssertionError(f"{name}/{arm}/{key} repeat mismatch")
                checks["tensors"] += 1
        self.ledger["repeat_check"] = checks
        write_json(self.output / "summary.json", summarize(self.ledger["records"], self.config))
        self.save()
        print("REPEAT " + json.dumps(checks), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("fixture", "confirmation"))
    parser.add_argument("--output", type=Path, default=ROOT / "runs/study-e0-hold-v1")
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    run = Run(args.output.resolve(), json.loads(MANIFEST.read_text()), args.phase)
    try:
        getattr(run, args.phase)()
    finally:
        run.save()


if __name__ == "__main__":
    main()
