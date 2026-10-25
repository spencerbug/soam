"""Grounded local-writing contract. H2 acquisition remains to be benchmarked."""

from .memory import (
    GroundedEvidence,
    LocalMemory,
    PredictionSnapshot,
    UpdateProposal,
    encoder_identity,
)
from .rules import CorrectionRule, DampedJacobianDelta, LocalSignals, WriteConfig

__all__ = [
    "CorrectionRule",
    "DampedJacobianDelta",
    "GroundedEvidence",
    "LocalMemory",
    "LocalSignals",
    "PredictionSnapshot",
    "UpdateProposal",
    "WriteConfig",
    "encoder_identity",
]
