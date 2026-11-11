"""Independent, read-only numerical/archive audit; charges cumulative Study A budget."""

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import torch

from soam.gating.engine import rollout
from soam.gating.models import Core, fold_fixed_reset
from soam.gating.runner import Budget, digest, dump

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-a-v2"
m = json.loads((OUT / "manifest.json").read_text())
budget = Budget(OUT, m)
torch.set_num_threads(1)
checks = {}
metrics_checked = 0
original_source = json.loads((OUT / "source.json").read_text())
source = json.loads((OUT / "source-amendment.json").read_text())["new_source"]
checks["source_matches_snapshot"] = all(
    hashlib.sha256((ROOT / k).read_bytes()).hexdigest() == v for k, v in source["files"].items()
)
checks["archived_source_matches"] = all(
    hashlib.sha256((OUT / "source" / k).read_bytes()).hexdigest() == v
    for k, v in original_source["files"].items()
)
checks["amended_source_archive_matches"] = all(
    hashlib.sha256((OUT / "source-amendment" / k).read_bytes()).hexdigest() == source["files"][k]
    for k in json.loads((OUT / "source-amendment.json").read_text())["changed_files"]
)
e1 = json.loads((ROOT / "reports/shared-population-study/confirmation/provenance.json").read_text())
checks["historical_e1_source_unchanged"] = all(
    hashlib.sha256((ROOT / k).read_bytes()).hexdigest() == v for k, v in e1["source_files"].items()
)
records = json.loads((OUT / "confirmation/results.json").read_text())
norm = torch.load(OUT / "normalization.pt", weights_only=False)
variance = norm["variance"]
rows = []
max_diff = 0.0
fold_max_difference = 0.0
for root in m["confirmation_roots"]:
    budget.check(reserve=False)
    ev = torch.load(OUT / "confirmation" / f"evaluation-{root}.pt", weights_only=False)
    root_records = [r for r in records if r["root"] == root]
    assert len({r["numerical"]["input"] for r in root_records}) == 1
    assert len({r["numerical"]["evaluation_input"] for r in root_records}) == 1
    for rec in root_records:
        path = OUT / "confirmation" / f"{root}-{rec['model']}-c{rec['config']}"
        paths = torch.load(path / "paths.pt", weights_only=False)
        recall = (
            paths["recall"]["output"][-1].numpy().astype(np.float64)
            - ev[0].clean[-1].numpy().astype(np.float64)
        ) ** 2
        free = (
            paths["free"]["output"].numpy().astype(np.float64)
            - ev[1].clean[1:].numpy().astype(np.float64)
        ) ** 2
        grounded = (
            paths["grounded"]["output"].numpy().astype(np.float64)
            - ev[1].clean[1:].numpy().astype(np.float64)
        ) ** 2
        measured = {
            "recall": recall.mean() / variance,
            "free8": free[:8].mean() / variance,
            "free32": free[:32].mean() / variance,
            "grounded32": grounded[:32].mean() / variance,
        }
        measured["J"] = 0.5 * (measured["recall"] + measured["free8"])
        for key, val in measured.items():
            diff = abs(float(val) - rec["metrics"][key])
            max_diff = max(max_diff, diff)
            assert diff < 1e-12
            metrics_checked += 1
        ck = torch.load(path / "checkpoint.pt", weights_only=False)

        def size(x):
            if isinstance(x, torch.Tensor):
                return x.numel() * x.element_size()
            if isinstance(x, dict):
                return sum(size(v) for v in x.values())
            if isinstance(x, (list, tuple)):
                return sum(size(v) for v in x)
            return 0

        assert digest(ck["model"]) == rec["numerical"]["checkpoint"]
        assert digest(ck["optimizer"]) == rec["numerical"]["optimizer"]
        assert digest(paths) == rec["numerical"]["paths"]
        if rec["model"] == "FR32":
            original = Core("fixed_reset", 32, rec["initialization_seed"])
            original.load_state_dict(ck["model"])
            folded = fold_fixed_reset(original)
            with torch.no_grad():
                for batch, role in zip(ev, ["recall", "free"]):
                    prediction = rollout(folded, *batch.inputs())["output"]
                    difference = float((prediction - paths[role]["output"]).abs().max())
                    fold_max_difference = max(fold_max_difference, difference)
                    assert difference < 1e-5
        diag = torch.load(path / "diagnostics.pt", weights_only=False)
        assert digest(diag) == rec["numerical"]["diagnostics"]
        for role in ("recall", "transition", "switch"):
            for gate in ("alpha", "reset"):
                values = diag[role]["path"][gate]
                assert values.isfinite().all() and (values >= 0).all() and (values <= 1).all()
        rows.append(
            {
                "root": root,
                "model": rec["model"],
                "persistent_tensor_bytes": size(ck["model"]),
                "optimizer_tensor_bytes": size(ck["optimizer"]),
                "diagnostic_probe_tensor_bytes": size(diag["probes"]),
                "trained_parameters": sum(v.numel() for v in ck["model"].values()),
                "fit_cpu_seconds": rec["fit_cpu"],
            }
        )
checks.update(
    metric_reductions=True,
    paired_training_and_evaluation=True,
    checkpoint_optimizer_and_trajectory_hashes=True,
    finite_bounded_gate_values=True,
)
repeat = json.loads((OUT / "repeat/reproduction.json").read_text())
checks["exact_scientific_repeat"] = repeat["exact"] and set(repeat["models"]) == set(m["variants"])
inv = json.loads((OUT / "inventory.json").read_text())
checks["complete_v2_inventory"] = len(inv) == 192 and set(inv.values()) == {"complete"}
checks["v1_confirmation_unexposed"] = not (ROOT / "runs/study-a-v1/confirmation").exists()
receipt = json.loads((OUT / "freeze/receipt.json").read_text())
expected = receipt.pop("sha256")
checks["frozen_receipt_hash"] = digest(receipt) == expected
checks["all"] = all(checks.values())
result = {
    "checks": checks,
    "independently_reduced_metrics": metrics_checked,
    "maximum_reduction_difference": max_diff,
    "fixed_reset_folding_max_output_difference": fold_max_difference,
    "resources": rows,
    "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scientific_source": source["sha256"],
    "cpu_seconds_at_write": time.process_time(),
}
dump(ROOT / "reports/study-a/audit.json", result)
assert checks["all"]
budget.finish("independent-audit", "complete")
print(json.dumps({k: v for k, v in result.items() if k != "resources"}, indent=2))
