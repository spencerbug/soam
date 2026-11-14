"""Measure actual matrix-gain attenuation separately from diagnostic precision weights."""

import hashlib
import json
from pathlib import Path

import numpy as np
import torch

from soam.robust.data import INTERMITTENT, generate
from soam.robust.engine import trace
from soam.robust.models import Config, Robust
from soam.robust.runner import MANIFEST, OUT, ROOT, load_models, receipt_check
from soam.robust.statistics import interval
from soam.temporal.runner import Budget, dump


@torch.no_grad()
def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    receipt = receipt_check()
    budget = Budget(OUT, m, "effective-gain-audit")
    dest = OUT / "effective-gain-audit"
    dest.mkdir(exist_ok=False)
    try:
        roots = receipt["confirmation_roots"]
        results = {}
        for root in roots:
            base = load_models(OUT / "confirmation" / str(root) / "fits")["FILTER2"]
            helper = Robust(base, Config())
            for name in receipt["inventory"]:
                if name == "PC16":
                    continue
                model = (
                    base if name == "FILTER2" else Robust(base, Config(**receipt["configs"][name]))
                )
                rows = {}
                for condition in (
                    "clean",
                    "partial",
                    "missing",
                    "noise",
                    "change",
                    "corrupt",
                    "coherent",
                    "sustained",
                ):
                    scores = []
                    for schedule in INTERMITTENT:
                        budget.check()
                        b = generate(
                            "confirmation", root, batch=20, condition=condition, schedule=schedule
                        )
                        path = trace(model, b.evidence)
                        shape = path["state"].shape[:2]
                        cov = path["state"][..., 2:6].double().reshape(-1, 2, 2)
                        mask = b.evidence.mask[1:].reshape(-1, 12)
                        gain, _ = helper._gain(
                            cov, mask, torch.full(mask.shape, 0.0001, dtype=torch.double)
                        )
                        reference = gain.norm(dim=(-1, -2)).reshape(shape)
                        actual = path["gain"].norm(dim=(-1, -2))
                        sensed = b.evidence.mask[1:].any(-1)
                        ratio = (actual / reference.clamp_min(1e-30))[sensed]
                        scores.append(
                            {
                                "mean_gain_ratio": float(ratio.mean()),
                                "gain_ratio_below_half": float((ratio < 0.5).double().mean()),
                                "observed_count": int(sensed.sum()),
                                "rejected_count": int((ratio == 0).sum()),
                                "downweighted_count": int((ratio < 0.5).sum()),
                            }
                        )
                    rows[condition] = {k: float(np.mean([v[k] for v in scores])) for k in scores[0]}
                results.setdefault(name, {})[str(root)] = rows
        draws = np.random.default_rng(m["bootstrap_seed"]).integers(
            0, len(roots), (m["bootstrap_resamples"], len(roots))
        )
        cis = {
            n: {
                c: {
                    k: interval([results[n][str(r)][c][k] for r in roots], draws=draws)
                    for k in results[n][str(roots[0])][c]
                }
                for c in results[n][str(roots[0])]
            }
            for n in results
        }
        record = {
            "roots": results,
            "intervals": cis,
            "definition": "Frobenius norm of actual gain divided by nominal-R gain at SAME actual prior covariance and mask. Counts are mean per intermittent cell; diagnostic precision multipliers are separate. PC16 has no Kalman gain matrix; fixed control0.5 is not a probability.",
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "receipt": receipt["sha256"],
            "selection_changed": False,
        }
        dump(dest / "effective-gain.json", record)
        dump(ROOT / "reports/study-b2/effective-gain.json", record)
        budget.finish("complete")
    except BaseException as e:
        budget.finish("failed", repr(e))
        raise


if __name__ == "__main__":
    main()
