# Assignment 2 — Recreating Figure 9

**Source paper:** V. U. Zavorotny, S. Gleason, E. Cardellach, A. Camps, "Tutorial on Remote Sensing Using GNSS Bistatic Radar of Opportunity," *IEEE Geoscience and Remote Sensing Magazine*, vol. 2, no. 4, pp. 8–45, December 2026.

**Figure caption (original):** *"Example of the noise-free DDM generated using the CYGNSS End to End Simulator (E2ES) under the following conditions: receiver altitude: 500 km, reflection incidence angle: 20°, 11 dBi receiver antenna gain, wind speed: 5 m/s."*

---

## Approach: Physics over pixel-tracing

The first decision was *how* to recreate the figure. Two options existed:

1. **Digitise the bitmap** — invert the colormap, extract pixel values, replot
2. **Regenerate from physics** — implement the actual model equations from the paper

I chose **option 2**. The figure comes from a simulator (CYGNSS E2ES), so replicating the physics is a truer recreation than tracing pixels. It also means the result is reusable — you can change wind speed, altitude, or incidence angle and get a new valid DDM.

---

## Equations Used

### Bistatic Radar Equation (Eq. 11)

The DDM is the ensemble mean of the correlation power as a function of time delay τ and frequency offset f:

$$
\langle |Y(\tau, f)|^2 \rangle = \frac{\lambda^2}{(4\pi)^3} T_i^2 \, P_t G_t \iint \frac{G_r}{R_t^2 R_r^2} \, |\chi(\tau, f)|^2 \, \sigma_0 \, dS
$$

where:
- $\lambda$ is the carrier wavelength (GPS L1: 0.1903 m)
- $T_i$ is the coherent integration time (1 ms for C/A code)
- $P_t G_t$ is the transmitter Effective Isotropic Radiated Power (EIRP)
- $G_r$ is the receiver antenna gain pattern (11 dBi, assumed isotropic)
- $R_t$, $R_r$ are distances from the surface point to the transmitter and receiver respectively
- $|\chi(\tau, f)|^2$ is the Woodward Ambiguity Function (WAF)
- $\sigma_0$ is the normalised bistatic radar cross section (BRCS)
- $dS$ is the surface area element

### Woodward Ambiguity Function — WAF factorisation

The WAF is factored as the product of a delay response and a Doppler response:

$$
|\chi(\tau, f)|^2 = \Lambda^2(\tau) \cdot |S(f)|^2
$$

where $\Lambda(\tau)$ is the triangular C/A code correlation function (half-width one chip, $\tau_c = c / f_{\text{chip}} \approx 293$ m):

$$
\Lambda(\tau) = \max\!\left(1 - \frac{|\tau|}{\tau_c},\; 0\right)
$$

and $S(f)$ is the sinc-shaped Doppler response set by the coherent integration time $T_i$:

$$
|S(f)|^2 = \text{sinc}^2(f \, T_i)
$$

The width of $\Lambda$ determines the equi-range annulus zone width; the width of $S$ determines the equi-Doppler zone width ($\Delta f_{\text{Dop}} = 2/T_i = 2$ kHz for $T_i = 1$ ms).

### Normalised BRCS — KA-GO (Eq. 12)

The normalised bistatic radar cross section is computed from the geometric-optics limit of the Kirchhoff approximation:

$$
\sigma_0 = \pi |\mathcal{R}_0|^2 \left(\frac{|\mathbf{q}|}{q_z}\right)^4 P\!\left(-\frac{\mathbf{q}_\perp}{q_z}\right)
$$

where:
- $\mathcal{R}_0$ is the Fresnel reflection coefficient evaluated at the local specular facet angle
- $\mathbf{q} = k(\hat{n} - \hat{m})$ is the scattering vector ($\hat{m}$ = incident direction, $\hat{n}$ = scattered direction, $k = 2\pi/\lambda$)
- $q_z$ is the vertical component of $\mathbf{q}$
- $\mathbf{q}_\perp / q_z$ gives the local surface slope required to specularly link transmitter and receiver at that point
- $P(\mathbf{s})$ is the probability density function of surface slopes

This model is valid for quasi-specular forward scattering of L-band LHCP waves, which is exactly the CYGNSS geometry.

### Fresnel Reflection Coefficient

For RHCP-transmit / LHCP-receive (the CYGNSS antenna configuration), the effective reflection coefficient is:

$$
\mathcal{R}_{LR} = \frac{1}{2}(R_{HH} - R_{VV})
$$

$$
R_{HH} = \frac{\cos\theta_i - \sqrt{\varepsilon_r - \sin^2\theta_i}}{\cos\theta_i + \sqrt{\varepsilon_r - \sin^2\theta_i}}, \qquad
R_{VV} = \frac{\varepsilon_r \cos\theta_i - \sqrt{\varepsilon_r - \sin^2\theta_i}}{\varepsilon_r \cos\theta_i + \sqrt{\varepsilon_r - \sin^2\theta_i}}
$$

where $\varepsilon_r \approx 73 - 59i$ is the complex dielectric permittivity of sea water at L-band. At 20° incidence this gives $|\mathcal{R}_{LR}|^2 \approx 0.677$.

### Mean-Square Slopes and the Slope PDF (Eq. 14)

