"""Compare contract-check runs, excluding timing-bearing proposal/receipt IDs."""

import argparse
import json
from pathlib import Path

import torch

IGNORED = {
    "proposal_seconds",
    "commit_seconds",
    "rollback_seconds",
    "receipt_id",
    "proposal_id",
    "checkpoint_files",
}


def numerical(value):
    if isinstance(value, dict):
        return {k: numerical(v) for k, v in value.items() if k not in IGNORED}
    if isinstance(value, list):
        return [numerical(v) for v in value]
    return value


def verify(original, repeat):
    a = json.loads((original / "results.json").read_text())
    b = json.loads((repeat / "results.json").read_text())
    if not a or numerical(a) != numerical(b):
        raise AssertionError("Numerical contract metrics differ or no trials found")
    for left, right in zip(a, b):
        for label in ("before", "after"):
            x = torch.load(original / left["checkpoint_files"][label]["path"], weights_only=True)
            y = torch.load(repeat / right["checkpoint_files"][label]["path"], weights_only=True)
            if (
                x["identity"] != y["identity"]
                or x["state_dict"].keys() != y["state_dict"].keys()
                or not all(torch.equal(v, y["state_dict"][k]) for k, v in x["state_dict"].items())
            ):
                raise AssertionError(f"Checkpoint mismatch: {left['seed']}, {label}")
    return {
        "exact_metrics_and_checkpoint_match": True,
        "seeds": [r["seed"] for r in a],
        "excluded_fields": sorted(IGNORED),
        "note": "Checkpoint contents compared separately; proposal IDs contain execution timings.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("repeat", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.original, args.repeat)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
