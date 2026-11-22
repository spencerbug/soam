"""Finite, untrained AO-1 algebra audit; never fits or evaluates a learned model."""

import argparse
import hashlib
import json
import platform
import resource
import time
from pathlib import Path

import numpy as np


def capped(matrix, cap):
    return matrix * min(1.0, cap / max(float(np.abs(matrix).sum(1).max()), 1e-30))


def advance(h, recurrent, action_matrices, action, bias):
    matrix = recurrent + np.einsum("k,kij->ij", action, action_matrices)
    return 0.5 * h + 0.5 * np.tanh(matrix @ h + bias)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    start_cpu, start_wall = time.process_time(), time.monotonic()
    root = Path(__file__).resolve().parents[1]
    path = root / "docs/protocols/study_ao1_v1.json"
    manifest = json.loads(path.read_text())
    settings = manifest["design_audit"]
    rng = np.random.Generator(np.random.PCG64(settings["seed"]))
    results = {}

    q, r = np.linalg.qr(rng.normal(size=(96, 24)), mode="reduced")
    q *= np.where(np.diag(r) >= 0, 1.0, -1.0)
    x = rng.normal(size=24)
    orth_error = float(np.abs(q.T @ q - np.eye(24)).max())
    norm_error = float(abs(np.linalg.norm(q @ x) - np.linalg.norm(x)))
    assert orth_error < settings["projection_tolerance"]
    assert norm_error < settings["projection_tolerance"]
    assert np.linalg.matrix_rank(q) == 24 and (np.linalg.norm(q, axis=1) > 0).all()
    results["dense_projection"] = {
        "rank": 24,
        "orthonormality_max_error": orth_error,
        "norm_error": norm_error,
        "minimum_row_norm": float(np.linalg.norm(q, axis=1).min()),
    }

    n = 8
    recurrent = capped(rng.normal(size=(n, n)), 2.0)
    actions = np.stack([capped(rng.normal(size=(n, n)), 1.0) for _ in range(2)])
    h = rng.uniform(-0.8, 0.8, n)
    action = rng.uniform(-1, 1, 2)
    bias = rng.uniform(-0.2, 0.2, n)
    matrix = recurrent + np.einsum("k,kij->ij", action, actions)
    gain = 1 - np.tanh(matrix @ h + bias) ** 2
    analytic = 0.5 * np.eye(n) + 0.5 * gain[:, None] * matrix
    eps = settings["finite_difference_epsilon"]
    numeric = np.column_stack(
        [
            (
                advance(h + eps * np.eye(n)[i], recurrent, actions, action, bias)
                - advance(h - eps * np.eye(n)[i], recurrent, actions, action, bias)
            )
            / (2 * eps)
            for i in range(n)
        ]
    )
    jac_error = float(np.abs(analytic - numeric).max())
    assert jac_error < settings["jacobian_tolerance"]
    results["jacobian_max_error"] = jac_error

    largest = 0.0
    for _ in range(settings["bound_samples"]):
        state = rng.uniform(-1, 1, n)
        pred = advance(state, recurrent, actions, rng.uniform(-1, 1, 2), bias)
        # Arbitrary finite sensory projection: tanh bounds every component.
        corrected = 0.5 * pred + 0.5 * np.tanh(rng.normal(size=n))
        largest = max(largest, float(np.abs(pred).max()), float(np.abs(corrected).max()))
    assert largest <= 1 + 1e-12
    results["sampled_bound_max_abs"] = largest

    fixed = 0.7
    for _ in range(settings["scalar_iterations"]):
        fixed = 0.5 * fixed + 0.5 * np.tanh(1.5 * fixed)
    residual = float(abs(fixed - np.tanh(1.5 * fixed)))
    derivative = float(0.5 + 0.75 * (1 - np.tanh(1.5 * fixed) ** 2))
    assert fixed > 0.5 and residual < 1e-12 and derivative < 1
    results["stable_without_routing_counterexample"] = {
        "fixed_point": float(fixed),
        "residual": residual,
        "local_multiplier": derivative,
        "off_diagonal_connections": 0,
    }

    directed = np.array([[0.0, 2.0], [-2.0, 0.0]])
    initial = np.array([0.01, 0.0])
    updated = 0.5 * initial + 0.5 * np.tanh(directed @ initial)

    def energy(v):
        return float(np.sum(v * np.arctanh(v) + 0.5 * np.log1p(-(v**2))))

    energy_change = energy(updated) - energy(initial)
    multiplier = float(np.abs(np.linalg.eigvals(0.5 * np.eye(2) + 0.5 * directed)).max())
    assert energy_change > 0 and multiplier > 1
    results["directed_energy_counterexample"] = {
        "energy_before": energy(initial),
        "energy_after": energy(updated),
        "energy_increase": energy_change,
        "origin_multiplier_magnitude": multiplier,
    }

    chain = np.zeros((3, 3))
    chain[1, 0] = chain[2, 1] = 0.8

    def route_difference(w):
        full = np.tanh(np.full(3, 0.1))
        cut = full.copy()
        reference = np.zeros(3)
        assert np.array_equal(full, cut)
        for _ in range(2):
            u = w @ cut
            u[1] += w[1, 0] * (reference[0] - cut[0])
            full = 0.5 * full + 0.5 * np.tanh(w @ full)
            cut = 0.5 * cut + 0.5 * np.tanh(u)
            reference = 0.5 * reference + 0.5 * np.tanh(w @ reference)
        return float(full[2] - cut[2])

    mediated = route_difference(chain)
    common_input_only = route_difference(np.zeros((3, 3)))
    assert mediated > 0 and common_input_only == 0
    results["dense_input_route_fixture"] = {
        "downstream_difference_after_two_steps": mediated,
        "common_input_only_difference": common_input_only,
    }

    inventory = manifest["inventory"]
    families = len(manifest["models"])
    assert families == inventory["fitted_families"] == 7
    assert families * 4 * 3 == inventory["development_fits"] == 84
    assert families * 20 == inventory["confirmation_fits"] == 140
    assert 84 + 140 + 7 == inventory["scientific_fits"] == 231
    assert len(manifest["primary_criteria"]) == 16
    assert len({c["name"] for c in manifest["primary_criteria"]}) == 16
    dev, confirm = map(
        set, (manifest["streams"]["development_roots"], manifest["streams"]["confirmation_roots"])
    )
    assert len(dev) == 3 and len(confirm) == 20 and not dev & confirm
    assert manifest["streams"]["repeat_root"] in confirm
    assert 3 * 96**2 + 96 + 12 * 96 + 12 == 28908
    assert 3 * 3 * 56**2 + 168 + 12 * 168 + 12 == 30420
    assert 3 * 96 * (96 + 2) + 6 * 96 + 12 * 96 + 12 == 29964
    assert 3 * 96 * 97 // 2 + 96 + 12 * 96 + 12 == 15228
    assert (1 + 12 + 12 * 13 // 2) * 9 == 819
    assert 819 * 12 + 2 * 90 == 10008
    assert 800 * 16 * 33 == manifest["training"]["original_clean_snapshot_records_per_fit"]
    assert 800 * 4 * 32 == manifest["training"]["extra_stationary_target_replays_per_fit"]
    tuples = {(a, b, c) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)}
    held = set(map(tuple, manifest["task"]["heldout_attribute_tuples"]))
    assert len(held) == 2 and held < tuples and len(tuples - held) == 6
    theta, psi = 0.37, -0.92
    v = np.array(
        [
            np.cos(theta),
            np.sin(theta),
            np.cos(psi),
            np.sin(psi),
            1,
            -1,
            -1,
            -np.cos(theta),
            -np.sin(theta),
        ]
    )
    assert abs(v @ v - 6) < 1e-12
    results["manifest_inventory_and_formulas"] = "pass"

    cpu, wall = time.process_time() - start_cpu, time.monotonic() - start_wall
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if platform.system() == "Darwin" else peak * 1024
    assert cpu <= 60 and wall <= 120 and peak_bytes <= 1024**3
    numeric_contract = {k: v for k, v in manifest.items() if k != "status"}
    report = {
        "scope": "untrained algebra only; no learned-model result",
        "seed": settings["seed"],
        "source_baseline": "c121d69",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "manifest_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "contract_sha256_excluding_status": hashlib.sha256(
            json.dumps(numeric_contract, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "cpu_seconds": cpu,
        "wall_seconds": wall,
        "peak_rss_bytes": peak_bytes,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
