from __future__ import annotations

import json
import math
from pathlib import Path

from plot_atlas import get_palette, save_figure, timecourse


CHANNELS = (
    ("mean_ekra_to_full_rate", "Mean $E_{KRA}$ → full rate"),
    ("nonnegative_directional_barrier", "Nonnegative barrier sensitivity"),
)


def save_clean_figure(fig, output: Path) -> None:
    """Save Plot Atlas outputs and normalize generated SVG line endings."""
    save_figure(fig, output)
    svg = output if output.suffix.lower() == ".svg" else output.with_suffix(".svg")
    normalized = "\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n"
    svg.write_text(normalized)


def _series(result_path: Path, field: str):
    payload = json.loads(result_path.read_text())
    rows = sorted(payload["composition_results"], key=lambda item: item["paper_formula_x"])
    x = [item["paper_formula_x"] for item in rows]
    values = [[item[channel][field] for item in rows] for channel, _ in CHANNELS]
    # The discovery composition was excluded by contract. Insert an explicit
    # gap so the lines do not visually interpolate through held-out x=2.4.
    insertion = next((index for index, value in enumerate(x) if value > 2.4), len(x))
    x.insert(insertion, 2.4)
    for series in values:
        series.insert(insertion, math.nan)
    return x, values


def render_fraction_panel(ax, result_path: Path) -> None:
    x, values = _series(result_path, "fraction_meeting_rate_ratio_threshold")
    palette = get_palette("nature_feature_analysis")
    colors = [palette["roles"]["global"], palette["roles"]["retrained"]]
    timecourse(
        ax,
        x,
        values,
        [label for _, label in CHANNELS],
        colors,
        xlabel=r"NASICON composition $x$ in Na$_{1+x}$Zr$_2$Si$_x$P$_{3-x}$O$_{12}$",
        ylabel="Matched pairs above\nfrozen rate-ratio threshold",
        legend=True,
        line_width=1.9,
        marker_size=4.4,
    )
    ax.set_xlim(-0.05, 3.05)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xticks([0, 0.6, 1.2, 1.8, 2.4, 3.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.axvline(2.4, color="#777777", linewidth=1.0, linestyle=(0, (3, 2)), zorder=1)
    ax.text(2.37, 0.04, "discovery\ncomposition", rotation=90, ha="right", va="bottom", color="#666666", fontsize=7.5)
    ax.grid(False)


def render_max_ratio_panel(ax, result_path: Path) -> None:
    x, values = _series(result_path, "maximum_rate_ratio")
    palette = get_palette("nature_feature_analysis")
    colors = [palette["roles"]["global"], palette["roles"]["retrained"]]
    timecourse(
        ax,
        x,
        values,
        [label for _, label in CHANNELS],
        colors,
        xlabel=r"NASICON composition $x$ in Na$_{1+x}$Zr$_2$Si$_x$P$_{3-x}$O$_{12}$",
        ylabel="Maximum matched-pair\naggregate-rate ratio",
        legend=True,
        line_width=1.9,
        marker_size=4.4,
    )
    ax.set_yscale("log")
    ax.set_xlim(-0.05, 3.05)
    ax.set_ylim(0.92, 35)
    ax.set_xticks([0, 0.6, 1.2, 1.8, 2.4, 3.0])
    ax.set_yticks([1, 2, 5, 10, 20], labels=["1", "2", "5", "10", "20"])
    ax.axhline(1.25, color=colors[0], linewidth=1.0, linestyle=(0, (4, 3)), alpha=0.8)
    ax.axhline(1.20, color=colors[1], linewidth=1.0, linestyle=(0, (2, 2)), alpha=0.8)
    ax.axvline(2.4, color="#777777", linewidth=1.0, linestyle=(0, (3, 2)), zorder=1)
    ax.text(2.37, 31, "discovery\ncomposition", rotation=90, ha="right", va="top", color="#666666", fontsize=7.5)
    ax.grid(False)
