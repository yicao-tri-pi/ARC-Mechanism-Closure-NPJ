from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, List

from .countermodels import verify_countermodel
from .schema import (
    ClaimCase,
    ClaimDecision,
    DecisionStatus,
    IdentifiabilityStatus,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _evidence_integrity(case: ClaimCase, source_root: Path) -> str:
    saw_local = False
    for ref in case.evidence:
        if ref.source_kind not in {"local_artifact", "formal_receipt"}:
            continue
        saw_local = True
        path = source_root / ref.path
        if not path.exists():
            return "missing"
        if ref.sha256 and _sha256(path) != ref.sha256:
            return "hash_mismatch"
    return "verified" if saw_local else "external_only"


def audit_claim(case: ClaimCase, source_root: Path) -> ClaimDecision:
    integrity = _evidence_integrity(case, source_root)
    reasons: List[str] = []

    if integrity in {"missing", "hash_mismatch"}:
        return ClaimDecision(
            claim_id=case.claim_id,
            identifiability=IdentifiabilityStatus.UNDERDETERMINED,
            decision=DecisionStatus.INCONCLUSIVE,
            promotion_ceiling="unverified_source_only",
            evidence_integrity=integrity,
            missing_measurements=case.required_measurements,
            reasons=["local evidence did not pass the declared provenance check"],
        )

    verified_countermodels: List[str] = []
    failed_countermodels: List[str] = []
    for countermodel in case.countermodels:
        result = verify_countermodel(countermodel)
        if result.valid:
            verified_countermodels.append(countermodel.id)
        else:
            failed_countermodels.append(countermodel.id)

    missing_measurements = sorted(set(case.required_measurements) - set(case.observed_variables))

    assumption_required_types = {"formal_identity", "predictive", "causal", "mechanistic"}
    missing_assumption_specification = (
        case.claim_type in assumption_required_types and not case.assumptions
    )

    if missing_assumption_specification:
        identifiability = IdentifiabilityStatus.UNDERDETERMINED
        reasons.append("the admissible model class is unspecified because required assumptions are absent")
    elif verified_countermodels:
        identifiability = IdentifiabilityStatus.NON_IDENTIFIABLE
        reasons.append("an executable witness pair reproduces the observable but changes the target")
    elif missing_measurements:
        identifiability = IdentifiabilityStatus.UNDERDETERMINED
        reasons.append("required measurements are absent from the evidence package")
    else:
        identifiability = IdentifiabilityStatus.IDENTIFIED

    empirical = case.empirical_decision
    if empirical and empirical.trigger_met is True and "falsif" in empirical.rule.lower():
        decision = DecisionStatus.FALSIFIED
        reasons.append("the frozen empirical falsification rule is met")
    elif (
        identifiability == IdentifiabilityStatus.IDENTIFIED
        and case.formal_receipt
        and case.formal_receipt.status == "kernel_checked"
        and case.claim_type == "formal_identity"
    ):
        decision = DecisionStatus.SUPPORTED
        reasons.append("the scoped conditional identity has a kernel-checked receipt")
    elif empirical and empirical.trigger_met is True and "support" in empirical.rule.lower():
        decision = DecisionStatus.SUPPORTED
        reasons.append("the frozen empirical support rule is met")
    else:
        decision = DecisionStatus.INCONCLUSIVE
        if identifiability != IdentifiabilityStatus.IDENTIFIED:
            reasons.append("no unique scientific target is recoverable from current measurements")
        else:
            reasons.append("the claim is structurally evaluable but no decisive empirical rule is met")

    if missing_assumption_specification:
        decision = DecisionStatus.INCONCLUSIVE
        ceiling = "proposal_only"
        reasons.append("model-dependent claims fail closed when their assumptions are absent")
    elif decision == DecisionStatus.FALSIFIED:
        ceiling = "bounded_falsification_only"
    elif case.claim_type == "formal_identity" and decision == DecisionStatus.SUPPORTED:
        ceiling = "conditional_formal_result_only"
    elif decision == DecisionStatus.SUPPORTED:
        ceiling = "source_scoped_support_only"
    elif identifiability == IdentifiabilityStatus.NON_IDENTIFIABLE:
        ceiling = "compatibility_only"
    else:
        ceiling = "proposal_only"

    return ClaimDecision(
        claim_id=case.claim_id,
        identifiability=identifiability,
        decision=decision,
        promotion_ceiling=ceiling,
        evidence_integrity=integrity,
        verified_countermodels=verified_countermodels,
        failed_countermodels=failed_countermodels,
        missing_measurements=missing_measurements,
        reasons=reasons,
    )


def audit_dataset(cases: Iterable[ClaimCase], source_root: Path) -> List[ClaimDecision]:
    return [audit_claim(case, source_root) for case in cases]
