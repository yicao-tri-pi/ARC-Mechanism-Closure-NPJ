import importlib.util
import hashlib
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_script():
    spec = importlib.util.spec_from_file_location(
        "nasicon_short_pilot", REPO / "scripts/run_nasicon_short_kmc_pilot.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_finite_final_requires_positive_time_and_finite_transport_values() -> None:
    module = load_script()
    valid = {"time": 1.0, "D_J": 2.0, "D_tracer": 3.0, "conductivity": 4.0, "msd": 5.0}
    assert module.finite_final(valid) is True
    assert module.finite_final({**valid, "time": 0.0}) is False
    assert module.finite_final({**valid, "conductivity": math.inf}) is False


def test_short_pilot_is_feasible_but_direction_unstable() -> None:
    contract = REPO / "experiments/nasicon_short_kmc_pilot_contract_v0.1.json"
    result = json.loads((REPO / "results/nasicon_short_kmc_pilot_v0.1.json").read_text())
    assert result["contract_sha256"] == hashlib.sha256(contract.read_bytes()).hexdigest()
    assert result["aggregate"]["requested_run_count"] == 6
    assert result["aggregate"]["completed_run_count"] == 6
    assert result["aggregate"]["feasibility_rule_pass"] is True
    assert result["aggregate"]["direction_consistent_across_seeds"] is False
    ratios = [item["conductivity_ratio_high_over_low"] for item in result["paired_summary"]]
    assert min(ratios) < 1 < max(ratios)
