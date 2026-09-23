import importlib.util
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_script(relative: str, name: str):
    path = REPO / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_production_contract_freezes_source_length_pair_and_gates() -> None:
    contract = json.loads(
        (REPO / "experiments/nasicon_production_kmc_contract_v0.1.json").read_text()
    )
    assert contract["simulation"]["measurement_passes"] == 3000
    assert contract["simulation"]["paired_random_seeds"] == [104729, 130363, 155921]
    assert contract["pair_provenance"]["structure_indices"] == [10, 41]
    assert contract["primary_endpoint"]["window_passes"] == 500
    assert set(contract["convergence_gate"]["metrics"]) == {
        "conductivity",
        "D_J",
        "D_tracer",
        "H_R",
    }


def test_relative_median_drift_uses_two_nonoverlapping_windows() -> None:
    module = load_script("scripts/run_nasicon_production_shard.py", "production_shard")
    diagnostic = module.relative_median_drift([1.0] * 500 + [1.1] * 500, 500)
    assert diagnostic["preceding_window_median"] == 1.0
    assert diagnostic["late_window_median"] == 1.1
    assert abs(diagnostic["relative_median_drift"] - (0.1 / 1.1)) < 1e-12


def test_aggregator_requires_all_bound_shards(tmp_path: Path) -> None:
    module = load_script("scripts/aggregate_nasicon_production.py", "production_aggregate")
    contract_path = REPO / "experiments/nasicon_production_kmc_contract_v0.1.json"
    contract = json.loads(contract_path.read_text())
    contract_hash = module.sha256(contract_path)
    shard_paths = []
    for seed in contract["simulation"]["paired_random_seeds"]:
        for structure in contract["pair_provenance"]["structure_indices"]:
            path = tmp_path / f"{seed}_{structure}.json"
            path.write_text(
                json.dumps(
                    {
                        "status": "complete",
                        "contract_sha256": contract_hash,
                        "seed": seed,
                        "structure_index": structure,
                        "primary_endpoint": 2.0 if structure == 41 else 1.0,
                        "run_convergence_gate_pass": True,
                    }
                )
            )
            shard_paths.append(path)
    result = module.aggregate(contract_path, shard_paths)
    assert result["aggregate"]["study_convergence_gate_pass"] is True
    assert result["aggregate"]["directional_confirmation_rule_pass"] is True
    assert [item["ratio_high_over_low"] for item in result["paired_summary"]] == [2.0] * 3


def test_frozen_production_result_retains_reversal_and_failed_convergence() -> None:
    result = json.loads((REPO / "results/nasicon_production_kmc_v0.1.json").read_text())
    assert result["aggregate"] == {
        "requested_run_count": 6,
        "completed_run_count": 6,
        "study_convergence_gate_pass": False,
        "directional_confirmation_rule_pass": False,
    }
    pairs = result["paired_summary"]
    assert [item["seed"] for item in pairs] == [104729, 130363, 155921]
    assert [item["ratio_high_over_low"] > 1 for item in pairs] == [False, True, True]
    assert [item["pair_convergence_gate_pass"] for item in pairs] == [False, True, True]


def test_frozen_production_shards_are_complete_and_contract_bound() -> None:
    module = load_script("scripts/aggregate_nasicon_production.py", "production_result_check")
    contract_path = REPO / "experiments/nasicon_production_kmc_contract_v0.1.json"
    contract_hash = module.sha256(contract_path)
    shard_dir = REPO / "results/nasicon_production_shards"
    shards = sorted(shard_dir.glob("*.json"))
    assert len(shards) == 6
    payloads = [json.loads(path.read_text()) for path in shards]
    assert all(item["status"] == "complete" for item in payloads)
    assert all(item["completed_measurement_passes"] == 3000 for item in payloads)
    assert all(item["contract_sha256"] == contract_hash for item in payloads)
    assert all(len(item["curves"]["conductivity"]) == 3000 for item in payloads)
    assert sum(item["run_convergence_gate_pass"] for item in payloads) == 5
