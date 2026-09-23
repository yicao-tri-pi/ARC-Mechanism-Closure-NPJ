#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from plot_atlas import apply_publication_style

from _nasicon_heldout_panels import render_fraction_panel, save_clean_figure


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    apply_publication_style(10.5)
    fig, ax = plt.subplots(figsize=(6.4, 4.7))
    render_fraction_panel(ax, args.result)
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.18, top=0.96)
    save_clean_figure(fig, args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
