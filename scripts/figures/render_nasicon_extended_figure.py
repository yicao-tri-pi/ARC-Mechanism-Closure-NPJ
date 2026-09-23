#!/usr/bin/env python3
"""Render standalone panels or the composite NASICON v0.2 closure figure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from plot_atlas import apply_publication_style, get_palette, panel_label, save_figure


SEEDS = (104729, 130363, 155921)
STRUCTURES = (10, 41)


def load_shards(shard_dir: Path) -> dict[tuple[int, int], dict]:
    return {
        (seed, structure): json.loads(
            (shard_dir / f"seed_{seed}_structure_{structure}.json").read_text()
        )
        for seed in SEEDS
        for structure in STRUCTURES
    }


def trajectory_panel(ax, shards: dict[tuple[int, int], dict]) -> None:
    palette = get_palette("nature_feature_analysis")
    colors = {10: palette["roles"]["global"], 41: palette["roles"]["retrained"]}
    styles = ("-", (0, (5, 2)), (0, (1, 1)))
    for seed_index, seed in enumerate(SEEDS):
        for structure in STRUCTURES:
            curve = shards[(seed, structure)]["curves"]["conductivity"]
            ax.plot(
                range(1, len(curve) + 1), curve, color=colors[structure],
                linestyle=styles[seed_index], linewidth=1.15, alpha=0.90,
            )
    ax.axvspan(4001, 5000, color="#D9D9D9", alpha=0.35, linewidth=0)
    ax.axvspan(5001, 6000, color="#F2D17E", alpha=0.30, linewidth=0)
    ax.text(4500, 9.8, "preceding", ha="center", va="top", fontsize=8, color="#666666")
    ax.text(5500, 9.8, "late", ha="center", va="top", fontsize=8, color="#806000")
    ax.set(
        xlabel="Measurement pass",
        ylabel="Cumulative conductivity (mS cm$^{-1}$)",
        xlim=(1, 6000), ylim=(0, 10.2),
    )
    ax.grid(False)
    structure_handles = [
        plt.Line2D([0], [0], color=colors[10], linewidth=2, label="Structure 10 (low initial rate)"),
        plt.Line2D([0], [0], color=colors[41], linewidth=2, label="Structure 41 (high initial rate)"),
    ]
    seed_handles = [
        plt.Line2D([0], [0], color="#555555", linestyle=styles[i], linewidth=1.4, label=f"Seed {seed}")
        for i, seed in enumerate(SEEDS)
    ]
    legend = ax.legend(handles=structure_handles, loc="upper left", frameon=False, fontsize=7.5)
    ax.add_artist(legend)
    ax.legend(handles=seed_handles, loc="upper left", bbox_to_anchor=(0, 0.79), frameon=False, fontsize=7.2)


def paired_panel(ax, aggregate: dict) -> None:
    palette = get_palette("nature_feature_analysis")
    low_color = palette["roles"]["global"]
    high_color = palette["roles"]["retrained"]
    label_offsets = {104729: 0.22, 130363: -0.22, 155921: 0.0}
    for item in aggregate["paired_summary"]:
        converged = item["pair_convergence_gate_pass"]
        line_color = "#333333" if converged else "#C4473A"
        marker = "o" if converged else "X"
        low = item["low_late_window_median_conductivity_mS_cm"]
        high = item["high_late_window_median_conductivity_mS_cm"]
        ax.plot([0, 1], [low, high], color=line_color, linewidth=1.35, alpha=0.88)
        ax.scatter(
            [0, 1], [low, high], color=[low_color, high_color], edgecolor=line_color,
            linewidth=1.0, s=52, marker=marker, zorder=3,
        )
        ax.text(1.08, high + label_offsets[item["seed"]], f'{item["seed"]}: {item["ratio_high_over_low"]:.3f}x',
                va="center", fontsize=8, color=line_color)
    ax.set_xticks([0, 1], ["Structure 10\nlow initial rate", "Structure 41\nhigh initial rate"])
    ax.set_ylabel("Late-window median conductivity (mS cm$^{-1}$)")
    ax.set_xlim(-0.25, 1.72)
    ax.set_ylim(0, 9.4)
    ax.grid(False)
    ax.text(
        0.02, 0.98,
        "Closure rule: FAIL\n4/6 runs converged; 1/3 pairs converged\nconverged pair reverses direction",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color="#9D2F27",
    )


def save_clean(fig, output: Path) -> None:
    save_figure(fig, output)
    svg = output if output.suffix.lower() == ".svg" else output.with_suffix(".svg")
    if svg.exists():
        svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")


def render(shard_dir: Path, aggregate_path: Path, output: Path, panel: str) -> None:
    shards = load_shards(shard_dir)
    aggregate = json.loads(aggregate_path.read_text())
    apply_publication_style(10.5)
    if panel == "trajectory":
        fig, ax = plt.subplots(figsize=(6.4, 4.8))
        trajectory_panel(ax, shards)
    elif panel == "paired":
        fig, ax = plt.subplots(figsize=(6.4, 4.8))
        paired_panel(ax, aggregate)
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
        trajectory_panel(axes[0], shards)
        paired_panel(axes[1], aggregate)
        panel_label(axes[0], "a", x=-0.14, y=1.04)
        panel_label(axes[1], "b", x=-0.14, y=1.04)
        fig.subplots_adjust(left=0.08, right=0.98, bottom=0.19, top=0.96, wspace=0.28)
    if panel != "composite":
        fig.subplots_adjust(left=0.15, right=0.97, bottom=0.18, top=0.96)
    save_clean(fig, output)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-dir", type=Path, required=True)
    parser.add_argument("--aggregate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--panel", choices=("trajectory", "paired", "composite"), default="composite")
    args = parser.parse_args()
    render(args.shard_dir, args.aggregate, args.output, args.panel)


if __name__ == "__main__":
    main()
