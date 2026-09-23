#!/usr/bin/env python3
"""Run a bounded, seeded end-to-end NASICON kMC smoke test."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import math
import random
import subprocess
import sys
import time
from pathlib import Path

EXPECTED_UPSTREAM_COMMIT = "69eb10b7c52ddd85e39ebeb882b2e4ea617e7770"
ATTEMPT_FREQUENCY_HZ = 0.5e13
SUPERCELL_SHAPE = (8, 8, 8)


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


def event_summary(events: list[object]) -> dict:
    active = [event for event in events if event.probability > 0]
    barriers = np.asarray([event.barrier for event in active], dtype=float)
    ekra = np.asarray([event.ekra for event in active], dtype=float)
    rates = np.asarray([event.probability for event in active], dtype=float)
    quantiles = [0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0]
    return {
        "active_directed_event_count": len(active),
        "directional_barrier_mev": {
            "mean": float(np.mean(barriers)),
            "standard_deviation": float(np.std(barriers)),
            "quantiles": {
                str(q): float(value)
                for q, value in zip(quantiles, np.quantile(barriers, quantiles))
            },
            "negative_count": int(np.sum(barriers < 0)),
        },
        "ekra_mev": {
            "mean": float(np.mean(ekra)),
            "standard_deviation": float(np.std(ekra)),
            "quantiles": {
                str(q): float(value)
                for q, value in zip(quantiles, np.quantile(ekra, quantiles))
            },
        },
        "rate_hz": {
            "sum": float(np.sum(rates)),
            "mean": float(np.mean(rates)),
            "quantiles": {
                str(q): float(value)
                for q, value in zip(quantiles, np.quantile(rates, quantiles))
            },
        },
    }


def active_graph_summary(events: list[object]) -> dict:
    adjacency: dict[int, set[int]] = {}
    directed_edges = 0
    for event in events:
        if event.probability <= 0:
            continue
        left = int(event.na1_index)
        right = int(event.na2_index)
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
        directed_edges += 1

    unseen = set(adjacency)
    component_sizes = []
    while unseen:
        start = unseen.pop()
        stack = [start]
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            neighbors = adjacency[node] & unseen
            unseen.difference_update(neighbors)
            stack.extend(neighbors)
        component_sizes.append(size)
    component_sizes.sort(reverse=True)
    undirected_edges = sum(len(neighbors) for neighbors in adjacency.values()) // 2
    return {
        "active_site_count": len(adjacency),
        "active_directed_event_count": directed_edges,
        "active_undirected_edge_count": undirected_edges,
        "connected_component_count": len(component_sizes),
        "largest_component_site_count": component_sizes[0] if component_sizes else 0,
        "largest_component_site_fraction": (
            component_sizes[0] / len(adjacency) if adjacency else 0.0
        ),
        "interpretation": (
            "instantaneous occupied-vacant event graph only; periodic wrapping and "
            "long-time dynamic percolation are not certified"
        ),
    }


def finite_metrics(summary: dict) -> bool:
    keys = ("time", "D_J", "D_tracer", "conductivity", "f", "H_R", "msd")
    return all(math.isfinite(float(summary[key])) for key in keys)


def run_structure(
    *,
    KMC: type,
    Tracker: type,
    row: object,
    upstream: Path,
    composition: float,
    structure_index: int,
    temperature: int,
    seed: int,
    equilibration_passes: int,
    measurement_passes: int,
) -> dict:
    inputs = upstream / "inputs"
    started = time.perf_counter()
    random.seed(seed)
    np.random.seed(seed)
    model = KMC()
    with contextlib.redirect_stdout(io.StringIO()):
        events = model.initialization(
            row.occ,
            str(inputs / "prim.json"),
            str(inputs / "fitting_results.pkl"),
            str(inputs / "fitting_results_site.pkl"),
            str(inputs / "events_888_site.pkl"),
            SUPERCELL_SHAPE,
            ATTEMPT_FREQUENCY_HZ,
            temperature,
            lce_fname=str(inputs / "lce.pkl"),
            lce_site_fname=str(inputs / "lce_site.pkl"),
        )
        model.load_site_event_list(str(inputs / "event_kernal_888.csv"))

    initial_events = event_summary(events)
    initial_graph = active_graph_summary(events)
    model.v = ATTEMPT_FREQUENCY_HZ
    model.T = temperature
    pass_length = len([site for site in model.structure.species if "Na" in site.symbol])

    for _ in range(equilibration_passes):
        for _ in range(pass_length):
            event, _time_change = model.propose(events)
            model.update(event, events)

    with contextlib.redirect_stdout(io.StringIO()):
        tracker = Tracker(model.occ_global, model.structure, temperature, ATTEMPT_FREQUENCY_HZ)
    measurement_summaries = []
    for current_pass in range(measurement_passes):
        for _ in range(pass_length):
            event, time_change = model.propose(events)
            tracker.update(event, model.occ_global, time_change)
            model.update(event, events)
        with np.errstate(divide="ignore", invalid="ignore"):
            tracker.summary(current_pass, composition, structure_index)
        measurement_summaries.append(
            {
                key: float(tracker.results[key][-1])
                for key in (
                    "time",
                    "D_J",
                    "D_tracer",
                    "conductivity",
                    "f",
                    "H_R",
                    "msd",
                    "final_na_at_na1",
                    "average_na_at_na1",
                )
            }
        )

    final_events = event_summary(events)
    final_graph = active_graph_summary(events)
    runtime = time.perf_counter() - started
    final = measurement_summaries[-1]
    passed = (
        len(measurement_summaries) == measurement_passes
        and final["time"] > 0
        and finite_metrics(final)
        and initial_graph["active_site_count"] > 0
        and final_graph["active_site_count"] > 0
    )
    return {
        "structure_index": structure_index,
        "seed": seed,
        "pass_length_events": pass_length,
        "equilibration_passes": equilibration_passes,
        "measurement_passes": measurement_passes,
        "attempted_kmc_events": pass_length * (equilibration_passes + measurement_passes),
        "initial_event_summary": initial_events,
        "initial_active_graph": initial_graph,
        "measurement_summaries": measurement_summaries,
        "final_event_summary": final_events,
        "final_active_graph": final_graph,
        "runtime_seconds": runtime,
        "seconds_per_measurement_pass_including_amortized_setup": runtime / measurement_passes,
        "naive_runtime_projection_for_3000_measurement_passes_hours": (
            runtime / measurement_passes * 3000 / 3600
        ),
        "smoke_gate_pass": passed,
    }


def main() -> None:
    global np, pd
    import numpy as np  # noqa: PLC0415
    import pandas as pd  # noqa: PLC0415

    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--composition", type=float, default=0.2)
    parser.add_argument("--structure-indices", type=int, nargs="+", default=[48, 49])
    parser.add_argument("--temperature", type=int, default=573)
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--equilibration-passes", type=int, default=1)
    parser.add_argument("--measurement-passes", type=int, default=3)
    args = parser.parse_args()

    upstream = args.upstream_root.resolve()
    commit = git_commit(upstream)
    if commit != EXPECTED_UPSTREAM_COMMIT:
        raise RuntimeError(f"expected upstream {EXPECTED_UPSTREAM_COMMIT}, found {commit}")
    sys.path.insert(0, str(upstream / "lib"))
    from kmc import KMC, Tracker  # noqa: PLC0415

    hdf = upstream / "kmc/mc_results.h5"
    frame = pd.read_hdf(hdf)
    selected = frame[
        np.isclose(frame["comp"], args.composition)
        & frame["structure_index"].isin(args.structure_indices)
    ].sort_values("structure_index")
    if selected["structure_index"].tolist() != sorted(args.structure_indices):
        raise RuntimeError("declared structure rows are not uniquely present")

    required_inputs = [
        "inputs/prim.json",
        "inputs/fitting_results.pkl",
        "inputs/fitting_results_site.pkl",
        "inputs/events_888_site.pkl",
        "inputs/event_kernal_888.csv",
        "inputs/lce.pkl",
        "inputs/lce_site.pkl",
        "kmc/mc_results.h5",
        "lib/kmc.py",
        "lib/model.py",
    ]
    results = []
    for row in selected.itertuples(index=False):
        results.append(
            run_structure(
                KMC=KMC,
                Tracker=Tracker,
                row=row,
                upstream=upstream,
                composition=args.composition,
                structure_index=int(row.structure_index),
                temperature=args.temperature,
                seed=args.seed,
                equilibration_passes=args.equilibration_passes,
                measurement_passes=args.measurement_passes,
            )
        )

    payload = {
        "schema_version": "arc-nasicon-kmc-smoke-result-0.1",
        "upstream_commit": commit,
        "input_sha256": {
            relative: sha256(upstream / relative) for relative in required_inputs
        },
        "configuration": {
            "composition_parameter_comp": args.composition,
            "paper_formula_x": 3 - 3 * args.composition,
            "formula_na_content": 1 + (3 - 3 * args.composition),
            "structure_indices": sorted(args.structure_indices),
            "temperature_k": args.temperature,
            "attempt_frequency_hz": ATTEMPT_FREQUENCY_HZ,
            "supercell_shape": list(SUPERCELL_SHAPE),
            "seed": args.seed,
            "equilibration_passes": args.equilibration_passes,
            "measurement_passes": args.measurement_passes,
        },
        "package_versions": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "pandas", "tables", "pymatgen", "numba")
        },
        "structure_results": results,
        "all_smoke_gates_pass": all(item["smoke_gate_pass"] for item in results),
        "interpretation_boundary": (
            "This verifies code-path and artifact completeness only. Three measurement "
            "passes are not a convergence study; conductivity, Haven ratio, and graph "
            "summaries must not be interpreted as scientific estimates."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if not payload["all_smoke_gates_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
