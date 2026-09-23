#!/usr/bin/env python3
"""Aggregate completed NASICON production shards under the frozen contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(contract_path: Path, shard_paths: list[Path]) -> dict:
    contract = json.loads(contract_path.read_text())
    simulation = contract["simulation"]
    provenance = contract["pair_provenance"]
    expected = {
        (seed, structure)
        for seed in simulation["paired_random_seeds"]
        for structure in provenance["structure_indices"]
    }
    shards = [json.loads(path.read_text()) for path in shard_paths]
    observed = {(item["seed"], item["structure_index"]) for item in shards}
    if observed != expected or len(shards) != len(expected):
        raise ValueError(f"expected shards {sorted(expected)}, observed {sorted(observed)}")
    contract_hash = sha256(contract_path)
    if any(item["contract_sha256"] != contract_hash for item in shards):
        raise ValueError("a shard is not bound to the frozen contract")
    if any(item["status"] != "complete" for item in shards):
        raise ValueError("a shard is incomplete")

    high_index = provenance["high_initial_rate_structure"]
    low_index = provenance["low_initial_rate_structure"]
    pairs = []
    for seed in simulation["paired_random_seeds"]:
        by_structure = {
            item["structure_index"]: item for item in shards if item["seed"] == seed
        }
        high = by_structure[high_index]
        low = by_structure[low_index]
        ratio = high["primary_endpoint"] / low["primary_endpoint"]
        pairs.append(
            {
                "seed": seed,
                "high_initial_rate_structure": high_index,
                "low_initial_rate_structure": low_index,
                "high_late_window_median_conductivity_mS_cm": high["primary_endpoint"],
                "low_late_window_median_conductivity_mS_cm": low["primary_endpoint"],
                "ratio_high_over_low": ratio,
                "pair_convergence_gate_pass": bool(
                    high["run_convergence_gate_pass"] and low["run_convergence_gate_pass"]
                ),
            }
        )
    study_converged = all(item["pair_convergence_gate_pass"] for item in pairs)
    direction_confirmed = study_converged and all(item["ratio_high_over_low"] > 1 for item in pairs)
    return {
        "schema_version": contract.get(
            "result_schema_version", "arc-nasicon-production-kmc-result-0.1"
        ),
        "contract_path": str(contract_path),
        "contract_sha256": contract_hash,
        "shard_sha256": {str(path): sha256(path) for path in shard_paths},
        "paired_summary": pairs,
        "aggregate": {
            "requested_run_count": len(expected),
            "completed_run_count": len(shards),
            "study_convergence_gate_pass": study_converged,
            "directional_confirmation_rule_pass": direction_confirmed,
        },
        "interpretation_boundary": contract["interpretation_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--shards", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = aggregate(args.contract, args.shards)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
