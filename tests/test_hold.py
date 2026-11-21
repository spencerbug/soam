"""Pairing, evidence boundaries, loss weighting and inference rules for E0-HOLD."""

import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import torch
from torch import nn

from soam.hold.runner import MANIFEST, inventory
from soam.hold.statistics import classify, rules, summarize
from soam.hold.training import eligible, fit, mapped_root, objective, state_hash
from soam.navigation.data import Batch, Evidence, generate
from soam.navigation.engine import evaluate, rollout
from soam.navigation.engine import fit as old_fit
from soam.navigation.models import make


@pytest.fixture
def config():
    cfg = json.loads(MANIFEST.read_text())
    cfg.update(
        updates=3,
        batch=8,
        train_horizon=4,
        long_horizon=9,
        evaluation_batch=4,
        free_horizon=6,
        grid=32,
        atlas_burnin=2,
        stationary_steps=8,
        perturbation_steps=4,
    )
    return cfg


@pytest.mark.parametrize("name", ["NAV32", "SYM32", "GRU32"])
def test_short_arm_exactly_reproduces_historical_fitter(name, config):
    a, b = make(name, 7), make(name, 7)
    first = old_fit(a, mapped_root(9301), config, 0.003, fixture=True)
    second = fit(b, mapped_root(9301), config, "SHORT24", fixture=True)
    np.testing.assert_array_equal(first["trace"], second["trace"])
    assert state_hash(a) == state_hash(b)
    assert first["training_data_sha256"] == second["training_data_sha256"]


def test_same_data_and_initialization_no_extra_observations(config):
    a, b = make("NAV32", 18), make("NAV32", 18)
    assert state_hash(a) == state_hash(b)
    short = fit(a, mapped_root(9301), config, "SHORT24", fixture=True)
    long = fit(b, mapped_root(9301), config, "LONG128", fixture=True)
    assert short["training_data_sha256"] == long["training_data_sha256"]
    x, y = short["exposure"], long["exposure"]
    assert x["extra_observations"] == y["extra_observations"] == 0
    assert x["eligible_stationary_episodes"] == y["eligible_stationary_episodes"] > 0
    assert y["extra_stationary_transition_examples"] == y["eligible_stationary_episodes"] * 5
    assert x["extra_stationary_transition_examples"] == 0
    assert x["distinct_prefix_sensory_snapshots"] == y["distinct_prefix_sensory_snapshots"]
    before = copy.deepcopy(b.state_dict())
    evaluate(b, "fixture", mapped_root(9301), config)
    assert all(torch.equal(before[k], v) for k, v in b.state_dict().items())


def test_stationary_eligibility_and_prefix_objective():
    batch, _ = generate("fixture", mapped_root(9301), batch=32, horizon=4)
    model = make("GRU32", 4)
    path = rollout(model, batch.evidence)
    expected = 12 * (
        (path["prior"] - batch.target[1:]).square().mean()
        + 0.5 * (path["posterior"] - batch.target).square().mean()
    )
    torch.testing.assert_close(objective(model, batch, 4), expected)
    stationary = eligible(batch)
    assert stationary.any()
    bad = batch.target.clone()
    bad[-1, stationary] += 0.1
    with pytest.raises(AssertionError, match="constant"):
        eligible(replace(batch, target=bad))


def test_equal_episode_weight_and_no_moving_or_observed_tail():
    # A constant-error test double makes excess stationary loss weighting detectable.
    class Constant(nn.Module):
        def __init__(self):
            super().__init__()
            self.level = nn.Parameter(torch.tensor(0.1))
            self.calls, self.corrections = [], 0

        def initialize(self, z, mask):
            return torch.arange(len(z)).float()[:, None]

        def readout(self, h):
            return self.level.expand(len(h), 12)

        def predict(self, h, action):
            self.calls.append((h.clone(), action.clone()))
            return h

        def correct(self, h, z, mask):
            self.corrections += 1
            return h

    target = torch.tensor([0.2, 0.7]).reshape(1, 2, 1).expand(5, 2, 12).clone()
    actions = torch.zeros(4, 2, 1)
    actions[:, 1] = 0.1
    evidence = Evidence(target.clone(), torch.ones_like(target, dtype=torch.bool), actions)
    batch = Batch(evidence, target)
    short, long = Constant(), Constant()
    a, b = objective(short, batch, 4), objective(long, batch, 9)
    torch.testing.assert_close(a, b, atol=1e-6, rtol=1e-6)
    a.backward()
    b.backward()
    torch.testing.assert_close(short.level.grad, long.level.grad)
    assert long.corrections == 4 and len(long.calls) == 9
    assert all(len(h) == 1 and not h.any() and not action.any() for h, action in long.calls[4:])


def test_fresh_streams_inventory_and_historical_sources():
    cfg = json.loads(MANIFEST.read_text())
    roots = {mapped_root(r) for r in cfg["confirmation_roots"]}
    assert len(roots) == 20 and not roots.intersection(range(101, 211))
    rows = inventory(cfg)
    assert len(rows) == len({r["id"] for r in rows}) == 147
    assert sum(r["phase"] == "confirmation" for r in rows) == 140
    assert len(inventory(cfg, fixture=True)) == 7
    frozen = json.loads(Path("reports/study-e0/receipt.json").read_text())["source"]["source_files"]
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in frozen.items())


def synthetic_records(config, long_free=0.02, long_pose=3.0):
    records = {}
    for row in inventory(config):
        if row["phase"] != "confirmation":
            continue
        long = row["arm"] == "LONG128"
        values = {
            "free_nmse": long_free if long else 0.02,
            "grounded_nmse": 0.01,
            "return_nmse": 0.01,
            "normal_ratio": 0.15 if long else 0.14,
            "normal_pose_deg": 0.2,
            "tangent_ratio": 1.0,
            "stationary_deg": long_pose if long else 14.0,
        }
        records[row["id"]] = {"evaluation": {"metrics": values}}
    return records


def test_gain_fix_and_noninferiority_are_all_required(config):
    cfg = dict(config, bootstrap_resamples=1000)
    assert len(rules(cfg)) == cfg["family_size"] == 13
    good = summarize(synthetic_records(cfg), cfg)
    assert good["outcome"] == "supported bounded fix"
    harmful = summarize(synthetic_records(cfg, long_free=0.04), cfg)
    assert harmful["outcome"] == "tradeoff"
    persistent = summarize(synthetic_records(cfg, long_pose=7.0), cfg)
    assert persistent["outcome"] == "negative declared joint fix"
    intervals = copy.deepcopy(good["adjusted_NAV32"])
    intervals["absolute/stationary_deg"] = {"lo": 8.0, "hi": 13.0, "width": 5.0}
    assert classify(intervals, cfg)["outcome"] == "inconclusive"
    intervals["absolute/stationary_deg"] = None
    assert classify(intervals, cfg)["outcome"] == "inconclusive"


def test_long_fit_exact_repetition(config):
    a, b = make("NAV32", 22), make("NAV32", 22)
    x, y = [fit(m, mapped_root(9301), config, "LONG128", fixture=True) for m in (a, b)]
    np.testing.assert_array_equal(x["trace"], y["trace"])
    assert state_hash(a) == state_hash(b)
    assert x["exposure"] == y["exposure"]
