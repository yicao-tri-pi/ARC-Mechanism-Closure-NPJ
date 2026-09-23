#!/usr/bin/env python3
"""Render the paper workflow and cross-case evidence-status figures.

The colors follow the Plot Atlas ``nature_feature_analysis`` palette.  The
figures contain no synthetic scientific measurements: Fig. 1 is conceptual and
Fig. 5 summarizes the frozen artifact/gate status documented in this repo.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


COLORS = {
    "blue": "#3A82B4",
    "gray": "#999999",
    "green": "#4AAF4F",
    "orange": "#D66A3A",
    "red": "#B63A32",
    "pale_blue": "#E7F0F6",
    "pale_green": "#E8F4E8",
    "pale_orange": "#F8E9E1",
    "ink": "#222222",
}


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 10.5,
            "axes.linewidth": 1.4,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def save(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "pdf", "svg"):
        fig.savefig(stem.with_suffix(f".{suffix}"), dpi=400, bbox_inches="tight")


def workflow(output: Path) -> None:
    style()
    fig, ax = plt.subplots(figsize=(12.5, 4.7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    labels = [
        ("Evidence +\nphysical knowledge", "Domain constraint", COLORS["pale_blue"], COLORS["blue"]),
        ("AI mechanism\nenumeration", "Candidate space", COLORS["pale_blue"], COLORS["blue"]),
        ("Claim certificate +\nformal obligation", "Specification", COLORS["pale_orange"], COLORS["orange"]),
        ("Fidelity, Lean +\nnumerical checks", "Conditional validity", COLORS["pale_green"], COLORS["green"]),
        ("Discriminating\nobservation", "Closure design", COLORS["pale_green"], COLORS["green"]),
        ("Empirical\nmechanism closure", "World-facing claim", "#F2F2F2", COLORS["gray"]),
    ]
    xs = np.linspace(0.085, 0.915, len(labels))
    width, height = 0.135, 0.27
    for index, (x, (title, subtitle, fill, edge)) in enumerate(zip(xs, labels)):
        box = FancyBboxPatch(
            (x - width / 2, 0.55),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            facecolor=fill,
            edgecolor=edge,
            linewidth=2.2,
        )
        ax.add_patch(box)
        ax.text(x, 0.705, title, ha="center", va="center", weight="bold", color=COLORS["ink"], fontsize=10.5)
        ax.text(x, 0.585, subtitle, ha="center", va="center", color=edge, fontsize=8.8)
        if index < len(labels) - 1:
            ax.add_patch(
                FancyArrowPatch(
                    (x + width / 2 + 0.006, 0.685),
                    (xs[index + 1] - width / 2 - 0.006, 0.685),
                    arrowstyle="-|>",
                    mutation_scale=13,
                    linewidth=1.8,
                    color="#6E7781",
                )
            )

    ax.text(0.27, 0.94, "Hypothesis construction", ha="center", weight="bold", color=COLORS["blue"], fontsize=12)
    ax.plot([0.03, 0.465], [0.905, 0.905], color=COLORS["blue"], lw=3)
    ax.text(0.62, 0.94, "Machine-checkable criticism", ha="center", weight="bold", color=COLORS["orange"], fontsize=12)
    ax.plot([0.49, 0.755], [0.905, 0.905], color=COLORS["orange"], lw=3)
    ax.text(0.875, 0.94, "Scientific adjudication", ha="center", weight="bold", color=COLORS["green"], fontsize=12)
    ax.plot([0.78, 0.97], [0.905, 0.905], color=COLORS["green"], lw=3)

    cases = [
        (0.21, "NASICON", "structural non-identifiability", "mean barrier $\\nRightarrow$ long-time ordering"),
        (0.50, "EIS/NLEIS", "practical non-identifiability", "good fit $\\nRightarrow$ electrode allocation"),
        (0.79, "Polymer transport", "specification non-identifiability", "$\\sigma,\\tau_s$ $\\nRightarrow$ unique mechanism"),
    ]
    for x, case, failure, statement in cases:
        ax.text(x, 0.36, case, ha="center", va="center", weight="bold", fontsize=10.5)
        ax.text(x, 0.285, failure, ha="center", va="center", color=COLORS["red"], fontsize=9.2)
        ax.text(x, 0.205, statement, ha="center", va="center", fontsize=9.2)
    ax.text(
        0.5,
        0.07,
        "Lean proves consequences of encoded assumptions; domain evidence and closure observations decide whether those assumptions describe the material.",
        ha="center",
        va="center",
        fontsize=9.4,
        color="#4C4C4C",
    )
    save(fig, output / "fig1_workflow")
    plt.close(fig)


def evidence_matrix(output: Path) -> None:
    style()
    columns = [
        "Source\npacket",
        "Formal\ncertificate",
        "Executable\nwitness",
        "Primary\nquantitative gate",
        "Independent\nfidelity review",
        "Empirical\nclosure",
    ]
    rows = ["NASICON kMC", "EIS / NLEIS", "Wang polymer"]
    # 2 = complete/pass, 1 = informative failed gate, 0 = pending/not run.
    values = np.array(
        [
            [2, 2, 2, 1, 0, 0],
            [2, 2, 2, 1, 0, 0],
            [2, 2, 0, 0, 0, 0],
        ]
    )
    text = np.array(
        [
            ["frozen", "checked", "6,000-pass", "failed", "pending", "missing"],
            ["30 spectra", "checked", "multistart", "failed", "pending", "missing"],
            ["audited", "checked", "data absent", "not run", "pending", "missing"],
        ]
    )
    cmap = {2: COLORS["pale_green"], 1: COLORS["pale_orange"], 0: "#F0F0F0"}
    edge = {2: COLORS["green"], 1: COLORS["orange"], 0: COLORS["gray"]}
    fig, ax = plt.subplots(figsize=(10.8, 4.0))
    ax.set_xlim(0, len(columns))
    ax.set_ylim(0, len(rows))
    ax.invert_yaxis()
    ax.axis("off")
    for i, row in enumerate(rows):
        ax.text(-0.12, i + 0.5, row, ha="right", va="center", weight="bold", fontsize=10.5)
        for j in range(len(columns)):
            rect = FancyBboxPatch(
                (j + 0.04, i + 0.08),
                0.92,
                0.84,
                boxstyle="round,pad=0.01,rounding_size=0.035",
                facecolor=cmap[int(values[i, j])],
                edgecolor=edge[int(values[i, j])],
                linewidth=1.8,
            )
            ax.add_patch(rect)
            ax.text(j + 0.5, i + 0.5, text[i, j], ha="center", va="center", fontsize=9.2)
    for j, column in enumerate(columns):
        ax.text(j + 0.5, -0.18, column, ha="center", va="bottom", weight="bold", fontsize=9.5)

    ax.text(0.0, 3.35, "Complete / bound", color=COLORS["green"], weight="bold", fontsize=9.2)
    ax.text(1.35, 3.35, "Gate failed (result retained)", color=COLORS["orange"], weight="bold", fontsize=9.2)
    ax.text(3.5, 3.35, "Pending or missing", color=COLORS["gray"], weight="bold", fontsize=9.2)
    ax.text(
        0,
        3.68,
        "A failed gate is an informative scientific outcome, not a completed mechanism closure.",
        color="#4C4C4C",
        fontsize=9.2,
    )
    save(fig, output / "fig5_evidence_matrix")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    workflow(args.output_dir)
    evidence_matrix(args.output_dir)


if __name__ == "__main__":
    main()
