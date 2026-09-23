#!/usr/bin/env python3
"""Render the frozen source-length NASICON paired-kMC result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from plot_atlas import apply_publication_style, get_palette, panel_label, save_figure


SEEDS = (104729, 130363, 155921)
STRUCTURES = (10, 41)


def load_shards(shard_dir: Path) -> dict[tuple[int, int], dict]:
    shards = {}
    for seed in SEEDS:
        for structure in STRUCTURES:
            path = shard_dir / f"seed_{seed}_structure_{structure}.json"
            shards[(seed, structure)] = json.loads(path.read_text())
    return shards


def save_clean_figure(fig, output: Path) -> None:
    save_figure(fig, output)
    svg = output if output.suffix.lower() == ".svg" else output.with_suffix(".svg")
    normalized = "\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n"
    svg.write_text(normalized)


def render(shard_dir: Path, aggregate_path: Path, output: Path) -> None:
    shards = load_shards(shard_dir)
    aggregate = json.loads(aggregate_path.read_text())
    palette = get_palette("nature_feature_analysis")
    low_color = palette["roles"]["global"]
    high_color = palette["roles"]["retrained"]
    seed_styles = ("-", (0, (5, 2)), (0, (1, 1)))

    apply_publication_style(10.5)
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
    ax = axes[0]
    for seed_index, seed in enumerate(SEEDS):
        for structure, color in ((10, low_color), (41, high_color)):
            payload = shards[(seed, structure)]
            passes = range(1, len(payload["curves"]["conductivity"]) + 1)
            ax.plot(
                passes,
                payload["curves"]["conductivity"],
                color=color,
                linestyle=seed_styles[seed_index],
                linewidth=1.25,
                alpha=0.92,
            )
    ax.axvspan(2001, 2500, color="#D9D9D9", alpha=0.35, linewidth=0)
    ax.axvspan(2501, 3000, color="#F2D17E", alpha=0.30, linewidth=0)
    ax.text(2248, 9.8, "preceding", ha="center", va="top", fontsize=8, color="#666666")
    ax.text(2748, 9.8, "late", ha="center", va="top", fontsize=8, color="#806000")
    ax.set(xlabel="Measurement pass", ylabel="Cumulative conductivity (mS cm$^{-1}$)")
    ax.set_xlim(1, 3000)
    ax.set_ylim(0, 10.2)
    ax.grid(False)
    structure_handles = [
        plt.Line2D([0], [0], color=low_color, linewidth=2, label="Structure 10 (low initial rate)"),
        plt.Line2D([0], [0], color=high_color, linewidth=2, label="Structure 41 (high initial rate)"),
    ]
    seed_handles = [
        plt.Line2D([0], [0], color="#555555", linestyle=seed_styles[i], linewidth=1.4, label=f"Seed {seed}")
        for i, seed in enumerate(SEEDS)
    ]
    legend1 = ax.legend(handles=structure_handles, loc="upper left", frameon=False, fontsize=7.5)
    ax.add_artist(legend1)
    ax.legend(handles=seed_handles, loc="upper left", bbox_to_anchor=(0, 0.79), frameon=False, fontsize=7.2)

    ax = axes[1]
    summaries = aggregate["paired_summary"]
    x_low, x_high = 0, 1
    for item in summaries:
        passed = item["pair_convergence_gate_pass"]
        color = "#333333" if passed else "#C4473A"
        marker = "o" if passed else "X"
        low = item["low_late_window_median_conductivity_mS_cm"]
        high = item["high_late_window_median_conductivity_mS_cm"]
        ax.plot([x_low, x_high], [low, high], color=color, linewidth=1.35, alpha=0.85)
        ax.scatter([x_low, x_high], [low, high], color=[low_color, high_color], edgecolor=color,
                   linewidth=1.0, s=47, marker=marker, zorder=3)
        ratio = item["ratio_high_over_low"]
        ax.text(1.08, high, f'{item["seed"]}: {ratio:.3f}×', va="center", fontsize=8, color=color)
    ax.set_xticks([0, 1], ["Structure 10\nlow initial rate", "Structure 41\nhigh initial rate"])
    ax.set_ylabel("Late-window median conductivity (mS cm$^{-1}$)")
    ax.set_xlim(-0.25, 1.72)
    ax.set_ylim(0, 6.1)
    ax.grid(False)
    ax.text(
        0.02,
        0.98,
        "Frozen rule: FAIL\n1/3 ratios reversed; 1/3 pairs not converged",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="#9D2F27",
    )

    panel_label(axes[0], "a", x=-0.14, y=1.04)
    panel_label(axes[1], "b", x=-0.14, y=1.04)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.19, top=0.96, wspace=0.28)
    save_clean_figure(fig, output)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-dir", type=Path, required=True)
    parser.add_argument("--aggregate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render(args.shard_dir, args.aggregate, args.output)


if __name__ == "__main__":
    main()
