#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
esr_model_v3.py  --  replace the ASSUMED Stokes scaling of Layer 1 with a
MEASURED, literature-anchored mapping.

v0.2.0 took the ESR -> effective-aggregate-radius step to be a Stokes scaling
a ~ sqrt(ESR) and flagged that step as the weakest link in the model.

This version takes the step from measured data instead.  The chain is:

    ESR_1h  --(Westergren linear relation, r=0.990)-->  V_e
    V_e     --(hindered settling, phi=(1-Ht)^n, n=4.65)-->  V_s
    V_s     --(Stokes for a single aggregate)-->  alpha  (size parameter)
    R_agg   =  R_ef (1 + alpha)

All constants are from Higuchi & Watanabe, PLoS ONE 2022;17(7):e0270977:
    rho_e = 1100 kg/m^3, rho_p = 1025 kg/m^3, R_ef = 3.084e-6 m,
    mu_p  = 1.64e-3 Pa s,
    HAI = AI - k (Ht - 0.40)          with k = 0.284                 (Eq. 15)
    V_s = a (HAI - b)^4 + c           with a = 0.0541, b = 0.426     (Eq. 16)
    c   = 2 (rho_e - rho_p) g R_ef^2 / (9 mu_p)      (no-aggregation velocity)
    slope of the Westergren relation = 0.778

The scientific question this version answers is NOT "does the answer change"
(it largely does not) but "is the sqrt(ESR) scaling an arbitrary assumption,
or is it what the measured data imply?".  That is reported honestly either way.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
RES.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "savefig.dpi": 300, "figure.dpi": 300, "legend.frameon": False})
CB = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73",
      "verm": "#D55E00", "sky": "#56B4E9", "grey": "#999999", "black": "#000000"}

LOG = []
def say(s=""):
    print(s)
    LOG.append(str(s))

# ---------------------------------------------------------------- constants
RHO_E, RHO_P, G = 1100.0, 1025.0, 9.81          # kg/m^3 , m/s^2   (Higuchi refs 33,34)
R_EF  = 3.084e-6                                 # m               (Higuchi ref 13)
MU_P  = 1.64e-3                                  # Pa s            (Higuchi ref 35)
A16, B16, K_HAI  = 0.0541, 0.426, 0.284          # eqs 16, 15
N_HIND           = 4.65                          # Richardson-Zaki exponent
SLOPE_WG         = 0.778                         # Westergren -> V_e slope
MM_PER_MIN_TO_MS = 1e-3 / 60.0                   # 1 mm/min = 1.667e-5 m/s

C_NOAGG = 2.0 * (RHO_E - RHO_P) * G * R_EF**2 / (9.0 * MU_P)   # m/s
HT_REF  = 0.40                                   # Higuchi's max experimental Ht

ESR_GRID = [2, 5, 10, 20, 30, 40, 60, 80, 100]
ESR_REF  = 10.0


def ve_from_esr(esr, slope=SLOPE_WG):
    """Westergren ESR (mm/h) -> measured sedimentation velocity V_e (m/s)."""
    return slope * (np.asarray(esr, float) / 60.0) * MM_PER_MIN_TO_MS


def vs_from_ve(ve, Ht=HT_REF):
    """remove hindered settling:  V_e = V_s (1-Ht)^n  ->  V_s = V_e/(1-Ht)^n"""
    return ve / (1.0 - Ht) ** N_HIND


def alpha_from_vs(vs):
    """(1+alpha)^2 = V_s / c   (Stokes for a single aggregate)."""
    return np.sqrt(np.maximum(vs / C_NOAGG, 1.0)) - 1.0


def HAI_from_vs(vs):
    """invert eq (16):  V_s = a (HAI-b)^4 + c"""
    return B16 + ((np.maximum(vs - C_NOAGG, 0.0)) / A16) ** 0.25


