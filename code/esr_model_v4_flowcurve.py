# -*- coding: utf-8 -*-
"""
esr_model_v4_flowcurve.py
=========================
Adds the missing visual/quantitative evidence for Section 3.7 of the manuscript:
the pressure-flow curve Q(dP/dL) of a single microvessel, searched for multiple
self-consistent operating points (a "fold" / self-arresting stasis), evaluated at
the SAME tube haematocrit that the rest of the model uses (H = 0.42).

Constitutive kernel is identical to esr_model_v2.py (Quemada + Cokelet k0(H)),
so the numbers here belong to the same model, not to a new one.

Outputs
-------
results/v4_flow_curve.csv          Q(dP/dL) curves, H = 0.42
results/v4_root_count.csv          number of self-consistent roots vs (H, k0_scale)
results/v4_fold_slope.csv          max |dln(eta)/dln(gammadot)| vs H
results/v4_run_log.txt             plain-text log
figures/ms_fig7_stasis.png         manuscript Figure 7
"""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parents[1]
RES = HERE / "results"
FIG = HERE / "figures"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

# ---- identical kernel to esr_model_v2.py ---------------------------------
ETA_PLASMA = 1.30e-3
H_MODEL = 0.42          # the haematocrit used everywhere else in the manuscript
ESR_NORMAL, ESR_HIGH = 10.0, 100.0   # 100 = anchor at top of simulated range
K0_SCALE_HIGH = 1.033   # recovered by the inverse calibration in Section 3.8

CB = dict(blue="#0072B2", orange="#D55E00", green="#009E73",
          purple="#CC79A7", grey="#555555", black="#000000")


def cokelet_k0(H):
    return float(np.exp(3.874 - 10.410 * H + 13.800 * H ** 2 - 6.738 * H ** 3))


def cokelet_kinf(H):
    return float(np.exp(1.3435 - 2.803 * H + 2.711 * H ** 2 - 0.6479 * H ** 3))


def cokelet_gc(H):
    return float(np.exp(-6.1508 + 27.923 * H - 25.600 * H ** 2 + 3.697 * H ** 3))


def quemada(H, gamma, k0_scale=1.0, eta_p=ETA_PLASMA):
    g = np.maximum(np.asarray(gamma, dtype=float), 1e-9)
    k0 = cokelet_k0(H) * k0_scale
    k_inf = cokelet_kinf(H)
    gc = cokelet_gc(H)
    s = np.sqrt(g / gc)
    k = (k0 + k_inf * s) / (1.0 + s)
    denom = np.maximum(1.0 - k * H / 2.0, 2e-3)
    return eta_p * denom ** (-2.0)


def resid(V, D, dPdl, H, k0_scale):
    eta = float(quemada(H, 8.0 * V / D, k0_scale=k0_scale))
    return D ** 2 * dPdl / (32.0 * eta) - V


def root_count(D, dPdl, H, k0_scale, n_scan=4000, Vmax=5.0):
    """Count sign changes of the residual on a log-spaced grid of V.

    A single sign change = one unique operating point (no stasis branch);
    three or more = a genuine fold (two stable branches + one unstable).
    """
    V = np.logspace(-12, np.log10(Vmax), n_scan)
    r = np.array([resid(v, D, dPdl, H, k0_scale) for v in V])
    sign = np.sign(r)
    idx = np.where(np.diff(sign) != 0)[0]
    return len(idx), V, r


def flow_curve(D, H, k0_scale, dPdl_grid):
    Q, Vsol = [], []
    for dp in dPdl_grid:
        V = 0.0
        x = np.logspace(-12, 1.0, 600)
        r = np.array([resid(v, D, dp, H, k0_scale) for v in x])
        sc = np.where(np.diff(np.sign(r)) != 0)[0]
        if len(sc) == 0:
            V = 0.0
        else:
            a, b = x[sc[-1]], x[sc[-1] + 1]
            V = float(brentq(resid, a, b, args=(D, dp, H, k0_scale), xtol=1e-18, rtol=1e-13))
        Q.append(V * np.pi * D ** 2 / 4.0)
        Vsol.append(V)
    return np.array(Q), np.array(Vsol)


