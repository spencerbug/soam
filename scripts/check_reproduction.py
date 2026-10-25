"""Verify repeated metrics/checkpoints/trajectories; timing is intentionally excluded."""

import argparse
import json
from pathlib import Path

import numpy as np
import torch

TIMING_KEYS = {"training_seconds", "rollout_seconds", "seconds_per_transition"}


def numerical(value):
    if isinstance(value, dict):
        return {key: numerical(item) for key, item in value.items() if key not in TIMING_KEYS}
    if isinstance(value, list):
        return [numerical(item) for item in value]
    return value


def verify(original, repeat):
    first = json.loads((original / "results.json").read_text())
    second = json.loads((repeat / "results.json").read_text())
    indexed = {(row["model"], row["seed"]): row for row in first}
    checked = []
    for row in second:
        key = row["model"], row["seed"]
        if numerical(indexed[key]) != numerical(row):
            raise AssertionError(f"Numerical metrics differ for {key}")
        folder = f"{key[0]}-seed{key[1]}"
        a = torch.load(original / folder / "checkpoint.pt", weights_only=True)["state_dict"]
        b = torch.load(repeat / folder / "checkpoint.pt", weights_only=True)["state_dict"]
        if set(a) != set(b) or not all(torch.equal(a[k], b[k]) for k in a):
            raise AssertionError(f"Checkpoint parameters differ for {key}")
        with (
            np.load(original / folder / "trajectories.npz") as a,
            np.load(repeat / folder / "trajectories.npz") as b,
        ):
            if set(a.files) != set(b.files) or not all(np.array_equal(a[k], b[k]) for k in a):
                raise AssertionError(f"Saved trajectories differ for {key}")
        checked.append({"model": key[0], "seed": key[1]})
    if not checked:
        raise ValueError("No repeated runs found")
    return {
        "exact_numerical_match": True,
        "checked": checked,
        "excluded_fields": sorted(TIMING_KEYS),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("repeat", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.original, args.repeat)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text)
