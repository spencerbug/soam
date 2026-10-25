"""Capture source and runtime identity without depending on a remote repository."""

import hashlib
import json
import os
import platform
import subprocess
import sys

import numpy as np
import torch


def git(repo, *args):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def capture(repo, config):
    paths = sorted(
        [
            *repo.glob("soam/**/*.py"),
            *repo.glob("tests/**/*.py"),
            *repo.glob("configs/*.json"),
            repo / "pyproject.toml",
            repo / "uv.lock",
        ]
    )
    hashes = {
        str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
        if p.is_file()
    }
    source_hash = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    config_hash = hashlib.sha256(json.dumps(config.to_dict(), sort_keys=True).encode()).hexdigest()
    return {
        "commit": git(repo, "rev-parse", "HEAD"),
        "git_status": git(repo, "status", "--porcelain"),
        "source_sha256": source_hash,
        "source_files": hashes,
        "config_sha256": config_hash,
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "device": "cpu",
        "dtype": "float32",
        "torch_threads": config.threads,
        "deterministic_algorithms": True,
        "pid": os.getpid(),
    }
