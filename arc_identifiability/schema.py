from __future__ import annotations

from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, model_validator


class IdentifiabilityStatus(str, Enum):
    IDENTIFIED = "identified"
    NON_IDENTIFIABLE = "non_identifiable"
    UNDERDETERMINED = "underdetermined"


class DecisionStatus(str, Enum):
    SUPPORTED = "supported"
    FALSIFIED = "falsified"
    INCONCLUSIVE = "inconclusive"


class EvidenceRef(BaseModel):
    path: str
    sha256: Optional[str] = None
    role: str
    source_kind: Literal["local_artifact", "doi", "url", "formal_receipt"]


class Countermodel(BaseModel):
    id: str
    observable_expression: str
    target_expression: str
    witness_a: Dict[str, float]
    witness_b: Dict[str, float]
    atol: float = 1e-9
    observable_atol: Optional[float] = None
    observable_rtol: Optional[float] = None
    target_atol: Optional[float] = None
    target_rtol: Optional[float] = None
    explanation: str

    @model_validator(mode="after")
    def validate_witness_shape(self) -> "Countermodel":
        if self.atol <= 0:
            raise ValueError("countermodel tolerance must be positive")
        for name in ("observable_atol", "observable_rtol", "target_atol", "target_rtol"):
            value = getattr(self, name)
            if value is not None and value < 0:
                raise ValueError(f"{name} must be non-negative")
        observable_atol = self.observable_atol if self.observable_atol is not None else self.atol
        observable_rtol = self.observable_rtol if self.observable_rtol is not None else self.atol
        target_atol = self.target_atol if self.target_atol is not None else self.atol
        target_rtol = self.target_rtol if self.target_rtol is not None else self.atol
        if observable_atol == 0 and observable_rtol == 0:
            raise ValueError("observable equivalence needs a positive absolute or relative tolerance")
        if target_atol == 0 and target_rtol == 0:
            raise ValueError("target difference needs a positive absolute or relative tolerance")
        if set(self.witness_a) != set(self.witness_b):
            raise ValueError("countermodel witnesses must assign the same variables")
        return self


class FormalReceipt(BaseModel):
    theorem: str
    status: Literal["kernel_checked", "declared_only", "not_applicable"]
    audit_path: Optional[str] = None


class EmpiricalDecision(BaseModel):
    rule: str
    trigger_met: Optional[bool] = None
    evidence_summary: str


class AlternativePrediction(BaseModel):
    mechanism_id: str
    expected_outcome: str
    rationale: str


class ClosureExperiment(BaseModel):
    id: str
    measured_variable: str
    intervention_or_condition: str
    predictions: List[AlternativePrediction]
    decision_rule: str
    feasibility: Literal["high", "medium", "low", "unknown"]
    cost_tier: Literal["low", "medium", "high", "unknown"]
    safety_or_ethics: str
    expected_equivalence_class_reduction: Optional[float] = None

    @model_validator(mode="after")
    def validate_discrimination(self) -> "ClosureExperiment":
        if len(self.predictions) < 2:
            raise ValueError("a closure experiment needs predictions for at least two alternatives")
        mechanisms = [prediction.mechanism_id for prediction in self.predictions]
        if len(mechanisms) != len(set(mechanisms)):
            raise ValueError("closure predictions must use unique mechanism IDs")
        outcomes = {prediction.expected_outcome.strip().lower() for prediction in self.predictions}
        if len(outcomes) < 2:
            raise ValueError("a closure experiment must predict at least two distinct outcomes")
        reduction = self.expected_equivalence_class_reduction
        if reduction is not None and not 0 <= reduction <= 1:
            raise ValueError("expected equivalence-class reduction must be between zero and one")
        return self


class ExpectedOutcome(BaseModel):
    identifiability: IdentifiabilityStatus
    decision: DecisionStatus
    promotion_ceiling: str


class ClaimCase(BaseModel):
    claim_id: str
    title: str
    domain: str
    claim_type: Literal[
        "formal_identity",
        "descriptive",
        "predictive",
        "causal",
        "mechanistic",
        "universal",
    ]
    claim_text: str
    query_scope: str
    assumptions: List[str] = Field(default_factory=list)
    observed_variables: List[str] = Field(default_factory=list)
    target_variables: List[str] = Field(default_factory=list)
    required_measurements: List[str] = Field(default_factory=list)
    competing_mechanisms: List[str] = Field(default_factory=list)
    evidence: List[EvidenceRef]
    countermodels: List[Countermodel] = Field(default_factory=list)
    formal_receipt: Optional[FormalReceipt] = None
    empirical_decision: Optional[EmpiricalDecision] = None
    closure_measurements: List[str] = Field(default_factory=list)
    closure_experiments: List[ClosureExperiment] = Field(default_factory=list)
    expected: ExpectedOutcome

    @model_validator(mode="after")
    def validate_scientific_content(self) -> "ClaimCase":
        if not self.evidence:
            raise ValueError("every claim needs at least one evidence reference")
        if self.expected.identifiability != IdentifiabilityStatus.IDENTIFIED:
            if not self.closure_measurements and not self.closure_experiments:
                raise ValueError("unclosed claims must specify closure measurements")
        if self.expected.identifiability == IdentifiabilityStatus.NON_IDENTIFIABLE:
            if not self.countermodels:
                raise ValueError("non-identifiable claims need an executable countermodel")
        return self


class ClaimDecision(BaseModel):
    claim_id: str
    identifiability: IdentifiabilityStatus
    decision: DecisionStatus
    promotion_ceiling: str
    evidence_integrity: Literal["verified", "missing", "hash_mismatch", "external_only"]
    verified_countermodels: List[str] = Field(default_factory=list)
    failed_countermodels: List[str] = Field(default_factory=list)
    missing_measurements: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
