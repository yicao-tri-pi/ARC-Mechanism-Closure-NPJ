#!/usr/bin/env python3
"""Run the contract-frozen EIS-only versus joint EIS/NLEIS multistart study."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    temporary.write_text(json.dumps(payload, indent=2) + "\n")
    temporary.replace(path)


def git_commit(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
    ).stdout.strip()


def nrmse(data, prediction) -> float:
    import numpy as np

    denominator = float(np.sqrt(np.mean(np.abs(data) ** 2)))
    numerator = float(np.sqrt(np.mean(np.abs(data - prediction) ** 2)))
    return numerator / max(denominator, 1e-30)


def near_optimal(records: list[dict], rule_multiplier: float = 1.10, rule_offset: float = 0.005) -> list[dict]:
    successes = [record for record in records if record["status"] == "success"]
    if not successes:
        return []
    best = min(record["training_objective"] for record in successes)
    threshold = best * rule_multiplier + rule_offset
    return [record for record in successes if record["training_objective"] <= threshold]


def allocation_width(records: list[dict]) -> float | None:
    values = [record["allocation_fraction"] for record in records]
    return max(values) - min(values) if values else None


def randomized_positive(base, lower, upper, rng, first: bool):
    import numpy as np

    if first:
        return np.clip(np.asarray(base, dtype=float), lower + 1e-15, upper - 1e-15)
    factors = 10 ** rng.uniform(-1.0, 1.0, size=len(base))
    return np.clip(np.asarray(base, dtype=float) * factors, lower + 1e-15, upper - 1e-15)


def resume_multistart(rng, pending: dict | None, key: tuple[int, str, int]):
    if pending is None:
        return [], [], 0
    pending_key = (
        pending["soc_percent"], pending["cell_state"], pending["replicate_index"]
    )
    if pending_key != key:
        raise RuntimeError(
            f"checkpoint pending key {pending_key} does not match next corpus key {key}"
        )
    eis_records = list(pending["eis_records"])
    joint_records = list(pending["joint_records"])
    start_begin = int(pending["next_start_index"])
    if len(eis_records) != start_begin or len(joint_records) != start_begin:
        raise RuntimeError("checkpoint record counts do not match next_start_index")
    rng.bit_generator.state = pending["rng_state_after_last_start"]
    return eis_records, joint_records, start_begin


def run(
    contract_path: Path,
    data_root: Path,
    toolbox_root: Path,
    output_path: Path | None = None,
    selected_key: tuple[int, str, int] | None = None,
) -> dict:
    import numpy as np
    from impedance.models.circuits import CustomCircuit
    from nleis import EISandNLEIS
    from nleis.data_processing import data_truncation

    contract = json.loads(contract_path.read_text())
    contract_hash = sha256(contract_path)
    if git_commit(data_root) != contract["sources"]["data_repository"]["commit"]:
        raise RuntimeError("data repository commit mismatch")
    if git_commit(toolbox_root) != contract["sources"]["toolbox_repository"]["commit"]:
        raise RuntimeError("toolbox repository commit mismatch")

    eis_circuit = contract["models"]["linear_eis_circuit"]
    nleis_circuit = contract["models"]["second_harmonic_circuit"]
    starts = contract["optimization"]["multistart_count"]
    master_seed = contract["optimization"]["master_seed"]
    maxfev = contract["optimization"]["max_function_evaluations"]
    modulus = contract["split"]["heldout_modulus"]
    remainder = contract["split"]["heldout_remainder"]

    base_eis = np.asarray(
        [1e-7, 1e-3, 5e-3, 1e-3, 10, 1e-2, 100, 1e-3, 1e-3, 1e-3, 1e-2, 1000],
        dtype=float,
    )
    upper_eis = np.asarray([1e-5, 0.2, 1, 1, 1000, 100, 100000, 1, 1, 1000, 100, 100000], dtype=float)
    lower_eis = np.zeros(12, dtype=float)
    lower_joint = np.asarray([0, 0, 0, 0, 0, 0, 0, -1000, -0.3, 0, 0, 0, 0, 0, -1000, -0.3], dtype=float)
    upper_joint = np.asarray([1e-5, 0.2, 1, 1, 1000, 100, 100000, 1000, 0.3, 1, 1, 1000, 100, 100000, 1000, 0.3], dtype=float)

    existing = None
    if output_path is not None and output_path.exists():
        existing = json.loads(output_path.read_text())
        if existing.get("contract_sha256") != contract_hash:
            raise RuntimeError("checkpoint is bound to a different contract")
        if existing.get("data_commit") != git_commit(data_root):
            raise RuntimeError("checkpoint data commit mismatch")
        if existing.get("toolbox_commit") != git_commit(toolbox_root):
            raise RuntimeError("checkpoint toolbox commit mismatch")
        if existing.get("execution_selection") != (
            list(selected_key) if selected_key is not None else None
        ):
            raise RuntimeError("checkpoint execution selection mismatch")
        if existing.get("status") in {"complete", "shard_complete"}:
            return existing
    conditions = list(existing.get("conditions", [])) if existing else []
    pending_condition = existing.get("pending_condition") if existing else None
    completed_keys = {
        (item["soc_percent"], item["cell_state"], item["replicate_index"])
        for item in conditions
    }
    prior_runtime = float(existing.get("runtime_seconds", 0.0)) if existing else 0.0
    attempt_count = int(existing.get("attempt_count", 0)) + 1 if existing else 1
    started = time.perf_counter()

    def checkpoint(pending: dict | None) -> None:
        if output_path is None:
            return
        atomic_json(
            output_path,
            {
                "schema_version": "arc-nleis-joint-fit-result-0.1",
                "status": "running",
                "contract_path": str(contract_path),
                "contract_sha256": contract_hash,
                "data_commit": git_commit(data_root),
                "toolbox_commit": git_commit(toolbox_root),
                "attempt_count": attempt_count,
                "completed_spectrum_count": len(conditions),
                "runtime_seconds": prior_runtime + time.perf_counter() - started,
                "conditions": conditions,
                "pending_condition": pending,
                "execution_selection": list(selected_key) if selected_key is not None else None,
                "implementation_note": "Each spectrum uses a deterministic key-specific RNG. RNG state and both arm records are atomically checkpointed after every completed multistart pair.",
                "interpretation_boundary": contract["interpretation_boundary"],
            },
        )

    data_dir = data_root / "Part II" / "data"
    states = {"fresh": "f", "aged_100_cycles_at_2C": "a"}
    for soc in contract["corpus"]["soc_percent"]:
        for state_name in contract["corpus"]["cell_states"]:
            suffix = states[state_name]
            label = f"{soc}{suffix}"
            frequencies = np.loadtxt(data_dir / f"freq_{label}.txt")
            z1s = np.loadtxt(data_dir / f"Z1s_{label}.txt").view(complex)
            z2s = np.loadtxt(data_dir / f"Z2s_{label}.txt").view(complex)
            for replicate in contract["corpus"]["replicate_indices"]:
                key = (soc, state_name, replicate)
                if selected_key is not None and key != selected_key:
                    continue
                if key in completed_keys:
                    continue
                frequency, z1, z2, _, _ = data_truncation(
                    frequencies, z1s[replicate], z2s[replicate]
                )
                indices = np.arange(len(frequency))
                heldout = indices % modulus == remainder
                train = ~heldout
                rng = np.random.default_rng(master_seed + soc * 100 + (0 if suffix == "f" else 50) + replicate)
                eis_records, joint_records, start_begin = resume_multistart(
                    rng, pending_condition, key
                )
                for start_index in range(start_begin, starts):
                    eis_guess = randomized_positive(
                        base_eis, lower_eis, upper_eis, rng, start_index == 0
                    )
                    try:
                        model = CustomCircuit(eis_circuit, initial_guess=eis_guess.tolist())
                        fit_started = time.perf_counter()
                        model.fit(
                            frequency[train],
                            z1[train],
                            bounds=(lower_eis, upper_eis),
                            maxfev=maxfev,
                        )
                        train_prediction = model.predict(frequency[train])
                        heldout_prediction = model.predict(frequency[heldout])
                        parameters = np.asarray(model.parameters_, dtype=float)
                        fraction = float(parameters[3] / max(parameters[3] + parameters[8], 1e-30))
                        eis_records.append(
                            {
                                "start_index": start_index,
                                "status": "success",
                                "runtime_seconds": time.perf_counter() - fit_started,
                                "training_objective": nrmse(z1[train], train_prediction),
                                "heldout_eis_nrmse": nrmse(z1[heldout], heldout_prediction),
                                "allocation_fraction": fraction,
                                "rct_positive": float(parameters[3]),
                                "rct_negative": float(parameters[8]),
                                "parameters": parameters.tolist(),
                            }
                        )
                    except Exception as error:
                        eis_records.append(
                            {"start_index": start_index, "status": "failed", "error": repr(error)}
                        )

                    kappa = rng.uniform(-20.0, 20.0, size=2)
                    epsilon = rng.uniform(-0.2, 0.2, size=2)
                    joint_guess = np.asarray(
                        list(eis_guess[:7])
                        + [kappa[0], epsilon[0]]
                        + list(eis_guess[7:])
                        + [kappa[1], epsilon[1]],
                        dtype=float,
                    )
                    if start_index == 0:
                        joint_guess[7:] = np.asarray(
                            [-10, 0.05] + list(base_eis[7:]) + [0, 0], dtype=float
                        )
                    joint_guess = np.clip(joint_guess, lower_joint + 1e-15, upper_joint - 1e-15)
                    try:
                        model = EISandNLEIS(
                            eis_circuit, nleis_circuit, initial_guess=joint_guess.tolist()
                        )
                        fit_started = time.perf_counter()
                        model.fit(
                            frequency[train],
                            z1[train],
                            z2[train],
                            bounds=(lower_joint, upper_joint),
                            opt="max",
                            maxfev=maxfev,
                        )
                        train_z1, train_z2 = model.predict(frequency[train])
                        heldout_z1, heldout_z2 = model.predict(frequency[heldout])
                        parameters = np.asarray(model.parameters_, dtype=float)
                        train_eis = nrmse(z1[train], train_z1)
                        train_nleis = nrmse(z2[train], train_z2)
                        fraction = float(parameters[3] / max(parameters[3] + parameters[10], 1e-30))
                        joint_records.append(
                            {
                                "start_index": start_index,
                                "status": "success",
                                "runtime_seconds": time.perf_counter() - fit_started,
                                "training_objective": 0.5 * (train_eis + train_nleis),
                                "train_eis_nrmse": train_eis,
                                "train_nleis_nrmse": train_nleis,
                                "heldout_eis_nrmse": nrmse(z1[heldout], heldout_z1),
                                "heldout_nleis_nrmse": nrmse(z2[heldout], heldout_z2),
                                "allocation_fraction": fraction,
                                "rct_positive": float(parameters[3]),
                                "rct_negative": float(parameters[10]),
                                "parameters": parameters.tolist(),
                            }
                        )
                    except Exception as error:
                        joint_records.append(
                            {"start_index": start_index, "status": "failed", "error": repr(error)}
                        )
                    pending_condition = {
                        "soc_percent": soc,
                        "cell_state": state_name,
                        "replicate_index": replicate,
                        "next_start_index": start_index + 1,
                        "rng_state_after_last_start": rng.bit_generator.state,
                        "eis_records": eis_records,
                        "joint_records": joint_records,
                    }
                    checkpoint(pending_condition)
                    print(
                        f"soc={soc} state={state_name} replicate={replicate} start={start_index + 1}/{starts}",
                        flush=True,
                    )

                eis_near = near_optimal(eis_records)
                joint_near = near_optimal(joint_records)
                eis_width = allocation_width(eis_near)
                joint_width = allocation_width(joint_near)
                min_success = contract["optimization"]["minimum_successful_starts_per_arm"]
                min_near = contract["optimization"]["minimum_near_optimal_starts_per_arm"]
                eligible = (
                    sum(record["status"] == "success" for record in eis_records) >= min_success
                    and sum(record["status"] == "success" for record in joint_records) >= min_success
                    and len(eis_near) >= min_near
                    and len(joint_near) >= min_near
                )
                contraction = (
                    eligible
                    and eis_width is not None
                    and joint_width is not None
                    and joint_width <= 0.75 * eis_width
                )
                conditions.append(
                    {
                        "soc_percent": soc,
                        "cell_state": state_name,
                        "replicate_index": replicate,
                        "retained_frequency_count": int(len(frequency)),
                        "training_frequency_count": int(train.sum()),
                        "heldout_frequency_count": int(heldout.sum()),
                        "eis_only": {
                            "records": eis_records,
                            "successful_start_count": sum(record["status"] == "success" for record in eis_records),
                            "near_optimal_start_count": len(eis_near),
                            "allocation_range_width": eis_width,
                            "best_record": min(eis_near, key=lambda item: item["training_objective"]) if eis_near else None,
                        },
                        "joint_eis_nleis": {
                            "records": joint_records,
                            "successful_start_count": sum(record["status"] == "success" for record in joint_records),
                            "near_optimal_start_count": len(joint_near),
                            "allocation_range_width": joint_width,
                            "best_record": min(joint_near, key=lambda item: item["training_objective"]) if joint_near else None,
                        },
                        "eligible": eligible,
                        "allocation_contraction_gate_pass": bool(contraction),
                    }
                )
                pending_condition = None
                checkpoint(None)
                print(
                    f"soc={soc} state={state_name} replicate={replicate} completed={len(conditions)}/30",
                    flush=True,
                )

    eligible = [item for item in conditions if item["eligible"]]
    median_joint_eis = float(np.median([item["joint_eis_nleis"]["best_record"]["heldout_eis_nrmse"] for item in eligible])) if eligible else None
    median_joint_nleis = float(np.median([item["joint_eis_nleis"]["best_record"]["heldout_nleis_nrmse"] for item in eligible])) if eligible else None
    contraction_count = sum(item["allocation_contraction_gate_pass"] for item in conditions)
    error_gate = bool(
        median_joint_eis is not None
        and median_joint_nleis is not None
        and median_joint_eis <= 0.10
        and median_joint_nleis <= 0.20
    )
    joint_rule = len(eligible) == 30 and error_gate and contraction_count >= 20
    is_shard = selected_key is not None
    return {
        "schema_version": "arc-nleis-joint-fit-result-0.1",
        "status": "shard_complete" if is_shard else "complete",
        "contract_path": str(contract_path),
        "contract_sha256": contract_hash,
        "data_commit": git_commit(data_root),
        "toolbox_commit": git_commit(toolbox_root),
        "attempt_count": attempt_count,
        "completed_spectrum_count": len(conditions),
        "runtime_seconds": prior_runtime + time.perf_counter() - started,
        "conditions": conditions,
        "execution_selection": list(selected_key) if selected_key is not None else None,
        "aggregate": {
            "requested_spectrum_count": 30,
            "eligible_spectrum_count": len(eligible),
            "median_joint_heldout_eis_nrmse": median_joint_eis,
            "median_joint_heldout_nleis_nrmse": median_joint_nleis,
            "error_gate_pass": error_gate,
            "allocation_contraction_pass_count": contraction_count,
            "allocation_contraction_gate_pass": contraction_count >= 20,
            "joint_confirmation_rule_pass": joint_rule,
        },
        "interpretation_boundary": contract["interpretation_boundary"],
        "implementation_note": "Each spectrum uses a deterministic key-specific RNG. RNG state and both arm records are atomically checkpointed after every completed multistart pair.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--toolbox-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only-soc", type=int)
    parser.add_argument("--only-state")
    parser.add_argument("--only-replicate", type=int)
    args = parser.parse_args()
    selector_values = (args.only_soc, args.only_state, args.only_replicate)
    if any(value is not None for value in selector_values) and not all(
        value is not None for value in selector_values
    ):
        parser.error("--only-soc, --only-state, and --only-replicate must be supplied together")
    selected_key = (
        (args.only_soc, args.only_state, args.only_replicate)
        if all(value is not None for value in selector_values)
        else None
    )
    result = run(
        args.contract.resolve(),
        args.data_root.resolve(),
        args.toolbox_root.resolve(),
        args.output.resolve(),
        selected_key,
    )
    atomic_json(args.output.resolve(), result)


if __name__ == "__main__":
    main()
