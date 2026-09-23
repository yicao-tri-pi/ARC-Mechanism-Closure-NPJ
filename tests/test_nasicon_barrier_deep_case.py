import hashlib
import json
from pathlib import Path

from pydantic import TypeAdapter

from arc_identifiability.audit import audit_dataset
from arc_identifiability.schema import ClaimCase, DecisionStatus, IdentifiabilityStatus


REPO = Path(__file__).resolve().parents[1]


def test_nasicon_case_separates_initial_rate_falsification_from_conductivity_gap() -> None:
    payload = json.loads((REPO / "data/nasicon_barrier_deep_case_v0.1.json").read_text())
    cases = TypeAdapter(list[ClaimCase]).validate_python(payload["claims"])
    reproduction, initial_rate, conductivity = audit_dataset(cases, REPO)

    assert reproduction.identifiability == IdentifiabilityStatus.IDENTIFIED
    assert reproduction.decision == DecisionStatus.SUPPORTED
    assert reproduction.evidence_integrity == "verified"

    assert initial_rate.identifiability == IdentifiabilityStatus.NON_IDENTIFIABLE
    assert initial_rate.decision == DecisionStatus.FALSIFIED
    assert initial_rate.promotion_ceiling == "bounded_falsification_only"
    assert initial_rate.verified_countermodels == [
        "near_equal_mean_barrier_different_initial_rate_sum"
    ]

    assert conductivity.identifiability == IdentifiabilityStatus.UNDERDETERMINED
    assert conductivity.decision == DecisionStatus.INCONCLUSIVE
    assert conductivity.promotion_ceiling == "proposal_only"
    assert "matched_temperature_experimental_conductivity" in conductivity.missing_measurements


def test_nasicon_reproduction_and_lean_receipt_are_bound() -> None:
    result = json.loads(
        (REPO / "results/nasicon_initial_rate_reproduction_v0.1.json").read_text()
    )
    receipt = json.loads((REPO / "results/nasicon_barrier_lean_receipt.json").read_text())
    source = REPO / "formal/NasiconBarrierNonidentifiability.lean"

    assert result["upstream_commit"] == "69eb10b7c52ddd85e39ebeb882b2e4ea617e7770"
    assert result["configuration_scan"]["configuration_count"] == 50
    assert result["configuration_scan"]["all_pair_count"] == 1225
    assert result["configuration_scan"]["pairs_within_declared_mean_barrier_tolerance"] == 14
    assert result["configuration_scan"]["selection_status"] == "exploratory_post_hoc"
    assert [
        item["structure_index"] for item in result["selected_configuration_summaries"]
    ] == [48, 49]
    assert result["comparison"]["mean_barriers_equivalent_at_declared_tolerance"] is True
    assert result["comparison"]["aggregate_initial_rate_ratio"] > 1.48
    assert receipt["kernel_checked"] is True
    assert receipt["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
