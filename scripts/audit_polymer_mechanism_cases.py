#!/usr/bin/env python3
"""Reproduce bounded source-data checks for the Wang/Han polymer audits.

The script deliberately does not infer a microscopic mechanism.  It inventories
the public artifacts, reproduces selected within-paper descriptive contrasts,
and records where only summaries or processed traces are public.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "evidence" / "npj_mechanism_audit" / "sources"
OUTPUT_ROOT = ROOT / "evidence" / "npj_mechanism_audit" / "derived"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_scientific_summary(value: object) -> tuple[float, float | None]:
    """Parse strings such as ``4.2 × 10-5 ± 5.0 × 10-6``."""
    if isinstance(value, (int, float)):
        return float(value), None
    text = str(value).strip().replace("−", "-")
    parts = [part.strip() for part in text.split("±")]

    def parse_one(part: str) -> float:
        match = re.fullmatch(r"([0-9.]+)\s*[×x]\s*10\s*\^?\s*([+-]?\d+)", part)
        if match:
            return float(match.group(1)) * 10 ** int(match.group(2))
        return float(part)

    return parse_one(parts[0]), parse_one(parts[1]) if len(parts) == 2 else None


def workbook_inventory(path: Path) -> list[dict[str, object]]:
    workbook = load_workbook(path, data_only=False, read_only=False)
    rows: list[dict[str, object]] = []
    for sheet in workbook.worksheets:
        populated = [
            cell
            for row in sheet.iter_rows()
            for cell in row
            if cell.value is not None and str(cell.value).strip()
        ]
        formula_count = sum(cell.data_type == "f" for cell in populated)
        rows.append(
            {
                "file": path.name,
                "sheet": sheet.title,
                "max_row": sheet.max_row,
                "max_column": sheet.max_column,
                "populated_cells": len(populated),
                "formula_cells": formula_count,
            }
        )
    return rows


def han_p8_p10() -> list[dict[str, object]]:
    path = SOURCE_ROOT / "han2023" / "han2023_source_data_fig4.xlsx"
    workbook = load_workbook(path, data_only=True, read_only=True)
    sheet = workbook["Fig 4f"]
    conductivity = {}
    for polymer, tg, sigma, *_ in sheet.iter_rows(min_row=3, values_only=True):
        if polymer in {"P8", "P9", "P10"}:
            mean, sd = parse_scientific_summary(sigma)
            conductivity[str(polymer)] = {"tg_c": float(tg), "sigma_s_cm": mean, "sigma_sd": sd}

    # SI Table S7 values, verified against the official supplementary PDF.
    lithium_molarity = {"P8": 1.18, "P9": 0.99, "P10": 0.75}
    side_chain_n = {"P8": 13, "P9": 17, "P10": 23}
    mn_nmr_kda = {"P8": 18.3, "P9": 21.1, "P10": 24.2}
    output = []
    for polymer in ("P8", "P9", "P10"):
        row = {
            "polymer": polymer,
            "sequence": "alternating",
            "peo_repeat_n": side_chain_n[polymer],
            "tg_c": conductivity[polymer]["tg_c"],
            "sigma_s_cm": conductivity[polymer]["sigma_s_cm"],
            "sigma_sd_s_cm": conductivity[polymer]["sigma_sd"],
            "li_concentration_mol_l": lithium_molarity[polymer],
            "mn_nmr_kda": mn_nmr_kda[polymer],
        }
        row["sigma_per_li_molarity"] = row["sigma_s_cm"] / row["li_concentration_mol_l"]
        output.append(row)
    return output


def wang_materials() -> list[dict[str, object]]:
    """Values transcribed from Wang 2012 Supporting Information, Table I."""
    return [
        {
            "sample_name": "Poly(Polyethylene Oxide Styrene)-b-Polystyrene",
            "abbreviation": "PPEOSt-b-PSt",
            "mw_kg_mol": "5.8/4.6",
            "pdi": 1.26,
            "liclo4_wt_pct": 0.3,
            "o_li_ratio": 540,
            "tg_k": 338,
            "fragility_m": 108,
            "epsilon1": 0.75,
            "epsilon1_sd": 0.01,
            "epsilon2": 0.78,
            "epsilon2_sd": 0.01,
        },
        {
            "sample_name": "Poly(Polyethylene Oxide Styrene)",
            "abbreviation": "PPEOSt",
            "mw_kg_mol": "5.8",
            "pdi": 1.22,
            "liclo4_wt_pct": 0.3,
            "o_li_ratio": 370,
            "tg_k": 265,
            "fragility_m": 101,
            "epsilon1": 0.72,
            "epsilon1_sd": 0.02,
            "epsilon2": 0.76,
            "epsilon2_sd": 0.02,
        },
        {
            "sample_name": "Poly(Norbornene Carboxylic Ethoxymethyl Ester)",
            "abbreviation": "PNBCEM",
            "mw_kg_mol": "6.6",
            "pdi": 1.17,
            "liclo4_wt_pct": 0.5,
            "o_li_ratio": 320,
            "tg_k": 314,
            "fragility_m": 93,
            "epsilon1": 0.41,
            "epsilon1_sd": 0.01,
            "epsilon2": 0.46,
            "epsilon2_sd": 0.01,
        },
        {
            "sample_name": "Poly(Polyethylene Oxide Caprolactone)",
            "abbreviation": "PPEOCL",
            "mw_kg_mol": "7.0",
            "pdi": 1.20,
            "liclo4_wt_pct": 1.0,
            "o_li_ratio": 220,
            "tg_k": 210,
            "fragility_m": 80,
            "epsilon1": 0.16,
            "epsilon1_sd": 0.03,
            "epsilon2": 0.19,
            "epsilon2_sd": 0.02,
        },
        {
            "sample_name": "Poly(Polyethylene Oxide Methacrylate)",
            "abbreviation": "PPEOMA",
            "mw_kg_mol": "4.1",
            "pdi": 1.21,
            "liclo4_wt_pct": 0.5,
            "o_li_ratio": 460,
            "tg_k": 240,
            "fragility_m": 45,
            "epsilon1": -0.01,
            "epsilon1_sd": 0.05,
            "epsilon2": 0.05,
            "epsilon2_sd": 0.05,
        },
    ]


def linear_r2(x: list[float], y: list[float]) -> float:
    """Unweighted ordinary-least-squares R^2 for a line with intercept."""
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    ss_x = sum((value - x_mean) ** 2 for value in x)
    ss_y = sum((value - y_mean) ** 2 for value in y)
    cross = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    return cross**2 / (ss_x * ss_y)


def source_data_classification() -> list[dict[str, str]]:
    return [
        {
            "claim_family": "Fig. 4 P1-P10 conductivity",
            "public_level": "summary mean and SD",
            "replicates": "three independent replicates stated in caption; individual values absent",
            "promotion_limit": "descriptive group contrast; no replicate-level reanalysis",
        },
        {
            "claim_family": "Fig. 3 Raman and solid-state 7Li NMR",
            "public_level": "processed spectral x-y traces",
            "replicates": "no replicate spectra or uncertainty",
            "promotion_limit": "spectral trend support; Raman CIP/AGG deconvolution not independently reproducible",
        },
        {
            "claim_family": "Fig. 3/5 MD density, RDF, residence time, MSD",
            "public_level": "processed profiles and summary values",
            "replicates": "no trajectories, seeds, or independent initializations",
            "promotion_limit": "reported simulation output support; no uncertainty or trajectory-level reproduction",
        },
        {
            "claim_family": "Fig. 5 PFG-NMR diffusion",
            "public_level": "single SI spectrum and reported coefficient for P8; no attenuation series in XLSX",
            "replicates": "no sequence-panel replicate data",
            "promotion_limit": "supports P8 mobility magnitude, not experimental ordering of all sequences",
        },
        {
            "claim_family": "Fig. 5 VTF conductivity",
            "public_level": "seven processed conductivity values per sequence",
            "replicates": "no uncertainty or replicate-level impedance spectra",
            "promotion_limit": "reported VTF trend; parameter uncertainty and equivalent-circuit sensitivity unavailable",
        },
        {
            "claim_family": "Fig. 6 cycling",
            "public_level": "processed single-cell time/cycle traces",
            "replicates": "no cell-to-cell repeats or uncertainty",
            "promotion_limit": "demonstration-cell evidence only",
        },
    ]


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    source_paths = sorted(path for path in SOURCE_ROOT.rglob("*") if path.is_file())
    manifest = [
        {"path": str(path.relative_to(ROOT)), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in source_paths
    ]

    inventory = []
    for path in sorted((SOURCE_ROOT / "han2023").glob("*.xlsx")):
        inventory.extend(workbook_inventory(path))

    p8_p10 = han_p8_p10()
    wang = wang_materials()
    fragility = [float(row["fragility_m"]) for row in wang]
    tg = [float(row["tg_k"]) for row in wang]
    epsilon1 = [float(row["epsilon1"]) for row in wang]
    epsilon2 = [float(row["epsilon2"]) for row in wang]
    wang_correlations = {
        "calculation": "unweighted OLS with intercept using rounded SI Table I values",
        "rounded_table_r2_fragility_epsilon1": linear_r2(fragility, epsilon1),
        "rounded_table_r2_fragility_epsilon2": linear_r2(fragility, epsilon2),
        "rounded_table_r2_tg_epsilon1": linear_r2(tg, epsilon1),
        "rounded_table_r2_tg_epsilon2": linear_r2(tg, epsilon2),
        "article_reported_r2_fragility_epsilon1": 0.80,
        "article_reported_r2_fragility_epsilon2": 0.78,
        "article_reported_r2_tg_epsilon1": 0.31,
        "article_reported_r2_tg_epsilon2": 0.33,
        "interpretation": (
            "The rounded public SI table preserves the qualitative ordering but does not exactly "
            "reproduce the article's R^2 values. Unrounded fit inputs are not provided; with n=5, "
            "rounding and fit details can materially change R^2. This is a numerical reproducibility "
            "tension, not evidence against the descriptive decoupling result."
        ),
    }
    p8 = next(row for row in p8_p10 if row["polymer"] == "P8")
    contrasts = {
        "p8_over_p9_sigma_ratio": p8["sigma_s_cm"] / p8_p10[1]["sigma_s_cm"],
        "p8_over_p10_sigma_ratio": p8["sigma_s_cm"] / p8_p10[2]["sigma_s_cm"],
        "p8_p10_tg_span_c": max(row["tg_c"] for row in p8_p10) - min(row["tg_c"] for row in p8_p10),
        "p8_over_p10_li_concentration_ratio": p8["li_concentration_mol_l"] / p8_p10[2]["li_concentration_mol_l"],
        "p8_over_p10_sigma_per_li_ratio": p8["sigma_per_li_molarity"] / p8_p10[2]["sigma_per_li_molarity"],
        "interpretation": (
            "P8-P10 are all alternating polymers. Similar Tg does not identify conductivity, "
            "but Li concentration, side-chain length, and molecular weight change together; "
            "this is not a sequence counterexample."
        ),
    }
    if not math.isclose(contrasts["p8_over_p10_sigma_ratio"], 4.375, rel_tol=1e-12):
        raise AssertionError("Unexpected P8/P10 conductivity ratio")

    audit = {
        "schema_version": "polymer-mechanism-audit-1.0",
        "source_manifest": manifest,
        "wang2012_materials": wang,
        "wang2012_correlation_reanalysis": wang_correlations,
        "workbook_inventory": inventory,
        "han_p8_p10": p8_p10,
        "han_p8_p10_contrasts": contrasts,
        "source_data_classification": source_data_classification(),
        "scientific_scope": (
            "Descriptive source-data audit only. The calculations do not establish sequence causality, "
            "carrier identity, a dominant hopping pathway, or a microscopic mechanism."
        ),
    }
    (OUTPUT_ROOT / "polymer_source_data_audit_v0.1.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with (OUTPUT_ROOT / "han_p8_p10_verified.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(p8_p10[0]))
        writer.writeheader()
        writer.writerows(p8_p10)

    with (OUTPUT_ROOT / "han_source_data_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(inventory[0]))
        writer.writeheader()
        writer.writerows(inventory)

    with (OUTPUT_ROOT / "wang2012_materials_verified.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(wang[0]))
        writer.writeheader()
        writer.writerows(wang)

    (OUTPUT_ROOT / "wang2012_correlation_reanalysis.json").write_text(
        json.dumps(wang_correlations, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(json.dumps(contrasts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
