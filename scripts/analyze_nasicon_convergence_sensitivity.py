#!/usr/bin/env python3
"""Retrospective convergence sensitivity for completed NASICON production shards.

This diagnostic cannot replace the frozen v0.1 verdict. It evaluates how the
same drift rule behaves at earlier endpoints and under alternative window sizes
to inform a prospectively versioned follow-up.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path


METRIC_THRESHOLDS = {
    "conductivity": 0.15,
    "D_J": 0.15,
    "D_tracer": 0.15,
    "H_R": 0.20,
}


def metric_diagnostic(values: list[float], endpoint: int, window: int, threshold: float) -> dict:
    if endpoint > len(values) or endpoint < 2 * window:
        raise ValueError("endpoint must contain two complete, non-overlapping windows")
    preceding = values[endpoint - 2 * window : endpoint - window]
    late = values[endpoint - window : endpoint]
    preceding_median = statistics.median(preceding)
    late_median = statistics.median(late)
    drift = abs(late_median - preceding_median) / max(abs(late_median), 1e-30)
    finite = all(math.isfinite(value) for value in preceding + late)
    return {
        "preceding_window_median": preceding_median,
        "late_window_median": late_median,
        "relative_median_drift": drift,
        "threshold": threshold,
        "gate_pass": finite and drift <= threshold,
    }


def evaluate(payload: dict, endpoint: int, window: int) -> dict:
    metrics = {
        metric: metric_diagnostic(payload["curves"][metric], endpoint, window, threshold)
        for metric, threshold in METRIC_THRESHOLDS.items()
    }
    return {
        "seed": payload["seed"],
        "structure_index": payload["structure_index"],
        "endpoint_pass": endpoint,
        "window_passes": window,
        "metrics": metrics,
        "run_gate_pass": all(item["gate_pass"] for item in metrics.values()),
    }


def analyze(shard_paths: list[Path]) -> dict:
    shards = [json.loads(path.read_text()) for path in sorted(shard_paths)]
    if len(shards) != 6 or any(item.get("status") != "complete" for item in shards):
        raise ValueError("expected six complete production shards")

    endpoint_scan = []
    for endpoint in range(1000, 3001, 250):
        rows = [evaluate(item, endpoint, 500) for item in shards]
        endpoint_scan.append(
            {
                "endpoint_pass": endpoint,
                "window_passes": 500,
                "run_gate_pass_count": sum(row["run_gate_pass"] for row in rows),
                "study_gate_pass": all(row["run_gate_pass"] for row in rows),
                "runs": rows,
            }
        )

    window_scan = []
    for window in (250, 500, 750, 1000):
        rows = [evaluate(item, 3000, window) for item in shards]
        window_scan.append(
            {
                "endpoint_pass": 3000,
                "window_passes": window,
                "run_gate_pass_count": sum(row["run_gate_pass"] for row in rows),
                "study_gate_pass": all(row["run_gate_pass"] for row in rows),
                "runs": rows,
            }
        )

    return {
        "schema_version": "arc-nasicon-convergence-sensitivity-0.1",
        "analysis_status": "retrospective_design_diagnostic_only",
        "frozen_v0_1_verdict_unchanged": True,
        "endpoint_scan": endpoint_scan,
        "window_scan_at_3000": window_scan,
        "interpretation_boundary": (
            "These repeated looks are not confirmatory tests and cannot replace the frozen "
            "3,000-pass, 500-pass-window verdict. They are used only to design a new, "
            "prospectively versioned convergence protocol."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shards", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.shards)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
