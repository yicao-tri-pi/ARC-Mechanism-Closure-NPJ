#!/usr/bin/env python3
"""Execute the contract-frozen short NASICON kMC feasibility pilot."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import random
import subprocess
import sys
import time
import warnings
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


def finite_final(record: dict) -> bool:
    keys = ("time", "D_J", "D_tracer", "conductivity", "msd")
    return record["time"] > 0 and all(math.isfinite(record[key]) for key in keys)


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
    from kmc import KMC, Tracker  # noqa: PLC0415

    inputs = upstream / "inputs"
    frame = pd.read_hdf(upstream / "kmc/mc_results.h5")
    provenance = contract["pair_provenance"]
    simulation = contract["simulation"]
    selected = frame[
        np.isclose(frame["comp"], provenance["composition_parameter_comp"])
        & frame["structure_index"].isin(provenance["structure_indices"])
    ].sort_values("structure_index")
    if selected["structure_index"].tolist() != provenance["structure_indices"]:
        raise RuntimeError("declared pilot pair is not uniquely present")

    runs = []
    started = time.perf_counter()
    for seed in simulation["paired_random_seeds"]:
        for row in selected.itertuples(index=False):
            random.seed(seed)
            np.random.seed(seed)
            run_started = time.perf_counter()
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

                active = [event for event in events if event.probability > 0]
                directional = np.asarray([event.barrier for event in active], dtype=float)
                rates = np.asarray([event.probability for event in active], dtype=float)
                nonnegative = directional >= 0
                initial_summary = {
                    "mean_nonnegative_barrier_mev": float(np.mean(directional[nonnegative])),
                    "nonnegative_aggregate_rate_hz": float(np.sum(rates[nonnegative])),
                    "negative_directional_event_count": int(np.count_nonzero(~nonnegative)),
                }

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
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    for current_pass in range(simulation["measurement_passes"]):
                        for _ in range(pass_length):
                            event, time_change = model.propose(events)
                            tracker.update(event, model.occ_global, time_change)
                            model.update(event, events)
                        tracker.summary(
                            current_pass,
                            provenance["composition_parameter_comp"],
                            int(row.structure_index),
                        )

            curves = {
                key: [float(value) for value in tracker.results[key]]
                for key in ("time", "D_J", "D_tracer", "conductivity", "H_R", "f", "msd")
            }
            final = {key: values[-1] for key, values in curves.items()}
            run = {
                "seed": seed,
                "structure_index": int(row.structure_index),
                "initial_summary": initial_summary,
                "pass_length": pass_length,
                "curves": curves,
                "final": final,
                "final_finite": finite_final(final),
                "runtime_seconds": time.perf_counter() - run_started,
            }
            runs.append(run)
            print(
                f"completed seed={seed} structure={row.structure_index} "
                f"conductivity={final['conductivity']:.6g} mS/cm",
                flush=True,
            )

    rates_by_structure = {
        index: next(
            run["initial_summary"]["nonnegative_aggregate_rate_hz"]
            for run in runs
            if run["structure_index"] == index
        )
        for index in provenance["structure_indices"]
    }
    high_index = max(rates_by_structure, key=rates_by_structure.get)
    low_index = min(rates_by_structure, key=rates_by_structure.get)
    paired = []
    for seed in simulation["paired_random_seeds"]:
        by_index = {
            run["structure_index"]: run for run in runs if run["seed"] == seed
        }
        high = by_index[high_index]["final"]["conductivity"]
        low = by_index[low_index]["final"]["conductivity"]
        paired.append(
            {
                "seed": seed,
                "high_initial_rate_structure": high_index,
                "low_initial_rate_structure": low_index,
                "high_final_conductivity_mS_cm": high,
                "low_final_conductivity_mS_cm": low,
                "conductivity_ratio_high_over_low": high / low if low > 0 else None,
            }
        )

    ratios = [item["conductivity_ratio_high_over_low"] for item in paired]
    result = {
        "schema_version": "arc-nasicon-short-kmc-pilot-result-0.1",
        "contract_path": str(args.contract),
        "contract_sha256": sha256(args.contract),
        "upstream_commit": commit,
        "runs": runs,
        "paired_summary": paired,
        "aggregate": {
            "requested_run_count": len(simulation["paired_random_seeds"]) * 2,
            "completed_run_count": len(runs),
            "all_final_metrics_finite": all(run["final_finite"] for run in runs),
            "high_initial_rate_structure": high_index,
            "low_initial_rate_structure": low_index,
            "median_conductivity_ratio_high_over_low": float(np.median(ratios)),
            "conductivity_ratio_range_high_over_low": [float(np.min(ratios)), float(np.max(ratios))],
            "direction_consistent_across_seeds": all(ratio > 1 for ratio in ratios),
            "feasibility_rule_pass": (
                len(runs) == len(simulation["paired_random_seeds"]) * 2
                and all(run["final_finite"] for run in runs)
            ),
        },
        "total_runtime_seconds": time.perf_counter() - started,
        "interpretation_boundary": contract["interpretation_boundary"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
