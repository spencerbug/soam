"""Training from observed records; isolated no-write rollout and metric reduction."""

import math
import time

import torch

from soam.gating.models import bilinear


def rollout(model, z, valid, actions, roles, *, observed=None, overrides=None, perturb=None):
    """observed=None is free prediction. No targets/world/projection are accepted."""
    h = model.assimilate(None, z, valid)
    if perturb is not None:
        h = h + perturb
    hidden, outputs, gates = [h], [], {k: [] for k in ("alpha", "retention", "reset", "candidate")}
    for t, a in enumerate(actions):
        h, g = model.step(h, a, roles[t], overrides=overrides, diagnostics=True)
        outputs.append(model.readout(h))
        hidden.append(h)
        for key, values in gates.items():
            values.append(g[key])
        if observed is not None:
            h = model.assimilate(h, observed[t + 1], torch.ones_like(valid))
    return {
        "output": torch.stack(outputs),
        "hidden": torch.stack(hidden),
        **{k: torch.stack(v) for k, v in gates.items()},
    }


def objective(model, recall, transition=None):
    def predict(b, grounded=False):
        h = model.assimilate(None, b.z, b.valid)
        out = []
        for t, a in enumerate(b.actions):
            h = model.step(h, a, b.roles[t])
            out.append(model.readout(h))
            if grounded:
                h = model.assimilate(h, b.clean[t + 1], torch.ones_like(b.valid))
        return torch.stack(out)

    terms = {"recall": (predict(recall) - recall.clean[0]).square().mean()}
    if transition is not None:
        terms["free"] = (predict(transition) - transition.clean[1:]).square().mean()
        terms["grounded"] = (predict(transition, True) - transition.clean[1:]).square().mean()
    return terms


def metrics_from_paths(recall, free, grounded, recall_batch, transition_batch, variance):
    r = (recall["output"][-1].double() - recall_batch.clean[-1].double()).square().mean() / variance
    f = (free["output"].double() - transition_batch.clean[1:].double()).square().mean(
        (1, 2)
    ) / variance
    g = (grounded["output"].double() - transition_batch.clean[1:].double()).square().mean(
        (1, 2)
    ) / variance
    return {
        "recall": r.item(),
        "free8": f[:8].mean().item(),
        "free32": f[:32].mean().item(),
        "grounded32": g[:32].mean().item(),
        "J": 0.5 * (r + f[:8].mean()).item(),
        "free_curve": f.tolist(),
        "grounded_curve": g.tolist(),
    }


@torch.no_grad()
def evaluate(model, recall, transition, variance, *, overrides=None):
    before = {k: v.clone() for k, v in model.state_dict().items()}
    r = rollout(model, *recall.inputs(), overrides=overrides)
    f = rollout(model, *transition.inputs(), overrides=overrides)
    g = rollout(model, *transition.inputs(), observed=transition.clean, overrides=overrides)
    for key, value in model.state_dict().items():
        if not torch.equal(value, before[key]):
            raise AssertionError("inference changed persistent state")
    for path in (r, f, g):
        if any(not v.isfinite().all() for v in path.values()):
            raise FloatingPointError("nonfinite inference")
    return metrics_from_paths(r, f, g, recall, transition, variance), {
        "recall": r,
        "free": f,
        "grounded": g,
    }


def ridge(x, y, penalty):
    x, y = x.double(), y.double()
    return torch.linalg.solve(
        x.T @ x / len(x) + penalty * torch.eye(x.shape[-1], dtype=torch.float64), x.T @ y / len(x)
    ).T.float()


