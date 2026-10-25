import json
from dataclasses import replace

import pytest
import torch

from soam.config import Config
from soam.evaluation.compare import compare
from soam.evaluation.metrics import hidden_stability, prediction_metrics
from soam.evaluation.runner import run


def numeric_metrics(value):
    if isinstance(value, dict):
        return {key: numeric_metrics(item) for key, item in value.items() if "seconds" not in key}
    if isinstance(value, list):
        return [numeric_metrics(item) for item in value]
    return value


def test_metrics_detect_errors_and_instability():
    target = torch.ones(2, 4, 3)
    assert prediction_metrics(target, target)["nmse"] == 0
    assert prediction_metrics(torch.zeros_like(target), target)["nmse"] == 1
    hidden = torch.zeros(2, 4, 3)
    hidden[0, 2, 0] = 2
    assert hidden_stability(hidden, 1.5)["bound_violation_fraction"] == 0.5
    hidden[1, 2, 0] = float("nan")
    assert hidden_stability(hidden, 1.5)["invalid_trajectory_fraction"] == 0.5
    with pytest.raises(FloatingPointError):
        prediction_metrics(hidden, target)


def test_end_to_end_repeatability_provenance_and_no_overwrite(tmp_path):
    cfg = replace(Config.load("configs/smoke.json"), models=("additive",), steps=2)
    first = run(cfg, tmp_path / "first")
    repeat = run(cfg, tmp_path / "repeat")
    assert numeric_metrics(first) == numeric_metrics(repeat)
    provenance = json.loads((tmp_path / "first/provenance.json").read_text())
    assert len(provenance["source_sha256"]) == 64
    assert "soam/recurrent/models.py" in provenance["source_files"]
    assert provenance["deterministic_algorithms"]
    for name in ("checkpoint.pt", "diagnostics.png", "trajectories.npz", "metrics.json"):
        assert (tmp_path / "first/additive-seed11" / name).stat().st_size > 0
    with pytest.raises(FileExistsError):
        run(cfg, tmp_path / "first")
    compare([tmp_path / "first", tmp_path / "repeat"], tmp_path / "comparison.md")
    assert "## repeat" in (tmp_path / "comparison.md").read_text()
