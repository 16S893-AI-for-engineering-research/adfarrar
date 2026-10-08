#!/usr/bin/env python3
"""
Verify the Figure 9 recreation against the published figure.

Digitises the original raster embedded in the PDF (page 21, XObject /Im0) by
inverting the figure's own colourbar, calibrated using the tick-label positions
extracted from the PDF text layer. Then compares the digitised DDM with the
simulation produced by recreate_figure9.py.

Usage:  python3 verify_against_pdf.py [path/to/IEEE_GRSM_GNSSR_Tutorial_06985926.pdf]
"""

import sys
from pathlib import Path

import numpy as np

PDF_DEFAULT = Path(__file__).resolve().parent.parent / "IEEE_GRSM_GNSSR_Tutorial_06985926.pdf"
PAGE_INDEX = 13          # 0-based; printed page 21
XOBJECT = "/Im0"

# Image placement on the PDF page, in points (from pdfplumber page.images)
IMG_T = 65.191

# Pixel geometry of the 587x443 embedded raster, measured from the raster itself
PLOT_X0, PLOT_X1 = 1, 487        # axes box, left/right edge
PLOT_Y0, PLOT_Y1 = 1, 440        # axes box, top/bottom edge
CBAR_X0, CBAR_X1 = 562, 576      # clean interior columns of the colourbar
CBAR_Y0, CBAR_Y1 = 14, 438       # colourbar box, top/bottom

# Colourbar tick calibration from the PDF text layer (label centres, points)
CBAR_TICK_HI = (71.00, 1.2e-17)      # "1.2e-17"
CBAR_TICK_LO = (177.56, 2.0e-18)     # "2e-18"
PX_PER_PT = 3.3925                   # 587 px / (482.612-309.548) pt

N_DOPP, N_DELAY = 20, 36


def load_raster(pdf_path):
    """Extract the embedded CMYK JPEG for Figure 9 and return it as an array."""
    import io

    import pypdf
    from PIL import Image

    reader = pypdf.PdfReader(str(pdf_path))
    xobj = reader.pages[PAGE_INDEX]["/Resources"]["/XObject"][XOBJECT].get_object()
    assert xobj["/ColorSpace"] == "/DeviceCMYK", xobj["/ColorSpace"]
    img = Image.open(io.BytesIO(xobj._data))
    arr = np.asarray(img).astype(float)
    assert arr.shape == (443, 587, 4), arr.shape
    return arr


def digitise(cmyk):
    """Invert the figure's own colourbar to recover Watts per pixel."""
    rows = np.arange(CBAR_Y0, CBAR_Y1)
    lut = cmyk[rows, CBAR_X0:CBAR_X1].mean(axis=1)          # (n, 4)

    y_hi = (CBAR_TICK_HI[0] - IMG_T) * PX_PER_PT
    y_lo = (CBAR_TICK_LO[0] - IMG_T) * PX_PER_PT
    slope = (CBAR_TICK_HI[1] - CBAR_TICK_LO[1]) / (y_lo - y_hi)
    lut_val = CBAR_TICK_HI[1] - (rows - y_hi) * slope

    plot = cmyk[:, :PLOT_X1 + 2].reshape(-1, 4)
    dist = ((plot[:, None, :] - lut[None, :, :]) ** 2).sum(-1)
    nearest = dist.argmin(1)
    residual = np.sqrt(dist.min(1))
    watts = lut_val[nearest].reshape(cmyk.shape[0], PLOT_X1 + 2)
    return watts, residual, (lut_val[0], lut_val[-1])


