import importlib.util
import hashlib
import json
from pathlib import Path

from pydantic import TypeAdapter

from arc_identifiability.audit import audit_dataset
from arc_identifiability.schema import ClaimCase, DecisionStatus, IdentifiabilityStatus


REPO = Path(__file__).resolve().parents[1]


def load_script():
    path = REPO / "scripts/audit_nleis_public_data.py"
    spec = importlib.util.spec_from_file_location("nleis_data_audit", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_public_data_audit_has_all_conditions_and_replicates() -> None:
    result = json.loads((REPO / "results/nleis_public_data_audit_v0.1.json").read_text())
    assert result["condition_count"] == 10
    assert result["paired_spectrum_count"] == 30
    assert result["all_values_finite"] is True
    assert result["all_second_harmonic_rms_positive"] is True
    assert len(result["file_sha256"]) == 30
    assert all(item["frequency_count"] == 66 for item in result["conditions"])


def test_complex_matrix_rejects_unpaired_columns(tmp_path: Path) -> None:
    module = load_script()
    path = tmp_path / "bad.txt"
    path.write_text("1 2 3\n4 5 6\n")
    try:
        module.complex_matrix(path)
    except ValueError as error:
        assert "real/imaginary" in str(error)
    else:
        raise AssertionError("expected malformed complex matrix to fail")


def test_impedance_parity_lean_receipt_is_kernel_checked() -> None:
    receipt = json.loads((REPO / "results/impedance_parity_lean_receipt.json").read_text())
    assert receipt["kernel_checked"] is True
    assert receipt["returncode"] == 0
    source = REPO / "formal/ImpedanceParityNonidentifiability.lean"
    assert receipt["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()


def test_linear_eis_allocation_case_has_verified_countermodel() -> None:
    payload = json.loads((REPO / "data/nleis_parity_deep_case_v0.1.json").read_text())
    cases = TypeAdapter(list[ClaimCase]).validate_python(payload["claims"])
    decision = audit_dataset(cases, REPO)[0]
    assert decision.evidence_integrity == "verified"
    assert decision.identifiability == IdentifiabilityStatus.NON_IDENTIFIABLE
    assert decision.decision == DecisionStatus.INCONCLUSIVE
    assert decision.verified_countermodels == [
        "same_linear_sum_different_electrode_allocation"
    ]
    assert "second_harmonic_nleis_difference" in decision.missing_measurements
