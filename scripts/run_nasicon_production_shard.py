#!/usr/bin/env python3
"""Run one contract-frozen NASICON production kMC shard."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import os
import random
import statistics
import subprocess
import sys
import time
import warnings
from pathlib import Path


TRACKED_METRICS = ("time", "D_J", "D_tracer", "conductivity", "H_R", "f", "msd")


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


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def relative_median_drift(values: list[float], window_passes: int) -> dict:
    if len(values) < 2 * window_passes:
        raise ValueError("curve is too short for the frozen convergence windows")
    preceding = values[-2 * window_passes : -window_passes]
    late = values[-window_passes:]
    finite = all(math.isfinite(value) for value in preceding + late)
    preceding_median = float(statistics.median(preceding)) if finite else None
    late_median = float(statistics.median(late)) if finite else None
    drift = (
        abs(late_median - preceding_median) / max(abs(late_median), 1e-30)
        if finite
        else None
    )
    return {
        "preceding_window_median": preceding_median,
        "late_window_median": late_median,
        "relative_median_drift": drift,
        "all_values_finite": finite,
    }


def main() -> None:
    import numpy as np
    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--structure-index", type=int, required=True)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text())
    simulation = contract["simulation"]
    provenance = contract["pair_provenance"]
    if args.seed not in simulation["paired_random_seeds"]:
        raise ValueError("seed is outside the frozen contract")
    if args.structure_index not in provenance["structure_indices"]:
        raise ValueError("structure is outside the frozen contract")

    upstream = args.upstream_root.resolve()
    commit = git_commit(upstream)
    if commit != contract["upstream_commit"]:
        raise RuntimeError(f"expected upstream {contract['upstream_commit']}, found {commit}")

    sys.path.insert(0, str(upstream / "lib"))
    from kmc import KMC, Tracker  # noqa: PLC0415

    frame = pd.read_hdf(upstream / "kmc/mc_results.h5")
    selected = frame[
        np.isclose(frame["comp"], provenance["composition_parameter_comp"])
        & (frame["structure_index"] == args.structure_index)
    ]
    if len(selected) != 1:
        raise RuntimeError("declared production configuration is not uniquely present")
    row = next(selected.itertuples(index=False))

    random.seed(args.seed)
    np.random.seed(args.seed)
    started = time.perf_counter()
    inputs = upstream / "inputs"
    with contextlib.redirect_stdout(io.StringIO()):
        model = KMC()
        events = model.initialization(
            row.occ,
            str(inputs / "prim.json"),
            str(inputs / "fitting_results.pkl"),
            str(inputs / "fitting_results_site.pkl"),
            str(inputs / "events_888_site.pkl"),
            tuple(simulation["supercell_shape"]),
            simulation["attempt_frequency_hz"],
            simulation["temperature_k"],
            lce_fname=str(inputs / "lce.pkl"),
            lce_site_fname=str(inputs / "lce_site.pkl"),
        )
        model.load_site_event_list(str(inputs / "event_kernal_888.csv"))
        model.v = simulation["attempt_frequency_hz"]
        model.T = simulation["temperature_k"]
        pass_length = len([site for site in model.structure.species if "Na" in site.symbol])
        for _ in range(simulation["equilibration_passes"]):
            for _ in range(pass_length):
                event, _ = model.propose(events)
                model.update(event, events)
        tracker = Tracker(
            model.occ_global,
            model.structure,
            simulation["temperature_k"],
            simulation["attempt_frequency_hz"],
        )

    curves = {key: [] for key in TRACKED_METRICS}
    checkpoint_every = simulation["checkpoint_every_passes"]
    for current_pass in range(simulation["measurement_passes"]):
        for _ in range(pass_length):
            event, time_change = model.propose(events)
            tracker.update(event, model.occ_global, time_change)
            model.update(event, events)
        with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            tracker.summary(
                current_pass,
                provenance["composition_parameter_comp"],
                args.structure_index,
            )
        for key in TRACKED_METRICS:
            curves[key].append(float(tracker.results[key][-1]))

        completed = current_pass + 1
        if completed % checkpoint_every == 0 or completed == simulation["measurement_passes"]:
            atomic_json(
                args.output,
                {
                    "schema_version": "arc-nasicon-production-kmc-shard-0.1",
                    "status": "running" if completed < simulation["measurement_passes"] else "complete",
                    "contract_path": str(args.contract),
                    "contract_sha256": sha256(args.contract),
                    "upstream_commit": commit,
                    "seed": args.seed,
                    "structure_index": args.structure_index,
                    "pass_length": pass_length,
                    "completed_measurement_passes": completed,
                    "runtime_seconds": time.perf_counter() - started,
                    "curves": curves,
                },
            )
            print(
                f"seed={args.seed} structure={args.structure_index} passes={completed}",
                flush=True,
            )

    window = contract["primary_endpoint"]["window_passes"]
    diagnostics = {}
    passed = True
    for metric, rule in contract["convergence_gate"]["metrics"].items():
        diagnostic = relative_median_drift(curves[metric], window)
        diagnostic["threshold"] = rule["max_relative_median_drift"]
        diagnostic["gate_pass"] = bool(
            diagnostic["all_values_finite"]
            and diagnostic["relative_median_drift"] <= diagnostic["threshold"]
        )
        diagnostics[metric] = diagnostic
        passed = passed and diagnostic["gate_pass"]

    payload = json.loads(args.output.read_text())
    payload["convergence_diagnostics"] = diagnostics
    payload["run_convergence_gate_pass"] = passed
    payload["primary_endpoint"] = diagnostics["conductivity"]["late_window_median"]
    diagnostic_windows = contract["convergence_gate"].get(
        "diagnostic_only_window_passes", []
    )
    payload["diagnostic_only_convergence"] = {
        str(diagnostic_window): {
            metric: {
                **relative_median_drift(curves[metric], diagnostic_window),
                "threshold": rule["max_relative_median_drift"],
            }
            for metric, rule in contract["convergence_gate"]["metrics"].items()
        }
        for diagnostic_window in diagnostic_windows
    }
    for by_metric in payload["diagnostic_only_convergence"].values():
        for item in by_metric.values():
            item["gate_pass"] = bool(
                item["all_values_finite"]
                and item["relative_median_drift"] <= item["threshold"]
            )
    atomic_json(args.output, payload)


if __name__ == "__main__":
    main()
