"""Isolated key/ring probes and restoring-term controls; fixture namespace by default."""

import itertools
import math

import torch

from soam.handover.models import HandoverModel
from soam.handover.protocol import load_protocol, rng


@torch.no_grad()
def run_probes(seed=11, split="fixture", cases_per_group=1, selector=None):
    m = load_protocol()
    if split not in m["rng"]["split_ids"]:
        raise ValueError("unknown split")
    if not 1 <= cases_per_group <= m["probes"]["cases_per_group"]:
        raise ValueError("probe count outside manifest")
    if split == "fixture" and (seed != 11 or cases_per_group != 1):
        raise ValueError("fixture probes use one case per group, seed 11")
    analytic = HandoverModel("A2", seed)
    selector = HandoverModel("G2", seed) if selector is None else selector
    if selector.analytic:
        raise ValueError("GRU selector required")
    fingerprints = (analytic.persistent_fingerprint(), selector.persistent_fingerprint())
    rows, trajectories = [], {}
    for target in range(3):
        for corruption in range(2):
            for case in range(cases_per_group):
                condition = 100 + 2 * target + corruption
                generator = rng(seed, split, condition, case, "cue_masks")
                cue = analytic.patterns[:, target].clone()
                coordinates = generator.choice(16, 8 if corruption == 0 else 2, replace=False)
                cue[coordinates] *= 0 if corruption == 0 else -1
                for variant in ("A2", "key_passive_leak", "G2"):
                    identity = f"key-{target}-{corruption}-{case}-{variant}"
                    states, energies = [], []
                    if variant == "G2":
                        key = selector.selector(
                            torch.cat((cue, torch.zeros(16), torch.ones(1))), torch.zeros(16)
                        )
                        states.append(key.clone())
                        for _ in range(m["probes"]["key_steps"]):
                            key = selector.selector(torch.zeros(33), key)
                            states.append(key.clone())
                        weights = torch.softmax(selector.selector_readout(key), 0)
                    else:
                        key = cue.clone()
                        states.append(key.clone())
                        energies.append(float(analytic.key_energy(key)))
                        for _ in range(m["probes"]["key_steps"]):
                            key = analytic.key_substep(
                                key, coupled=False, restoring=variant != "key_passive_leak"
                            )
                            states.append(key.clone())
                            energies.append(float(analytic.key_energy(key)))
                        weights = torch.softmax(
                            m["attractor"]["beta"] * (analytic.patterns.T @ key), 0
                        )
                    trajectory = torch.stack(states)
                    if not torch.isfinite(trajectory).all() or trajectory.norm(dim=-1).max() > 10:
                        raise FloatingPointError("invalid key probe")
                    trajectories[identity] = trajectory
                    rows.append(
                        {
                            "id": identity,
                            "kind": "key",
                            "variant": variant,
                            "target": target,
                            "corruption": corruption,
                            "case": case,
                            "condition_rng_id": condition,
                            "final_weights": weights.tolist(),
                            "work": {
                                "key_substeps": 80 if variant != "G2" else 0,
                                "selector_calls": 81 if variant == "G2" else 0,
                                "readout_calls": int(variant == "G2"),
                                "linear_macs": 81 * 3 * 16 * (33 + 16) + 48
                                if variant == "G2"
                                else (80 * 96 + 48 if variant == "A2" else 48),
                                "diagnostic_energy_projections": len(energies),
                            },
                            "last_update_norm": float((states[-1] - states[-2]).norm()),
                            "endpoint_distance_to_template": float(
                                (key - analytic.patterns[:, target]).norm()
                            )
                            if variant != "G2"
                            else None,
                            "energy_max_increase": max(
                                b - a for a, b in itertools.pairwise(energies)
                            )
                            if energies
                            else None,
                        }
                    )
                    if energies:
                        trajectories[identity + "-energy"] = torch.tensor(
                            energies, dtype=torch.float64
                        )
    for perturbation in range(3):
        for action_mode, action in enumerate(m["probes"]["ring_actions"]):
            for case in range(cases_per_group):
                condition = 200 + 2 * perturbation + action_mode
                generator = rng(seed, split, condition, case, "perturbations")
                phase = float(generator.uniform(-math.pi, math.pi))
                if perturbation == 2:
                    phase += 0.3
                planar = torch.tensor([math.cos(phase), math.sin(phase)])
                initial = analytic.encoder(planar)
                if perturbation == 0:
                    initial *= 0.5
                elif perturbation == 1:
                    noise = torch.tensor(generator.normal(size=12), dtype=torch.float32)
                    orthogonal = noise - analytic.plane @ noise
                    initial = 1.5 * initial + 0.2 * orthogonal / orthogonal.norm()
                for variant, radial in (("A2", None), ("ring_lambda_zero", 0.0)):
                    identity = f"ring-{perturbation}-{action_mode}-{case}-{variant}"
                    pose, states = initial.clone(), [initial.clone()]
                    for _ in range(m["probes"]["ring_frames"]):
                        pose = analytic.ring(pose, action, analytic.gains[0], radial=radial)
                        states.append(pose.clone())
                    trajectory = torch.stack(states)
                    if not torch.isfinite(trajectory).all() or trajectory.norm(dim=-1).max() > 10:
                        raise FloatingPointError("invalid ring probe")
                    projected = analytic.plane @ pose
                    # Diagnostic use only; the model's ring propagator never calls this inverse.
                    decoded = analytic.encoder.diagnostic_inverse(pose)
                    angle = float(torch.atan2(decoded[1], decoded[0]))
                    expected = phase + action * m["probes"]["ring_frames"]
                    trajectories[identity] = trajectory
                    rows.append(
                        {
                            "id": identity,
                            "kind": "ring",
                            "variant": variant,
                            "perturbation": perturbation,
                            "action": action,
                            "case": case,
                            "condition_rng_id": condition,
                            "radial_error": abs(float(projected.norm()) - 1),
                            "work": {
                                "ring_propagations": m["probes"]["ring_frames"],
                                "linear_macs": 288 * m["probes"]["ring_frames"],
                            },
                            "orthogonal_error": float((pose - projected).norm()),
                            "phase_error_from_own_trajectory": abs(
                                (angle - expected + math.pi) % (2 * math.pi) - math.pi
                            ),
                        }
                    )
    if fingerprints != (analytic.persistent_fingerprint(), selector.persistent_fingerprint()):
        raise RuntimeError("probe changed persistent weights")
    return rows, trajectories
