"""Load the preregistered manifest and derive independent, reproducible streams."""

import hashlib
import json
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/protocols/handover_v1.json"
DOCUMENT = ROOT / "docs/HANDOVER_PROTOCOL.md"
V1_MANIFEST_SHA256 = "79875fee3b53bb00c385d6572dfa309e7f359371b449c2266d59261076b79611"
V1_DOCUMENT_SHA256 = "b0deaca9e98601bb7ba7252f677b1cae5416b5315f6778c8ecf9d6a51dbeb6c9"


def load_protocol(path=MANIFEST):
    if sha256(path) != V1_MANIFEST_SHA256 or sha256(DOCUMENT) != V1_DOCUMENT_SHA256:
        raise ValueError(
            "v1 protocol fingerprint changed; review a versioned amendment before running"
        )
    data = json.loads(Path(path).read_text())
    if data["protocol_id"] != "soam-handover-v1":
        raise ValueError("unsupported handover protocol")
    cells = data["episode_cells"]
    if len(cells) != 62 or len({json.dumps(c, sort_keys=True) for c in cells}) != 62:
        raise ValueError("v1 requires 62 distinct episode cells")
    if data["variants"] != ["A2", "A1", "G2", "GS24", "GS9"]:
        raise ValueError("unsupported candidate layout")
    if data["environment"]["observations"] != 192:
        raise ValueError("v1 requires the full observation schedule")
    if data["cue"]["dimension"] != 16 or data["environment"]["projection_dim"] != 12:
        raise ValueError("unsupported v1 dimensions")
    return data


def seed_sequence(seed, split, condition, episode, component):
    manifest = load_protocol()
    splits = manifest["rng"]["split_ids"]
    components = manifest["rng"]["component_ids"]
    if split not in splits or component not in components:
        raise ValueError("unknown stream")
    if any(type(x) is not int or x < 0 for x in (seed, condition, episode)):
        raise ValueError("stream indices must be nonnegative integers")
    return np.random.SeedSequence(
        [
            manifest["rng"]["namespace"],
            seed,
            splits[split],
            condition,
            episode,
            components[component],
        ]
    )


def rng(seed, split, condition, episode, component):
    return np.random.default_rng(seed_sequence(seed, split, condition, episode, component))


def initialization_seed(seed, architecture):
    index = {"selector": 0, "G2": 1, "GS24": 2, "GS9": 3}[architecture]
    # Weight initialization belongs to the training namespace even for an unfitted smoke model.
    sequence = seed_sequence(seed, "train", 0, index, "initialization")
    return int(sequence.generate_state(1, dtype=np.uint64)[0]) % (2**63 - 1)


def templates():
    h = torch.ones(1, 1)
    for _ in range(4):
        h = torch.cat((torch.cat((h, h), 1), torch.cat((h, -h), 1)), 0)
    return h[:, load_protocol()["cue"]["hadamard_columns_zero_based"]] / 4


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tensor_fingerprint(tensors):
    digest = hashlib.sha256()
    for name, value in sorted(tensors.items()):
        tensor = value.detach().cpu().contiguous()
        digest.update(name.encode())
        digest.update(str((tensor.dtype, tuple(tensor.shape))).encode())
        digest.update(tensor.numpy().tobytes())
    return digest.hexdigest()
