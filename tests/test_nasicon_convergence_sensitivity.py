import importlib.util
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_script():
    path = REPO / "scripts/analyze_nasicon_convergence_sensitivity.py"
    spec = importlib.util.spec_from_file_location("nasicon_convergence_sensitivity", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_metric_diagnostic_uses_nonoverlapping_windows() -> None:
    module = load_script()
    result = module.metric_diagnostic([1.0] * 500 + [1.1] * 500, 1000, 500, 0.15)
    assert result["preceding_window_median"] == 1.0
    assert result["late_window_median"] == 1.1
    assert result["gate_pass"] is True


def test_retrospective_result_preserves_frozen_verdict_boundary() -> None:
    result = json.loads(
        (REPO / "results/nasicon_convergence_sensitivity_v0.1.json").read_text()
    )
    assert result["analysis_status"] == "retrospective_design_diagnostic_only"
    assert result["frozen_v0_1_verdict_unchanged"] is True
    frozen = next(
        row
        for row in result["endpoint_scan"]
        if row["endpoint_pass"] == 3000 and row["window_passes"] == 500
    )
    assert frozen["run_gate_pass_count"] == 5
    assert frozen["study_gate_pass"] is False


def test_extended_contract_uses_longer_fixed_windows_without_replacing_v0_1() -> None:
    contract = json.loads(
        (REPO / "experiments/nasicon_extended_kmc_contract_v0.2.json").read_text()
    )
    assert contract["simulation"]["measurement_passes"] == 6000
    assert contract["primary_endpoint"]["window_passes"] == 1000
    assert contract["convergence_gate"]["windows"] == {
        "late": [5001, 6000],
        "preceding": [4001, 5000],
    }
    assert contract["convergence_gate"]["diagnostic_only_window_passes"] == [500, 1500]
    assert "not replaced" in contract["amendment_provenance"]["predecessor_verdict_remains"]
    assert contract["simulation"]["paired_random_seeds"] == [104729, 130363, 155921]
    assert contract["result_schema_version"] == "arc-nasicon-extended-kmc-result-0.2"


def test_aggregator_uses_versioned_result_schema(tmp_path: Path) -> None:
    aggregate_path = REPO / "scripts/aggregate_nasicon_production.py"
    spec = importlib.util.spec_from_file_location("extended_aggregate", aggregate_path)
    aggregate = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(aggregate)

    source_contract = json.loads(
        (REPO / "experiments/nasicon_extended_kmc_contract_v0.2.json").read_text()
    )
    source_contract["simulation"]["paired_random_seeds"] = [1]
    contract_path = tmp_path / "contract.json"
    contract_path.write_text(json.dumps(source_contract))
    contract_hash = aggregate.sha256(contract_path)
    shards = []
    for structure, endpoint in ((10, 1.0), (41, 2.0)):
        path = tmp_path / f"{structure}.json"
        path.write_text(
            json.dumps(
                {
                    "status": "complete",
                    "contract_sha256": contract_hash,
                    "seed": 1,
                    "structure_index": structure,
                    "primary_endpoint": endpoint,
                    "run_convergence_gate_pass": True,
                }
            )
        )
        shards.append(path)
    result = aggregate.aggregate(contract_path, shards)
    assert result["schema_version"] == "arc-nasicon-extended-kmc-result-0.2"


def test_extended_result_retains_all_runs_and_failed_closure() -> None:
    result = json.loads(
        (REPO / "results/nasicon_extended_kmc_v0.2.json").read_text()
    )
    assert result["schema_version"] == "arc-nasicon-extended-kmc-result-0.2"
    assert result["aggregate"] == {
        "requested_run_count": 6,
        "completed_run_count": 6,
        "study_convergence_gate_pass": False,
        "directional_confirmation_rule_pass": False,
    }
    pairs = result["paired_summary"]
    assert [row["seed"] for row in pairs] == [104729, 130363, 155921]
    assert [row["pair_convergence_gate_pass"] for row in pairs] == [
        False,
        False,
        True,
    ]
    assert [row["ratio_high_over_low"] > 1 for row in pairs] == [
        False,
        True,
        False,
    ]
    assert pairs[2]["ratio_high_over_low"] == 0.6041078065836858

    contract_hash = result["contract_sha256"]
    run_gates = []
    for seed in (104729, 130363, 155921):
        for structure in (10, 41):
            shard = json.loads(
                (
                    REPO
                    / "results/nasicon_extended_shards"
                    / f"seed_{seed}_structure_{structure}.json"
                ).read_text()
            )
            assert shard["status"] == "complete"
            assert shard["contract_sha256"] == contract_hash
            assert shard["completed_measurement_passes"] == 6000
            assert len(shard["curves"]["conductivity"]) == 6000
            assert set(shard["diagnostic_only_convergence"]) == {"500", "1500"}
            run_gates.append(shard["run_convergence_gate_pass"])
    assert sum(run_gates) == 4
