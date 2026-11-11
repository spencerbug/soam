"""Evaluator-only mechanistic probes; labels never flow into a recurrent core."""

import torch

from soam.encoders.projection import FixedProjection
from soam.gating.data import generate, seed
from soam.gating.engine import ridge, rollout


def corr(x, y):
    x, y = x.double().flatten(), y.double().flatten()
    x, y = x - x.mean(), y - y.mean()
    den = x.norm() * y.norm()
    return 0.0 if den < 1e-12 else float((x @ y) / den)


def r2(pred, true):
    num = (pred.double() - true.double()).square().sum()
    den = (true.double() - true.double().mean(0)).square().sum().clamp_min(1e-12)
    return float(1 - num / den)


def augment(x):
    return torch.cat((x, torch.ones_like(x[:, :1])), 1)


def probes(model, root, episodes, check):
    check()
    train = {}
    test = {}
    for role in ("recall", "transition"):
        for split, target in [("probe_train", train), ("diagnostic", test)]:
            b, world = generate(split, root, 17, role, batch=episodes, horizon=8)
            h = rollout(model, *b.inputs())["hidden"][1:].reshape(-1, model.n)
            target[role] = (h, world[1:].reshape(-1, 2).float())
    g = torch.Generator().manual_seed(seed("probe_train", root, 17, "nonlinear_probe"))
    weights = torch.randn(model.n, 64, generator=g) / model.n**0.5
    bias = torch.randn(64, generator=g)
    results = {}
    states = {}
    for role in ("recall", "transition"):
        x, y = train[role]
        xt, yt = test[role]
        mean, scale = x.mean(0), x.std(0).clamp_min(0.01)
        a = (x - mean) / scale
        at = (xt - mean) / scale
        linear = ridge(augment(a), y, 0.001)
        nonlinear = ridge(augment(torch.cat((a, torch.tanh(a @ weights + bias)), 1)), y, 0.001)
        p = augment(at) @ linear.T
        npred = augment(torch.cat((at, torch.tanh(at @ weights + bias)), 1)) @ nonlinear.T
        other = "transition" if role == "recall" else "recall"
        xo, yo = test[other]
        cross = augment((xo - mean) / scale) @ linear.T
        ev = torch.linalg.eigvalsh(torch.cov(xt.double().T)).clamp_min(0)
        rank = float(ev.sum().square() / ev.square().sum().clamp_min(1e-12))
        pairs = torch.randperm(len(xt), generator=g)
        dist_h = (xt - xt[pairs]).norm(dim=1)
        dist_x = (yt - yt[pairs]).norm(dim=1)
        results.update(
            {
                f"{role}_linear_r2": r2(p, yt),
                f"{role}_nonlinear_r2": r2(npred, yt),
                f"{role}_to_{other}_r2": r2(cross, yo),
                f"{role}_effective_rank": rank,
                f"{role}_distance_correlation": corr(dist_h, dist_x),
            }
        )
        if role == "transition":
            pp = p.reshape(8, episodes, 2)
            yy = yt.reshape(8, episodes, 2)
            results["decoded_motion_alignment"] = corr(pp[1:] - pp[:-1], yy[1:] - yy[:-1])
        states[role] = {"linear": linear, "nonlinear": nonlinear, "mean": mean, "scale": scale}
    results["probe_parameters_per_role"] = int(
        linear.numel() + nonlinear.numel() + weights.numel() + bias.numel() + 2 * model.n
    )
    return results, {"fits": states, "random_weights": weights, "random_bias": bias}


