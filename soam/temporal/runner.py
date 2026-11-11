"""Finite phases, immutable selections, cumulative resource ledger and exact repeat."""

import argparse
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

from soam.temporal.data import input_hash, normalization, seed, training_data
from soam.temporal.engine import evaluate, fit, headline, primary_batches, primary_score
from soam.temporal.models import LINEAR, SETTLERS, make

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/protocols/study_b_v1.json"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def tensor_hash(state):
    h = hashlib.sha256()
    for key, t in sorted(state.items()):
        h.update(key.encode())
        h.update(str(t.dtype).encode())
        h.update(t.detach().contiguous().numpy().tobytes())
    return h.hexdigest()


def source_identity():
    paths = sorted(
        [
            *ROOT.glob("soam/**/*.py"),
            *ROOT.glob("tests/*.py"),
            ROOT / "uv.lock",
            ROOT / "pyproject.toml",
            MANIFEST,
            ROOT / "docs/STUDY_B_PROTOCOL.md",
        ]
    )
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "hashes": hashes,
        "aggregate": digest(hashes),
        "dirty": subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines(),
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "threads": torch.get_num_threads(),
        "dtype": "float32 models; float64 fit/reductions",
        "device": "cpu",
    }


def size(path):
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


class Budget:
    def __init__(self, output, manifest, phase):
        self.output, self.m, self.phase = output, manifest, phase
        self.cpu, self.wall = time.process_time(), time.monotonic()
        self.ledger_path = output / "ledger.json"
        self.ledger = json.loads(self.ledger_path.read_text()) if self.ledger_path.exists() else []
        self.last_check = 0.0
        self.spent_cpu = sum(v["cpu_seconds"] for v in self.ledger)
        self.spent_wall = sum(v["wall_seconds"] for v in self.ledger)
        self.check(force=True)

    def check(self, force=False):
        cpu = time.process_time() - self.cpu
        if not force and cpu - self.last_check < 0.2:
            return
        self.last_check = cpu
        fraction = 1.0 if self.phase in {"report", "repeat"} else 0.9
        if self.spent_cpu + cpu > self.m["cpu_seconds"] * fraction:
            raise RuntimeError("CPU ceiling reached")
        if self.spent_wall + time.monotonic() - self.wall > self.m["wall_seconds"] * fraction:
            raise RuntimeError("Execution wall ceiling reached")
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != "darwin":
            rss *= 1024
        if rss > self.m["rss_bytes"]:
            raise RuntimeError("RSS ceiling reached")
        if force and size(self.output) > self.m["artifact_bytes"]:
            raise RuntimeError("Artifact ceiling reached")

    def finish(self, status, error=None):
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (
            1 if sys.platform == "darwin" else 1024
        )
        row = {
            "phase": self.phase,
            "status": status,
            "error": error,
            "cpu_seconds": time.process_time() - self.cpu,
            "wall_seconds": time.monotonic() - self.wall,
            "peak_rss_bytes": rss,
            "cumulative_artifact_bytes": size(self.output),
        }
        self.ledger.append(row)
        dump(self.ledger_path, self.ledger)
        print(json.dumps(row), flush=True)


def fit_one(output, phase, name, root, setting, data, budget, variance, development=None):
    dest = output / phase / str(root) / name / str(setting)
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "status.json", {"status": "running"})
    attempts = list(output.glob("**/status.json"))
    if len(attempts) > budget.m["max_fit_attempts"]:
        raise RuntimeError("Fit attempt ceiling reached")
    try:
        model = make(name, seed("train", root, 0, "initialization"))
        result = fit(model, data, setting, budget.check, development=development, variance=variance)
        result.update(
            {
                "name": name,
                "root": root,
                "setting": setting,
                "input_hash": input_hash(data),
                "checkpoint_hash": tensor_hash(model.state_dict()),
                "resources": model.resources(),
                "exposure": {
                    "episodes": sum(len(b.target[0]) for b in data),
                    "full_supervisory_observations": sum(
                        b.target.shape[0] * b.target.shape[1] for b in data
                    ),
                    "permitted_sensory_events": sum(
                        int(b.evidence.mask.any(-1).sum()) for b in data
                    ),
                    "permitted_feature_values": sum(int(b.evidence.mask.sum()) for b in data),
                    "offline_updates": 0 if name in LINEAR else len(data),
                    "replay": 0,
                },
            }
        )
        result["trace_hash"] = digest(result["trace"])
        torch.save(model.state_dict(), dest / "checkpoint.pt")
        dump(dest / "fit.json", result)
        dump(dest / "status.json", {"status": "fit complete"})
        budget.check(force=True)
        return model, dest, result
    except BaseException as error:
        dump(dest / "status.json", {"status": "failed", "error": repr(error)})
        raise


