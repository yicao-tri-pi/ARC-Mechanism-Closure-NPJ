#!/usr/bin/env python3
"""Recompute initial NASICON barrier and hopping-rate summaries.

This bounded reproduction uses the pinned public NASICON kMC implementation
without advancing the stochastic simulation.  It scans all 50 supplied
configurations at one composition and transparently reports the exploratory
pair with the largest aggregate-rate ratio among pairs whose mean barriers are
within the declared tolerance.  This is an audit of the initial event
catalogue, not a conductivity calculation or a preregistered confirmation.
"""

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

import numpy as np
import pandas as pd


UPSTREAM_COMMIT = "69eb10b7c52ddd85e39ebeb882b2e4ea617e7770"
COMPOSITION_PARAMETER = 0.2
EXPECTED_EXPLORATORY_PAIR = (48, 49)
TEMPERATURE_K = 573
ATTEMPT_FREQUENCY_HZ = 0.5e13
SUPERCELL_SHAPE = (8, 8, 8)
MEAN_BARRIER_TOLERANCE_MEV = 0.25


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def summarize(events: list[object], structure_index: int) -> dict:
    active = [event for event in events if event.probability > 0]
    barriers = np.asarray([event.barrier for event in active], dtype=float)
    rates = np.asarray([event.probability for event in active], dtype=float)
    return {
        "structure_index": structure_index,
        "active_directed_event_count": int(len(active)),
        "mean_active_barrier_mev": float(np.mean(barriers)),
        "median_active_barrier_mev": float(np.median(barriers)),
        "standard_deviation_active_barrier_mev": float(np.std(barriers)),
        "minimum_active_barrier_mev": float(np.min(barriers)),
        "maximum_active_barrier_mev": float(np.max(barriers)),
        "aggregate_initial_hopping_rate_hz": float(np.sum(rates)),
        "median_initial_hopping_rate_hz": float(np.median(rates)),
        "maximum_initial_hopping_rate_hz": float(np.max(rates)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    upstream = args.upstream_root.resolve()
    commit = git_commit(upstream)
    if commit != UPSTREAM_COMMIT:
        raise RuntimeError(f"expected upstream {UPSTREAM_COMMIT}, found {commit}")

    inputs = upstream / "inputs"
    kmc_root = upstream / "kmc"
    sys.path.insert(0, str(upstream / "lib"))
    from kmc import KMC  # noqa: PLC0415

    mc_results_path = kmc_root / "mc_results.h5"
    frame = pd.read_hdf(mc_results_path)
    selected = frame[np.isclose(frame["comp"], COMPOSITION_PARAMETER)].sort_values(
        "structure_index"
    )
    if selected["structure_index"].tolist() != list(range(1, 51)):
        raise RuntimeError("expected exactly the 50 declared structure indices")

    started = time.perf_counter()
    all_summaries = []
    for row in selected.itertuples(index=False):
        model = KMC()
        # Upstream initialization prints thousands of occupation entries.  The
        # complete numerical summaries are retained below instead.
        with contextlib.redirect_stdout(io.StringIO()):
            events = model.initialization(
                row.occ,
                str(inputs / "prim.json"),
                str(inputs / "fitting_results.pkl"),
                str(inputs / "fitting_results_site.pkl"),
                str(inputs / "events_888_site.pkl"),
                SUPERCELL_SHAPE,
                ATTEMPT_FREQUENCY_HZ,
                TEMPERATURE_K,
                lce_fname=str(inputs / "lce.pkl"),
                lce_site_fname=str(inputs / "lce_site.pkl"),
            )
        all_summaries.append(summarize(events, int(row.structure_index)))

    candidate_pairs = []
    for first_index, first_summary in enumerate(all_summaries):
        for second_summary in all_summaries[first_index + 1 :]:
            mean_difference = abs(
                first_summary["mean_active_barrier_mev"]
                - second_summary["mean_active_barrier_mev"]
            )
            if mean_difference > MEAN_BARRIER_TOLERANCE_MEV:
                continue
            first_rate = first_summary["aggregate_initial_hopping_rate_hz"]
            second_rate = second_summary["aggregate_initial_hopping_rate_hz"]
            rate_ratio = max(first_rate, second_rate) / min(first_rate, second_rate)
            candidate_pairs.append((rate_ratio, first_summary, second_summary))
    if not candidate_pairs:
        raise RuntimeError("no pair falls within the declared mean-barrier tolerance")
    rate_ratio, first, second = max(candidate_pairs, key=lambda item: item[0])
    selected_pair = (first["structure_index"], second["structure_index"])
    if selected_pair != EXPECTED_EXPLORATORY_PAIR:
        raise RuntimeError(
            f"expected exploratory pair {EXPECTED_EXPLORATORY_PAIR}, found {selected_pair}"
        )

    mean_difference = abs(
        first["mean_active_barrier_mev"] - second["mean_active_barrier_mev"]
    )
    first_rate = first["aggregate_initial_hopping_rate_hz"]
    second_rate = second["aggregate_initial_hopping_rate_hz"]

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
        "schema_version": "arc-external-reproduction-1.0",
        "upstream_repository": "https://github.com/caneparesearch/NASICON_KMC_paper_data",
        "upstream_commit": commit,
        "paper_doi": "10.1038/s41467-022-32190-7",
        "scope": (
            "Deterministic initialization of the public kMC event catalogue for all "
            "50 supplied 8x8x8 configurations at one composition and temperature, "
            "followed by an explicitly exploratory pair scan; no stochastic trajectory "
            "or macroscopic conductivity is computed."
        ),
        "inputs": {
            "composition_parameter_comp": COMPOSITION_PARAMETER,
            "paper_formula_x": 3 - 3 * COMPOSITION_PARAMETER,
            "formula_na_content": 1 + (3 - 3 * COMPOSITION_PARAMETER),
            "structure_indices": list(range(1, 51)),
            "temperature_k": TEMPERATURE_K,
            "attempt_frequency_hz": ATTEMPT_FREQUENCY_HZ,
            "supercell_shape": list(SUPERCELL_SHAPE),
            "sha256": {
                relative: sha256(upstream / relative) for relative in hashed_inputs
            },
        },
        "package_versions": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "pandas", "tables", "pymatgen", "numba")
        },
        "configuration_scan": {
            "configuration_count": len(all_summaries),
            "all_pair_count": len(all_summaries) * (len(all_summaries) - 1) // 2,
            "pairs_within_declared_mean_barrier_tolerance": len(candidate_pairs),
            "selection_status": "exploratory_post_hoc",
            "selection_rule": (
                "largest aggregate initial-rate ratio among all configuration "
                "pairs within 0.25 meV in mean active-event barrier"
            ),
            "mean_barrier_range_mev": [
                min(item["mean_active_barrier_mev"] for item in all_summaries),
                max(item["mean_active_barrier_mev"] for item in all_summaries),
            ],
            "aggregate_initial_rate_range_hz": [
                min(item["aggregate_initial_hopping_rate_hz"] for item in all_summaries),
                max(item["aggregate_initial_hopping_rate_hz"] for item in all_summaries),
            ],
        },
        "selected_configuration_summaries": [first, second],
        "comparison": {
            "absolute_mean_barrier_difference_mev": mean_difference,
            "declared_observational_tolerance_mev": MEAN_BARRIER_TOLERANCE_MEV,
            "mean_barriers_equivalent_at_declared_tolerance": (
                mean_difference <= MEAN_BARRIER_TOLERANCE_MEV
            ),
            "aggregate_initial_rate_ratio": rate_ratio,
            "aggregate_initial_rate_relative_difference": (
                abs(first_rate - second_rate) / min(first_rate, second_rate)
            ),
        },
        "runtime_seconds": time.perf_counter() - started,
        "interpretation_boundary": (
            "Near-equality of a mean barrier does not identify the aggregate initial "
            "event rate because event count and the full barrier distribution enter "
            "the Arrhenius sum. The displayed pair was selected exploratorily after "
            "scanning all 50 configurations and requires confirmation on held-out "
            "configurations. This result alone neither estimates conductivity nor tests "
            "the paper's full kMC and experimental conclusions."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
