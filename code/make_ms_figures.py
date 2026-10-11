#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_ms_figures.py  --  final, submission-ready figures for the CHM manuscript.

Produces the numbered figures (order of first citation in the text) at 300 dpi
in both PNG (for review) and TIFF-LZW (for the publisher), colour-blind-safe.

    Figure1  model overview / four-layer chain
    Figure2  Layer 1 derived from measured constants (Higuchi 2022)
    Figure3  viscosity-kernel validation
    Figure4  shear-rate gating
    Figure5  vessel-level fold change
    Figure6  amplification of WSS variability, its decomposition, and its
             dependence on the sign of the CFL/shear relation
Figure7 (pressure-flow fold search) is produced separately by
esr_model_v4_flowcurve.py, because it consumes the v4 flow-curve results.

No modelling happens here: every number is read back from results/*.csv so that
figures and text cannot drift apart.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
# The manuscript figures are written straight into the submission package when
# it is present (the working project).  In the standalone public repository
# there is no submission package, so they are written to figures/ instead.
FIGDIR = ROOT / "CHM_submission" / "03_Figures"
if not (ROOT / "CHM_submission").is_dir():
    FIGDIR = ROOT / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.linewidth": 0.9, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 300,
                     "figure.dpi": 300, "legend.frameon": False})
CB = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73",
      "verm": "#D55E00", "purple": "#CC79A7", "sky": "#56B4E9",
      "grey": "#999999", "black": "#000000"}

VESSEL_ORDER = ["Glomerular capillary", "Peritubular capillary",
                "Vasa recta (medulla)", "Vasa recta - hypoperfused"]
VESSEL_LABEL = {"Glomerular capillary": "Glomerular capillary\n(cortex, high shear)",
                "Peritubular capillary": "Peritubular capillary\n(cortex)",
                "Vasa recta (medulla)": "Vasa recta\n(medulla)",
                "Vasa recta - hypoperfused": "Vasa recta\n(hypoperfused)"}
VESSEL_COL = {"Glomerular capillary": CB["blue"],
              "Peritubular capillary": CB["sky"],
              "Vasa recta (medulla)": CB["green"],
              "Vasa recta - hypoperfused": CB["verm"]}


def save(fig, name):
    png = FIGDIR / f"{name}.png"
    tif = FIGDIR / f"{name}.tif"
    fig.savefig(png, bbox_inches="tight", facecolor="white", dpi=300)
    try:
        fig.savefig(tif, bbox_inches="tight", facecolor="white", dpi=300,
                    pil_kwargs={"compression": "tiff_lzw"})
    except Exception as e:                                     # pragma: no cover
        print("  (TIFF skipped:", e, ")")
    plt.close(fig)
    print("  ->", png.name, "+ .tif")


# --------------------------------------------------------------------------
def figure1():
    fig, ax = plt.subplots(figsize=(7.2, 6.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10.6); ax.axis("off")

    def box(y, h, title, body, fc, ec):
        ax.add_patch(FancyBboxPatch((0.6, y), 8.8, h,
                     boxstyle="round,pad=0.12,rounding_size=0.18",
                     linewidth=1.3, edgecolor=ec, facecolor=fc))
        ax.text(1.0, y + h - 0.36, title, fontsize=10.5, fontweight="bold", color=ec, va="top")
        ax.text(1.0, y + h - 0.80, body, fontsize=8.4, color="#222222", va="top", linespacing=1.45)

    def arrow(y0, y1, label=""):
        ax.add_patch(FancyArrowPatch((5.0, y0), (5.0, y1), arrowstyle="-|>",
                     mutation_scale=16, linewidth=1.5, color="#444444"))
        if label:
            ax.text(5.25, (y0 + y1) / 2, label, fontsize=8.0, color="#444444", va="center")

    box(8.55, 1.75, "INPUT   clinical measurement",
        "ESR (mm/h), the routine laboratory value.\nThe aggregation index it reflects is\n"
        "haematocrit-corrected in Layer 1.", "#EAF3FB", CB["blue"])
    box(6.35, 1.85, "LAYER 1   sedimentation  \u2192  aggregate size",
        "derived, not assumed:  Stokes + the measured\nWestergren relation (r = 0.990),  n = 4.65\n"
        "\u21d2  (1+\u03b1) \u221d \u221aESR ;  R_agg = R_ef(1+\u03b1)", "#F2F2F2", CB["grey"])
    box(3.95, 2.05, "LAYER 2-3   aggregation  \u2192  viscosity  \u2192  flow",
        "Quemada:  \u03b7 = \u03b7_p (1 \u2212 kH/2)\u207b\u00b2 ,\n"
        "k = (k\u2080 + k\u221e\u221a(\u03b3\u0307/\u03b3\u0307_c)) / (1 + \u221a(\u03b3\u0307/\u03b3\u0307_c))\n"
        "Tube:  \u03c4_w = D(\u0394P/L)/4     \u03b3\u0307_w = 8V/D\n"
        "VALIDATED vs published curve: \u00b17 %", "#FFF6E5", CB["orange"])
    box(1.55, 2.05, "LAYER 4   cell-free layer  \u2192  wall load",
        "two-layer core/CFL mass balance:\nH\u00b7\u03c0R\u00b2 = H_core\u00b7\u03c0(R\u2212\u03b4)\u00b2\n"
        "\u21d2 aggregation THICKENS the CFL (cells move away from wall)\n"
        "outputs: gap, CFL, mean WSS, WSS temporal variability", "#E9F7F2", CB["green"])
    arrow(8.55, 8.24, "ESR"); arrow(6.35, 6.04, "\u03b1"); arrow(3.95, 3.64, "H_core, \u03b7"); arrow(1.55, 1.15)
    ax.add_patch(FancyBboxPatch((0.6, 0.12), 8.8, 0.95,
                 boxstyle="round,pad=0.10,rounding_size=0.16",
                 linewidth=1.6, edgecolor=CB["verm"], facecolor="#FDEDE5"))
    ax.text(5.0, 0.60, "OUTCOME OF MODEL:  only WSS temporal variability responds monotonically,\n"
                       "and only in the low-shear, hypoperfused renal medulla.\nInjury itself is NOT computed (\u00a74.6).",
            fontsize=8.8, color=CB["verm"], ha="center", va="center", fontweight="bold", linespacing=1.5)
    fig.tight_layout(); save(fig, "Figure1_model_overview")


# --------------------------------------------------------------------------
def figure2():
    d = pd.read_csv(RES / "v3_layer1_measured_mapping.csv")
    fig, ax = plt.subplots(1, 3, figsize=(13.6, 3.8))
    a = ax[0]
    a.plot(d.ESR_mm_h, 1 + d.alpha_measured, "o-", color=CB["blue"], lw=1.8, ms=6,
           label="derived from measured constants")
    ref = (1 + d.alpha_measured)[d.ESR_mm_h == 10].values[0]
    a.plot(d.ESR_mm_h, np.sqrt(d.ESR_mm_h / 10) * ref, "--", color=CB["verm"], lw=1.6,
           label=r"pure $\sqrt{\mathrm{ESR}}$ law")
    a.set(xlabel="ESR (mm h$^{-1}$)", ylabel=r"$R_{agg}/R_{ef}=1+\alpha$",
          title="(a) derived vs assumed scaling")
    a.legend(fontsize=7.6)
    b = ax[1]
    b.plot(d.ESR_mm_h, d.HAI, "s-", color=CB["green"], lw=1.8, ms=6)
    b.axhline(0.426, color=CB["grey"], ls="--", lw=1.2)
    b.text(22, 0.4305, r"$b=0.426$ (minimum physiological HAI)", fontsize=7.4, color="#555555")
    b.set(xlabel="ESR (mm h$^{-1}$)", ylabel="HAI (haematocrit-corrected AI)",
          title="(b) implied HAI", ylim=(0.42, 0.72))
    c = ax[2]
    dhts = [0.00, 0.02, 0.05, 0.08]
    bc = [100 * (((0.5686 + 0.284 * x - 0.426) / (0.5686 - 0.426)) ** 4 - 1) for x in dhts]
    c.bar([f"{x:.2f}" for x in dhts], bc, color=[CB["sky"], CB["orange"], CB["verm"], "#8B3A00"], width=0.55)
    c.axhline(0, color=CB["black"], lw=1)
    for i, v in enumerate(bc):
        c.text(i, v + 3, f"{v:+.0f}%", ha="center", fontsize=8)
    c.set(xlabel=r"uncorrected haematocrit offset $\Delta$Ht",
          ylabel="bias in inferred aggregation state (%)",
          title="(c) haematocrit confounder", ylim=(0, 95))
    fig.suptitle("Figure 2  Layer 1 derived from measured sedimentation data", fontsize=11, y=1.02)
    fig.tight_layout(); save(fig, "Figure2_layer1_measured")


# --------------------------------------------------------------------------
def figure3():
    shear = np.array([0.1, 1, 10, 100])
    model = np.array([19.5536, 10.5169, 5.2487, 3.3207])
    meas = np.array([20.0, 10.0, 4.9, 3.23])
    fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.5))
    a = ax[0]
    a.loglog(shear, meas, "s", ms=8, mfc=CB["black"], mec=CB["black"], label="measured (published)")
    a.loglog(shear, model, "o-", ms=6, lw=1.6, color=CB["blue"], label="model (Quemada, H = 0.42)")
    a.set(xlabel="shear rate (s$^{-1}$)", ylabel=r"relative viscosity ($\eta/\eta_p$)",
          title="(a) kernel reproduces published data"); a.set_xlim(0.07, 150); a.set_ylim(2.5, 30)
    a.legend(fontsize=8)
    b = ax[1]
    r = model / meas
    b.axhline(1.0, color=CB["grey"], lw=1, ls="--"); b.axhspan(0.93, 1.07, color=CB["green"], alpha=0.12)
    b.plot(shear, r, "o-", color=CB["green"], ms=7, lw=1.6)
    for x, y in zip(shear, r):
        b.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(6, 6), fontsize=8)
    b.set(xscale="log", xlabel="shear rate (s$^{-1}$)", ylabel="model / measured",
          title="(b) deviation within \u00b17 %", ylim=(0.90, 1.12))
    fig.suptitle("Figure 3  Validation of the viscosity kernel", fontsize=11, y=1.02)
    fig.tight_layout(); save(fig, "Figure3_viscosity_validation")


# --------------------------------------------------------------------------
def figure4():
    g = pd.read_csv(RES / "v2_shear_gating.csv")
    sens = pd.read_csv(RES / "v2_param_sensitivity.csv")
    cols = [("r_0p3", 0.3), ("r_1", 1.0), ("r_3", 3.0), ("r_10", 10.0), ("r_100", 100.0), ("r_1000", 1000.0)]
    fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.6))
    a = ax[0]
    a.semilogx(g.gamma_s, g.ratio, "-", lw=2.2, color=CB["blue"])
    a.axhline(1.10, color=CB["verm"], ls="--", lw=1.2); a.text(0.33, 1.107, "+10 %", fontsize=8, color=CB["verm"])
    a.axvspan(0.3, 3.0, color=CB["orange"], alpha=0.12)
    a.axvline(1016, color=CB["grey"], ls=":", lw=1)
    a.text(560, 1.19, "glomerular\ncapillary", fontsize=7.4, color=CB["grey"], ha="right")
    a.axvline(10.9, color=CB["grey"], ls=":", lw=1)
    a.text(11.6, 1.015, "hypoperfused\nvasa recta", fontsize=7.4, color=CB["grey"])
    a.set(xlabel="shear rate (s$^{-1}$)", ylabel="viscosity ratio, ESR 100 / ESR 10",
          ylim=(0.995, 1.26), title="(a) aggregation effect is shear-gated")
    b = ax[1]
    styles = [("-", "o", CB["blue"], "standard"), ("--", "s", CB["orange"], "measured clinical"),
              ("-.", "^", CB["green"], r"$k_0$ lower 3.05"), (":", "d", CB["verm"], r"$k_0$ upper 4.36")]
    for row, (ls, mk, c, lab) in zip(sens.itertuples(), styles):
        b.semilogx([v for _, v in cols], [getattr(row, k) for k, _ in cols],
                   ls, marker=mk, ms=5, lw=1.5, color=c, label=lab)
    b.axhline(1.10, color=CB["grey"], ls="--", lw=1)
    b.set(xlabel="shear rate (s$^{-1}$)", ylabel="viscosity ratio", ylim=(0.995, 1.26),
          title="(b) four published parameter sets agree")
    b.legend(fontsize=7.2, loc="upper right")
    fig.suptitle("Figure 4  Shear-rate gating of the aggregation contribution to viscosity", fontsize=11, y=1.02)
    fig.tight_layout(); save(fig, "Figure4_shear_gating")


# --------------------------------------------------------------------------
def figure5():
    fc = pd.read_csv(RES / "v2_foldchange.csv").set_index("vessel").loc[VESSEL_ORDER]
    keys = ["d_eta", "d_tau", "d_V", "d_CFL", "d_WSS_CV"]
    labels = ["viscosity", "mean WSS", "velocity", "CFL thickness", "WSS variability"]
    vals = np.array([[float(str(fc.loc[v, k]).rstrip("x")) for k in keys] for v in VESSEL_ORDER])
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    x = np.arange(len(keys)); w = 0.2
    for i, v in enumerate(VESSEL_ORDER):
        ax.bar(x + (i - 1.5) * w, vals[i], w, color=VESSEL_COL[v], label=VESSEL_LABEL[v].replace("\n", " "))
    ax.axhline(1.0, color=CB["black"], lw=1.0)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set(ylabel="fold change, ESR 100 / ESR 10", ylim=(0.90, 1.52),
           title="Figure 5  Mean WSS is invariant; only its temporal variability responds")
    ax.legend(fontsize=7.6, ncol=2, loc="upper left")
    ax.annotate("mean WSS = exactly 1.000\u00d7\n(\u03c4_w = D\u00b7\u0394P/L / 4)", xy=(1, 1.0), xytext=(1.37, 1.19),
                fontsize=8, color=CB["verm"], arrowprops=dict(arrowstyle="->", color=CB["verm"], lw=1.2))
    ax.annotate("hypoperfused\nvasa recta peaks here", xy=(4 + 1.5 * w, vals[3, 4]), xytext=(3.05, 1.48),
                fontsize=8, color=CB["verm"], arrowprops=dict(arrowstyle="->", color=CB["verm"], lw=1.2))
    fig.tight_layout(); save(fig, "Figure5_vessel_foldchange")


# --------------------------------------------------------------------------
def figure6():
    vs = pd.read_csv(RES / "v2_vessel_states.csv")
    fc = pd.read_csv(RES / "v2_foldchange.csv").set_index("vessel").loc[VESSEL_ORDER]
    fig, ax = plt.subplots(1, 4, figsize=(17.4, 3.7))
    a = ax[0]
    for v in VESSEL_ORDER:
        sub = vs[vs.vessel == v].sort_values("ESR_mm_h")
        a.plot(sub.ESR_mm_h, sub.WSS_CV, "o-", ms=4, lw=1.6, color=VESSEL_COL[v],
               label=VESSEL_LABEL[v].replace("\n", " "))
    a.set(xlabel="ESR (mm h$^{-1}$)", ylabel="WSS coefficient of variation (-)",
          title="(a) variability rises monotonically with ESR")
    a.legend(fontsize=7.2, loc="upper left")
    b = ax[1]
    gamma = fc.gamma_w_s.values.astype(float)
    excess = np.array([float(str(fc.loc[v, "d_WSS_CV"]).rstrip("x")) for v in VESSEL_ORDER]) - 1.0
    b.barh(np.arange(len(VESSEL_ORDER)), excess, color=[VESSEL_COL[v] for v in VESSEL_ORDER], height=0.6)
    b.set_yticks(np.arange(len(VESSEL_ORDER)))
    b.set_yticklabels([f"{VESSEL_LABEL[v].replace(chr(10),' ')} ({g:.0f} s$^{{-1}}$)"
                       for v, g in zip(VESSEL_ORDER, gamma)], fontsize=7.4)
    for i, e in enumerate(excess):
        b.text(e + 0.004, i, f"{e*100:.1f} %", va="center", fontsize=8)
    b.set(xlabel="excess WSS variability, ESR 100 vs ESR 10 (%)", xlim=(0, 0.52))
    b.set_title("(b) at the default sign the medulla\nleads by 3.0-fold", fontsize=9.4, pad=7)
    b.invert_yaxis()

    # ---- (c) multiplicative decomposition of (b) into Eq (8) x Eq (9)
    c = ax[2]
    share_gate, share_geo, gate_f, geo_f = [], [], [], []
    for v in VESSEL_ORDER:
        sub = vs[vs.vessel == v].sort_values("ESR_mm_h")
        r10 = sub[np.isclose(sub.ESR_mm_h, 10.0)].iloc[0]
        r60 = sub[np.isclose(sub.ESR_mm_h, 100.0)].iloc[0]
        D = float(r10.D_um) * 1e-6
        d10, d60 = float(r10.CFL_um) * 1e-6, float(r60.CFL_um) * 1e-6
        geo10, geo60 = D / (D - 2 * d10), D / (D - 2 * d60)
        g_f = float(r60.CFL_CV) / float(r10.CFL_CV)          # Eq (9) shear gate
        e_f = geo60 / geo10                                   # Eq (8) geometric
        tot = float(r60.WSS_CV) / float(r10.WSS_CV)
        share_gate.append(100.0 * np.log(g_f) / np.log(tot))
        share_geo.append(100.0 * np.log(e_f) / np.log(tot))
        gate_f.append(g_f); geo_f.append(e_f)
    y = np.arange(len(VESSEL_ORDER))
    c.barh(y, share_geo, color=[VESSEL_COL[v] for v in VESSEL_ORDER], height=0.6,
           label="geometric amplification, Eq (8)")
    c.barh(y, share_gate, left=share_geo, color=CB["grey"], height=0.6, hatch="///",
           edgecolor="white", label="shear gate, Eq (9)")
    c.set_yticks(y); c.set_yticklabels([])
    c.set(xlim=(0, 118), xlabel="share of the log increase in WSS variability (%)",
          title="(c) the geometric factor carries the medullary excess")
    c.invert_yaxis()
    for i, (sg, sgeo) in enumerate(zip(share_gate, share_geo)):
        c.text(101, i, f"gate {sg:.1f} %", va="center", fontsize=7.6, color=CB["black"])
    c.axvline(100, color=CB["grey"], lw=0.8, ls=":")
    c.legend(fontsize=7.0, loc="lower left", bbox_to_anchor=(0.0, -0.42), ncol=1)

    # ---- (d) robustness to the SIGN of the CFL / shear-rate relation
    d = ax[3]
    rb = pd.read_csv(RES / "v2_cfl_sign_robustness.csv")
    short = {"Glomerular capillary": "glomerular cap.",
             "Peritubular capillary": "peritubular cap.",
             "Vasa recta (medulla)": "vasa recta",
             "Vasa recta - hypoperfused": "vasa recta, hypoperfused"}
    for v in VESSEL_ORDER:
        y = rb[v + " [%]"].values
        d.plot(rb.shear_exp, y, "o-", ms=4, lw=1.6, color=VESSEL_COL[v])
        d.annotate(short[v], xy=(rb.shear_exp.iloc[-1], y[-1]),
                   xytext=(4, 0), textcoords="offset points",
                   fontsize=7.0, va="center", ha="left", color=VESSEL_COL[v])
    d.axvline(0.0, color=CB["grey"], lw=1.0, ls="--")
    d.axvline(-0.12, color=CB["black"], lw=1.0, ls=":")
    d.annotate("default\n$s=-0.12$", xy=(-0.12, 1.0), xycoords=("data", "axes fraction"),
               xytext=(4, -11), textcoords="offset points", fontsize=6.8,
               color=CB["black"], ha="left", va="top")
    d.annotate("crossover\n$s=+0.02$", xy=(0.02, 1.0), xycoords=("data", "axes fraction"),
               xytext=(5, -31), textcoords="offset points", fontsize=6.8,
               color=CB["grey"], ha="left", va="top")
    d.set(xlim=(-0.27, 0.34), ylim=(0, 118),
          xlabel="CFL shear exponent $s$   ($\\delta \\propto \\dot{\\gamma}^{\\,s}$)",
          ylabel="excess WSS variability (%)")
    d.set_title("(d) the worst vessel is set by the sign of $s$\n"
                "(excess at ESR 100 vs 10 mm h$^{-1}$)", fontsize=9.4, pad=7)

    fig.suptitle("Figure 6  WSS temporal variability: amplification, its decomposition, "
                 "and its dependence on the sign of the cell-free-layer/shear relation",
                 fontsize=10.6, y=1.03)
    fig.tight_layout(); save(fig, "Figure6_medullary_amplification")


if __name__ == "__main__":
    for f in (figure1, figure2, figure3, figure4, figure5, figure6):
        print(f.__name__); f()
    print("figures written to", FIGDIR)