def fixture(output, m, budget, variance):
    data = training_data(m["fixture_root"], updates=20, batch=4, horizon=16, split="fixture")
    rows = []
    for name in m["candidates"]:
        setting = m["ridge_penalties"][0] if name in LINEAR else m["learning_rates"][0]
        model, dest, result = fit_one(
            output, "fixture", name, m["fixture_root"], setting, data, budget, variance
        )
        _, arrays, eval_cpu = evaluate(
            model,
            "fixture",
            m["fixture_root"],
            variance,
            k=4 if name in SETTLERS else 0,
            batch=20,
            check=budget.check,
            full=False,
        )
        np.savez_compressed(dest / "fixture.npz", **arrays)
        rows.append(
            {
                "name": name,
                "fit_cpu": result["fit_cpu_seconds"],
                "evaluation_cell_cpu": eval_cpu,
                "artifact_bytes": size(dest),
            }
        )
    # 4 development + 10 confirmation + 1 repeat per model. Training scales by updates.
    # 54 cells + settling-duration/schedule diagnostics, conservatively 4x for settlers.
    projected = 1.5 * sum(
        v["fit_cpu"] * 60 * 15
        + v["evaluation_cell_cpu"] * 54 * 15 * (4 if v["name"] in SETTLERS else 1)
        for v in rows
    )
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (
        1 if sys.platform == "darwin" else 1024
    )
    # Dense float32 error archives (54 cells, 20 episodes, 64 steps) + traces/checkpoints.
    projected_storage = int(
        1.5 * (256 * 400000 + 16 * 11 * 54 * 20 * 65 * 4 * 4 + 3 * 11 * 7 * 54 * 20 * 65 * 4 * 4)
    )
    record = {
        "rows": rows,
        "projected_cpu_seconds": projected,
        "projected_artifact_bytes": projected_storage,
        "peak_rss_bytes": rss,
        "projection_pass": bool(
            projected < 0.9 * m["cpu_seconds"]
            and projected_storage < m["artifact_bytes"]
            and rss * 1.25 < m["rss_bytes"]
        ),
    }
    dump(output / "fixture-projection.json", record)
    if not record["projection_pass"]:
        raise RuntimeError("Fixture feasibility projection failed; review before fitting")


def development(output, m, budget, variance):
    if not json.loads((output / "fixture-projection.json").read_text())["projection_pass"]:
        raise RuntimeError("No passing fixture")
    for root in m["development_roots"]:
        data = training_data(root)
        dev = primary_batches("development", root)
        for name in m["candidates"]:
            settings = m["ridge_penalties"] if name in LINEAR else m["learning_rates"]
            for setting in settings:
                model, dest, result = fit_one(
                    output, "development", name, root, setting, data, budget, variance, dev
                )
                scores = {
                    str(k): primary_score(model, dev, variance, k)
                    for k in (m["settling_durations"] if name in SETTLERS else [0])
                }
                dump(dest / "selection-scores.json", scores)
                print(
                    json.dumps(
                        {
                            "phase": "development",
                            "root": root,
                            "name": name,
                            "setting": setting,
                            "scores": scores,
                            "fit_cpu": result["fit_cpu_seconds"],
                        }
                    ),
                    flush=True,
                )


