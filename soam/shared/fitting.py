"""Frozen E1 fitting mechanics; engineering fixtures use isolated, bounded streams.

Scientific execution belongs to SOAM-051 after a complete feasibility ledger.
There is deliberately no study CLI or automatic configuration selection here.
"""

import copy
import time
from dataclasses import dataclass

import torch

from soam.platform.core import Command, tensor_check
from soam.shared.data import SharedTask, initialization_seed
from soam.shared.models import Candidate, manifest


@dataclass(frozen=True)
class FitPlan:
    fixture: bool = False
    recall_updates: int = 100
    joint_updates: int = 300
    batch_size: int = 16

    def validate(self):
        if type(self.fixture) is not bool:
            raise ValueError("explicit fixture flag required")
        values = (self.recall_updates, self.joint_updates, self.batch_size)
        if any(type(x) is not int or x < 1 for x in values):
            raise ValueError("positive integer fit dimensions required")
        if not self.fixture and values != (100, 300, 16):
            raise ValueError("study schedule is frozen")
        if self.fixture and any(x > limit for x, limit in zip(values, (2, 2, 2))):
            raise ValueError("fixture is limited to two updates per stage and batch two")
        return self


def parameter_check(model):
    for parameter in model.parameters():
        tensor_check(parameter, parameter.shape)


def losses(model, recall, transition=None):
    """Clean observed features score losses; they never enter a free rollout."""
    if recall.role != "recall" or len(recall.actions) != 10:
        raise ValueError("ten-update recall batch required")
    state = model.assimilate(model.initial_state(len(recall.initial.z)), recall.initial)
    outputs = []
    for action in recall.actions:
        state = model.advance(state, Command(action))
        outputs.append(model.readout(state))
    result = {"recall": (torch.stack(outputs) - recall.clean[0]).square().mean()}
    if transition is not None:
        if transition.role != "transition" or len(transition.actions) != 8:
            raise ValueError("eight-update transition batch required")
        initial = model.assimilate(
            model.initial_state(len(transition.initial.z)), transition.initial
        )
        free, grounded = initial, initial
        predicted_free, predicted_grounded = [], []
        for t, action in enumerate(transition.actions):
            free = model.advance(free, Command(action))
            grounded = model.advance(grounded, Command(action))
            predicted_free.append(model.readout(free))
            predicted_grounded.append(model.readout(grounded))
            # Only after scoring prediction t+1 may clean observation t+1 correct.
            grounded = model.assimilate(grounded, transition.later_observation(t + 1))
        result["free"] = (torch.stack(predicted_free) - transition.clean[1:]).square().mean()
        result["grounded"] = (
            (torch.stack(predicted_grounded) - transition.clean[1:]).square().mean()
        )
    for loss in result.values():
        tensor_check(loss, ())
    return result


def bilinear_inputs(features, actions):
    return torch.cat(
        (
            features,
            *(actions[..., j : j + 1] * features for j in range(3)),
            actions,
            torch.ones_like(actions[..., :1]),
        ),
        -1,
    )


class RidgeMoments:
    """Float64 sufficient statistics, including a regularized bias coordinate."""

    def __init__(self, inputs):
        self.xx = torch.zeros(inputs, inputs, dtype=torch.float64)
        self.xy = torch.zeros(inputs, 12, dtype=torch.float64)
        self.count = 0

    def add(self, x, y):
        x, y = x.reshape(-1, x.shape[-1]).double(), y.reshape(-1, 12).double()
        tensor_check(x, (len(y), len(self.xx)), torch.float64)
        tensor_check(y, (len(x), 12), torch.float64)
        self.xx += x.T @ x
        self.xy += x.T @ y
        self.count += len(x)

    def solve(self, penalty):
        if not self.count or penalty not in (0.0001, 0.01):
            raise ValueError("nonempty records and frozen ridge penalty required")
        result = torch.linalg.solve(
            self.xx / self.count + penalty * torch.eye(len(self.xx), dtype=torch.float64),
            self.xy / self.count,
        ).T.float()
        tensor_check(result, (12, len(self.xx)))
        return result


def exposure_counts(plan):
    plan.validate()
    b, r, j = plan.batch_size, plan.recall_updates, plan.joint_updates
    return {
        "distinct_recall_records": (r + j) * b,
        "transition_episodes": j * b,
        "executed_transitions": j * b * 8,
        "distinct_transition_sensor_records": j * b * 9,
        "recall_loss_feature_vectors": (r + j) * b * 10,
        "free_loss_feature_vectors": j * b * 8,
        "grounded_loss_feature_vectors": j * b * 8,
        "transition_records_shared_by_free_and_grounded": True,
    }