def fit_ridge(model, data, penalty, upto=None):
    records = data["recall"] if upto is None else data["recall"][:upto]
    r = len(data["recall"]) - len(data["transition"])
    transitions = data["transition"] if upto is None else data["transition"][: max(0, upto - r)]
    clean = torch.cat([b.clean[0] for b in records])
    x = torch.cat(
        [torch.cat((b.z, b.valid.float(), torch.ones_like(b.z[:, :1])), 1) for b in records]
    )
    with torch.no_grad():
        if model.n == 2:
            mean = clean.double().mean(0)
            _, _, v = torch.linalg.svd(clean.double() - mean, full_matrices=False)
            # Pin sign for deterministic component orientation.
            p = v[:2].T
            for j in range(2):
                if p[p[:, j].abs().argmax(), j] < 0:
                    p[:, j] *= -1
            model.P.copy_(p.float())
            model.mean.copy_(mean.float())
            targets = (clean - model.mean) @ model.P
        else:
            targets = clean
        model.L.copy_(ridge(x, targets, penalty))
        if transitions:
            z = torch.cat([b.clean[:-1].reshape(-1, 12) for b in transitions])
            y = torch.cat([b.clean[1:].reshape(-1, 12) for b in transitions])
            a = torch.cat([b.actions.reshape(-1, 3) for b in transitions])
            if model.n == 2:
                z, y = (z - model.mean) @ model.P, (y - model.mean) @ model.P
            model.B.copy_(ridge(bilinear(z, a), y, penalty))


def fit(
    model, data, config, check, *, development=None, variance=None, checkpoints=(100, 400, 600, 800)
):
    start = time.process_time()
    trace = []
    learning = {}
    nrecall = len(data["recall"]) - len(data["transition"])
    is_ridge = model.kind in ("ridge", "pca_ridge")
    optimizer = None if is_ridge else torch.optim.Adam(model.parameters(), lr=config["lr"])
    setup_cpu = time.process_time() - start
    if is_ridge:
        stages = checkpoints if development else (len(data["recall"]),)
        for count in stages:
            if count > len(data["recall"]):
                continue
            check()
            fit_ridge(model, data, config["ridge"], upto=count)
            if development:
                learning[str(count)] = evaluate(model, *development, variance)[0]
        trace = [
            {
                "algorithm": "ridge",
                "records": len(data["recall"]) * len(data["recall"][0].z),
                "penalty": config["ridge"],
            }
        ]
    else:
        for i, recall in enumerate(data["recall"]):
            check()
            if "decay_start" in config and i >= config["decay_start"]:
                progress = (i - config["decay_start"]) / max(
                    1, config["decay_end"] - config["decay_start"] - 1
                )
                ratio = config["final_lr_ratio"] + (1 - config["final_lr_ratio"]) * 0.5 * (
                    1 + math.cos(math.pi * min(progress, 1.0))
                )
                for group in optimizer.param_groups:
                    group["lr"] = config["lr"] * ratio
            optimizer.zero_grad(set_to_none=True)
            transition = None if i < nrecall else data["transition"][i - nrecall]
            terms = objective(model, recall, transition)
            loss = terms["recall"] + terms.get("free", 0) + 0.3 * terms.get("grounded", 0)
            if not loss.isfinite():
                raise FloatingPointError("nonfinite loss")
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
            optimizer.step()
            trace.append(
                {
                    "update": i + 1,
                    "total": loss.item(),
                    "gradient_norm": grad.item(),
                    "learning_rate": optimizer.param_groups[0]["lr"],
                    **{k: v.item() for k, v in terms.items()},
                }
            )
            if development and i + 1 in checkpoints:
                learning[str(i + 1)] = evaluate(model, *development, variance)[0]
        if any(not p.isfinite().all() for p in model.parameters()):
            raise FloatingPointError("nonfinite parameter")
    check()
    return {
        "trace": trace,
        "learning": learning,
        "cpu_seconds": time.process_time() - start,
        "setup_cpu_seconds": setup_cpu,
        "optimizer_state": None if optimizer is None else optimizer.state_dict(),
        "exposure": {
            "recall_episodes": len(data["recall"]) * len(data["recall"][0].z),
            "transition_episodes": len(data["transition"]) * len(data["transition"][0].z),
            "distinct_transition_records": len(data["transition"])
            * len(data["transition"][0].z)
            * 9,
            "gradient_updates": 0 if is_ridge else len(data["recall"]),
            "replays": 0,
            "ridge_full_refits_for_development": len(learning) if is_ridge else 0,
        },
    }
