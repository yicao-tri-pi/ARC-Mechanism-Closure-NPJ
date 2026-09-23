#!/usr/bin/env python3
"""Audit the public paired EIS/2nd-NLEIS corpus without fitting a model."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

SOCS = (10, 30, 40, 50, 60)
STATES = ("f", "a")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
    ).stdout.strip()


def float_rows(path: Path) -> list[list[float]]:
    rows = [[float(value) for value in line.split()] for line in path.read_text().splitlines() if line.strip()]
    if not rows or len({len(row) for row in rows}) != 1:
        raise ValueError(f"{path} is not a rectangular numeric matrix")
    return rows


def complex_matrix(path: Path) -> list[list[complex]]:
    raw = float_rows(path)
    if len(raw[0]) % 2:
        raise ValueError(f"{path} is not a rectangular real/imaginary matrix")
    return [
        [complex(row[index], row[index + 1]) for index in range(0, len(row), 2)]
        for row in raw
    ]


def audit(root: Path, expected_commit: str) -> dict:
    if git_commit(root) != expected_commit:
        raise RuntimeError("NLEIS source checkout does not match the pinned commit")
    data_dir = root / "Part II" / "data"
    conditions = []
    file_hashes = {}
    all_finite = True
    for soc in SOCS:
        for state in STATES:
            label = f"{soc}{state}"
            paths = {
                "frequency": data_dir / f"freq_{label}.txt",
                "linear_eis": data_dir / f"Z1s_{label}.txt",
                "second_harmonic_nleis": data_dir / f"Z2s_{label}.txt",
            }
            for role, path in paths.items():
                file_hashes[str(path.relative_to(root))] = sha256(path)
            frequency_rows = float_rows(paths["frequency"])
            if any(len(row) != 1 for row in frequency_rows):
                raise ValueError(f"frequency file for {label} must contain one column")
            frequency = [row[0] for row in frequency_rows]
            z1 = complex_matrix(paths["linear_eis"])
            z2 = complex_matrix(paths["second_harmonic_nleis"])
            if len(z1) != len(z2) or any(len(a) != len(b) for a, b in zip(z1, z2)):
                raise ValueError(f"paired data shape mismatch for {label}")
            if any(len(row) != len(frequency) for row in z1 + z2):
                raise ValueError(f"paired data shape mismatch for {label}")
            finite = (
                all(math.isfinite(value) for value in frequency)
                and all(math.isfinite(value.real) and math.isfinite(value.imag) for row in z1 for value in row)
                and all(math.isfinite(value.real) and math.isfinite(value.imag) for row in z2 for value in row)
            )
            all_finite = all_finite and finite
            z2_rms = [math.sqrt(sum(abs(value) ** 2 for value in row) / len(row)) for row in z2]
            conditions.append(
                {
                    "soc_percent": soc,
                    "cell_state": "fresh" if state == "f" else "aged_100_cycles_at_2C",
                    "replicate_count": len(z1),
                    "frequency_count": len(frequency),
                    "frequency_min_hz": min(frequency),
                    "frequency_max_hz": max(frequency),
                    "all_values_finite": finite,
                    "second_harmonic_rms_by_replicate": z2_rms,
                    "all_second_harmonic_rms_positive": all(value > 0 for value in z2_rms),
                }
            )
    return {
        "schema_version": "arc-nleis-public-data-audit-0.1",
        "upstream_repository": "https://github.com/yuefan98/2nd-NLEIS-manuscripts.git",
        "upstream_commit": expected_commit,
        "license": "MIT",
        "condition_count": len(conditions),
        "paired_spectrum_count": sum(item["replicate_count"] for item in conditions),
        "all_values_finite": all_finite,
        "all_second_harmonic_rms_positive": all(
            item["all_second_harmonic_rms_positive"] for item in conditions
        ),
        "conditions": conditions,
        "file_sha256": file_hashes,
        "interpretation_boundary": (
            "This audit establishes public paired-data completeness and nonzero recorded "
            "second-harmonic signals. It does not reproduce model fits, identify electrode "
            "parameters, validate the physical model, or establish experimental causality."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream-root", type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.upstream_root.resolve(), args.expected_commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