@torch.no_grad()
def diagnose(model, root, variance, manifest, check, gate_mean=None):
    check()
    count = manifest["diagnostic_episodes"]
    horizon = manifest["diagnostic_horizon"]
    summary = {}
    arrays = {}
    projection = FixedProjection(12, 1729).matrix.double()
    for role in ("recall", "transition", "switch"):
        b, world = generate(
            "diagnostic", root, 0, role, batch=count, horizon=horizon if role != "recall" else 10
        )
        path = rollout(model, *b.inputs())
        arrays[role] = {"path": path, "world": world, "actions": b.actions, "roles": b.roles}
        error = (path["output"].double() - b.clean[1:].double()).square().mean((1, 2)) / variance
        summary[f"{role}_nmse"] = error.mean().item()
        summary[f"{role}_endpoint_nmse"] = error[-1].item()
        alpha = path["alpha"]
        delta = path["hidden"][1:] - path["hidden"][:-1]
        summary[f"{role}_alpha_mean"] = alpha.mean().item()
        summary[f"{role}_alpha_between_unit_sd"] = (
            alpha.mean((0, 1)).std().item() if model.n > 1 else 0.0
        )
        summary[f"{role}_reset_mean"] = path["reset"].mean().item()
        summary[f"{role}_gate_change_correlation"] = (
            sum(corr(alpha[..., i], delta[..., i].abs()) for i in range(model.n)) / model.n
        )
        summary[f"{role}_alpha_action_correlation"] = corr(alpha.mean(-1), b.actions.norm(dim=-1))
        arrays[role]["per_unit_update_correlation"] = torch.tensor(
            [corr(alpha[..., i], delta[..., i].abs()) for i in range(model.n)]
        )
        arrays[role]["per_unit_alpha"] = alpha.mean((0, 1))
        if role == "transition":
            decoded = path["output"].double() @ projection
            target = world[1:]
            summary["free128"] = error.mean().item()
            summary["late_output_variance_ratio"] = float(
                path["output"][-32:].double().var((0, 1)).mean()
                / b.clean[-32:].double().var((0, 1)).mean().clamp_min(1e-12)
            )
            radii = target.norm(dim=-1)
            predrad = decoded.norm(dim=-1)
            phase = torch.atan2(decoded[..., 1], decoded[..., 0]) - torch.atan2(
                target[..., 1], target[..., 0]
            )
            wrapped = torch.atan2(phase.sin(), phase.cos()).abs()
            usable = radii > 0.05
            summary["radial_error"] = float((predrad - radii).abs().mean())
            summary["phase_error_radians"] = float(wrapped[usable].mean())
            summary["coordinate_bias_norm"] = float((decoded - target).mean((0, 1)).norm())
            summary["motion_energy_ratio"] = float(
                (decoded[1:] - decoded[:-1]).square().mean()
                / (target[1:] - target[:-1]).square().mean().clamp_min(1e-12)
            )
            summary["hidden_max_abs"] = float(path["hidden"].abs().max())
            arrays[role]["nmse_curve"] = error
            arrays[role]["radial_error_curve"] = (predrad - radii).abs().mean(1)
            arrays[role]["phase_error_curve"] = wrapped.mean(1)
        if role in ("recall", "transition"):
            g = torch.Generator().manual_seed(seed("diagnostic", root, 0, f"{role}/perturb"))
            perturb = torch.randn(count, model.n, generator=g)
            perturb = 0.15 * perturb / perturb.square().mean(1, keepdim=True).sqrt()
            p = rollout(model, *b.inputs(), perturb=perturb)
            ratio = (p["hidden"] - path["hidden"]).square().mean(-1).sqrt() / 0.15
            pe = (p["output"].double() - b.clean[1:].double()).square().mean(-1) / variance
            summary[f"{role}_perturb_gap_ratio"] = float(ratio[-1].mean())
            summary[f"{role}_perturb_output_nmse"] = float(pe[-1].mean())
            summary[f"{role}_perturb_excess_nmse"] = float(pe[-1].mean() - error[-1])
            summary[f"{role}_useful_recovery_fraction"] = float(
                ((ratio[-1] <= 0.5) & (pe[-1] <= 0.03)).float().mean()
            )
            arrays[role]["perturb_gap_ratio"] = ratio
            arrays[role]["perturb_nmse"] = pe
            # Contradictory sensory content; mask unchanged, no role-authority change.
            corrupt = rollout(model, -b.z, b.valid, b.actions, b.roles)
            summary[f"{role}_contradictory_cue_nmse"] = float(
                (corrupt["output"].double() - b.clean[1:].double()).square().mean() / variance
            )
            summary[f"{role}_cue_alpha_change"] = float((corrupt["alpha"] - alpha).abs().mean())
            summary[f"{role}_cue_reset_change"] = float(
                (corrupt["reset"] - path["reset"]).abs().mean()
            )
            arrays[role]["contradictory_alpha"] = corrupt["alpha"]
        check()
    b, _ = generate("diagnostic", root, 0, "transition", batch=count, horizon=8)
    h = model.encode(b.z, b.valid)
    a = b.actions[0]
    q = b.roles[0]
    _, base = model.step(h, a, q, diagnostics=True)
    for label, aa, qq in [
        ("zero_action", torch.zeros_like(a), q),
        ("reverse_action", -a, q),
        ("toggle_role", a, q.flip(-1)),
    ]:
        _, g = model.step(h, aa, qq, diagnostics=True)
        for field in ("alpha", "reset", "candidate"):
            summary[f"{label}_{field}_change"] = float((g[field] - base[field]).abs().mean())
    for label, overrides in [("alpha_half", {"alpha": 0.5}), ("reset_one", {"reset": 1.0})] + (
        [] if gate_mean is None else [("alpha_development_mean", {"alpha": gate_mean})]
    ):
        p = rollout(model, *b.inputs(), overrides=overrides)
        summary[f"intervention_{label}_free8"] = float(
            (p["output"].double() - b.clean[1:].double()).square().mean() / variance
        )
    probe, params = probes(model, root, manifest["probe_episodes"], check)
    summary.update(probe)
    arrays["probes"] = params
    if any(not torch.isfinite(torch.tensor(v)) for v in summary.values()):
        raise FloatingPointError("nonfinite diagnostic")
    return summary, arrays
