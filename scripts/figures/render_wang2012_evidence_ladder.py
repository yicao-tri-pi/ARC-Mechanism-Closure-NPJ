#!/usr/bin/env python3
"""Render the Wang 2012 observation–inference–mechanism evidence ladder.

This is a data-free scientific schematic. It summarizes provenance and logical
status; it does not reproduce or estimate a numerical result from the paper.
Each stage can be rendered independently for reuse in a composite figure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ATLAS = Path(
    "/Users/yicao/.codex/.chatgpt-projects/"
    "g-p-6aa88e35293481918a7b8159df39d546/plot_library"
)
sys.path.insert(0, str(ATLAS / "src"))

from plot_atlas.palettes import get_palette  # noqa: E402
from plot_atlas.style import apply_publication_style, panel_label  # noqa: E402


SUPPORTED = "#178F78"
NONIDENTIFYING = "#2B68A6"
TENSION = "#CE6237"
INK = "#252525"
MUTED = "#667085"
LIGHT = "#F7F8FA"


def set_status_palette(name: str):
    """Map semantic evidence roles to registered, swappable atlas palettes."""
    global SUPPORTED, NONIDENTIFYING, TENSION
    if name == "isotope_sites":
        base = get_palette("isotope_sites")
        accent = get_palette("paired_slate_orange")
        SUPPORTED = base["categorical"][0]
        NONIDENTIFYING = base["categorical"][3]
        TENSION = accent["end"]
    elif name == "climate_spectrum":
        base = get_palette("climate_spectrum")
        SUPPORTED = base["categorical"][1]
        NONIDENTIFYING = base["categorical"][0]
        TENSION = base["categorical"][4]
    else:
        raise ValueError(f"Unsupported palette: {name}")


def _box(ax, xy, width, height, title, body, color, *, title_size=8.4):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.025,rounding_size=0.035",
            facecolor="white", edgecolor=color, linewidth=1.6,
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (x + 0.025, y + height - 0.26), width - 0.05, 0.22,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            facecolor=color, edgecolor="none", alpha=0.14,
        )
    )
    ax.text(x + 0.07, y + height - 0.15, title, color=INK, fontsize=title_size,
            fontweight="bold", ha="left", va="center")
    ax.text(x + 0.07, y + height - 0.34, body, color=INK, fontsize=7.3,
            ha="left", va="top", linespacing=1.35)


def _chip(ax, x, y, text, color, *, width=None):
    width = width or max(0.65, 0.083 * len(text) + 0.22)
    ax.add_patch(FancyBboxPatch(
        (x, y), width, 0.22, boxstyle="round,pad=0.015,rounding_size=0.04",
        facecolor=color, edgecolor="none", alpha=0.15,
    ))
    ax.text(x + width / 2, y + 0.11, text, fontsize=6.8, color=INK,
            ha="center", va="center")


def _arrow(ax, x0, x1, y=0.52):
    ax.add_patch(FancyArrowPatch(
        (x0, y), (x1, y), arrowstyle="-|>", mutation_scale=11,
        linewidth=1.25, color="#8A94A3",
    ))


def _base(ax, label):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.9)
    ax.axis("off")
    panel_label(ax, label, x=-0.015, y=1.02)


def draw_observation(ax, label="a"):
    _base(ax, label)
    _box(
        ax, (0.25, 0.35), 4.1, 1.05,
        "Direct observables",
        "Broadband dielectric spectroscopy\n"
        r"conductivity, $\sigma(T)$" "\n"
        r"segmental relaxation, $\tau_s(T)$",
        SUPPORTED,
    )
    _arrow(ax, 4.48, 5.20, 0.88)
    _box(
        ax, (5.35, 0.35), 4.35, 1.05,
        "Descriptive claim",
        r"$\sigma T\tau_s$ changes by 4–6 orders" "\n"
        "in rigid-chain samples; flexible controls\n"
        "remain approximately coupled",
        SUPPORTED,
    )
    _chip(ax, 3.86, 0.04, "SUPPORTED · class A", SUPPORTED, width=2.2)


def draw_inference(ax, label="b"):
    _base(ax, label)
    _box(
        ax, (0.25, 0.35), 2.45, 1.05,
        "Measured EP response",
        "polarization time\n"
        "polarization length\n"
        "blocking-electrode spectra",
        SUPPORTED,
    )
    _arrow(ax, 2.82, 3.30, 0.88)
    _box(
        ax, (3.43, 0.35), 2.95, 1.05,
        "Trukhan inversion",
        r"Debye EP; $\Delta\varepsilon_{EP}\gg\varepsilon_R$" "\n"
        r"equal Li$^{+}$/anion diffusivity" "\n"
        "electrode-material omission\n"
        "constant normalization",
        TENSION,
    )
    _arrow(ax, 6.50, 6.98, 0.88)
    _box(
        ax, (7.10, 0.35), 2.60, 1.05,
        "Derived quantities",
        r"diffusivity, $D(T)$" "\n"
        r"mobile-ion fraction, $p(T)$" "\n"
        "not directly measured",
        NONIDENTIFYING,
    )
    _chip(ax, 3.18, 0.04, "NON-IDENTIFYING + MODEL TENSION", TENSION, width=3.65)


def draw_mechanism(ax, label="c"):
    _base(ax, label)
    _box(
        ax, (0.25, 0.35), 2.45, 1.05,
        "Published narrative",
        "rigid chain → packing frustration\n"
        "→ loose local structure\n"
        "→ facilitated ion transport",
        NONIDENTIFYING,
    )
    _arrow(ax, 2.82, 3.30, 0.88)
    _box(
        ax, (3.43, 0.34), 4.05, 1.17,
        "Observation-equivalent alternatives",
        "carrier concentration / association\n"
        "local side-chain mobility / hopping\n"
        "cluster correlations · morphology · interfaces",
        NONIDENTIFYING,
    )
    _arrow(ax, 7.60, 8.08, 0.88)
    _box(
        ax, (8.20, 0.35), 1.55, 1.05,
        "Verdict",
        "plausible\nnot exclusive\nno scope-matched\nfalsifier found",
        NONIDENTIFYING,
        title_size=8.0,
    )
    _chip(ax, 3.62, 0.04, "PROMOTION CEILING · scope-limited mechanism", NONIDENTIFYING, width=3.78)


PANELS = {
    "observation": draw_observation,
    "inference": draw_inference,
    "mechanism": draw_mechanism,
}


def render(panel: str, output: Path, palette: str):
    apply_publication_style(font_size=8.0)
    set_status_palette(palette)

    if panel == "all":
        fig, axes = plt.subplots(3, 1, figsize=(7.2, 5.0))
        for ax, (name, fn), label in zip(axes, PANELS.items(), "abc"):
            fn(ax, label)
        fig.subplots_adjust(left=0.03, right=0.985, top=0.98, bottom=0.025, hspace=0.11)
    else:
        fig, ax = plt.subplots(figsize=(7.2, 1.72))
        PANELS[panel](ax, "")
        fig.subplots_adjust(left=0.025, right=0.985, top=0.98, bottom=0.04)

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".png"), dpi=400, facecolor="white")
    fig.savefig(output.with_suffix(".svg"), facecolor="white", metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--panel", choices=["all", *PANELS], default="all",
        help="Render the complete ladder or one independently reusable stage.",
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path("figures/wang2012_evidence_ladder"),
    )
    parser.add_argument(
        "--palette", choices=["isotope_sites", "climate_spectrum"],
        default="isotope_sites",
        help="Registered Plot Atlas palette used for evidence-status roles.",
    )
    args = parser.parse_args()
    render(args.panel, args.output, args.palette)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
