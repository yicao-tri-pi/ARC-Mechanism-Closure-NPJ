#!/usr/bin/env python3
"""Render the source-grounded P8-P10 audit panel.

Each subpanel can be rendered independently with ``--panel``.  The figure uses
reported summary values only; sigma/cLi is labeled as a proxy, not mobility.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogLocator, NullFormatter


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ATLAS = Path(
    "/Users/yicao/.codex/.chatgpt-projects/"
    "g-p-6aa88e35293481918a7b8159df39d546/plot_library"
)
ATLAS = Path(os.environ.get("PLOT_ATLAS_ROOT", DEFAULT_ATLAS))
sys.path.insert(0, str(ATLAS / "src"))

from plot_atlas import apply_publication_style, bold_tick_labels, get_palette, panel_label, save_figure  # noqa: E402


def load_rows() -> list[dict[str, float | str]]:
    path = ROOT / "evidence" / "npj_mechanism_audit" / "derived" / "han_p8_p10_verified.csv"
    rows = []
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "polymer": row["polymer"],
                    "n": float(row["peo_repeat_n"]),
                    "tg": float(row["tg_c"]),
                    "sigma": float(row["sigma_s_cm"]),
                    "sigma_sd": float(row["sigma_sd_s_cm"]),
                    "li": float(row["li_concentration_mol_l"]),
                    "sigma_per_li": float(row["sigma_per_li_molarity"]),
                }
            )
    return rows


def common_axis(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.25)
    ax.tick_params(direction="out", width=1.15, length=4)
    bold_tick_labels(ax)


def tg_panel(ax, rows, colors) -> None:
    x = np.arange(len(rows))
    ax.scatter(x, [row["tg"] for row in rows], s=65, c=colors, edgecolor="#222222", linewidth=0.8, zorder=3)
    ax.axhspan(-35, -31, color="#D9E8E7", alpha=0.7, zorder=0)
    ax.set_xticks(x, [row["polymer"] for row in rows])
    ax.set_ylabel("Glass transition, $T_g$ (°C)")
    ax.set_ylim(-38, -28)
    ax.set_yticks([-38, -36, -34, -32, -30, -28])
    common_axis(ax)


def conductivity_panel(ax, rows, colors) -> None:
    x = np.arange(len(rows))
    values = np.array([row["sigma"] for row in rows])
    errors = np.array([row["sigma_sd"] for row in rows])
    ax.bar(x, values, yerr=errors, color=colors, edgecolor="#222222", linewidth=0.8,
           capsize=3, error_kw={"elinewidth": 1.1, "capthick": 1.1}, zorder=2)
    ax.set_yscale("log")
    ax.set_xticks(x, [row["polymer"] for row in rows])
    ax.set_ylabel("Ionic conductivity, σ (S cm$^{-1}$)")
    ax.set_ylim(5e-6, 7e-5)
    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=4))
    ax.yaxis.set_minor_formatter(NullFormatter())
    common_axis(ax)


def carrier_panel(ax, rows, colors) -> None:
    x = np.arange(len(rows))
    li = np.array([row["li"] for row in rows])
    proxy = np.array([row["sigma_per_li"] for row in rows]) * 1e5
    ax.plot(x, li, color="#263E69", marker="o", markersize=7, linewidth=1.8,
            markerfacecolor="white", markeredgewidth=1.4, label="Li concentration")
    ax.set_xticks(x, [row["polymer"] for row in rows])
    ax.set_ylabel("Li concentration (mol l$^{-1}$)", color="#263E69")
    ax.tick_params(axis="y", colors="#263E69")
    ax.set_ylim(0.6, 1.3)
    ax2 = ax.twinx()
    ax2.plot(x, proxy, color="#C12F55", marker="s", markersize=6.5, linewidth=1.8,
             markerfacecolor="white", markeredgewidth=1.4, label="σ/$c_{Li}$ proxy")
    ax2.set_ylabel("σ/$c_{Li}$ proxy ($10^{-5}$ S cm$^{-1}$ M$^{-1}$)", color="#C12F55")
    ax2.tick_params(axis="y", colors="#C12F55", direction="out", width=1.15, length=4)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_linewidth(1.25)
    bold_tick_labels(ax2)
    common_axis(ax)


def make_figure(panel: str):
    apply_publication_style(10.5)
    rows = load_rows()
    palette = get_palette("isotope_sites")
    colors = [palette["categorical"][i] for i in (0, 1, 2)]
    renderers = {"tg": tg_panel, "sigma": conductivity_panel, "carriers": carrier_panel}
    if panel == "all":
        fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6))
        for label, key, ax in zip("abc", ("tg", "sigma", "carriers"), axes):
            renderers[key](ax, rows, colors)
            panel_label(ax, label, x=-0.18, y=1.08)
        fig.subplots_adjust(left=0.075, right=0.93, bottom=0.2, top=0.88, wspace=0.52)
        return fig
    fig, ax = plt.subplots(figsize=(4.2, 3.5))
    renderers[panel](ax, rows, colors)
    fig.subplots_adjust(left=0.22, right=0.82 if panel == "carriers" else 0.96, bottom=0.2, top=0.94)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", choices=("all", "tg", "sigma", "carriers"), default="all")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "figures" / "han_p8_p10_nonidentifiability.png",
    )
    args = parser.parse_args()
    fig = make_figure(args.panel)
    save_figure(fig, args.output)
    plt.close(fig)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
