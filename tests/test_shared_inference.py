import numpy as np
import pytest

from soam.shared.inference import choose_configs, classify, paired_intervals
from soam.shared.models import manifest


def test_bootstrap_pairs_roots_and_uses_fixed_family_correction():
    values = np.arange(10, dtype=float) / 100
    matrix = np.stack([values] * 7, 1)
    intervals = paired_intervals(matrix, family_size=7)
    assert intervals == paired_intervals(matrix, family_size=7)
    assert len(set(intervals["lower"])) == 1
    assert intervals["lower"][0] <= intervals["ordinary_lower"][0]
    with pytest.raises(ValueError, match="ten paired roots"):
        paired_intervals(np.ones((200, 7)), family_size=7)


def test_development_selection_ignores_recall_for_tuning_but_enforces_screen():
    data = {
        r["id"]: np.tile([[[0.1, 0.02]], [[0.1 - 1e-13, 0.01]]], (1, 3, 1))
        for r in manifest()["models"]
    }
    decision = choose_configs(data)
    assert set(decision["selected_configs"].values()) == {0}
    assert decision["primary_reference"] == "D25"
    assert decision["confirmation_allowed"]
    data["G28"][0, :, 1] = 0.04
    decision = choose_configs(data)
    assert not decision["confirmation_allowed"]
    data["L12"][:, :, 0] = 1e-7
    assert choose_configs(data)["floor_limited"]


def evidence():
    return {
        "utility": np.tile([0.2] * 5 + [0.0, 0.0], (10, 1)),
        "causal": np.tile([0.01, 0.01, 0.004, 0.004, 0.2, 0.2], (10, 1)),
        "candidate_recall": np.full(10, 0.01),
        "candidate_transition": np.full(10, 0.05),
    }


def test_frozen_outcome_precedence_and_negative_result():
    data = evidence()
    assert classify(**data)["outcome"] == "useful_sharing_supported"
    assert (
        classify(**data, invalid=True, incomplete=True)["outcome"]
        == "invalid_execution_or_comparison"
    )
    data["candidate_recall"][:] = 0.03
    assert classify(**data, incomplete=True)["outcome"].startswith("incomplete")
    assert classify(**data)["outcome"] == "recall_interference_or_failure"
    data = evidence()
    data["causal"][:, 4] = 0.01
    assert classify(**data)["outcome"] == "directional_failure"
    data = evidence()
    data["utility"][:, 0] = 0.05
    assert classify(**data)["outcome"] == "precise_no_practical_benefit"
    data = evidence()
    data["utility"][:, 5] = np.linspace(-0.1, 0.1, 10)
    assert classify(**data)["outcome"] == "inconclusive_or_mechanism_unresolved"
