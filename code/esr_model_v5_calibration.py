# -*- coding: utf-8 -*-
"""Supplementary Note S1 generator: the inverse calibration, written out, plus a
sensitivity analysis of the two recovered quantities to the two clinical targets.
Also retrieves the source abstract so the sample size can be quoted honestly.
"""
import urllib.request, re, html, json, time
from pathlib import Path
import numpy as np
from scipy.optimize import fsolve

HERE = Path(__file__).resolve().parents[1]
RES = HERE / "results"
# Supplementary Table S2 is written into the submission package when it is
# present (the working project); in the standalone public repository there is
# no submission package, so it is written to supplementary/ instead.
SUP = HERE / "CHM_submission" / "04_Supplementary"
if not (HERE / "CHM_submission").is_dir():
    SUP = HERE / "supplementary"

ETA_PLASMA = 1.30e-3
H = 0.42


def fetch(u, t=3):
    for i in range(t):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            return urllib.request.urlopen(req, timeout=35).read().decode("utf-8", "ignore")
        except Exception:
            if i == t - 1:
                return None
            time.sleep(2)


def k0(H):
    return float(np.exp(3.874 - 10.410 * H + 13.800 * H ** 2 - 6.738 * H ** 3))


def kinf(H):
    return float(np.exp(1.3435 - 2.803 * H + 2.711 * H ** 2 - 0.6479 * H ** 3))


def gc(H):
    return float(np.exp(-6.1508 + 27.923 * H - 25.600 * H ** 2 + 3.697 * H ** 3))


def eta(g, k0v, phi=1.0, ep=ETA_PLASMA):
    k = (k0v + kinf(H) * np.sqrt(g / gc(H))) / (1.0 + np.sqrt(g / gc(H)))
    den = max(1.0 - k * H / 2.0, 2e-3)
    return ep * phi * den ** (-2.0)


def solve(lo_target, hi_target):
    base = {1.0: eta(1.0, k0(H)), 100.0: eta(100.0, k0(H))}

    def resid(p):
        phi, k0h = p
        return [eta(1.0, k0h, phi) - base[1.0] * lo_target,
                eta(100.0, k0h, phi) - base[100.0] * hi_target]

    sol, info, ier, msg = fsolve(resid, [1.15, 4.6], full_output=True)
    return float(sol[0]), float(sol[1]), ier


def main():
    log = []
    def say(s=""):
        print(s); log.append(str(s))

    # ---- source abstract -------------------------------------------------
    say("=" * 78)
    say("Supplementary Note S1  --  inverse calibration, written out")
    say("=" * 78)
    x = fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=6410531&retmode=xml")
    abs_txt = ""
    if x:
        m = re.search(r"<Abstract>(.*?)</Abstract>", x, re.S)
        if m:
            abs_txt = html.unescape(re.sub("<[^>]+>", " ", m.group(1)))
            abs_txt = re.sub(r"\s+", " ", abs_txt).strip()
    say("[source] McGinley 1983 (PMID 6410531) indexed abstract text:")
    say("    " + (abs_txt if abs_txt else "(no abstract indexed)"))
    say()

    k0n = k0(H)
    say(f"fixed constants at H = {H}:  k0 = {k0n:.4f},  k_inf = {kinf(H):.4f},  "
        f"gamma_c = {gc(H):.4f} s-1,  eta_p = {ETA_PLASMA*1e3:.3f} mPa.s")
    say()

    phi, k0h, ier = solve(1.41, 1.25)
    say(f"[central solution]  phi = {phi:.4f}   k0_high = {k0h:.4f}   "
        f"amplification = {k0h/k0n:.4f}x   (ier={ier})")
    say()

    # ---- sensitivity -----------------------------------------------------
    say("[sensitivity] recovered (phi, amplification) vs the two target increments")
    rows = []
    for dlo in (-0.10, -0.05, 0.0, 0.05, 0.10):
        for dhi in (-0.10, -0.05, 0.0, 0.05, 0.10):
            p, kh, _ = solve(1.41 + dlo, 1.25 + dhi)
            rows.append(dict(d_low_pp=dlo * 100, d_high_pp=dhi * 100,
                             phi=p, k0_high=kh, amplification=kh / k0n,
                             inside_clinical_range=(3.05 <= kh <= 4.36)))
    import csv
    with open(SUP / "Supplementary_Table_S2_InverseCalibration_Sensitivity.csv",
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    arr = np.array([[r["phi"], r["amplification"]] for r in rows])
    say(f"    phi          range over +/-10 pp : {arr[:,0].min():.3f} - {arr[:,0].max():.3f}")
    say(f"    amplification range over +/-10 pp : {arr[:,1].min():.3f} - {arr[:,1].max():.3f}")
    say(f"    rows with recovered k0 outside the published clinical range [3.05, 4.36]: "
        f"{sum(0 if r['inside_clinical_range'] else 1 for r in rows)}/{len(rows)}")
    say()

    # ---- what if only the low-shear target moves (the more uncertain one) --
    say("[one-at-a-time]  +/-10 pp on the low-shear target only")
    for d in (-0.10, 0.0, 0.10):
        p, kh, _ = solve(1.41 + d, 1.25)
        say(f"    low target {1.41+d:.2f}x -> phi = {p:.3f}, amplification = {kh/k0n:.3f}x")
    say("[one-at-a-time]  +/-10 pp on the high-shear target only")
    for d in (-0.10, 0.0, 0.10):
        p, kh, _ = solve(1.41, 1.25 + d)
        say(f"    high target {1.25+d:.2f}x -> phi = {p:.3f}, amplification = {kh/k0n:.3f}x")
    say()
    say("NOTE  The gating of the aggregation effect (Section 3.3) does not depend on")
    say("      these two numbers: it follows from the functional form of the Quemada")
    say("      law.  Only the ABSOLUTE magnitude of the low-shear viscosity increment")
    say("      is set by the calibration, and that magnitude is what the ranges above")
    say("      bound.")

    SUP.mkdir(parents=True, exist_ok=True)
    (RES / "v5_calibration_log.txt").write_text("\n".join(log), encoding="utf-8")
    json.dump(dict(k0n=k0n, phi=phi, k0_high=k0h, amplification=k0h / k0n,
                   phi_min=float(arr[:, 0].min()), phi_max=float(arr[:, 0].max()),
                   amp_min=float(arr[:, 1].min()), amp_max=float(arr[:, 1].max())),
              open(RES / "v5_calibration.json", "w"), indent=1)
    print("\nsaved results/v5_calibration.json and Supplementary_Table_S2")


if __name__ == "__main__":
    main()
