"""Read sealed E1 evidence; write only a new Prompt 0 verification receipt."""
import hashlib
import json
import platform
import resource
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

from soam.shared.archive import InputStore
from soam.shared.continuation import tree_identity
from soam.shared.execution import compare_repeat

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("verification.json")
assert not OUT.exists(), "Preserve prior preflight receipt"
started_cpu, started_wall = time.process_time(), time.perf_counter()
torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check():
    assert time.process_time() - started_cpu < 120, "Read-only audit CPU limit"
    assert time.perf_counter() - started_wall < 240, "Read-only audit wall limit"
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 2 * 1024**3


compact = ROOT / "reports/shared-population-study/confirmation"
raw = ROOT / "runs/e1-confirmation-v1-a1"
record = read(compact / "provenance.json")
sources = {}
for name, expected in record["source_files"].items():
    at_run = subprocess.check_output(["git", "show", record["commit"] + ":" + name], cwd=ROOT)
    assert hashlib.sha256(at_run).hexdigest() == expected == sha(ROOT / name), name
    sources[name] = expected
assert hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest() == record["source_sha256"]

checked = {}
for folder in ("e1-archive-a1", "shared-population-harness", "shared-population-study/development",
               "shared-population-study/continuation", "shared-population-study/confirmation",
               "shared-population-gate"):
    parent = ROOT / "reports" / folder
    for name, expected in read(parent / "sha256.json").items():
        assert sha(parent / name) == expected, (folder, name)
        checked[str((parent / name).relative_to(ROOT))] = expected

gate = read(ROOT / "reports/shared-population-gate/audit.json")
archives = {}
for name, key in (("e1-development-v1-a1", "development_archive"),
                  ("e1-confirmation-v1-a1", "confirmation_archive")):
    check()
    actual = tree_identity(ROOT / "runs" / name)
    assert actual == gate[key], name
    archives[name] = actual

for name in ("config.json", "provenance.json", "inventory.json", "result.json", "reproduction.json", "status.json"):
    assert sha(compact / name) == sha(raw / name), name
config = read(raw / "config.json")
resolved = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
assert resolved == gate["resolved_study_config_sha256"]
repeat = compare_repeat(raw / "confirmation/11", raw / "repeat/11", InputStore(raw / "input-objects"), check)
assert repeat == read(compact / "reproduction.json")
check()
manifest = read(ROOT / "docs/protocols/shared_population_v1.json")
receipt = {
    "date": "2026-11-10", "review_commit": git("rev-parse", "HEAD"),
    "branch": git("branch", "--show-current"), "git_status": git("status", "--short"),
    "command": "UV_CACHE_DIR=/private/tmp/soam-prompt0-uv-cache uv run --offline python reports/preflight-2026-11-10/verify.py",
    "environment": {"python": platform.python_version(), "platform": platform.platform(),
                    "numpy": np.__version__, "torch": torch.__version__, "torch_threads": torch.get_num_threads(),
                    "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
                    "uv_lock_sha256": sha(ROOT / "uv.lock"), "device": "cpu"},
    "execution_commit": record["commit"], "source_sha256": record["source_sha256"],
    "source_files_verified": sources, "compact_files_verified": checked, "archives": archives,
    "resolved_study_config_sha256": resolved, "config_file_sha256": sha(raw / "config.json"),
    "capture_wrapper_config_sha256": record["config_sha256"],
    "protocol_sha256": record["protocol_sha256"], "manifest_sha256": record["manifest_sha256"],
    "streams": manifest["streams"], "selected_configs": config["selected_configs"],
    "archived_repeat_rechecked": repeat, "new_fits": 0, "new_scientific_observations": 0,
    "scope": "Repository engineering preflight; archived repeat compared, no models refitted or new trial allocation",
    "cpu_seconds": time.process_time() - started_cpu,
    "wall_seconds": time.perf_counter() - started_wall,
    "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}
OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: receipt[k] for k in ("review_commit", "environment", "archives", "archived_repeat_rechecked", "cpu_seconds", "wall_seconds", "peak_rss_bytes")}, indent=2))