def fit(
    family,
    root,
    config_index,
    *,
    plan,
    archive_batch,
    checkpoint,
    budget_check,
    batch_provider=None,
):
    """Bounded fitter with mandatory archive/checkpoint/budget hooks.

    Exceptions propagate without retry or rescue. The owner runner must record
    failure rows for all unexecuted cells and must enforce study/phase budgets.
    """
    started = time.process_time()
    plan.validate()
    protocol = manifest()
    split = "fixture/train" if plan.fixture else "train"
    seed = initialization_seed(split, root, family, config_index)
    model = Candidate(family, seed)
    task = SharedTask()
    batch_provider = task.training_batch if batch_provider is None else batch_provider

    def check():
        budget_check()
        if time.process_time() - started > protocol["fit"]["per_fit_cpu_seconds"]:
            raise TimeoutError("frozen per-fit CPU limit exceeded; no retry")

    ridge = family == "L12"
    optimizer = (
        None
        if ridge
        else torch.optim.Adam(
            model.parameters(),
            lr=protocol["fit"]["gradient_configs"][config_index]["learning_rate"],
            betas=(0.9, 0.999),
            eps=1e-8,
            weight_decay=0,
        )
    )
    if ridge:
        l_moments, b_moments = RidgeMoments(25), RidgeMoments(52)
        penalty = protocol["fit"]["ridge_configs"][config_index]["lambda"]
    trace = []
    # Keep joint packet indices 100..399 even in a shortened fixture.
    stages = (
        ("recall", range(plan.recall_updates)),
        ("joint", range(100, 100 + plan.joint_updates)),
    )
    for stage, updates in stages:
        for update in updates:
            check()
            recall, episodes = batch_provider(
                root, update, "recall", fixture=plan.fixture, batch_size=plan.batch_size
            )
            archive_batch(update, "recall", episodes)
            transition = None
            if stage == "joint":
                transition, episodes = batch_provider(
                    root, update, "transition", fixture=plan.fixture, batch_size=plan.batch_size
                )
                archive_batch(update, "transition", episodes)
            if ridge:
                initial = recall.initial
                x = torch.cat(
                    (initial.z, initial.valid.float(), torch.ones_like(initial.z[:, :1])), 1
                )
                l_moments.add(x, recall.clean[0])
                if transition is not None:
                    b_moments.add(
                        bilinear_inputs(transition.clean[:-1], transition.actions),
                        transition.clean[1:],
                    )
                trace.append(
                    {
                        "update": update,
                        "stage": stage,
                        "L_records": l_moments.count,
                        "B_pairs": b_moments.count,
                    }
                )
            else:
                parameter_check(model)
                optimizer.zero_grad(set_to_none=True)
                terms = losses(model, recall, transition)
                total = terms["recall"] + terms.get("free", 0) + 0.3 * terms.get("grounded", 0)
                tensor_check(total, ())
                total.backward()
                norm = torch.nn.utils.clip_grad_norm_(
                    model.parameters(), 1.0, error_if_nonfinite=True
                )
                optimizer.step()
                parameter_check(model)
                trace.append(
                    {
                        "update": update,
                        "stage": stage,
                        "total": total.item(),
                        "gradient_norm_before_clip": norm.item(),
                        **{name: loss.item() for name, loss in terms.items()},
                    }
                )
            check()
        if ridge:
            with torch.no_grad():
                model.L.copy_(l_moments.solve(penalty))
                if stage == "joint":
                    model.B.copy_(b_moments.solve(penalty))
            parameter_check(model)
        checkpoint(
            "recall" if stage == "recall" else "final",
            copy.deepcopy(model.state_dict()),
            None if optimizer is None else copy.deepcopy(optimizer.state_dict()),
        )
        check()
    return model, {
        "fixture_only": plan.fixture,
        "initialization_seed": seed,
        "initialization_key": [
            "soam-e1-shared",
            1,
            split,
            root,
            0,
            f"fit-initialization/{family}/{config_index}",
        ],
        "trace": trace,
        "exposure": exposure_counts(plan),
        "algorithm": "normalized_ridge" if ridge else "adam",
        "cpu_seconds": time.process_time() - started,
    }