The slope variance (mean-square slope, MSS) is obtained by integrating the surface elevation spectrum $W(\mathbf{l})$ up to a spectral cut-off wavenumber $l^*$ appropriate for L-band:

$$
\sigma^2_{x,y} = \iint_{|\mathbf{l}| \leq l^*} l^2_{x,y} \, W(\mathbf{l}) \, d^2l
$$

Separate MSS values are used along the up-wind ($\sigma_u^2$) and cross-wind ($\sigma_c^2$) directions to capture ocean wave anisotropy. These were computed from the L-band-filtered Cox-Munk / Katzberg wind model (ref. [21] of the paper) at $U_{10} = 5$ m/s:

$$
\sigma_u^2 = 0.45 \times 0.00316\,f(U_{10}), \qquad \sigma_c^2 = 0.45 \times (0.003 + 0.00192\,f(U_{10}))
$$

where the 0.45 factor is the L-band spectral cut-off scale factor and $f(U_{10}) = 6\ln(U_{10}) - 4$ for $3.49 \leq U_{10} < 46$ m/s.

The slope PDF is a bivariate Gaussian:

$$
P(s_x, s_y) = \frac{1}{2\pi\sigma_u\sigma_c} \exp\!\left(-\frac{s_x^2}{2\sigma_u^2} - \frac{s_y^2}{2\sigma_c^2}\right)
$$

### Equi-Doppler Lines (Eq. 15)

The Doppler frequency offset at any surface point is given by the relative velocities of transmitter and receiver projected onto the incident and scattered unit vectors:

$$
\Delta f = -\frac{f_c}{c}\left[\mathbf{V}_{TX} \cdot \hat{m}(\mathbf{r}) - \mathbf{V}_{RX} \cdot \hat{n}(\mathbf{r})\right]
$$

referenced to the value at the nominal specular point so that the DDM peak sits at $\Delta f = 0$. The loci of constant $\Delta f$ on the surface are hyperbolae, forming the equi-Doppler lines visible in Fig. 8a of the paper.

---

## Implementation Choices

### Surface integration grid
A 1401 × 1401 point grid centred on the specular point, extending ±320 km, was used. At 500 km altitude and 20° incidence the glistening zone extends several hundred kilometres; this grid fully encloses it while keeping the computation under 2 seconds.

### DDM output grid
The axes (Doppler range −5.25 to +4.75 kHz, delay range −2 to +7 chips, 500 Hz × 0.25 chip sampling) were **measured directly from the published figure** by extracting tick-label coordinates from the PDF text layer and fitting a linear pixel-to-physical-unit mapping. This gave sub-pixel accurate axis calibration without having to guess the CYGNSS DDM sampling format. The result is 20 Doppler bins × 36 delay bins.

### Geometry
The caption states altitude (500 km), incidence angle (20°), and antenna gain (11 dBi) but not the transmitter or receiver velocity vectors. An in-plane geometry was assumed — receiver and transmitter velocities both in the incidence plane — using typical LEO (~7.6 km/s) and GPS (~3.9 km/s) orbital speeds. This produces the symmetric horseshoe shape. Any residual asymmetry between the two arms in the published figure likely reflects the true off-plane E2ES geometry, which is not published.

### GPS EIRP
Set to 26.8 dBW for GPS L1 C/A, the nominal block IIF value. This is not stated in the paper and is the primary source of the ~3% amplitude offset between simulation and publication.

---

## Verification

Rather than eyeballing the result, the published DDM was independently digitised from the PDF and compared numerically against the simulation.

**Digitisation method:** The figure's own colorbar was inverted in native CMYK space (avoiding CMYK→RGB conversion artefacts). Tick-label positions extracted from the PDF text layer (`1.2e-17` at cy = 71.00 pt, `2e-18` at cy = 177.56 pt) provided the linear Watts-per-pixel calibration. Median colour-match residual was 1.7/255 per channel.

**Metrics:**

| Metric | Published | Simulated |
|---|---|---|
| Peak power | 1.216 × 10⁻¹⁷ W (−169.2 dBW) | 1.179 × 10⁻¹⁷ W (−169.3 dBW) |
| Peak cell location | 0.00 kHz, +0.38 chips | 0.00 kHz, +0.38 chips |
| Full-grid correlation | — | **0.975** |
| Median \|rel. error\| (cells > 10% peak) | — | 14.4% |

The peak power agrees to within 3%, the peak cell location is identical, and the full-grid correlation of 0.975 confirms the overall DDM shape and power distribution are well reproduced. The −169.3 dBW peak is also independently consistent with Figure 10 of the same paper, which shows peak DDM power at 5 m/s wind speed of approximately −169 dBW.

---

## Output Files

| File | Description |
|---|---|
| `figure9_ddm/recreate_figure9.py` | Main simulation script |
| `figure9_ddm/verify_against_pdf.py` | Digitises published figure and runs comparison |
| `figure9_ddm/compare_side_by_side.py` | Generates side-by-side comparison plot |
| `figure9_ddm/figure9_recreated.png` | Recreated Figure 9 |
| `figure9_ddm/figure9_comparison.png` | Side-by-side: published vs. recreated + delay waveform cut |
| `figure9_ddm/figure9_ddm.npz` | Simulated DDM data (Doppler axis Hz, delay axis chips, power in W) |
| `figure9_ddm/figure9_ddm_published.npz` | Digitised published DDM data |
