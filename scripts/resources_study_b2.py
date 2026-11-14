"""Cost existing screened candidates; no new tuning or trials."""

import hashlib
import json
from pathlib import Path

import torch

from soam.robust.engine import latency, operation_profile
from soam.robust.models import Config, Robust
from soam.robust.runner import MANIFEST, OUT, ROOT, load_models, receipt_check
from soam.temporal.runner import Budget, dump


def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    receipt = receipt_check()
    budget = Budget(OUT, m, "screen-cost-audit")
    dest = OUT / "screen-cost-audit"
    dest.mkdir(exist_ok=False)
    try:
        base = load_models(OUT / "screen1/15101/fits")
        rows = {}
        for phase in ("screen1", "screen2", "hybrid"):
            configs = json.loads((OUT / phase / "configs.json").read_text())
            for config in configs:
                name = config["name"]
                model = Robust(base["FILTER2"], Config(**config))
                budget.check()
                source = [
                    json.loads((OUT / phase / str(r) / name / "results.json").read_text())
                    for r in m["development_roots"]
                ]
                rows[name] = {
                    "phase": phase,
                    "configuration": config,
                    "resources": model.resources(),
                    "primary_fit_shared_with": "FILTER2; no added fitting",
                    "screening_cpu_seconds_with_diagnostics": sum(
                        x["evaluation_cpu_seconds"] for x in source
                    ),
                    "development_root_headlines": [x["headline"] for x in source],
                    "latency": latency(model),
                    "operations": operation_profile(model),
                }
        dump(dest / "all-candidates.json", rows)
        dump(ROOT / "reports/study-b2/development-candidates.json", rows)
        dump(
            dest / "provenance.json",
            {
                "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "receipt": receipt["sha256"],
                "new_fits": 0,
                "selection_changed": False,
                "timing_data": "fixture; existing development-fitted weights only",
            },
        )
        budget.finish("complete")
    except BaseException as e:
        budget.finish("failed", repr(e))
        raise


if __name__ == "__main__":
    main()
