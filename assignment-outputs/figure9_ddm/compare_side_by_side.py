#!/usr/bin/env python3
"""
Side-by-side comparison: published Figure 9 vs. the recreation.

Requires figure9_ddm.npz (from recreate_figure9.py) and
figure9_ddm_published.npz (from verify_against_pdf.py).

Usage:  python3 compare_side_by_side.py
Writes: figure9_comparison.png
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

HERE = Path(__file__).resolve().parent
EXTENT = [-5.25, 4.75, -2.0, 7.0]


def main():
    pub = np.load(HERE / "figure9_ddm_published.npz")["ddm_watts"]
    sim = np.load(HERE / "figure9_ddm.npz")["ddm_watts"]

    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.linewidth": 0.6,
    })

    vmax = max(pub.max(), sim.max())
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.3))

    for ax, data, title in (
        (axes[0], pub, "Published Fig. 9\n(digitised from PDF)"),
        (axes[1], sim, "Recreated\n(bistatic radar eq. 11 + KA-GO)"),
    ):
        im = ax.imshow(data, origin="lower", extent=EXTENT, aspect="auto",
                       cmap="jet", interpolation="nearest", vmin=0, vmax=vmax)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("Doppler (kHz)")
        ax.xaxis.set_major_locator(MultipleLocator(2))
        ax.yaxis.set_major_locator(MultipleLocator(2))
        cb = fig.colorbar(im, ax=ax, pad=0.03, fraction=0.055)
        cb.set_label("Watts")
        cb.outline.set_linewidth(0.6)
    axes[0].set_ylabel("Delay (Chips)")

    # Delay cut through the peak Doppler bin, and Doppler cut through peak delay
    ax = axes[2]
    jd = pub.sum(0).argmax()
    delay_ax = -2 + 0.25 * (np.arange(36) + 0.5)
    ax.plot(delay_ax, pub[:, jd] * 1e18, "k-", lw=1.4, label="published")
    ax.plot(delay_ax, sim[:, jd] * 1e18, "r--", lw=1.4, label="recreated")
    ax.set_xlabel("Delay (Chips)")
    ax.set_ylabel(r"Power ($10^{-18}$ W)")
    ax.set_title(f"Delay waveform at {-5.25 + 0.5*(jd+0.5):+.2f} kHz", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.3, lw=0.4)

    fig.tight_layout()
    fig.savefig(HERE / "figure9_comparison.png", dpi=200, bbox_inches="tight")
    print("wrote figure9_comparison.png")


if __name__ == "__main__":
    main()