def bin_to_grid(watts):
    """Median-reduce the raster onto the 20 x 36 DDM grid (row 0 = -2 chips)."""
    xe = np.linspace(PLOT_X0, PLOT_X1, N_DOPP + 1)
    ye = np.linspace(PLOT_Y0, PLOT_Y1, N_DELAY + 1)
    g = np.empty((N_DELAY, N_DOPP))
    for i in range(N_DELAY):
        for j in range(N_DOPP):
            cell = watts[int(ye[i]) + 3:int(ye[i + 1]) - 2,
                         int(xe[j]) + 5:int(xe[j + 1]) - 4]
            g[i, j] = np.median(cell)
    return g[::-1]          # flip: PDF row 0 is the top (+7 chips)


def ascii_map(a, label):
    print(f"\n{label}")
    ramp = " .:-=+*#%@"
    for i in range(N_DELAY - 1, -1, -1):
        row = "".join(ramp[min(9, int(a[i, j] / a.max() * 9.999))] for j in range(N_DOPP))
        print(f"{-2 + 0.25 * (i + 0.5):6.2f} |{row}|")
    print("       " + "-" * (N_DOPP + 2))


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF_DEFAULT
    if not pdf_path.exists():
        sys.exit(f"PDF not found: {pdf_path}")

    cmyk = load_raster(pdf_path)
    watts, residual, ends = digitise(cmyk)
    print(f"colourbar range     : {ends[1]:.3e} .. {ends[0]:.3e} W")
    print(f"colour match resid. : median {np.median(residual):.1f}, "
          f"p95 {np.percentile(residual, 95):.1f} (0-255 per-channel)")

    pub = bin_to_grid(watts)
    np.savez("figure9_ddm_published.npz", ddm_watts=pub)

    sim_file = Path(__file__).resolve().parent / "figure9_ddm.npz"
    if not sim_file.exists():
        sys.exit("run recreate_figure9.py first to produce figure9_ddm.npz")
    sim = np.load(sim_file)["ddm_watts"]

    print(f"\npeak published       : {pub.max():.3e} W ({10*np.log10(pub.max()):+.1f} dBW)")
    print(f"peak simulated       : {sim.max():.3e} W ({10*np.log10(sim.max()):+.1f} dBW)")
    print(f"peak ratio sim/pub   : {sim.max()/pub.max():.3f}")

    pi = np.unravel_index(pub.argmax(), pub.shape)
    si = np.unravel_index(sim.argmax(), sim.shape)
    for tag, k in (("published", pi), ("simulated", si)):
        print(f"peak cell {tag:9s}: Doppler {-5.25 + 0.5*(k[1]+0.5):+.2f} kHz, "
              f"delay {-2 + 0.25*(k[0]+0.5):+.2f} chips")

    # Agreement over the signal-bearing region
    mask = pub > 0.1 * pub.max()
    rel = np.abs(sim[mask] - pub[mask]) / pub[mask]
    print(f"\nover cells >10% peak ({mask.sum()} cells):")
    print(f"  median |rel. error| : {np.median(rel)*100:.1f}%")
    print(f"  p90    |rel. error| : {np.percentile(rel, 90)*100:.1f}%")
    print(f"  correlation         : {np.corrcoef(pub[mask], sim[mask])[0,1]:.4f}")
    print(f"  correlation (all)   : {np.corrcoef(pub.ravel(), sim.ravel())[0,1]:.4f}")

    ascii_map(pub, "PUBLISHED (digitised from PDF)")
    ascii_map(sim, "SIMULATED (recreate_figure9.py)")

    # Horseshoe arm: Doppler of the row maximum vs. delay
    print("\nhorseshoe arm location (Doppler of row max, kHz):")
    print(" delay   published  simulated")
    for i in range(1, N_DELAY, 3):
        if pub[i].max() < 0.05 * pub.max():
            continue
        dp = -5.25 + 0.5 * (abs(pub[i]).argmax() + 0.5)
        ds = -5.25 + 0.5 * (abs(sim[i]).argmax() + 0.5)
        print(f"{-2 + 0.25*(i+0.5):6.2f}    {abs(dp):5.2f}      {abs(ds):5.2f}")


if __name__ == "__main__":
    main()
