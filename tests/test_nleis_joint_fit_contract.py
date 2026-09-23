import importlib.util
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_script():
    path = REPO / "scripts/run_nleis_joint_fit.py"
    spec = importlib.util.spec_from_file_location("nleis_joint_fit", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_aggregator():
    path = REPO / "scripts/aggregate_nleis_joint_fit.py"
    spec = importlib.util.spec_from_file_location("aggregate_nleis_joint_fit", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_contract_freezes_full_corpus_and_confirmation_rule() -> None:
    contract = json.loads((REPO / "experiments/nleis_joint_fit_contract_v0.1.json").read_text())
    assert contract["corpus"]["expected_spectrum_count"] == 30
    assert contract["optimization"]["multistart_count"] == 12
    assert contract["split"]["heldout_modulus"] == 5
    assert contract["confirmation_rule"]["contraction_gate"].endswith("at least 20 of 30 spectra")
    assert contract["models"]["arms"] == ["eis_only", "joint_eis_nleis"]


def test_near_optimal_and_width_are_deterministic() -> None:
    module = load_script()
    records = [
        {"status": "success", "training_objective": 0.10, "allocation_fraction": 0.2},
        {"status": "success", "training_objective": 0.11, "allocation_fraction": 0.5},
        {"status": "success", "training_objective": 0.20, "allocation_fraction": 0.9},
        {"status": "failed"},
    ]
    selected = module.near_optimal(records)
    assert len(selected) == 2
    assert abs(module.allocation_width(selected) - 0.3) < 1e-12


def test_atomic_checkpoint_replaces_complete_json(tmp_path: Path) -> None:
    module = load_script()
    output = tmp_path / "checkpoint.json"
    module.atomic_json(output, {"status": "running", "completed_spectrum_count": 1})
    assert json.loads(output.read_text()) == {
        "status": "running",
        "completed_spectrum_count": 1,
    }
    assert list(tmp_path.glob("*.tmp-*")) == []


def test_multistart_resume_restores_rng_and_records_after_json_roundtrip() -> None:
    import numpy as np

    module = load_script()
    uninterrupted = np.random.default_rng(1701)
    uninterrupted.uniform(size=7)
    state = uninterrupted.bit_generator.state
    expected_next = uninterrupted.uniform(size=5)
    pending = json.loads(
        json.dumps(
            {
                "soc_percent": 0,
                "cell_state": "fresh",
                "replicate_index": 0,
                "next_start_index": 1,
                "rng_state_after_last_start": state,
                "eis_records": [{"start_index": 0}],
                "joint_records": [{"start_index": 0}],
            }
        )
    )
    resumed = np.random.default_rng(999)
    eis_records, joint_records, start_begin = module.resume_multistart(
        resumed, pending, (0, "fresh", 0)
    )
    assert start_begin == 1
    assert eis_records == [{"start_index": 0}]
    assert joint_records == [{"start_index": 0}]
    assert np.array_equal(resumed.uniform(size=5), expected_next)


def test_shard_aggregator_requires_and_orders_all_30_unique_keys(tmp_path: Path) -> None:
    module = load_aggregator()
    contract_path = REPO / "experiments/nleis_joint_fit_contract_v0.1.json"
    contract = json.loads(contract_path.read_text())
    common = {
        "contract_sha256": module.sha256(contract_path),
        "data_commit": "data",
        "toolbox_commit": "toolbox",
        "attempt_count": 1,
        "runtime_seconds": 1.0,
    }
    conditions = []
    for soc in contract["corpus"]["soc_percent"]:
        for state in contract["corpus"]["cell_states"]:
            for replicate in contract["corpus"]["replicate_indices"]:
                conditions.append(
                    {
                        "soc_percent": soc,
                        "cell_state": state,
                        "replicate_index": replicate,
                        "eligible": True,
                        "allocation_contraction_gate_pass": True,
                        "joint_eis_nleis": {
                            "best_record": {
                                "heldout_eis_nrmse": 0.01,
                                "heldout_nleis_nrmse": 0.02,
                            }
                        },
                    }
                )
    paths = []
    for index, condition in enumerate(conditions):
        path = tmp_path / f"shard_{index}.json"
        path.write_text(json.dumps({**common, "conditions": [condition]}))
        paths.append(path)
    result = module.aggregate(contract_path, paths)
    assert result["completed_spectrum_count"] == 30
    assert result["aggregate"]["eligible_spectrum_count"] == 30
    assert result["aggregate"]["joint_confirmation_rule_pass"] is True
    assert [item["soc_percent"] for item in result["conditions"][:6]] == [10] * 6


def test_frozen_joint_fit_result_fails_identifiability_closure() -> None:
    result = json.loads((REPO / "results/nleis_joint_fit_v0.1.json").read_text())
    assert result["status"] == "complete"
    assert result["completed_spectrum_count"] == 30
    aggregate = result["aggregate"]
    assert aggregate["eligible_spectrum_count"] == 26
    assert aggregate["error_gate_pass"] is True
    assert aggregate["allocation_contraction_pass_count"] == 3
    assert aggregate["allocation_contraction_gate_pass"] is False
    assert aggregate["joint_confirmation_rule_pass"] is False
    assert aggregate["median_joint_heldout_eis_nrmse"] < 0.10
    assert aggregate["median_joint_heldout_nleis_nrmse"] < 0.20
