#!/usr/bin/env python3
"""
Recreation of Figure 9 from:

    V. U. Zavorotny, S. Gleason, E. Cardellach, A. Camps,
    "Tutorial on Remote Sensing Using GNSS Bistatic Radar of Opportunity,"
    IEEE Geoscience and Remote Sensing Magazine, vol. 2, no. 4, pp. 8-45, Dec. 2014.
    (IEEE_GRSM_GNSSR_Tutorial_06985926.pdf, p. 21)

Original caption
----------------
"FIGURE 9. Example of the noise-free DDM generated using the CYGNSS End to End
Simulator (E2ES) under the following conditions: receiver altitude: 500 km,
reflection incidence angle: 20 deg, 11 dBi receiver antenna gain,
wind speed: 5 m/s."

Approach
--------
The DDM is regenerated from the bistatic radar equation given as Eq. (11) of the
same paper (the Zavorotny-Voronovich model):

    <|Y(tau,f)|^2> = (lambda^2 / (4 pi)^3) * Pt*Gt
                     * Integral[ Gr * |chi(tau,f)|^2 * sigma0 / (Rt^2 Rr^2) ] dS

with

  * the Woodward Ambiguity Function factorised as in the paper,
    |chi|^2 = Lambda^2(tau) * |S(f)|^2, where Lambda is the triangular C/A code
    correlation (half-width 1 chip) and S is the sinc-shaped Doppler response of
    width 2/Ti (Ti = 1 ms coherent integration);

  * sigma0 from the geometric-optics limit of the Kirchhoff approximation,
    Eq. (12):  sigma0 = pi |Re|^2 (q/qz)^4 P(-q_perp/qz), with a bivariate
    Gaussian slope PDF whose mean-square slopes follow the L-band-filtered
    Cox-Munk/Katzberg wind model (Eq. (14) discussion, ref. [21] of the paper).

The output grid matches the CYGNSS DDM sampling read off the published figure:
20 Doppler bins of 500 Hz and 36 delay bins of 0.25 chip.

Usage:  python3 recreate_figure9.py
Writes: figure9_recreated.png / .pdf  and  figure9_ddm.npz
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ----------------------------------------------------------------------------
# Physical and signal constants
# ----------------------------------------------------------------------------
C_LIGHT = 2.99792458e8          # m/s
F_L1 = 1575.42e6                # Hz, GPS L1 carrier
LAMBDA = C_LIGHT / F_L1         # m, ~0.1903
CHIP_RATE = 1.023e6             # chips/s, C/A code
CHIP_LEN = C_LIGHT / CHIP_RATE  # m, ~293.05
T_COH = 1.0e-3                  # s, coherent integration time

EIRP_DBW = 26.8                 # dBW, GPS L1 C/A effective isotropic radiated power
PT_GT = 10.0 ** (EIRP_DBW / 10.0)

R_EARTH = 6371.0e3              # m
H_GPS = 20200.0e3               # m, GPS orbit altitude

# ----------------------------------------------------------------------------
# Scenario from the Figure 9 caption
# ----------------------------------------------------------------------------
H_RX = 500.0e3                  # m, receiver altitude
THETA_INC = np.deg2rad(20.0)    # reflection incidence angle
GR_DBI = 11.0                   # dBi, receiver antenna gain
GR_LIN = 10.0 ** (GR_DBI / 10.0)
U10 = 5.0                       # m/s, wind speed

V_RX = 7.6e3                    # m/s, LEO receiver speed
V_TX = 3.9e3                    # m/s, GPS transmitter speed

# DDM output grid (CYGNSS sampling, as measured from the published figure)
N_DOPP, N_DELAY = 20, 36
DOPP_STEP = 500.0               # Hz per Doppler bin
DELAY_STEP = 0.25               # chips per delay bin
DOPP_MIN = -5.25e3              # Hz, left edge of first Doppler bin
DELAY_MIN = -2.0                # chips, bottom edge of first delay bin


# ----------------------------------------------------------------------------
# Surface and electromagnetic models
# ----------------------------------------------------------------------------
def mean_square_slopes(u10):
    """L-band-filtered mean-square slopes (up/cross-wind) vs. 10-m wind speed.

    Cox-Munk relations rescaled for the L-band slope cut-off of Eq. (14),
    following the Katzberg effective-wind formulation used by the CYGNSS E2ES.
    """
    if u10 <= 3.49:
        f = u10
    elif u10 < 46.0:
        f = 6.0 * np.log(u10) - 4.0
    else:
        f = 0.411 * u10
    scale = 0.45                       # L-band spectral-cut-off factor
    mss_up = scale * (0.00316 * f)
    mss_cross = scale * (0.003 + 0.00192 * f)
    return mss_up, mss_cross


def fresnel_lhcp(theta_i, eps_r=complex(73.0, -59.0)):
    """|Re|^2 for an RHCP wave reflected into LHCP off sea water."""
    ct = np.cos(theta_i)
    s = np.sqrt(eps_r - np.sin(theta_i) ** 2)
    r_hh = (ct - s) / (ct + s)
    r_vv = (eps_r * ct - s) / (eps_r * ct + s)
    r_lr = 0.5 * (r_hh - r_vv)
    return np.abs(r_lr) ** 2


def waf_delay(dtau_chips):
    """Lambda^2: squared triangular C/A correlation, half-width one chip."""
    return np.clip(1.0 - np.abs(dtau_chips), 0.0, None) ** 2


def waf_doppler(df_hz, t_coh=T_COH):
    """|S(f)|^2: squared sinc Doppler response, width 2/Ti."""
    return np.sinc(df_hz * t_coh) ** 2


# ----------------------------------------------------------------------------
# Bistatic geometry
# ----------------------------------------------------------------------------
def build_geometry():
    """Specular point at the origin; incidence plane = x-z plane.

    Transmitter towards -x, receiver towards +x, both velocities in-plane so
    that equi-Doppler lines run across the incidence plane (the symmetric
    configuration sketched in Fig. 8a of the paper).
    """
    st, ct = np.sin(THETA_INC), np.cos(THETA_INC)

    r_rx = H_RX / ct                       # slant range, specular -> receiver
    rx = np.array([r_rx * st, 0.0, H_RX])

    # Slant range specular -> GPS using spherical geometry at 20 deg incidence
    r_sat = R_EARTH + H_GPS
    elev = 0.5 * np.pi - THETA_INC
    r_tx = -R_EARTH * np.sin(elev) + np.sqrt(
        r_sat ** 2 - (R_EARTH * np.cos(elev)) ** 2
    )
    tx = np.array([-r_tx * st, 0.0, r_tx * ct])

    # In-plane velocities (receiver flying along +x, transmitter opposing)
    v_rx = V_RX * np.array([np.cos(np.deg2rad(8.0)), 0.0, -np.sin(np.deg2rad(8.0))])
    v_tx = V_TX * np.array([-0.35, 0.0, -0.20])
    v_tx *= V_TX / np.linalg.norm(v_tx)

    return tx, rx, v_tx, v_rx


def delay_doppler_sigma0(X, Y, tx, rx, v_tx, v_rx):
    """Per-surface-point delay (chips), Doppler (Hz), sigma0 and 1/(Rt^2 Rr^2)."""
    P = np.stack([X, Y, np.zeros_like(X)], axis=-1)

    d_tx = P - tx                      # transmitter -> surface
    d_rx = rx - P                      # surface -> receiver
    Rt = np.linalg.norm(d_tx, axis=-1)
    Rr = np.linalg.norm(d_rx, axis=-1)

    m_hat = d_tx / Rt[..., None]       # incident propagation direction
    n_hat = d_rx / Rr[..., None]       # scattered propagation direction

    # Excess path delay relative to the nominal specular point
    Rt0 = np.linalg.norm(tx)
    Rr0 = np.linalg.norm(rx)
    delay_chips = ((Rt + Rr) - (Rt0 + Rr0)) / CHIP_LEN

    # Doppler, Eq. (15): Df = -(f/c) [ Vtx.m - Vrx.n ], referenced to the
    # nominal specular point so that the DDM peak sits near 0 Hz.
    m0 = -tx / Rt0
    n0 = rx / Rr0
    dopp0 = -(F_L1 / C_LIGHT) * (m0 @ v_tx - n0 @ v_rx)
    dopp = -(F_L1 / C_LIGHT) * (m_hat @ v_tx - n_hat @ v_rx) - dopp0

    # --- sigma0, geometric optics limit of the Kirchhoff approximation ------
    k = 2.0 * np.pi / LAMBDA
    q = k * (n_hat - m_hat)            # scattering vector
    qz = q[..., 2]
    q_mag = np.linalg.norm(q, axis=-1)

    # local slope of the specular facet required to link Tx and Rx
    sx = -q[..., 0] / qz
    sy = -q[..., 1] / qz

    mss_u, mss_c = mean_square_slopes(U10)
    pdf = np.exp(-0.5 * (sx ** 2 / mss_u + sy ** 2 / mss_c)) / (
        2.0 * np.pi * np.sqrt(mss_u * mss_c)
    )

    # local incidence angle on the tilted facet, for the Fresnel coefficient
    cos_loc = np.clip(0.5 * q_mag / k, -1.0, 1.0)
    refl = fresnel_lhcp(np.arccos(cos_loc))

    sigma0 = np.pi * refl * (q_mag / np.abs(qz)) ** 4 * pdf

    return delay_chips, dopp, sigma0, 1.0 / (Rt ** 2 * Rr ** 2)


# ----------------------------------------------------------------------------
# DDM synthesis
# ----------------------------------------------------------------------------
def simulate_ddm(half_width=320.0e3, n_grid=1401):
    """Integrate the bistatic radar equation onto the delay-Doppler grid."""
    tx, rx, v_tx, v_rx = build_geometry()

    # Surface grid centred on the specular point
    s = np.linspace(-half_width, half_width, n_grid)
    dA = (s[1] - s[0]) ** 2
    X, Y = np.meshgrid(s, s, indexing="xy")

    delay, dopp, sigma0, inv_r4 = delay_doppler_sigma0(X, Y, tx, rx, v_tx, v_rx)

    # Scalar prefactor of Eq. (11)
    pre = LAMBDA ** 2 / (4.0 * np.pi) ** 3 * PT_GT
    weight = pre * GR_LIN * inv_r4 * sigma0 * dA     # Watts per surface cell

    # Bin centres of the output DDM
    dopp_ax = DOPP_MIN + DOPP_STEP * (np.arange(N_DOPP) + 0.5)
    delay_ax = DELAY_MIN + DELAY_STEP * (np.arange(N_DELAY) + 0.5)

    # Only cells that can contribute through the WAF support
    live = (
        (delay > delay_ax[0] - 1.5)
        & (delay < delay_ax[-1] + 1.5)
        & (dopp > dopp_ax[0] - 3.0e3)
        & (dopp < dopp_ax[-1] + 3.0e3)
        & (weight > 0.0)
    )
    d_l, f_l, w_l = delay[live], dopp[live], weight[live]

    ddm = np.zeros((N_DELAY, N_DOPP))
    for i, tau in enumerate(delay_ax):
        g_tau = waf_delay(tau - d_l)
        hit = g_tau > 0.0
        if not np.any(hit):
            continue
        wt = w_l[hit] * g_tau[hit]
        fh = f_l[hit]
        for j, fc in enumerate(dopp_ax):
            ddm[i, j] = np.sum(wt * waf_doppler(fc - fh))

    return dopp_ax, delay_ax, ddm


# ----------------------------------------------------------------------------
# Plotting, styled to match the published figure
# ----------------------------------------------------------------------------
def plot_figure9(dopp_ax, delay_ax, ddm, outstem="figure9_recreated"):
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.linewidth": 0.6,
        "xtick.direction": "out",
        "ytick.direction": "out",
    })

    extent = [
        (dopp_ax[0] - DOPP_STEP / 2) / 1e3,
        (dopp_ax[-1] + DOPP_STEP / 2) / 1e3,
        delay_ax[0] - DELAY_STEP / 2,
        delay_ax[-1] + DELAY_STEP / 2,
    ]

    fig, ax = plt.subplots(figsize=(4.3, 3.25))
    im = ax.imshow(
        ddm,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="jet",
        interpolation="nearest",
        vmin=0.0,
    )

    ax.set_xlabel("Doppler (kHz)")
    ax.set_ylabel("Delay (Chips)")
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.set_xlim(-5.25, 4.75)
    ax.set_ylim(-2.0, 7.0)

    cbar = fig.colorbar(im, ax=ax, pad=0.03, fraction=0.055)
    cbar.set_label("Watts")
    cbar.outline.set_linewidth(0.6)
    cbar.locator = MultipleLocator(2e-18)
    cbar.update_ticks()

    def fmt_sci(v, _pos):
        """Render ticks as in the published figure: 2e-18 ... 1e-17, 1.2e-17."""
        if v == 0:
            return "0"
        exp = int(np.floor(np.log10(abs(v))))
        man = v / 10.0 ** exp
        man_s = f"{man:g}"
        return f"{man_s}e{exp}" if man_s != "1" else f"1e{exp}"

    cbar.ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(fmt_sci))

    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(f"{outstem}.{ext}", dpi=300, bbox_inches="tight")
    print(f"wrote {outstem}.png / {outstem}.pdf")
    return fig


def main():
    dopp_ax, delay_ax, ddm = simulate_ddm()

    pk = np.unravel_index(np.argmax(ddm), ddm.shape)
    print(f"grid                : {N_DOPP} Doppler x {N_DELAY} delay bins "
          f"({DOPP_STEP:.0f} Hz, {DELAY_STEP} chip)")
    print(f"peak power          : {ddm.max():.3e} W "
          f"({10*np.log10(ddm.max()):.1f} dBW)")
    print(f"peak location       : Doppler {dopp_ax[pk[1]]/1e3:+.2f} kHz, "
          f"delay {delay_ax[pk[0]]:+.2f} chips")
    mss_u, mss_c = mean_square_slopes(U10)
    print(f"MSS (up/cross)      : {mss_u:.5f} / {mss_c:.5f}  at U10 = {U10} m/s")
    print(f"|Fresnel_LHCP|^2    : {fresnel_lhcp(THETA_INC):.3f}")

    np.savez("figure9_ddm.npz", doppler_hz=dopp_ax, delay_chips=delay_ax, ddm_watts=ddm)
    plot_figure9(dopp_ax, delay_ax, ddm)


if __name__ == "__main__":
    main()
