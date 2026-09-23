#!/usr/bin/env python3
"""Render standalone panels or composite for the frozen NLEIS joint-fit study."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from plot_atlas import apply_publication_style, get_palette, panel_label, save_figure


def width_panel(ax, result: dict) -> None:
    eligible = [row for row in result["conditions"] if row["eligible"]]
    x = np.asarray([row["eis_only"]["allocation_range_width"] for row in eligible])
    y = np.asarray([row["joint_eis_nleis"]["allocation_range_width"] for row in eligible])
    passed = np.asarray([row["allocation_contraction_gate_pass"] for row in eligible])
    palette = get_palette("nature_feature_analysis")
    ax.scatter(x[~passed], y[~passed], s=42, color=palette["neutral"], edgecolor="#333333", linewidth=.7, label="No 25% contraction")
    ax.scatter(x[passed], y[passed], s=52, color=palette["roles"]["retrained"], edgecolor="#333333", linewidth=.8, label="Contraction gate passed")
    grid = np.logspace(-4, 0, 200)
    ax.plot(grid, grid, color="#777777", linestyle="--", linewidth=1, label="Equal width")
    ax.plot(grid, .75 * grid, color="#9D2F27", linestyle=":", linewidth=1.4, label="Frozen 0.75x gate")
    ax.set(xscale="log", yscale="log", xlim=(1e-4, 1.2), ylim=(1e-4, 1.2),
           xlabel="EIS-only allocation-range width", ylabel="Joint EIS+NLEIS allocation-range width")
    ax.grid(False)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left")
    ax.text(.98, .04, "3/30 pass; 26/30 eligible", transform=ax.transAxes, ha="right", va="bottom", color="#9D2F27", fontsize=8.5)


def error_panel(ax, result: dict) -> None:
    eligible = [row for row in result["conditions"] if row["eligible"]]
    eis = np.asarray([row["joint_eis_nleis"]["best_record"]["heldout_eis_nrmse"] for row in eligible])
    nleis = np.asarray([row["joint_eis_nleis"]["best_record"]["heldout_nleis_nrmse"] for row in eligible])
    palette = get_palette("nature_feature_analysis")
    rng = np.random.default_rng(1701)
    for index, (values, color) in enumerate(((eis, palette["roles"]["global"]), (nleis, palette["roles"]["retrained"]))):
        ax.scatter(index + rng.uniform(-.10, .10, len(values)), values, s=28, color=color, alpha=.78, edgecolor="#333333", linewidth=.45)
        ax.plot([index-.18, index+.18], [np.median(values)]*2, color="#111111", linewidth=2.2)
    ax.axhline(.10, color=palette["roles"]["global"], linestyle="--", linewidth=1)
    ax.axhline(.20, color=palette["roles"]["retrained"], linestyle="--", linewidth=1)
    ax.set_xticks([0, 1], ["Linear EIS", "Second-harmonic NLEIS"])
    ax.set(xlim=(-.45, 1.45), ylabel="Held-out NRMSE")
    ax.grid(False)
    ax.text(.03, .97, "Median: 0.024 / 0.116\nerror gate: PASS", transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color="#24713A")


def render(result_path: Path, output: Path, panel: str) -> None:
    result = json.loads(result_path.read_text())
    apply_publication_style(10.5)
    if panel == "widths":
        fig, ax = plt.subplots(figsize=(6.1, 4.8)); width_panel(ax, result)
    elif panel == "errors":
        fig, ax = plt.subplots(figsize=(6.1, 4.8)); error_panel(ax, result)
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8))
        width_panel(axes[0], result); error_panel(axes[1], result)
        panel_label(axes[0], "a", x=-.15, y=1.04); panel_label(axes[1], "b", x=-.15, y=1.04)
        fig.subplots_adjust(left=.09, right=.98, bottom=.18, top=.96, wspace=.30)
    if panel != "composite": fig.subplots_adjust(left=.16, right=.97, bottom=.18, top=.96)
    save_figure(fig, output)
    svg = output if output.suffix.lower() == ".svg" else output.with_suffix(".svg")
    if svg.exists():
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--panel", choices=("widths", "errors", "composite"), default="composite")
    args = parser.parse_args(); render(args.result, args.output, args.panel)


if __name__ == "__main__": main()
