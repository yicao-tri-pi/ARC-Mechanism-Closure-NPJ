#!/usr/bin/env python3
"""Run the frozen cross-composition NASICON initialization confirmation."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import subprocess
import sys
import time
from pathlib import Path

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
    ).stdout.strip()


def pair_scan(
    summaries: list[dict], *, observable: str, target: str, tolerance: float, threshold: float
) -> dict:
    matched = []
    for left_index, left in enumerate(summaries):
        for right in summaries[left_index + 1 :]:
            difference = abs(left[observable] - right[observable])
            if difference > tolerance:
                continue
            ratio = max(left[target], right[target]) / min(left[target], right[target])
            matched.append(
                {
                    "left_structure_index": left["structure_index"],
                    "right_structure_index": right["structure_index"],
                    "observable_absolute_difference_mev": difference,
                    "target_rate_ratio": ratio,
                }
            )
    matched.sort(key=lambda item: item["target_rate_ratio"], reverse=True)
    above = [item for item in matched if item["target_rate_ratio"] >= threshold]
    return {
        "matched_pair_count": len(matched),
        "pairs_meeting_rate_ratio_threshold": len(above),
        "fraction_meeting_rate_ratio_threshold": len(above) / len(matched) if matched else None,
        "maximum_rate_ratio": matched[0]["target_rate_ratio"] if matched else None,
        "maximum_ratio_pair": matched[0] if matched else None,
    }


def summarize(events: list[object], structure_index: int) -> dict:
    import numpy as np

    active = [event for event in events if event.probability > 0]
    directional = np.asarray([event.barrier for event in active], dtype=float)
    ekra = np.asarray([event.ekra for event in active], dtype=float)
    rates = np.asarray([event.probability for event in active], dtype=float)
    nonnegative = directional >= 0
    return {
        "structure_index": structure_index,
        "active_event_count": len(active),
        "mean_ekra_mev": float(np.mean(ekra)),
        "full_aggregate_rate_hz": float(np.sum(rates)),
        "negative_directional_event_count": int(np.count_nonzero(~nonnegative)),
        "negative_directional_rate_fraction": float(np.sum(rates[~nonnegative]) / np.sum(rates)),
        "mean_nonnegative_directional_barrier_mev": float(np.mean(directional[nonnegative])),
        "nonnegative_aggregate_rate_hz": float(np.sum(rates[nonnegative])),
    }


def main() -> None:
    import numpy as np
    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text())
    upstream = args.upstream_root.resolve()
    commit = git_commit(upstream)
    if commit != contract["upstream_commit"]:
        raise RuntimeError(f"expected upstream {contract['upstream_commit']}, found {commit}")

    sys.path.insert(0, str(upstream / "lib"))
    from kmc import KMC  # noqa: PLC0415

    inputs = upstream / "inputs"
    frame = pd.read_hdf(upstream / "kmc/mc_results.h5")
    started = time.perf_counter()
    composition_results = []
    for composition in contract["heldout_compositions"]:
        rows = frame[np.isclose(frame["comp"], composition)].sort_values("structure_index")
        expected_indices = contract["configuration_indices_per_composition"]
        if rows["structure_index"].tolist() != expected_indices:
            raise RuntimeError(f"unexpected structure indices for composition {composition}")
        summaries = []
        for row in rows.itertuples(index=False):
            model = KMC()
            with contextlib.redirect_stdout(io.StringIO()):
                events = model.initialization(
                    row.occ,
                    str(inputs / "prim.json"),
                    str(inputs / "fitting_results.pkl"),
                    str(inputs / "fitting_results_site.pkl"),
                    str(inputs / "events_888_site.pkl"),
                    tuple(contract["supercell_shape"]),
                    contract["attempt_frequency_hz"],
                    contract["temperature_k"],
                    lce_fname=str(inputs / "lce.pkl"),
                    lce_site_fname=str(inputs / "lce_site.pkl"),
                )
            summaries.append(summarize(events, int(row.structure_index)))

        source_channel = contract["channels"]["mean_ekra_to_full_rate"]
        sensitivity_channel = contract["channels"]["nonnegative_directional_barrier"]
        composition_results.append(
            {
                "composition_parameter_comp": composition,
                "paper_formula_x": 3 - 3 * composition,
                "formula_na_content": 4 - 3 * composition,
                "negative_directional_rate_fraction_range": [
                    min(item["negative_directional_rate_fraction"] for item in summaries),
                    max(item["negative_directional_rate_fraction"] for item in summaries),
                ],
                "mean_ekra_to_full_rate": pair_scan(
                    summaries,
                    observable="mean_ekra_mev",
                    target="full_aggregate_rate_hz",
                    tolerance=source_channel["observable_absolute_tolerance_mev"],
                    threshold=source_channel["target_rate_ratio_threshold"],
                ),
                "nonnegative_directional_barrier": pair_scan(
                    summaries,
                    observable="mean_nonnegative_directional_barrier_mev",
                    target="nonnegative_aggregate_rate_hz",
                    tolerance=sensitivity_channel["observable_absolute_tolerance_mev"],
                    threshold=sensitivity_channel["target_rate_ratio_threshold"],
                ),
            }
        )
        print(f"completed composition {composition}", flush=True)

    channel_summary = {}
    for channel_name in contract["channels"]:
        results = [item[channel_name] for item in composition_results]
        total_matched = sum(item["matched_pair_count"] for item in results)
        total_above = sum(item["pairs_meeting_rate_ratio_threshold"] for item in results)
        channel_summary[channel_name] = {
            "compositions_with_matched_pairs": sum(item["matched_pair_count"] > 0 for item in results),
            "compositions_meeting_rate_ratio_threshold": sum(
                item["pairs_meeting_rate_ratio_threshold"] > 0 for item in results
            ),
            "pooled_matched_pair_count": total_matched,
            "pooled_pairs_meeting_rate_ratio_threshold": total_above,
            "pooled_fraction_meeting_rate_ratio_threshold": (
                total_above / total_matched if total_matched else None
            ),
        }

    rule = contract["joint_confirmation_rule"]
    source_pass = (
        channel_summary["mean_ekra_to_full_rate"]["compositions_meeting_rate_ratio_threshold"]
        >= rule["mean_ekra_to_full_rate_minimum_compositions"]
    )
    sensitivity_pass = (
        channel_summary["nonnegative_directional_barrier"]["compositions_meeting_rate_ratio_threshold"]
        >= rule["nonnegative_directional_barrier_minimum_compositions"]
    )

    hashed_inputs = [
        "inputs/prim.json",
        "inputs/fitting_results.pkl",
        "inputs/fitting_results_site.pkl",
        "inputs/events_888_site.pkl",
        "inputs/lce.pkl",
        "inputs/lce_site.pkl",
        "kmc/mc_results.h5",
        "lib/kmc.py",
        "lib/model.py",
    ]
    payload = {
        "schema_version": "arc-nasicon-heldout-result-0.1",
        "contract_path": str(args.contract),
        "contract_sha256": sha256(args.contract),
        "upstream_commit": commit,
        "input_sha256": {relative: sha256(upstream / relative) for relative in hashed_inputs},
        "package_versions": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "pandas", "tables", "pymatgen", "numba")
        },
        "composition_results": composition_results,
        "channel_summary": channel_summary,
        "confirmation": {
            "mean_ekra_to_full_rate_pass": source_pass,
            "nonnegative_directional_barrier_pass": sensitivity_pass,
            "joint_rule_pass": source_pass and sensitivity_pass,
        },
        "runtime_seconds": time.perf_counter() - started,
        "interpretation_boundary": contract["interpretation_boundary"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
