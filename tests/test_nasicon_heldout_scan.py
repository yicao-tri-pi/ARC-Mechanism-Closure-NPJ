import importlib.util
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_script():
    spec = importlib.util.spec_from_file_location(
        "nasicon_heldout", REPO / "scripts/run_nasicon_heldout_scan.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_pair_scan_enumerates_and_applies_frozen_thresholds() -> None:
    module = load_script()
    summaries = [
        {"structure_index": 1, "observable": 10.0, "target": 1.0},
        {"structure_index": 2, "observable": 10.1, "target": 1.3},
        {"structure_index": 3, "observable": 11.0, "target": 4.0},
    ]
    result = module.pair_scan(
        summaries,
        observable="observable",
        target="target",
        tolerance=0.25,
        threshold=1.25,
    )
    assert result["matched_pair_count"] == 1
    assert result["pairs_meeting_rate_ratio_threshold"] == 1
    assert result["maximum_ratio_pair"]["left_structure_index"] == 1
    assert result["maximum_ratio_pair"]["right_structure_index"] == 2


def test_frozen_heldout_result_passes_both_channels() -> None:
    contract = REPO / "experiments/nasicon_heldout_contract_v0.1.json"
    result = json.loads(
        (REPO / "results/nasicon_heldout_composition_scan_v0.1.json").read_text()
    )
    assert result["contract_sha256"] == hashlib.sha256(contract.read_bytes()).hexdigest()
    assert len(result["composition_results"]) == 12
    assert result["confirmation"] == {
        "mean_ekra_to_full_rate_pass": True,
        "nonnegative_directional_barrier_pass": True,
        "joint_rule_pass": True,
    }
    assert result["channel_summary"]["mean_ekra_to_full_rate"][
        "compositions_meeting_rate_ratio_threshold"
    ] == 11
    assert result["channel_summary"]["nonnegative_directional_barrier"][
        "compositions_meeting_rate_ratio_threshold"
    ] == 11
