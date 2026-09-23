#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from plot_atlas import apply_publication_style, panel_label

from _nasicon_heldout_panels import (
    render_fraction_panel,
    render_max_ratio_panel,
    save_clean_figure,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    apply_publication_style(10.5)
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
    render_fraction_panel(axes[0], args.result)
    render_max_ratio_panel(axes[1], args.result)
    panel_label(axes[0], "a", x=-0.14, y=1.04)
    panel_label(axes[1], "b", x=-0.14, y=1.04)
    fig.subplots_adjust(left=0.08, right=0.99, bottom=0.19, top=0.96, wspace=0.30)
    save_clean_figure(fig, args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
