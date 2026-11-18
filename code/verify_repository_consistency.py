# -*- coding: utf-8 -*-
"""Check that the numbers in the manuscript agree with the numerical output in results/.

Reads manuscript/Manuscript_ESR_renal_medulla_hypothesis.md and the CSVs in results/,
and asserts that (i) every reference 1-34 is cited and cited in order of first appearance,
(ii) the thirteen numbered equations are present, (iii) the excess WSS variability quoted
for Table 6 matches results/v2_vessel_states.csv at every ESR, (iv) the Table 5 ratios
match, and (v) the s-sweep values of Table 7 match results/v2_cfl_sign_robustness.csv.

Run from the repository root:  python code/verify_repository_consistency.py
Exit status 0 = all checks pass.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MS = ROOT / "manuscript" / "Manuscript_ESR_renal_medulla_hypothesis.md"
RES = ROOT / "results"

n_ok = n_bad = 0


def ok(cond, msg):
    global n_ok, n_bad
    if cond:
        n_ok += 1
    else:
        n_bad += 1
        print("  FAIL:", msg)


text = MS.read_bytes().decode("utf-8").replace("\r\n", "\n")

# ---- references -----------------------------------------------------------
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹"


def s2i(s):
    return int("".join(str(SUP.index(c)) for c in s))


pat = re.compile(r"(?<!\u207b)[" + SUP + r"]["+SUP+r",\u207b]*")
SCI = set("gf)DR0")
body = text[text.index("## 1. Introduction"):text.index("## References")]
first = []
for m in pat.finditer(body):
    if m.start() > 0 and body[m.start() - 1] in SCI:
        continue
    for tok in m.group(0).split(","):
        if "⁻" in tok:
            a, b = tok.split("⁻")
            first.extend(range(s2i(a), s2i(b) + 1))
        else:
            first.append(s2i(tok))
seen = []
for n in first:
    if n not in seen:
        seen.append(n)
ok(seen == list(range(1, 35)), "references are not cited in strict 1-34 first-appearance order: %s" % seen)

refs = re.findall(r"^(\d+)\. ", text[text.index("## References"):], re.M)
ok([int(x) for x in refs] == list(range(1, 35)), "reference list is not 1-34")

# ---- equations ------------------------------------------------------------
eqs = re.findall(r"\\tag\{(\d+[a-c]?)\}", text)
ok(eqs == ["1", "2", "3", "4a", "4b", "5", "6", "7", "7a", "7b", "7c", "8", "9"],
   "equation labels wrong or out of order: %s" % eqs)

# ---- Table 5 / Table 6 vs CSV --------------------------------------------
rows = list(csv.DictReader(open(RES / "v2_vessel_states.csv", newline="", encoding="utf-8")))
by = {(r["vessel"], int(float(r["ESR_mm_h"]))): r for r in rows}
vessels = ["Glomerular capillary", "Peritubular capillary",
           "Vasa recta (medulla)", "Vasa recta - hypoperfused"]
for v in vessels:
    a, b = by[(v, 10)], by[(v, 100)]
    for key in ("CFL_um", "WSS_CV"):
        r = round(float(b[key]) / float(a[key]), 3)
        ok(("%.3f" % r) in text, "Table 5 ratio %s %s = %.3f absent" % (v, key, r))
    ok(float(b["H_core"]) <= 0.950001, "H_core exceeds the packing bound: %s" % v)
for v in vessels:
    base = float(by[(v, 10)]["WSS_CV"])
    for e in (20, 40, 60, 80, 100, 120, 150):
        x = 100 * (float(by[(v, e)]["WSS_CV"]) / base - 1)
        ok(("%.1f%%" % x) in text, "Table 6 %s at ESR %d = %.1f%% absent" % (v, e, x))

# ---- Table 7 vs CSV -------------------------------------------------------
rb = list(csv.DictReader(open(RES / "v2_cfl_sign_robustness.csv", newline="", encoding="utf-8")))
ok(len(rb) == 5, "sign sweep should have 5 rows, has %d" % len(rb))
for r in rb:
    for v in vessels:
        x = float(r[v + " [%]"])
        ok(("%.1f%%" % x) in text, "Table 7 s=%s %s = %.1f%% absent" % (r["shear_exp"], v, x))

# ---- abstract length ------------------------------------------------------
ab = re.search(r"## Abstract\n\n(.*?)\n\n\*\*Keywords", text, re.S).group(1).replace("**", "")
wc = len(ab.split())
ok(wc <= 200, "abstract is %d words (limit 200)" % wc)

print("\n%d checks passed, %d failed" % (n_ok, n_bad))
sys.exit(1 if n_bad else 0)
