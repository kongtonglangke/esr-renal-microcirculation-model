# Supplementary Note S1 — The inverse calibration, written out

**Purpose.** Section 2.6 of the manuscript states that the mapping from ESR to the aggregation parameter k₀ was not assumed but obtained by *inverting* a published clinical whole-blood viscosity increment. This note gives the complete algebra, the source data with its actual sample size, and an uncertainty analysis of the two recovered quantities. It is provided so that the calibration can be repeated exactly.

---

## S1.1 The two unknowns and the two constraints

The Quemada law used throughout the model is

    η(γ̇) = η_p · (1 − k H / 2)⁻² ,      k(γ̇) = (k₀ + k∞ √(γ̇/γ̇_c)) / (1 + √(γ̇/γ̇_c)),

with H the tube haematocrit and, at H = 0.42, the Cokelet (1987) haematocrit-dependent parameterisation

    k₀(H) = exp(3.874 − 10.410 H + 13.800 H² − 6.738 H³),
    k∞(H) = exp(1.3435 − 2.803 H + 2.711 H² − 0.6479 H³),
    γ̇_c(H) = exp(−6.1508 + 27.923 H − 25.600 H² + 3.697 H³),

evaluated at H = 0.42 as k₀ = 4.2077, k∞ = 1.8157, γ̇_c = 3.7997 s⁻¹, with reference plasma viscosity η_p = 1.30 mPa·s.

Two quantities are unknown and are solved for simultaneously:

- **φ** — the *multiplicative* increase in plasma viscosity (the fibrinogen-borne part of the rheological change);
- **k₀,high** — the value of the aggregation parameter in the "elevated ESR" state (the cell-borne part).

## S1.2 The source measurement, with its actual sample size

The calibration target is the whole-blood viscosity increment measured by McGinley and colleagues in nephrotic syndrome (ref. 2; PMID 6410531). Because the precision of the target governs the precision of the calibration, the source is quoted here in full rather than cited in passing:

> Blood viscosity and its major determinants (haematocrit, plasma viscosity and fibrinogen) as well as several haemostatic variables were measured in **21 patients with the nephrotic syndrome, and 21 controls matched for age, sex, smoking habit and serum creatinine**. Blood viscosity was significantly increased in the nephrotic group, measured at a **low shear rate (mean increase 41%, p < 0.01) and at a high shear rate (mean increase 25%, p < 0.01)**. Haematocrit was not significantly increased, but plasma viscosity was significantly higher (p < 0.01), associated with increased plasma macroglobulins especially fibrinogen, which was increased to double the plasma concentration of the control group (p < 0.01).
>
> — Abstract, *Thromb Haemost* 1983;49(3):155–157.

Three properties of this source matter for the calibration:

1. **The haematocrit was not significantly raised.** This is what licenses attributing the entire viscosity increment to the two unknowns φ and k₀,high; had haematocrit differed, a third unknown would have been required.
2. **The design is matched (21 vs 21), and both increments are significant at p < 0.01.** The source gives a mean increment but no standard deviation for the increment itself; the ±10-percentage-point band used below is therefore a deliberately conservative envelope, not the study's own confidence interval.
3. **The perturbation is large.** A 41% viscosity rise is at the upper end of what is seen clinically, so the calibration is a high-signal anchor; it also means that the recovered amplification is more likely to be an over- than an under-estimate of the physiological range.

## S1.3 The equations actually solved

Writing γ̇_lo = 1 s⁻¹ and γ̇_hi = 100 s⁻¹, and defining the *reference* viscosities at k₀ = k₀,high = k₀(H) and φ = 1 as b_lo and b_hi, the two residuals are

    f₁(φ, k₀,high) = φ · (1 − k(1,     k₀,high) · H/2)⁻² · η_p − 1.41 · b_lo = 0,
    f₂(φ, k₀,high) = φ · (1 − k(100,   k₀,high) · H/2)⁻² · η_p − 1.25 · b_hi = 0.