def freeze(output, m, budget, variance):
    selection = {}
    unresolved = []
    timings = []
    for name in m["candidates"]:
        choices = []
        for setting in m["ridge_penalties"] if name in LINEAR else m["learning_rates"]:
            dirs = [
                output / "development" / str(root) / name / str(setting)
                for root in m["development_roots"]
            ]
            scores = [json.loads((d / "selection-scores.json").read_text()) for d in dirs]
            for k in m["settling_durations"] if name in SETTLERS else [0]:
                choices.append((float(np.mean([s[str(k)] for s in scores])), setting, k, dirs))
        j, setting, k, dirs = min(choices, key=lambda v: (v[0], v[1], v[2]))
        fits = [json.loads((d / "fit.json").read_text()) for d in dirs]
        if name not in LINEAR:
            earlier = np.mean([f["learning"]["1050"] for f in fits])
            later = np.mean([f["learning"]["1200"] for f in fits])
            improvement = float((earlier - later) / max(earlier, 1e-6))
        else:
            improvement = 0.0
        if improvement > 0.2 and name in {"GA32", "PC32", "MIX32"}:
            unresolved.append(name)
        selection[name] = {
            "setting": setting,
            "k": k,
            "development_J": j,
            "late_improvement": improvement,
        }
        timings.append(float(np.mean([f["fit_cpu_seconds"] for f in fits])))
    spent = budget.spent_cpu + time.process_time() - budget.cpu
    # Measured training plus fixture evaluation projection, diagnostic overhead retained.
    projected_remaining = 1.5 * sum(timings) * 11 + sum(
        v["evaluation_cell_cpu"] * 54 * 11 * (4 if v["name"] in SETTLERS else 1)
        for v in json.loads((output / "fixture-projection.json").read_text())["rows"]
    )
    record = {
        "protocol": digest(m),
        "source": source_identity()["aggregate"],
        "selection": selection,
        "optimization_unresolved": unresolved,
        "normalization": variance,
        "spent_cpu": spent,
        "projected_remaining_cpu": projected_remaining,
        "remaining_cpu": m["cpu_seconds"] - spent,
        "projection_pass": bool(projected_remaining < 0.9 * m["cpu_seconds"] - spent),
        "confirmation_roots": m["confirmation_roots"],
        "review": "Fixed primary GA32 contrasts, 10-contrast family, fresh streams, no source change, preserved negative gates; deterministic fit reproduction required.",
    }
    record["sha256"] = digest(record)
    if not record["projection_pass"]:
        dump(output / "freeze-projection-failed.json", record)
        raise RuntimeError("Remaining allocation projection fails")
    path = output / "confirmation-receipt.json"
    with path.open("x") as f:
        json.dump(record, f, indent=2, sort_keys=True, allow_nan=False)
    print(json.dumps(record), flush=True)


