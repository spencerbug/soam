"""Read-only post-confirmation archive and failure audit; no fits or new streams."""

import hashlib
import json
from pathlib import Path

import numpy as np
import torch

from soam.acquisition.engine import array_hash
from soam.acquisition.models import Core, Memory
from soam.temporal.runner import Budget, digest, dump, size

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs/study-d-v1"
REPORT = ROOT / "reports/study-d"


def read(path):
    return json.loads(path.read_text())


def main():
    torch.set_num_threads(1)
    receipt = read(OUT / "freeze/receipt.json")
    assert digest({k: v for k, v in receipt.items() if k != "sha256"}) == receipt["sha256"]
    budget = Budget(OUT, receipt["manifest"]["limits"], "archive-audit")
    dest = OUT / "archive-audit"
    dest.mkdir(exist_ok=False)
    try:
        verified, failures = 0, {}
        for root in receipt["manifest"]["confirmation_roots"]:
            base = OUT / "confirmation" / str(root)
            checkpoint = torch.load(base / "fit/core.pt", weights_only=True)
            core = Core(checkpoint["a"], checkpoint["b"])
            for name in ("NOWRITE", "KV", "REG", "FAST"):
                result = read(base / name / "result.json")
                with np.load(base / name / "inputs.npz") as inputs:
                    assert array_hash(dict(inputs)) == result["input_hash"]
                model = Memory(name, core, result["setting"], result["threshold"])
                model.restore(torch.load(base / name / "last-memory.pt", weights_only=True))
                assert model.fingerprint() == result["memory_hashes"]["d2/3"]
                verified += 1
                with np.load(base / name / "arrays.npz") as a:
                    old_error = a["d2_error"][:, -1, :-1, :, 1:].mean(-1)
                    index = np.unravel_index(np.argmax(old_error), old_error.shape)
                    value = float(old_error[index])
                    if name not in failures or value > failures[name]["worst_free8"]:
                        preserved = failures.get(name, {}).get("representative_first_root")
                        failures[name] = {
                            "root": root,
                            "sequence_object_query": list(map(int, index)),
                            "worst_free8": value,
                        }
                        if preserved is not None:
                            failures[name]["representative_first_root"] = preserved
                    if root == receipt["manifest"]["repeat_root"]:
                        failures[name]["representative_first_root"] = {
                            "root": root,
                            "sequence": 0,
                            "object": 0,
                            "initial_free8": float(a["d2_error"][0, 0, 0, :, 1:].mean()),
                            "final_free8": float(a["d2_error"][0, -1, 0, :, 1:].mean()),
                        }
            budget.check()
        expected_trials = 88
        statuses = [read(p)["status"] for p in OUT.glob("**/status.json")]
        assert len(statuses) == expected_trials and all(s == "complete" for s in statuses)
        fits = [read(p)["status"] for p in OUT.glob("**/fit-status.json")]
        assert len(fits) == 16 and all(s == "complete" for s in fits)
        for relative, sha in receipt["source"]["hashes"].items():
            assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == sha
            assert (
                hashlib.sha256((OUT / "freeze/source" / relative).read_bytes()).hexdigest() == sha
            )
        artifact_hashes = {
            str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(OUT.rglob("*"))
            if p.is_file() and dest not in p.parents and p != OUT / "ledger.json"
        }
        audit = {
            "status": "pass",
            "model_evaluations_complete": len(statuses),
            "fits_complete": len(fits),
            "input_and_checkpoint_checks": verified,
            "frozen_files": len(receipt["source"]["hashes"]),
            "raw_artifact_files": len(artifact_hashes),
            "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_fingerprint": receipt["source"]["aggregate"],
            "scope": "Saved-array/archive audit only; no new fits, streams or thresholds",
        }
        dump(dest / "verification.json", audit)
        dump(REPORT / "archive-verification.json", audit)
        dump(REPORT / "representative-failures.json", failures)
        dump(REPORT / "artifact-sha256.json", artifact_hashes)
        budget.check(force=True)
        budget.finish("complete")
        ledger = read(OUT / "ledger.json")
        resources = {
            "phases": ledger,
            "cpu_seconds": sum(r["cpu_seconds"] for r in ledger),
            "wall_seconds": sum(r["wall_seconds"] for r in ledger),
            "peak_rss_bytes": max(r["peak_rss_bytes"] for r in ledger),
            "artifact_bytes_including_reports": size(OUT) + size(REPORT),
            "fits": len(fits),
            "model_evaluations": len(statuses),
        }
        assert (
            resources["artifact_bytes_including_reports"]
            < receipt["manifest"]["limits"]["artifact_bytes"]
        )
        dump(REPORT / "resource-final.json", resources)
        print(json.dumps(audit))
    except Exception as exc:
        budget.finish("failed", repr(exc))
        raise


if __name__ == "__main__":
    main()