# ------------------------------------------------------------------- main
def main():
    say("=" * 84)
    say("ESR -> renal microcirculation : MEASURED Layer-1 mapping   v0.3.0")
    say("=" * 84)
    say()
    say("[1] Literature constants used for the Layer-1 replacement")
    say(f"    rho_e  = {RHO_E:.0f} kg/m^3   rho_p = {RHO_P:.0f} kg/m^3   "
        f"(Higuchi refs 33,34)")
    say(f"    R_ef   = {R_EF:.4e} m        mu_p  = {MU_P*1e3:.2f} mPa.s (Higuchi refs 13,35)")
    say(f"    c (no-aggregation V_s, eq 2) = {C_NOAGG:.4e} m/s = {C_NOAGG*1e6:.4f} um/s")
    say(f"    eq15  HAI = AI - {K_HAI}(Ht - 0.40)")
    say(f"    eq16  V_s = {A16}(HAI - {B16})^4 + c")
    say(f"    hindered settling exponent n = {N_HIND} ; Westergren slope = {SLOPE_WG}")
    say()

    # ---------------- derived alpha(ESR) -------------------------------
    ve  = ve_from_esr(ESR_GRID)
    vs  = vs_from_ve(ve)
    al  = alpha_from_vs(vs)
    hai = HAI_from_vs(vs)
    one_plus = 1.0 + al
    tbl = pd.DataFrame({
        "ESR_mm_h": ESR_GRID,
        "V_e_um_s": ve * 1e6,
        "V_s_um_s": vs * 1e6,
        "HAI": hai,
        "alpha_measured": al,
        "R_agg_um_measured": one_plus * R_EF * 1e6,
    })
    say("[2] MEASURED Layer-1 mapping (Higuchi 2022), Ht = 0.40")
    say(tbl.to_string(index=False, float_format=lambda x: f"{x:10.4f}"))
    say()

    # ---------------- is it sqrt(ESR)? ---------------------------------
    ln = np.log(np.asarray(ESR_GRID, float))
    lnr = np.log(one_plus)
    expo = np.polyfit(ln, lnr, 1)[0]
    pred = np.exp(np.polyval(np.polyfit(ln, lnr, 1), ln))
    resid = (pred - one_plus) / one_plus * 100.0
    say("[3] Is the sqrt(ESR) scaling an assumption, or is it what the data imply?")
    say(f"    power-law fit  (1+alpha) ~ ESR^q  ->  q = {expo:.4f}")
    say(f"    reference assumption in v0.2.0        q = 0.5000")
    say(f"    maximum deviation of the measured mapping from a pure sqrt law: "
        f"{np.max(np.abs(resid)):.2f} %")
    say("    HONEST READING - this is an ALGEBRAIC IDENTITY, not an independent")
    say("    validation.  Every step of the chain is linear or proportional:")
    say("      V_s = c (1+alpha)^2         (Stokes, single aggregate)")
    say("      V_s ~ ESR                   (Westergren relation, measured, r=0.990)")
    say("      =>  (1+alpha) ~ sqrt(ESR)   identically.")
    say("    What the replacement therefore achieves is NOT a new numerical result")
    say("    but a CHANGE IN EPISTEMIC STATUS: the sqrt(ESR) scaling is no longer a")
    say("    free assumption; it follows from Stoke's law together with the")
    say("    measured near-linear Westergren relation.  The empirical content sits")
    say("    in the Westergren linearity (r = 0.990, n = 32), which is measurable")
    say("    and falsifiable.  We state this plainly rather than presenting a")
    say("    tautological '0 % deviation' as if it were a validation.")
    say()

    # ---------------- ratio check --------------------------------------
    rel = one_plus / one_plus[ESR_GRID.index(int(ESR_REF))]
    sqrt_law = np.sqrt(np.asarray(ESR_GRID, float) / ESR_REF)
    rel_tbl = pd.DataFrame({
        "ESR_mm_h": ESR_GRID,
        "R_agg_ratio_measured": rel,
        "R_agg_ratio_sqrt_law": sqrt_law,
        "pct_diff": (rel - sqrt_law) / sqrt_law * 100.0,
    })
    say("[4] Relative aggregate-size change, measured vs the v0.2.0 sqrt law")
    say(rel_tbl.to_string(index=False, float_format=lambda x: f"{x:12.5f}"))
    say()

    # ---------------- Ht sensitivity -----------------------------------
    say("[5] Ht sensitivity of the INFERRED aggregation (Higuchi eq 15)")
    say("    Eq 15 states  HAI = AI - k (Ht - 0.40), i.e.  AI = HAI + k (Ht - 0.40).")
    say("    If an uncorrected AI is read as though it were the HAI, the inferred")
    say("    aggregation state is biased by k*dHt, and V_s responds as the 4th")
    say("    power of (HAI - b).  At a typical elevated state this is large:")
    rows = []
    for dht in [0.00, 0.02, 0.05, 0.08]:
        h0 = 0.5686                              # HAI at ESR 10, Ht 0.40 (from table)
        h1 = h0 + K_HAI * dht                    # neglect of Ht correction -> overestimate
        ratio = ((max(h1 - B16, 0)) / (h0 - B16)) ** 4
        rows.append(dict(delta_Ht=dht, Ht=0.40 + dht, HAI_naive=h1,
                         V_s_bias_factor=ratio, pct_bias=(ratio - 1) * 100))
    say(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:12.4f}"))
    say("    -> a patient with Ht 0.45 whose uncorrected aggregation index is read")
    say("       as the corrected value will have their aggregation state OVER-")
    say("       estimated by about +40-45 %.  This quantitatively supports Sec. 3.7")
    say("       of the manuscript (\"ESR alone under-determines the rheology\") and")
    say("       identifies haematocrit, not ESR, as the missing covariate.")
    say()

    # ---------------- does the vessel-level conclusion change? ---------
    say("[6] Does the vessel-level conclusion change when Layer 1 is measured?")
    say(f"    The ONLY quantity that entered the vessel calculation from Layer 1 was")
    say(f"    the RELATIVE aggregate-size change ESR60/ESR10:")
    say(f"      measured mapping : {rel[ESR_GRID.index(60)]:.4f}")
    say(f"      v0.2.0 sqrt law  : {sqrt_law[ESR_GRID.index(60)]:.4f}")
    say(f"    they agree to {abs(rel[ESR_GRID.index(60)]/sqrt_law[ESR_GRID.index(60)]-1)*100:.3f} %,")
    say("    so every vessel-level number in the manuscript is unchanged.  Reported")
    say("    honestly: this upgrade strengthens the METHODS, not the numbers.")
    say()

    # ---------------- figures ------------------------------------------
    fig, ax = plt.subplots(1, 3, figsize=(13.6, 3.8))

    a = ax[0]
    a.plot(ESR_GRID, one_plus, "o-", color=CB["blue"], lw=1.8, ms=6,
           label="measured mapping (Higuchi 2022)")
    a.plot(ESR_GRID, np.sqrt(np.asarray(ESR_GRID) / ESR_REF) * one_plus[2], "--",
           color=CB["verm"], lw=1.6, label=r"pure $\sqrt{\mathrm{ESR}}$ law")
    a.set(xlabel="ESR (mm/h)", ylabel=r"$R_{agg}/R_{ef}=1+\alpha$",
          title="(a) measured vs assumed scaling")

    b = ax[1]
    b.plot(ESR_GRID, hai, "s-", color=CB["green"], lw=1.8, ms=6)
    b.axhline(B16, color=CB["grey"], ls="--", lw=1.2)
    b.text(20, B16 + 0.006, r"$b=0.426$ (minimum physiological HAI)", fontsize=7.6, color="#555555")
    b.set(xlabel="ESR (mm/h)", ylabel="HAI  (hematocrit-corrected AI)",
          title="(b) implied HAI")

    c = ax[2]
    dhts = [0.00, 0.02, 0.05, 0.08]
    cvals = [100.0 * (((0.5686 + K_HAI * d - B16) / (0.5686 - B16)) ** 4 - 1) for d in dhts]
    c.bar([f"{d:.2f}" for d in dhts], cvals,
          color=[CB["sky"], CB["orange"], CB["verm"], "#8B3A00"], width=0.55)
    c.axhline(0, color=CB["black"], lw=1)
    c.set(xlabel=r"uncorrected haematocrit offset $\Delta$Ht",
          ylabel="bias in inferred aggregation state (%)",
          title="(c) Ht confounder of an uncorrected AI")
    for i, v in enumerate(cvals):
        c.text(i, v + (3 if v >= 0 else -8), f"{v:+.0f}%", ha="center", fontsize=8)

    fig.suptitle("Fig. 6  Layer 1 replaced by a measured mapping (Higuchi & Watanabe 2022)", fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig(FIG / "ms_fig6_layer1_measured.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    say("[F] figure -> figures/ms_fig6_layer1_measured.png")

    # ---------------- save ---------------------------------------------
    tbl.to_csv(RES / "v3_layer1_measured_mapping.csv", index=False)
    rel_tbl.to_csv(RES / "v3_scaling_check.csv", index=False)
    (RES / "v3_run_log.txt").write_text("\n".join(LOG), encoding="utf-8")
    (RES / "v3_constants.json").write_text(json.dumps({
        "source": "Higuchi M, Watanabe N. PLoS ONE 2022;17(7):e0270977 (PMID 35819942)",
        "rho_e_kg_m3": RHO_E, "rho_p_kg_m3": RHO_P, "R_ef_m": R_EF,
        "mu_p_Pa_s": MU_P, "a_eq16": A16, "b_eq16": B16, "k_eq15": K_HAI,
        "n_hindered": N_HIND, "westergren_slope": SLOPE_WG,
        "c_no_aggregation_m_s": C_NOAGG,
        "fitted_exponent_q": float(expo),
        "max_dev_from_sqrt_law_pct": float(np.max(np.abs(resid))),
    }, indent=2), encoding="utf-8")
    say()
    say("saved: results/v3_layer1_measured_mapping.csv, v3_scaling_check.csv,")
    say("       results/v3_run_log.txt, results/v3_constants.json")


if __name__ == "__main__":
    main()
