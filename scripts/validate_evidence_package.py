#!/usr/bin/env python3
"""Validate immutable bindings without rerunning expensive experiments."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []

    manifest_path = ROOT / "provenance/migration_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for item in manifest["files"]:
        path = ROOT / item["path"]
        require(path.is_file(), f"missing manifest file: {item['path']}", failures)
        if path.is_file():
            require(path.stat().st_size == item["bytes"], f"size drift: {item['path']}", failures)
            require(sha256(path) == item["sha256"], f"hash drift: {item['path']}", failures)

    for receipt_name, source_name in [
        ("nasicon_barrier_lean_receipt.json", "NasiconBarrierNonidentifiability.lean"),
        ("impedance_parity_lean_receipt.json", "ImpedanceParityNonidentifiability.lean"),
        ("polymer_mechanism_lean_receipt.json", "PolymerMechanismAudit.lean"),
    ]:
        receipt = json.loads((ROOT / "results" / receipt_name).read_text())
        source = ROOT / "formal" / source_name
        require(receipt.get("kernel_checked") is True, f"receipt not kernel checked: {receipt_name}", failures)
        require(sha256(source) == receipt["source_sha256"], f"Lean source drift: {source_name}", failures)

    nasicon = json.loads((ROOT / "results/nasicon_initial_rate_reproduction_v0.1.json").read_text())
    for relative, expected in nasicon["inputs"]["sha256"].items():
        path = ROOT / "third_party/NASICON_KMC_paper_data" / relative
        require(path.is_file(), f"missing NASICON input: {relative}", failures)
        if path.is_file():
            require(sha256(path) == expected, f"NASICON input drift: {relative}", failures)

    nleis = json.loads((ROOT / "results/nleis_public_data_audit_v0.1.json").read_text())
    for relative, expected in nleis["file_sha256"].items():
        path = ROOT / "third_party/2nd-NLEIS-manuscripts" / relative
        require(path.is_file(), f"missing NLEIS input: {relative}", failures)
        if path.is_file():
            require(sha256(path) == expected, f"NLEIS input drift: {relative}", failures)

    if failures:
        print("Evidence validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Evidence validation passed: {manifest['file_count']} inventoried files; Lean and raw-data bindings intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
