"""A1 immutable input objects with explicit, verified replay references."""

import hashlib
import json
import re

from soam.platform.core import fingerprint

FILES = ("observations.npz", "clean-records.npz", "targets.npz", "streams.json")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(episodes):
    hashes = []
    for episode in episodes:
        arrays = {
            **episode.observed_arrays(),
            "clean": episode.clean_records,
            "target_features": episode.targets.features,
            "world": episode.targets.world,
        }
        hashes.append([fingerprint(arrays), episode.stream_seeds])
    return hashlib.sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class InputStore:
    def __init__(self, root, budget=None):
        self.root, self.budget = root, budget

    def object_path(self, key):
        if not isinstance(key, str) or re.fullmatch("[0-9a-f]{64}", key) is None:
            raise ValueError("invalid input object digest")
        path = self.root / key
        if self.root.is_symlink() or path.is_symlink():
            raise ValueError("symlink input store/object rejected")
        return path

    def verify(self, key, manifest_digest=None):
        path = self.object_path(key)
        if any(p.is_symlink() for p in path.iterdir()):
            raise ValueError("symlink object member rejected")
        if {p.name for p in path.iterdir()} != {*FILES, "manifest.json"}:
            raise ValueError("incomplete or unexpected input object members")
        if manifest_digest is not None and digest(path / "manifest.json") != manifest_digest:
            raise ValueError("input manifest digest mismatch")
        metadata = json.loads((path / "manifest.json").read_text())
        expected = {name: digest(path / name) for name in FILES}
        if metadata != {"version": "a1", "identity": key, "files": expected}:
            raise ValueError("input object integrity mismatch")
        return path

    def write(self, reference_path, episodes):
        from soam.shared.runner import archive_episodes, restore_episodes

        if self.budget is None:
            raise ValueError("writing requires a budget owner")
        self.budget.check()
        key = identity(episodes)
        path = self.object_path(key)
        if path.exists():
            self.verify(key)
            if identity(restore_episodes(path)) != key:
                raise ValueError("input identity collision or content mismatch")
        else:
            archive_episodes(path, episodes, self.budget)
            self.budget.json(
                path / "manifest.json",
                {
                    "version": "a1",
                    "identity": key,
                    "files": {name: digest(path / name) for name in FILES},
                },
            )
        reference = {
            "version": "a1",
            "object": key,
            "manifest_sha256": digest(path / "manifest.json"),
        }
        self.budget.json(reference_path / "input-ref.json", reference)
        self.budget.check()
        return key

    def restore(self, reference_path):
        from soam.shared.runner import restore_episodes

        reference = json.loads((reference_path / "input-ref.json").read_text())
        if (
            set(reference) != {"version", "object", "manifest_sha256"}
            or reference["version"] != "a1"
        ):
            raise ValueError("invalid input reference")
        path = self.verify(reference["object"], reference["manifest_sha256"])
        episodes = restore_episodes(path)
        if identity(episodes) != reference["object"]:
            raise ValueError("restored input identity mismatch")
        return episodes


def verify_contract():
    from soam.shared.models import ROOT

    expected = "fed2ac44ecd1183ddc35e79c1ef0a25ba55e7cbe5f372e87e025d896a1156a13"
    if digest(ROOT / "docs/E1_ARCHIVE_A1.md") != expected:
        raise ValueError("A1 archive contract changed")
    return expected
