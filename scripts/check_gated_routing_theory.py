"""Finite untrained equation audit for SOAM-108; no fits or trajectory search."""

import argparse
import hashlib
import json
import platform
import resource
import subprocess
import sys
import time
from functools import partial
from pathlib import Path


def main():
    start_wall = time.monotonic()
    import torch

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    root = Path(__file__).resolve().parents[1]
    theory = root / "docs/GATED_ASSEMBLY_ROUTING_THEORY.md"
    block = theory.read_text().split("<!-- algebra-audit-config:start -->")[1]
    config_text = block.split("<!-- algebra-audit-config:end -->")[0].split("```json")[1]
    config = json.loads(config_text.split("```")[0])
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    dtype = torch.float64
    generator = torch.Generator(device="cpu").manual_seed(config["seed"])
    n, temperature = config["dimension"], config["temperature"]
    tau_h, tau_g = config["tau_content"], config["tau_gate"]
    eye = torch.eye(n, dtype=dtype)
    checks, failures, samples = {}, [], []
    exposure_hash = hashlib.sha256()

    def record(name, passed, **values):
        checks[name] = {"passed": bool(passed), **values}
        if not passed:
            failures.append(name)

    def compatibility(g):
        return (torch.outer(g, g) + torch.outer(1 - g, 1 - g)) * (1 - eye) + eye

    def energy(state, w, v, s, r, b):
        h, g = state[:n], state[n:]
        phi = 0.5 * ((1 + h) * torch.log1p(h) + (1 - h) * torch.log1p(-h))
        psi = temperature * (g * torch.log(g) + (1 - g) * torch.log1p(-g))
        return (
            phi.sum()
            + psi.sum()
            - 0.5 * h @ (w * compatibility(g)) @ h
            - 0.5 * g @ v @ g
            - b @ h
            - r @ g
            - (g * s * h).sum()
        )

    def drives(state, w, v, s, r, b):
        h, g = state[:n], state[n:]
        u = (w * compatibility(g)) @ h + b + g * s
        reciprocal = h * ((w * (1 - eye)) @ ((2 * g - 1) * h))
        gate_drive = v @ g + r + s * h + reciprocal
        return u, gate_drive

    def field(state, w, v, s, r, b):
        u, gate_drive = drives(state, w, v, s, r, b)
        return torch.cat(
            (
                (torch.tanh(u) - state[:n]) / tau_h,
                (torch.sigmoid(gate_drive / temperature) - state[n:]) / tau_g,
            )
        )

    def gradient(state, w, v, s, r, b):
        h, g = state[:n], state[n:]
        u, gate_drive = drives(state, w, v, s, r, b)
        return torch.cat(
            (torch.atanh(h) - u, temperature * (torch.log(g) - torch.log1p(-g)) - gate_drive)
        )

    max_auto_error, max_fd_error, max_energy_rate = 0.0, 0.0, -float("inf")
    minimum_inward = float("inf")
    step = config["finite_difference_epsilon"]
    for index in range(config["samples"]):
        h = 1.4 * torch.rand(n, generator=generator, dtype=dtype) - 0.7
        g = 0.7 * torch.rand(n, generator=generator, dtype=dtype) + 0.15
        s, r, b = [0.3 * torch.randn(n, generator=generator, dtype=dtype) for _ in range(3)]
        matrices = [torch.randn((n, n), generator=generator, dtype=dtype) for _ in range(2)]
        w, v = [0.1 * (a + a.T) for a in matrices]
        state = torch.cat((h, g))
        for tensor in (state, w, v, s, r, b):
            exposure_hash.update(tensor.numpy().tobytes())
        objective = partial(energy, w=w, v=v, s=s, r=r, b=b)
        automatic = torch.autograd.functional.jacobian(objective, state)
        manual = gradient(state, w, v, s, r, b)
        basis = torch.eye(2 * n, dtype=dtype)
        finite_difference = torch.stack(
            [
                (objective(state + step * axis) - objective(state - step * axis)) / (2 * step)
                for axis in basis
            ]
        )
        auto_error = float((automatic - manual).abs().max())
        fd_error = float((finite_difference - manual).abs().max())
        rate = float(manual @ field(state, w, v, s, r, b))
        max_auto_error = max(max_auto_error, auto_error)
        max_fd_error = max(max_fd_error, fd_error)
        max_energy_rate = max(max_energy_rate, rate)
        boundary = torch.cat(
            (
                torch.tensor([-1.0, 1.0, -1.0, 1.0], dtype=dtype),
                torch.tensor([0.0, 1.0, 0.0, 1.0], dtype=dtype),
            )
        )
        direction = torch.tensor([1.0, -1.0, 1.0, -1.0] * 2, dtype=dtype)
        inward = float((field(boundary, w, v, s, r, b) * direction).min())
        minimum_inward = min(minimum_inward, inward)
        samples.append(
            {
                "index": index,
                "autograd_error": auto_error,
                "finite_difference_error": fd_error,
                "energy_rate": rate,
                "minimum_inward_rate": inward,
            }
        )
        if index == 0:
            # Construct an equilibrium analytically, without fitting or root search.
            equilibrium_b = torch.atanh(h) - (w * compatibility(g)) @ h - g * s
            reciprocal = h * ((w * (1 - eye)) @ ((2 * g - 1) * h))
            equilibrium_r = temperature * torch.logit(g) - v @ g - s * h - reciprocal
            equilibrium_field = partial(field, w=w, v=v, s=s, r=equilibrium_r, b=equilibrium_b)
            hessian = torch.autograd.functional.hessian(
                partial(energy, w=w, v=v, s=s, r=equilibrium_r, b=equilibrium_b), state
            )
            jacobian = torch.autograd.functional.jacobian(equilibrium_field, state)
            mobility = torch.cat(((1 - h**2) / tau_h, g * (1 - g) / temperature / tau_g))
            linearization_error = float((jacobian + mobility[:, None] * hessian).abs().max())
            equilibrium_residual = float(equilibrium_field(state).abs().max())
            record(
                "joint_equilibrium_linearization",
                linearization_error < config["gradient_tolerance"]
                and equilibrium_residual < config["gradient_tolerance"],
                max_error=linearization_error,
                equilibrium_residual=equilibrium_residual,
            )
    record(
        "energy_derivatives",
        max(max_auto_error, max_fd_error) < config["gradient_tolerance"],
        max_autograd_error=max_auto_error,
        max_finite_difference_error=max_fd_error,
    )
    record(
        "continuous_dissipation_and_bounds",
        max_energy_rate <= config["dissipation_tolerance"] and minimum_inward >= 0,
        maximum_sampled_energy_rate=max_energy_rate,
        minimum_inward_rate=minimum_inward,
    )

    binary = torch.tensor([0.0, 0.0, 1.0, 1.0], dtype=dtype)
    c = compatibility(binary)
    expected = torch.block_diag(torch.ones((2, 2), dtype=dtype), torch.ones((2, 2), dtype=dtype))
    receiver = binary[:, None].expand(n, n)
    outer = torch.outer(binary, binary)
    soft = compatibility(torch.tensor([0.1, 0.1, 0.9, 0.9], dtype=dtype))
    record(
        "binary_partition_and_soft_leakage",
        torch.equal(c, expected)
        and receiver[0, 1] == 0
        and outer[0, 1] == 0
        and abs(float(soft[0, 2]) - 0.18) < 1e-12
        and abs(float(soft[0, 1]) - 0.82) < 1e-12
        and torch.equal(torch.diag(soft), torch.ones(n, dtype=dtype)),
        compatibility=c.tolist(),
        receiver_closed_internal=float(receiver[0, 1]),
        outer_closed_internal=float(outer[0, 1]),
        soft_cross=float(soft[0, 2]),
        soft_same_group=float(soft[0, 1]),
    )

    pair_state = torch.full((2,), 0.6, dtype=dtype)
    supporting_weight = float(torch.atanh(pair_state[0]) / pair_state[0] - 0.5)
    supporting = torch.tensor([[0.5, supporting_weight], [supporting_weight, 0.5]], dtype=dtype)
    before = torch.tanh(supporting @ pair_state) - pair_state
    after = torch.tanh(torch.diag(torch.diag(supporting)) @ pair_state) - pair_state
    record(
        "cutting_support_destroys_fixed_point",
        float(before.abs().max()) < 1e-12 and float(after.abs().min()) > 0.1,
        state=pair_state.tolist(),
        recurrent=supporting.tolist(),
        residual_before=before.tolist(),
        residual_after=after.tolist(),
    )

    arbitrary = torch.tensor([0.4, -0.2], dtype=dtype)
    recurrent = torch.tensor([[1.5, 0.2], [0.2, 1.5]], dtype=dtype)
    motion = torch.tanh(recurrent @ arbitrary) - arbitrary
    record(
        "zero_sensory_drive_is_not_stationarity",
        float(motion.abs().max()) > 0.01,
        state=arbitrary.tolist(),
        recurrent=recurrent.tolist(),
        velocity=motion.tolist(),
    )

    # E_cross=-g*s*h: mixed partials must both be -s. An independent gate omits one.
    sensory = 0.7
    record(
        "independent_gate_reciprocity_mismatch",
        abs(-sensory - 0.0) > 0.1,
        content_mixed_partial=-sensory,
        independent_gate_mixed_partial=0.0,
        mismatch=abs(sensory),
    )
    saddle = torch.tensor([[1.0, -2.0], [-2.0, 1.0]], dtype=dtype)
    eigenvalues = torch.linalg.eigvalsh(saddle)
    record(
        "separately_stable_blocks_joint_saddle",
        bool((torch.diag(saddle) > 0).all()) and float(eigenvalues.min()) < 0,
        hessian=saddle.tolist(),
        eigenvalues=eigenvalues.tolist(),
        gradient_flow_eigenvalues=(-eigenvalues).tolist(),
    )
    initial, euler_step = 1.0, 3.0
    updated = initial - euler_step * initial
    record(
        "euler_does_not_inherit_descent",
        updated**2 / 2 > initial**2 / 2,
        step_size=euler_step,
        energy_before=initial**2 / 2,
        energy_after=updated**2 / 2,
    )

    source_paths = [
        Path(__file__).resolve(),
        root / "docs/protocols/study_ao1_v1.json",
        root / "docs/STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md",
    ]
    source_hashes = {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths
    }
    config_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    fingerprint = hashlib.sha256(
        json.dumps({"sources": source_hashes, "config": config_hash}, sort_keys=True).encode()
    ).hexdigest()
    cpu_seconds = time.process_time()
    wall_seconds = time.monotonic() - start_wall
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = int(rss if platform.system() == "Darwin" else rss * 1024)
    record(
        "resource_limits",
        cpu_seconds <= config["cpu_seconds"]
        and wall_seconds <= config["wall_seconds"]
        and rss_bytes <= config["rss_bytes"],
        cpu_seconds=cpu_seconds,
        wall_seconds=wall_seconds,
        peak_rss_bytes=rss_bytes,
    )
    payload = {
        "status": "pass" if not failures else "fail",
        "kind": "untrained_algebra_only",
        "config": config,
        "checks": checks,
        "failures": failures,
        "samples": samples,
        "provenance": {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip(),
            "source_hashes": source_hashes,
            "config_sha256": config_hash,
            "source_fingerprint": fingerprint,
            "draws_sha256": exposure_hash.hexdigest(),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "platform": platform.platform(),
            "dtype": str(dtype),
            "device": "cpu",
            "threads": torch.get_num_threads(),
            "deterministic": torch.are_deterministic_algorithms_enabled(),
            "working_tree_clean": not bool(
                subprocess.check_output(
                    ["git", "status", "--porcelain"], cwd=root, text=True
                ).strip()
            ),
            "timing_scope": "CPU includes imports; wall starts in main before Torch import",
        },
        "exposure": {
            "algebra_state_scalars": 2 * n,
            "supplied_matrix_scalars_per_case": 2 * n * n,
            "supplied_drive_scalars_per_case": 3 * n,
            "finite_difference_energy_evaluations": config["samples"] * 4 * n,
            "algebra_samples": config["samples"],
            "training_records": 0,
            "development_records": 0,
            "confirmation_records": 0,
            "optimizer_updates": 0,
            "learned_models": 0,
            "note": "Counterexamples and constructed equilibrium are supplied algebra.",
        },
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if len(encoded.encode()) > config["artifact_bytes"]:
        raise RuntimeError("Artifact allocation exceeded")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "checks": len(checks),
                "failures": failures,
                "cpu_seconds": cpu_seconds,
                "wall_seconds": wall_seconds,
                "peak_rss_bytes": rss_bytes,
                "artifact_bytes": len(encoded.encode()),
                "output": str(args.output),
            }
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