def confirmation(output, m, budget, variance, repeat=False):
    receipt = json.loads((output / "confirmation-receipt.json").read_text())
    if receipt["sha256"] != digest({k: v for k, v in receipt.items() if k != "sha256"}):
        raise RuntimeError("Receipt modified")
    if source_identity()["aggregate"] != receipt["source"] or digest(m) != receipt["protocol"]:
        raise RuntimeError("Source/protocol changed after freeze")
    phase = "repeat" if repeat else "confirmation"
    for root in [m["repeat_root"]] if repeat else m["confirmation_roots"]:
        data = training_data(root)
        for name in m["candidates"]:
            choice = receipt["selection"][name]
            model, dest, result = fit_one(
                output, phase, name, root, choice["setting"], data, budget, variance
            )
            rows, arrays, cpu = evaluate(
                model, "confirmation", root, variance, k=choice["k"], check=budget.check
            )
            result = {
                "headline": headline(rows),
                "rows": rows,
                "inference_cpu_seconds": cpu,
                "prediction_hash": tensor_hash({k: torch.from_numpy(v) for k, v in arrays.items()}),
            }
            np.savez_compressed(dest / "errors.npz", **arrays)
            dump(dest / "evaluation.json", result)
            diagnostics = {}
            if name in SETTLERS:
                for k in m["settling_durations"]:
                    if k == choice["k"]:
                        diagnostics[f"fixed{k}"] = {
                            "headline": result["headline"],
                            "rows": rows,
                            "prediction_hash": result["prediction_hash"],
                        }
                    else:
                        r, a, _cost = evaluate(
                            model, "confirmation", root, variance, k=k, check=budget.check
                        )
                        diagnostics[f"fixed{k}"] = {
                            "headline": headline(r),
                            "rows": r,
                            "prediction_hash": tensor_hash(
                                {key: torch.from_numpy(v) for key, v in a.items()}
                            ),
                        }
                for mode in ["event", "learned", "periodic"] if name == "SET32" else []:
                    r, a, _cost = evaluate(
                        model, "confirmation", root, variance, k=4, mode=mode, check=budget.check
                    )
                    diagnostics[mode] = {
                        "headline": headline(r),
                        "rows": r,
                        "prediction_hash": tensor_hash(
                            {key: torch.from_numpy(v) for key, v in a.items()}
                        ),
                    }
            if name == "FILTER2":
                r, a, _c = evaluate(
                    model, "confirmation", root, variance, metadata=True, check=budget.check
                )
                diagnostics["supplied_noise"] = {
                    "headline": headline(r),
                    "rows": r,
                    "prediction_hash": tensor_hash(
                        {key: torch.from_numpy(v) for key, v in a.items()}
                    ),
                }
            dump(dest / "diagnostics.json", diagnostics)
            dump(dest / "status.json", {"status": "complete"})
            budget.check(force=True)
            print(
                json.dumps({"phase": phase, "root": root, "name": name, **result["headline"]}),
                flush=True,
            )
    if repeat:
        checks = {}
        for name in m["candidates"]:
            setting = receipt["selection"][name]["setting"]
            base = Path(str(m["repeat_root"])) / name / str(setting)
            orig = output / "confirmation" / base
            rep = output / "repeat" / base
            a, b = [json.loads((d / "fit.json").read_text()) for d in (orig, rep)]
            ev = [json.loads((d / "evaluation.json").read_text()) for d in (orig, rep)]
            di = [json.loads((d / "diagnostics.json").read_text()) for d in (orig, rep)]
            checks[name] = {
                key: a[key] == b[key] for key in ("input_hash", "checkpoint_hash", "trace_hash")
            }
            checks[name].update(
                predictions=ev[0]["prediction_hash"] == ev[1]["prediction_hash"],
                diagnostics=di[0] == di[1],
            )
        dump(output / "reproduction.json", checks)
        if not all(all(v.values()) for v in checks.values()):
            raise RuntimeError("Numerical reproduction differs")


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--phase",
        choices=["fixture", "development", "freeze", "confirmation", "repeat", "report"],
        required=True,
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = source_identity()
    if (output / "source.json").exists():
        if json.loads((output / "source.json").read_text())["aggregate"] != source["aggregate"]:
            raise RuntimeError("Execution source identity changed")
    else:
        dump(output / "source.json", source)
        dump(output / "manifest.json", m)
        for rel in source["hashes"]:
            dst = output / "source" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, dst)
    phase_marker = output / f"{args.phase}-started.json"
    with phase_marker.open("x") as f:
        json.dump({"phase": args.phase, "source": source["aggregate"]}, f)
    budget = Budget(output, m, args.phase)
    try:
        variance = normalization()
        if args.phase == "fixture":
            fixture(output, m, budget, variance)
        elif args.phase == "development":
            development(output, m, budget, variance)
        elif args.phase == "freeze":
            freeze(output, m, budget, variance)
        elif args.phase == "report":
            from soam.temporal.render import render

            print(json.dumps(render(output, m, budget)), flush=True)
        else:
            confirmation(output, m, budget, variance, repeat=args.phase == "repeat")
        budget.check(force=True)
        budget.finish("complete")
    except BaseException as error:
        budget.finish("failed", repr(error))
        raise


if __name__ == "__main__":
    main()