This is a determinate (2 × 2) algebraic system because the two observations are at shear rates far apart on the Quemada curve, so they constrain φ and k₀,high almost independently. It was solved with a Newton-type solver (`scipy.optimize.fsolve`) from the starting point (φ, k₀,high) = (1.15, 4.6); convergence was verified.

## S1.4 Central solution

| Quantity | Value |
|---|---|
| Plasma-viscosity multiple φ | **1.2281** |
| k₀ in the elevated state, k₀,high | **4.3455** |
| Implied amplification k₀,high / k₀(H) | **1.0328×** |
| Published clinical range of k₀ (ref. 12) | 3.05 – 4.36 |
| Recovered k₀,high inside that range? | **Yes** |

The independent consistency check — that the recovered k₀,high falls inside the range measured directly by viscosimetry in clinical blood samples — is the reason this calibration is treated as a constraint rather than as curve fitting.

## S1.5 Uncertainty of the two recovered quantities

The solver was re-run across a grid of perturbations of the two targets, ±10 percentage points on each in 5-point steps (25 combinations; full table in *Supplementary Table S2*).

| | minimum | maximum |
|---|---|---|
| φ over the ±10 pp grid | 1.107 | 1.356 |
| amplification over the ±10 pp grid | 0.991 | 1.071 |

One factor at a time:

| Perturbation | φ | amplification |
|---|---|---|
| low-shear target 1.31× (−10 pp) | 1.241 | 1.013× |
| low-shear target 1.41× (central) | 1.228 | 1.033× |
| low-shear target 1.51× (+10 pp) | 1.216 | 1.050× |
| high-shear target 1.15× (−10 pp) | 1.117 | 1.054× |
| high-shear target 1.25× (central) | 1.228 | 1.033× |
| high-shear target 1.35× (+10 pp) | 1.341 | 1.012× |

Two consequences are worth stating plainly.

- The **plasma-borne fraction is robust**: φ stays between 1.11 and 1.36 across the whole grid, so the qualitative conclusion of Section 3.8 — that most of the clinical viscosity rise is plasma-borne rather than cell-borne — does not depend on the exact targets.
- The **cell-borne amplification is small in every case** (0.99–1.07×). Even at the most favourable corner of the grid it is 1.07×, which is still far below the ≈1.15× that Section 3.7 shows would be needed for a flow-curve fold. The stasis conclusion is therefore insensitive to the calibration.
- Ten of the 25 grid points place the recovered k₀,high marginally outside the published clinical range (3.05–4.36). All of the failures are at the corners where the high-shear target is displaced downwards, i.e. where the fit demands more aggregation than viscosimetry reports. This is reported rather than hidden: it means the calibration is consistent with the clinical range only within roughly ±5 percentage points of the published increments, and it is an additional reason for treating the absolute magnitudes as provisional while treating the *gating* — which follows from the functional form of the Quemada law and not from these two numbers — as the robust result.

## S1.6 What the calibration does **not** determine

The calibration fixes the **absolute magnitude** of the low-shear viscosity increment. It does not affect:

- the shear-rate gating of the aggregation effect (Section 3.3), which follows from the shape of k(γ̇) and is independent of φ and k₀,high;
- the viscosity-independence of the mean wall shear stress (Section 3.4), which is an exact consequence of tube geometry;
- the thickening of the cell-free layer with aggregation (Section 3.5), which follows from mass conservation;
- the monotonic rise of the wall-stress coefficient of variation (Section 3.6), which is set by the gating of Equation (9).

These four results — the ones the paper's argument rests on — are therefore invariant to the uncertainty quantified above.

---

*Generated by `code/esr_model_v5_calibration.py`. Numerical output: `results/v5_calibration.json`, `results/v5_calibration_log.txt`, `CHM_submission/04_Supplementary/Supplementary_Table_S2_InverseCalibration_Sensitivity.csv`.*