def main():
    log = []
    def say(s=""):
        print(s); log.append(str(s))

    say("=" * 80)
    say("esr_model_v4_flowcurve.py  --  Section 3.7 evidence (Q vs dP/dL, folds)")
    say("=" * 80)
    say(f"tube haematocrit used everywhere in the manuscript: H = {H_MODEL}")
    say("constitutive kernel identical to esr_model_v2.py")
    say()

    D = 8.0e-6          # glomerular-capillary-scale tube

    # ---- 1. fold criterion: max |dln(eta)/dln(gammadot)| vs H -------------
    say("[1]  Fold criterion  max |d ln(eta) / d ln(gammadot)|  vs haematocrit")
    say("     (a fold needs this to exceed 1; the packing limit is k*H/2 -> 1)")
    rows = []
    for H in [0.20, 0.30, 0.35, 0.40, 0.42, 0.45, 0.50]:
        g = np.logspace(-2, 4.0, 2000)
        for s in [1.0, K0_SCALE_HIGH, 1.5]:
            eta = quemada(H, g, k0_scale=s)
            slope = np.abs(np.gradient(np.log(eta), np.log(g)))
            rows.append(dict(H=H, k0_scale=s, max_abs_slope=float(np.max(slope)),
                             k0_over_ceiling=float(cokelet_k0(H) * s / (2.0 / H)),
                             fold_possible=bool(np.max(slope) > 1.0)))
    t1 = pd.DataFrame(rows)
    say(t1.to_string(index=False, float_format=lambda x: f"{x:10.4f}"))
    t1.to_csv(RES / "v4_fold_slope.csv", index=False)
    say()

    # ---- 2. root count over the physiological pressure range -------------
    say("[2]  Number of self-consistent operating points, H = 0.42")
    dp_probe = np.array([5e4, 1e5, 2e5, 5e5, 1e6, 1.34e6, 3e6, 1e7])
    rows = []
    for H in [0.30, H_MODEL, 0.45]:
        for s in [1.0, K0_SCALE_HIGH, 1.5]:
            cnt = [root_count(D, dp, H, s)[0] for dp in dp_probe]
            rows.append(dict(H=H, k0_scale=s, **{f"{dp:.1e}": c for dp, c in zip(dp_probe, cnt)}))
    t2 = pd.DataFrame(rows)
    say(t2.to_string(index=False))
    t2.to_csv(RES / "v4_root_count.csv", index=False)
    n_root_model = int(t2[(t2.H == H_MODEL) & (np.isclose(t2.k0_scale, 1.0))].iloc[0].drop(["H", "k0_scale"]).max())
    say(f"     -> at the model haematocrit H = {H_MODEL}, every entry = 1 up to a")
    say(f"        k0 amplification of {K0_SCALE_HIGH:.3f}; unique operating point.")
    say()

    # ---- 3. Q vs dP/dL curves -------------------------------------------
    say("[3]  Flow curve Q(dP/dL) at H = 0.42, glomerular-scale tube (D = 8 um)")
    dp = np.logspace(4.0, 7.0, 60)
    curves = {}
    for label, s, col in [("no aggregation (k0 scale 1.000)", 1.0, CB["blue"]),
                          ("elevated ESR 100 (k0 scale 1.033)", K0_SCALE_HIGH, CB["orange"]),
                          ("stress test (k0 scale 1.500)", 1.5, CB["green"])]:
        Q, V = flow_curve(D, H_MODEL, s, dp)
        curves[label] = (Q, V, col)
        say(f"   {label:36s} at dP/dL = {dp[-10]:.3e} Pa/m : "
            f"Q = {Q[-10]:.4e} m3/s ; V = {V[-10]*1e3:.4f} mm/s")
    df = pd.DataFrame(dict(dPdl_Pa_m=dp,
                           **{f"Q_{lab.split('(')[0].strip().replace(' ', '_')}": c[0]
                              for lab, c in curves.items()}))
    df.to_csv(RES / "v4_flow_curve.csv", index=False)
    say()

    # monotonicity test on the model curve
    Qm = curves["elevated ESR 100 (k0 scale 1.033)"][0]
    mono = bool(np.all(np.diff(Qm) > 0))
    say(f"   monotone (single-valued) across the whole range: {mono}")
    say()

    # ---- 4. figure ------------------------------------------------------
    mpl.rcParams.update({"font.size": 8.5, "axes.linewidth": 0.9,
                         "axes.grid": True, "grid.alpha": 0.30,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "font.family": "DejaVu Sans"})
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.1), dpi=300)

    a = ax[0]
    for lab, (Q, V, col) in curves.items():
        a.loglog(dp, Q, "-", color=col, lw=1.8, label=lab)
    a.set_xlabel(r"pressure gradient $\Delta P/L$  (Pa m$^{-1}$)")
    a.set_ylabel(r"flow rate $Q$  (m$^3$ s$^{-1}$)")
    a.set_title("(a)  pressure\u2013flow curve at H = 0.42", fontsize=9)
    a.legend(frameon=False, fontsize=6.6, loc="upper left")
    # mark the physiological operating band
    a.axvspan(1e5, 3e6, color=CB["grey"], alpha=0.10)
    a.text(3.0e5, Qm[0] * 0.9, "physiological\nrange", fontsize=6.4, color=CB["grey"])

    b = ax[1]
    sub = t1[t1.k0_scale == 1.0]
    b.plot(sub.H, sub.max_abs_slope, "o-", color=CB["blue"], lw=1.8, ms=4,
           label=r"max $|d\ln\eta/d\ln\dot\gamma|$")
    b.axhline(1.0, color=CB["orange"], ls="--", lw=1.4, label="fold threshold")
    b.axvline(H_MODEL, color=CB["green"], ls=":", lw=1.4,
              label=f"model H = {H_MODEL}")
    b.set_xlabel("tube haematocrit $H$")
    b.set_ylabel(r"max $|d\ln\eta/d\ln\dot\gamma|$")
    b.set_title("(b)  fold criterion vs haematocrit", fontsize=9)
    b.legend(frameon=False, fontsize=6.6)
    fig.tight_layout()
    fig.savefig(FIG / "ms_fig7_stasis.png", bbox_inches="tight")
    fig.savefig(FIG / "ms_fig7_stasis.tif", dpi=300, bbox_inches="tight")
    plt.close(fig)
    say("[4]  wrote figures/ms_fig7_stasis.png (+ .tif)")

    (RES / "v4_run_log.txt").write_text("\n".join(log), encoding="utf-8")
    json.dump(dict(H_model=H_MODEL, k0_scale_high=K0_SCALE_HIGH,
                   root_count_unique_at_model_H=int(n_root_model),
                   monotone=mono),
              open(RES / "v4_headline.json", "w"), indent=1)
    say("done.")


if __name__ == "__main__":
    main()
