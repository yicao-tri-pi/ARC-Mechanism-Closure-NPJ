import importlib.util
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def load_script():
    path = REPO / "scripts/run_nasicon_kmc_smoke.py"
    spec = importlib.util.spec_from_file_location("nasicon_smoke", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_smoke_contract_is_bounded_and_paired() -> None:
    contract = json.loads(
        (REPO / "experiments/nasicon_kmc_smoke_contract_v0.1.json").read_text()
    )
    arm = contract["arms"][0]
    assert contract["interpretation"] == "implementation smoke test only; no scientific comparison or convergence claim"
    assert contract["resources"]["processes"] == 1
    assert arm["structure_indices"] == [48, 49]
    assert arm["measurement_passes"] == 3
    assert "not converged" in contract["nonclaims"][0]


def test_graph_summary_detects_components() -> None:
    module = load_script()

    class Event:
        def __init__(self, left: int, right: int, probability: float):
            self.na1_index = left
            self.na2_index = right
            self.probability = probability

    summary = module.active_graph_summary(
        [Event(0, 1, 1.0), Event(1, 2, 2.0), Event(7, 8, 1.0), Event(2, 9, 0.0)]
    )
    assert summary["active_site_count"] == 5
    assert summary["active_undirected_edge_count"] == 3
    assert summary["connected_component_count"] == 2
    assert summary["largest_component_site_count"] == 3


def test_remote_smoke_receipt_binds_outputs() -> None:
    receipt = json.loads(
        (REPO / "results/nasicon_kmc_smoke_remote_receipt_v0.1.json").read_text()
    )
    result_path = REPO / "results/nasicon_kmc_smoke_remote_v0.1.json"
    resource_path = REPO / "results/nasicon_kmc_smoke_remote_resource_v0.1.txt"

    assert receipt["exit_status"] == 0
    assert receipt["result"]["all_smoke_gates_pass"] is True
    assert hashlib.sha256(result_path.read_bytes()).hexdigest() == receipt["artifact_sha256"][
        "results/nasicon_kmc_smoke_remote_v0.1.json"
    ]
    assert hashlib.sha256(resource_path.read_bytes()).hexdigest() == receipt["artifact_sha256"][
        "results/nasicon_kmc_smoke_remote_resource_v0.1.txt"
    ]

    result = json.loads(result_path.read_text())
    assert result["all_smoke_gates_pass"] is True
    assert len(result["structure_results"]) == 2
    assert all(run["measurement_passes"] == 3 for run in result["structure_results"])
