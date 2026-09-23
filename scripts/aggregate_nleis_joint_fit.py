#!/usr/bin/env python3
"""Merge a partial full-corpus checkpoint and completed NLEIS spectrum shards."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(path)


def aggregate(contract_path: Path, inputs: list[Path]) -> dict:
    contract = json.loads(contract_path.read_text())
    contract_hash = sha256(contract_path)
    payloads = [json.loads(path.read_text()) for path in inputs]
    if any(item["contract_sha256"] != contract_hash for item in payloads):
        raise RuntimeError("input contract hash mismatch")
    if len({item["data_commit"] for item in payloads}) != 1:
        raise RuntimeError("input data commits differ")
    if len({item["toolbox_commit"] for item in payloads}) != 1:
        raise RuntimeError("input toolbox commits differ")
    by_key = {}
    for payload in payloads:
        for condition in payload["conditions"]:
            key = (
                condition["soc_percent"], condition["cell_state"],
                condition["replicate_index"],
            )
            if key in by_key:
                raise RuntimeError(f"duplicate condition key: {key}")
            by_key[key] = condition
    conditions = [
        by_key[(soc, state, replicate)]
        for soc in contract["corpus"]["soc_percent"]
        for state in contract["corpus"]["cell_states"]
        for replicate in contract["corpus"]["replicate_indices"]
        if (soc, state, replicate) in by_key
    ]
    expected = contract["corpus"]["expected_spectrum_count"]
    if len(conditions) != expected:
        raise RuntimeError(f"expected {expected} unique conditions, found {len(conditions)}")
    eligible = [item for item in conditions if item["eligible"]]
    median_eis = float(np.median([
        item["joint_eis_nleis"]["best_record"]["heldout_eis_nrmse"] for item in eligible
    ])) if eligible else None
    median_nleis = float(np.median([
        item["joint_eis_nleis"]["best_record"]["heldout_nleis_nrmse"] for item in eligible
    ])) if eligible else None
    contraction_count = sum(item["allocation_contraction_gate_pass"] for item in conditions)
    error_gate = bool(
        median_eis is not None and median_nleis is not None
        and median_eis <= 0.10 and median_nleis <= 0.20
    )
    return {
        "schema_version": "arc-nleis-joint-fit-result-0.1",
        "status": "complete",
        "contract_path": str(contract_path),
        "contract_sha256": contract_hash,
        "data_commit": payloads[0]["data_commit"],
        "toolbox_commit": payloads[0]["toolbox_commit"],
        "attempt_count": sum(item.get("attempt_count", 1) for item in payloads),
        "completed_spectrum_count": len(conditions),
        "runtime_seconds": sum(item["runtime_seconds"] for item in payloads),
        "conditions": conditions,
        "aggregate": {
            "requested_spectrum_count": expected,
            "eligible_spectrum_count": len(eligible),
            "median_joint_heldout_eis_nrmse": median_eis,
            "median_joint_heldout_nleis_nrmse": median_nleis,
            "error_gate_pass": error_gate,
            "allocation_contraction_pass_count": contraction_count,
            "allocation_contraction_gate_pass": contraction_count >= 20,
            "joint_confirmation_rule_pass": len(eligible) == expected and error_gate and contraction_count >= 20,
        },
        "aggregation_inputs": [str(path) for path in inputs],
        "interpretation_boundary": contract["interpretation_boundary"],
        "implementation_note": "Independent spectrum shards preserve contract-bound key-specific RNG seeds; aggregation requires exactly 30 unique corpus keys.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    atomic_json(args.output, aggregate(args.contract.resolve(), [p.resolve() for p in args.input]))


if __name__ == "__main__":
    main()
