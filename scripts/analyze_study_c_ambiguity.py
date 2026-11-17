"""Post-confirmation descriptive audits from saved arrays; no fitting or selection."""

import hashlib
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.ambiguity.data import PRIMARY
from soam.ambiguity.runner import MANIFEST, OUT, REPORT, receipt_check
from soam.robust.statistics import interval
from soam.temporal.runner import Budget, dump


def main():
    m = json.loads(MANIFEST.read_text())
    receipt = receipt_check()
    roots = m["confirmation_roots"]
    names = receipt["selection"]["inventory"]
    dest = OUT / "secondary-audit"
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m["limits"], "secondary-audit")
    try:
        draws = np.random.default_rng(m["bootstrap_seed"]).integers(0, 10, (20000, 10))
        limits, delayed, calibration = {}, {}, {}
        bins = np.linspace(0, 1, 11)
        for name in names:
            pair_scores, confident, nll, reveal, next_cue = [], [], [], [], []
            bin_roots = []
            for root in roots:
                budget.check()
                base = OUT / "confirmation" / str(root) / name
                with np.load(base / "change.npz") as a, np.load(base / "coherent.npz") as b:
                    assert np.array_equal(a["prob"], b["prob"])
                    p = a["prob"][23:].astype(float)
                    y1, y2 = a["labels"][23:], b["labels"][23:]
                    assert np.array_equal(y1, 1 - y2)
                    pair_scores.append(float(0.5 * (np.square(p - y1) + np.square(p - y2)).mean()))
                    confident.append(float((np.maximum(p, 1 - p) > 0.95).mean()))
                    q = np.clip(p, 1e-8, 1 - 1e-8)
                    nll.append(float(-0.5 * (np.log(q) + np.log(1 - q)).mean()))
                with np.load(base / "delayed.npz") as a:
                    reveal.append(float(np.square(a["prob"][27] - a["labels"][27]).mean()))
                    next_cue.append(float(np.square(a["prob"][31] - a["labels"][31]).mean()))
                records = np.zeros((10, 3))
                for condition in PRIMARY:
                    with np.load(base / (condition + ".npz")) as a:
                        p, y = a["prob"].flatten().astype(float), a["labels"].flatten()
                        index = np.minimum(np.searchsorted(bins, p, side="right") - 1, 9)
                        for j in range(10):
                            use = index == j
                            records[j] += [use.sum(), p[use].sum(), y[use].sum()]
                bin_roots.append(records)
            limits[name] = {
                "paired_brier_post24": interval(pair_scores, draws=draws),
                "confident_fraction_post24": interval(confident, draws=draws),
                "paired_nll_post24": interval(nll, draws=draws),
                "brier_floor": 0.25,
                "nll_floor": float(np.log(2)),
                "label": "equal-prior constructed cause pair; descriptive stress, not a new primary gate",
            }
            delayed[name] = {
                "first_revealing_cue_brier": interval(reveal, draws=draws),
                "next_cue_brier": interval(next_cue, draws=draws),
            }
            data = np.array(bin_roots)
            totals = data.sum(0)
            sampled = data[draws].sum(1)
            rows = []
            for j in range(10):
                valid = sampled[:, j, 0] > 0
                rate = sampled[valid, j, 2] / sampled[valid, j, 0]
                rows.append(
                    {
                        "bin": j,
                        "count": int(totals[j, 0]),
                        "mean_probability": float(totals[j, 1] / totals[j, 0])
                        if totals[j, 0]
                        else None,
                        "frequency": float(totals[j, 2] / totals[j, 0]) if totals[j, 0] else None,
                        "frequency_interval": np.quantile(rate, [0.025, 0.975]).tolist()
                        if len(rate)
                        else None,
                    }
                )
            calibration[name] = rows
        results = json.loads((REPORT / "root-results.json").read_text())
        contrasts = {}
        for reference in ("ADAPT1-C", "FILTER2-C", "FILTER2-M"):
            contrasts["TWO16 vs " + reference] = {
                metric: interval(
                    [
                        results[str(r)][reference]["headline"][metric]
                        - results[str(r)]["TWO16"]["headline"][metric]
                        for r in roots
                    ],
                    draws=draws,
                )
                for metric in ("brier", "prior_nmse", "late_brier")
            }
        dump(REPORT / "ambiguity-limits.json", limits)
        dump(REPORT / "delayed-resolution.json", delayed)
        dump(REPORT / "calibration.json", calibration)
        dump(REPORT / "secondary-family-comparisons.json", contrasts)
        fig, ax = plt.subplots(figsize=(7, 6), constrained_layout=True)
        ax.plot([0, 1], [0, 1], "k--", lw=1, label="Calibrated frequency")
        for name in ("PC16", receipt["selection"]["r2"], "TWO16", "ADAPT1-C", "ADAPT1-M"):
            rows = [x for x in calibration[name] if x["count"] >= 100]
            ax.plot(
                [x["mean_probability"] for x in rows],
                [x["frequency"] for x in rows],
                "o-",
                label=name,
            )
        ax.set(
            xlabel="Mean candidate probability",
            ylabel="Observed + frequency",
            xlim=(0, 1),
            ylim=(0, 1),
            title="Primary-condition calibration (descriptive bins)",
        )
        ax.legend(fontsize=9)
        for extension in ("png", "svg"):
            fig.savefig(REPORT / ("calibration." + extension), dpi=160)
        plt.close(fig)
        source_path = Path(__file__).resolve()
        dump(
            dest / "provenance.json",
            {
                "script": str(source_path),
                "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
                "confirmation_receipt": receipt["sha256"],
                "scope": "saved-array descriptive calibration/information-limit audit only; no primary threshold, source mechanism, fit, selection or confirmation observation changed",
            },
        )
        budget.check(force=True)
        budget.finish("complete")
    except Exception as error:
        budget.finish("failed", repr(error))
        raise


if __name__ == "__main__":
    main()
