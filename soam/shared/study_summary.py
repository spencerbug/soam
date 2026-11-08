"""Connect complete E1 cell inventories to the existing frozen inference rules."""

import numpy as np

from soam.platform.runner import read_arrays
from soam.shared.execution import FAMILIES, cell_inventory
from soam.shared.inference import classify, paired_intervals
from soam.shared.models import manifest


def root_summary(path, result, store, count=20):
    cells = result["cells"]
    if set(cells) != set(cell_inventory(count)):
        raise ValueError("missing or unexpected root cells")
    means = {}
    for name, cell in cells.items():
        if cell["status"] == "complete":
            condition = name.rsplit("-", 1)[0]
            means.setdefault(condition, []).append(cell["metrics"])
    means = {
        name: {key: np.mean([v[key] for v in values], axis=0).tolist() for key in values[0]}
        for name, values in means.items()
        if len(values) == count
    }
    summary = {
        "complete": all(cell["status"] == "complete" for cell in cells.values()),
        "condition_means": means,
        "fit_status": result["fits"],
        "cell_status_counts": {
            status: sum(c["status"] == status for c in cells.values())
            for status in sorted({c["status"] for c in cells.values()})
        },
    }
    if not summary["complete"]:
        return summary
    ratios, zero_ratios, predictions, targets, errors = [], [], [], [], []
    for i in range(count):
        arrays = {
            kind: read_arrays(path / "cells" / name / "arrays.npz")
            for kind, name in (
                ("intact", f"S32-recall_final-{i}"),
                ("perturb", f"perturb-{i}"),
                ("zero_S", f"zero_S-{i}"),
                ("zero_S_perturb", f"zero_S_perturb-{i}"),
            )
        }
        for a, b, destination in (
            ("intact", "perturb", ratios),
            ("zero_S", "zero_S_perturb", zero_ratios),
        ):
            initial = (
                (
                    arrays[b]["anchor_state"][:, :-2].double()
                    - arrays[a]["anchor_state"][:, :-2].double()
                )
                .square()
                .mean()
                .sqrt()
            )
            distance = (
                (
                    arrays[b]["free_states"][..., :-2].double()
                    - arrays[a]["free_states"][..., :-2].double()
                )
                .square()
                .mean((1, 2))
                .sqrt()
            )
            destination.append((distance / initial).numpy())
        predictions.append(arrays["perturb"]["free_features"][-1].double().numpy())
        episode = store.restore(path / "evaluation-data" / f"recall-{i}")[0]
        targets.append(episode.targets.features[-1].double().numpy())
        errors.append(cells[f"perturb-{i}"]["metrics"]["recall_nmse"])
    ratios, zero_ratios = np.array(ratios), np.array(zero_ratios)
    summary["recovery"] = {
        "distance_ratios_by_episode": ratios.tolist(),
        "zero_S_distance_ratios_by_episode": zero_ratios.tolist(),
        "halving_fraction": float(np.mean(ratios[:, -1] <= 0.5)),
        "halving_advantage": float(
            np.mean(ratios[:, -1] <= 0.5) - np.mean(zero_ratios[:, -1] <= 0.5)
        ),
        "perturbed_recall_nmse": float(np.mean(errors)),
        "false_recovery_fraction": float(np.mean(np.array(errors) > 0.05)),
        "feature_variance_ratio": float(
            np.var(np.concatenate(predictions), axis=0).mean()
            / np.var(np.concatenate(targets), axis=0).mean()
        ),
    }
    summary["exact_T32_equivalence_and_bank_isolation"] = True
    return summary


def aggregate(roots):
    protocol = manifest()
    expected = protocol["streams"]["confirmation_roots"]
    if list(roots) != expected:
        raise ValueError("exact ordered confirmation roots required; repeat is not an extra root")
    if not all(row["complete"] for row in roots.values()):
        return {
            "outcome": "incomplete_or_inconclusive_or_candidate_instability",
            "root_summaries": roots,
            "uncertainty": "unavailable for incomplete inventory",
        }
    utility, causal, recall, transition = [], [], [], []
    refs = protocol["comparisons"]["required_references"]
    floor = False
    for row in roots.values():
        m = row["condition_means"]
        s = m["S32-transition"]["free8_nmse"]
        r = m["S32-recall_final"]["recall_nmse"]
        comparisons = [m[f"{family}-transition"]["free8_nmse"] for family in refs]
        floor |= any(v <= 1e-6 for v in comparisons)
        utility.append(
            [(v - s) / max(v, 1e-6) for v in comparisons]
            + [
                r - m["S32-recall_pre"]["recall_nmse"],
                r - m["D25-recall_final"]["recall_nmse"],
            ]
        )
        causal.append(
            [
                m["targeted-recall"]["recall_nmse"] - r,
                m["targeted-transition"]["free8_nmse"] - s,
                m["targeted-recall"]["recall_nmse"] - m["readout-recall"]["recall_nmse"],
                m["targeted-transition"]["free8_nmse"] - m["readout-transition"]["free8_nmse"],
                (m["action_shift"]["free8_nmse"] - s) / max(s, 1e-6),
                (m["zero_A"]["free8_nmse"] - s) / max(s, 1e-6),
            ]
        )
        recall.append(r)
        transition.append(s)
    result = classify(
        utility=utility,
        causal=causal,
        candidate_recall=recall,
        candidate_transition=transition,
        floor_limited=floor,
    )
    # Always publish all seven/six intervals, even when an earlier floor rule wins.
    result.update(
        utility=paired_intervals(utility, family_size=7),
        causal=paired_intervals(causal, family_size=6),
        root_order=expected,
        root_summaries=roots,
        utility_root_contrasts=utility,
        causal_root_contrasts=causal,
        required_references=refs,
        T32="exact equality on separate-role episodes; not a superiority reference",
    )
    recovery = {}
    for name in (
        "halving_fraction",
        "halving_advantage",
        "perturbed_recall_nmse",
        "false_recovery_fraction",
        "feature_variance_ratio",
    ):
        recovery[name] = paired_intervals(
            [[r["recovery"][name]] for r in roots.values()], family_size=1
        )
    # This diagnostic has ordinary root intervals, separate from the utility gate.
    tests = [
        ("halving_fraction", 0.9, True),
        ("halving_advantage", 0.2, True),
        ("perturbed_recall_nmse", 0.02, False),
        ("false_recovery_fraction", 0.05, False),
        ("feature_variance_ratio", 0.8, True),
        ("feature_variance_ratio", 1.2, False),
    ]
    passes, overlaps = [], []
    for name, threshold, lower_bound in tests:
        lo, hi = recovery[name]["lower"][0], recovery[name]["upper"][0]
        passes.append(lo >= threshold if lower_bound else hi <= threshold)
        overlaps.append(lo <= threshold <= hi)
    result["recovery"] = {
        "intervals": recovery,
        "outcome": "finite_horizon_recovery_supported"
        if all(passes)
        else "inconclusive"
        if any(overlaps)
        else "diagnostic_criteria_not_met",
        "claim_limit": "finite-horizon recovery toward unperturbed trajectories, not global attraction",
    }
    # All family/condition means, including SYM32 and random lesions, stay visible.
    result["families"] = list(FAMILIES)
    return result
