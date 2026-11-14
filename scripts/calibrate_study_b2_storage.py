"""Engineering addendum: measure compression at the actual batch size before screening."""

import io
import json

import numpy as np
import torch

from soam.robust.data import normalization
from soam.robust.engine import batches, evaluate
from soam.robust.models import Config, Robust
from soam.robust.runner import MANIFEST, OUT, load_models, snapshot
from soam.temporal.runner import Budget, dump


def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    budget = Budget(OUT, m, "fixture-storage-a1")
    dest = OUT / "fixture-storage-a1"
    dest.mkdir(exist_ok=False)
    try:
        snapshot(dest)
        model = Robust(load_models(OUT / "fixture/fits")["FILTER2"], Config("HUBER99", "huber"))
        data = batches("fixture", m["fixture_root"], 20)
        sizes = {}
        cpu = {}
        for detail in (False, True):
            _, arrays, cost = evaluate(model, data, normalization(), budget.check, detail)
            stream = io.BytesIO()
            np.savez_compressed(stream, **arrays)
            sizes[str(detail)] = len(stream.getvalue())
            cpu[str(detail)] = cost
        original = json.loads((OUT / "fixture/projection.json").read_text())
        artifact = 1.5 * (140 * sizes["False"] + 8 * (sizes["True"] - sizes["False"]) + 30 * 2**20)
        projected_cpu = original["projected_cpu_seconds"] + 1.5 * 200 * max(
            0, cpu["False"] - max(v["evaluation_cpu_seconds"] for v in original["timings"].values())
        )
        result = {
            "supersedes_storage_projection_only": "fixture-storage-correction failed; A1 bounds actual inventory at130+10reserve evaluations, detailed traces only every4 first4 episodes, all error arrays retained",
            "compressed_bytes": sizes,
            "actual_batch": 20,
            "measured_cpu": cpu,
            "projected_artifact_bytes": artifact,
            "projected_cpu_seconds": projected_cpu,
            "projection_pass": artifact < m["artifact_bytes"]
            and projected_cpu < m["cpu_seconds"] * 0.9,
            "original_fixture_preserved": True,
        }
        dump(dest / "projection.json", result)
        assert result["projection_pass"]
        budget.finish("complete")
    except BaseException as e:
        budget.finish("failed", repr(e))
        raise


if __name__ == "__main__":
    main()
