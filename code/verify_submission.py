# -*- coding: utf-8 -*-
"""
verify_submission.py  --  three independent verification methods, repeatable.

Method A (structural)   : numbering, cross-references, reference-list integrity,
                          placeholder scan.
Method B (numerical)    : every quantitative claim in the manuscript is matched
                          against the model output tables (single source of truth).
Method C (logical/text) : claim-to-claim consistency, duplicate headings,
                          long-sentence outliers, spelling-variant consistency,
                          caption/body agreement.

Method D (amendment)    : re-derives the multiplicative decomposition of the
                          WSS-CV response from results/v2_vessel_states.csv on
                          an independent code path, and guards the sign
                          disclosure that accompanies it (ledger, shipped code,
                          equation cross-references, caption panels).

Run repeatedly; the report states PASS/FAIL for every item so that three
consecutive clean rounds can be demonstrated.
"""
from __future__ import annotations
import csv, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
RES = HERE / "results"
SUB = HERE / "CHM_submission"

# --- public-repository guard ------------------------------------------------
# This script validates the complete submission package (CHM_submission/).
# That package is NOT distributed in the public repository, because it contains
# the cover letter and the reviewer suggestions.  The script is shipped for
# transparency; every numerical result it checks is present under results/.
if not SUB.is_dir():
    print("Skipped: CHM_submission/ (the submission package) is not part of "
          "this repository.")
    raise SystemExit(0)
MS = HERE / "Manuscript_ESR_renal_medulla_hypothesis_v0.1.md"

fails: list[str] = []
warns: list[str] = []
checks = 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
    return cond


def warn(cond, msg):
    if not cond:
        warns.append(msg)


def load_csv(name, key=None):
    with open(RES / name, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return {(r[key] if key else None): r for r in rows}


def fnum(x):
    try:
        return float(str(x).replace("x", "").replace("%", "").replace("\u00d7", ""))
    except Exception:
        return None


def main():
    s = MS.read_text(encoding="utf-8")
    body = s[s.index("## 1. Introduction"):s.index("## Declarations")]
    captions = s[s.index("## Figure captions"):s.index("## Tables (in the body")]
    refs_block = s[s.index("## References"):s.index("## Figure captions")]

    # ==================================================================
    # METHOD A -- structural
    # ==================================================================
    # A1 tables defined exactly once, numbered 1..6 in order
    tdefs = re.findall(r"\*\*Table (\d)\.\*\*", body)
    ok(tdefs == ["1", "2", "3", "4", "5", "6", "7"],
       "A1 table definitions must be 1..7 in order, got %s" % tdefs)

    # A2 figures defined exactly once, numbered 1..7 in order
    fdefs = re.findall(r"\*\*Figure (\d)\.\*\*", captions)
    ok(fdefs == [str(i) for i in range(1, 8)],
       "A2 figure captions must be 1..7 in order, got %s" % fdefs)

    # A3 every in-text Table/Figure call-out resolves
    for m in sorted(set(re.findall(r"Table (\d)", body))):
        ok(1 <= int(m) <= 7, "A3 Table %s referenced but not defined" % m)
    for m in sorted(set(re.findall(r"Figure (\d)", body))):
        ok(1 <= int(m) <= 7, "A3 Figure %s referenced but not defined" % m)

    # A4 equation labels: 1,2,3,4a,4b,5,6,7,7a,8,9 each exactly once
    eqs = re.findall(r"^\s{4}.*\((\d+[ab]?)\)\s*$", s, flags=re.M)
    ok(sorted(eqs) == sorted(["1", "2", "3", "4a", "4b", "5", "6", "7", "7a", "8", "9"]),
       "A4 equation labels wrong/duplicated: %s" % sorted(eqs))

    # A5 reference list: 1..28 consecutive, no gaps, no duplicates
    nums = [int(x) for x in re.findall(r"^(\d+)\. ", refs_block, flags=re.M)]
    ok(nums == list(range(1, 29)), "A5 reference list is not 1..28: %s" % nums)

    # A6 every reference cited at least once in the body
    sup = "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"
    d = {c: str(i) for i, c in enumerate(sup)}
    cited = set()
    for run in re.findall("[%s]+" % sup, body):
        cited.add(int("".join(d[c] for c in run)))
    missing = [n for n in range(1, 29) if n not in cited]
    ok(not missing, "A6 references with no in-text citation: %s" % missing)

    # A7 no orphan in-text citation beyond the list
    orphan = sorted(n for n in cited if n > 28 or n < 1)
    ok(not orphan, "A7 in-text citations outside 1..28: %s" % orphan)

    # A8 placeholder scan across every deliverable text file
    bad_patterns = ["[to be completed]", "[disease]", "TODO", "TBD", "XXX",
                    "[to be supplied]", "[Year]", "[author]"]
    scan = [MS] + list(SUB.rglob("*.md"))
    for f in scan:
        t = f.read_text(encoding="utf-8", errors="ignore")
        for b in bad_patterns:
            ok(b not in t, "A8 placeholder %r found in %s" % (b, f.name))

    # A9 every supplementary file named in the statements exists
    st = (SUB / "06_Statements_and_Declarations.md").read_text(encoding="utf-8")
    for name in re.findall(r"`(Supplementary_[A-Za-z0-9_\-\.]+)`", st):
        ok((SUB / "04_Supplementary" / name).exists(),
           "A9 statements cite %s but the file is absent" % name)
    ms_names = re.findall(r"`(Supplementary_[A-Za-z0-9_\-\.]+)`", s)
    for name in ms_names:
        ok((SUB / "04_Supplementary" / name).exists(),
           "A9 manuscript cites %s but the file is absent" % name)

    # A10 figure files exist for every caption
    figdir = SUB / "03_Figures"
    for i in range(1, 8):
        hits = list(figdir.glob("Figure%d_*.png" % i)) + list(figdir.glob("Figure%d_*.tif" % i))
        ok(len(hits) >= 2, "A10 Figure %d lacks png+tif in 03_Figures" % i)

    # A11 every reference line agrees with the independently retrieved PubMed
    #     metadata (year / volume / first page or article number)
    meta = json.load(open(RES / "refs_verified_metadata.json", encoding="utf-8"))
    for line in refs_block.split("\n"):
        m = re.match(r"^(\d+)\. (.+?)\. \*([^*]+)\*\. (\d{4});(.+?)\.", line)
        if not m:
            continue
        num, rest, jour, year, tail = m.groups()
        pm = re.search(r"PMID (\d+)", line)
        if not pm:
            continue
        md = meta.get(pm.group(1))
        if md is None:
            continue
        ok(md["year"][:4] == year,
           "A11 ref %s year %s != PubMed %s" % (num, year, md["year"][:4]))
        vol = str(md.get("vol") or "")
        if vol:
            ok(re.search(r"\b%s\b" % re.escape(vol), tail) or vol in tail,
               "A11 ref %s volume %s not found in %r" % (num, vol, tail[:60]))
        pages = str(md.get("pages") or "")
        eloc = str(md.get("eloc") or "")
        if pages:
            firstp = re.split(r"[-–]", pages)[0].strip()
            ok(firstp and firstp in tail,
               "A11 ref %s first page %s not in %r" % (num, firstp, tail[:60]))
        elif eloc.lower().startswith("doi:"):
            # publisher stores the DOI in the e-location field; the reference
            # must then carry that DOI verbatim
            doi = eloc.split(":", 1)[1].strip()
            ok(doi.lower() in line.lower(),
               "A11 ref %s DOI %s not present in the reference line" % (num, doi))
        elif eloc:
            art = re.sub(r"^e", "", eloc.strip())
            ok(art in tail, "A11 ref %s article number %s not in %r" % (num, art, tail[:60]))

    # A12 the delivered DOCX really carries the corrected content
    try:
        from docx import Document
        doc = Document(str(SUB / "02_Manuscript.docx"))
        dtxt = "\n".join(p.text for p in doc.paragraphs)
        dtab = "\n".join(c.text for t in doc.tables for r in t.rows for c in r.cells)
        dall = dtxt + "\n" + dtab
        ok(len(doc.tables) == 7, "A12 manuscript DOCX has %d tables, expected 7" % len(doc.tables))
        for key in ["Equation (8)", "Equation (9)", "Equation (7a)", "Equation (7)", "Table 5",
                    "Table 6", "Table 7", "1.033", "1.228", "46.0%", "15.2%", "42.8%",
                    "ESR 100", "10\u2013100", "Figure 7", "tinnitus",
                    "doi:10.1055/s-0038-1657351", "doi:10.1063/1.5127879",
                    "doi:10.1016/j.mvr.2025.104859"]:
            hit = (key in dall) or (key.lower() in dall.lower())
            ok(hit, "A12 DOCX is missing %r" % key)
        for bad in ["[disease]", "[to be completed]", "TODO"]:
            ok(bad not in dall, "A12 DOCX still contains placeholder %r" % bad)
    except ImportError:
        warn(False, "A12 python-docx unavailable; DOCX readback skipped")

    # A13 staleness: every .docx must be at least as new as its .md source, and
    #     02_Manuscript.md must be identical to the working manuscript.
    ok((SUB / "02_Manuscript.md").read_text(encoding="utf-8") == s,
       "A13 CHM_submission/02_Manuscript.md differs from the working manuscript")
    for md_file in SUB.rglob("*.md"):
        dx = md_file.with_suffix(".docx")
        if dx.exists():
            ok(dx.stat().st_mtime >= md_file.stat().st_mtime - 1,
               "A13 stale DOCX: %s is older than %s" % (dx.name, md_file.name))

    # A14 the parameter ledger records the ESR anchoring decisions introduced
    #     with the 10-100 mm/h range extension
    led0 = (SUB / "04_Supplementary" /
            "Supplementary_Table_S1_Parameter_Ledger.csv").read_text(encoding="utf-8-sig")
    for key in ["esr_reference", "esr_simulated_range", "esr_calibration_anchor",
                "esr_clinical_reference"]:
        ok(key in led0, "A14 parameter ledger does not record %s" % key)

    # ==================================================================
    # METHOD B -- numerical claims vs model output
    # ==================================================================
    fc = load_csv("v2_foldchange.csv", "vessel")
    cal = json.load(open(RES / "v5_calibration.json", encoding="utf-8"))
    head = json.load(open(RES / "v4_headline.json", encoding="utf-8"))
    vig = load_csv("v2_viscosity_vs_shear.csv")
    with open(RES / "v2_viscosity_vs_shear.csv", newline="", encoding="utf-8-sig") as fh:
        vig = {r[""]: r for r in csv.DictReader(fh)}   # keyed by the shear-rate index
    gate = load_csv("v2_shear_gating.csv")

    def claim(pat, expected, tol, msg):
        m = re.search(pat, s)
        if not m:
            ok(False, "B %s -- pattern not found: %s" % (msg, pat))
            return
        got = fnum(m.group(1) if m.groups() else m.group(0))
        ok(got is not None and abs(got - expected) <= tol,
           "B %s: manuscript says %s, model gives %s" % (msg, got, expected))

    # B1 mean WSS is exactly invariant
    claim(r"ratio (1\.000)\u00d7 in every case", 1.000, 1e-9, "mean WSS invariance")
    for v, r in fc.items():
        ok(fnum(r["d_tau"]) == 1.0, "B1 %s mean WSS fold-change != 1.000" % v)

    # B2 medullary / glomerular amplification quoted in the abstract (ESR 10 -> 100)
    m2 = re.search(r"reaches ([0-9.]+)% in the hypoperfused medulla against "
                   r"([0-9.]+)% in the glomerular capillary", s)
    ok(m2 is not None, "B2 abstract amplification sentence not found")
    if m2:
        gm = 100 * (fnum(fc["Glomerular capillary"]["d_WSS_CV"]) - 1)
        hm = 100 * (fnum(fc["Vasa recta - hypoperfused"]["d_WSS_CV"]) - 1)
        ok(abs(float(m2.group(1)) - hm) < 0.05,
           "B2 abstract medullary %.1f%% != model %.1f%%" % (float(m2.group(1)), hm))
        ok(abs(float(m2.group(2)) - gm) < 0.05,
           "B2 abstract glomerular %.1f%% != model %.1f%%" % (float(m2.group(2)), gm))

    # B3 calibration numbers
    claim(r"plasma-viscosity multiple of ([0-9.]+)", cal["phi"], 0.001, "phi")
    claim(r"amplification of only ([0-9.]+)\u00d7", cal["amplification"], 0.001, "amplification")
    claim(r"\(from 4\.208 to ([0-9.]+)\)", cal["k0_high"], 0.001, "k0_high")
    ok(abs(cal["k0n"] - 4.208) < 0.001, "B3 k0 normal %.3f != 4.208" % cal["k0n"])

    # B4 fold threshold ~1.15x
    claim(r"amplification of about ([0-9.]+)\u00d7 at H = 0\.42", 1.16, 0.02,
          "fold threshold")

    # B5 abstract word count
    ab = s[s.index("## Abstract"):s.index("**Keywords:**")]
    ab = re.sub(r"\(Abstract:.*?\)", "", ab.replace("## Abstract", ""))
    ok(len(ab.split()) == 198, "B5 abstract is %d words, not 198" % len(ab.split()))

    # B5b this journal requires a STRUCTURED abstract; the five labels must
    #     be present (it was a single unlabelled paragraph before this round)
    for lab in ["**Background.**", "**Objective.**", "**Methods.**",
                "**Results.**", "**Conclusions.**"]:
        ok(lab in ab, "B5b structured-abstract label %s missing" % lab)

    # B6 main-text word count claim
    keep = [ln for ln in body.split("\n")
            if not ln.strip().startswith("|")
            and not ln.strip().startswith("**Table")
            and not ln.strip().startswith("**Figure")]
    w = len(" ".join(keep).split())
    ok(8500 <= w <= 9300, "B6 main-text word count %d outside the stated ~8,900 band" % w)

    # B7 reference count and DOI count
    ok(len(nums) == 28, "B7 reference count %d != 28" % len(nums))
    dois = len(re.findall(r"doi:10\.", refs_block))
    ok(dois == 24, "B7 DOI count %d != 24" % dois)

    # B8 shear-gating ratios quoted in the text, recomputed from the ESR columns
    for sr, exp in [("0.1 1/s", 1.332), ("0.520795 1/s", 1.191),
                    ("2.71227 1/s", 1.097), ("14.1254 1/s", 1.046),
                    ("1995.26 1/s", 1.004)]:
        row = vig.get(sr)
        ok(row is not None, "B8 shear rate %r missing from v2_viscosity_vs_shear.csv" % sr)
        if row:
            got = fnum(row["ESR100"]) / fnum(row["ESR10"])
            ok(abs(got - exp) < 0.002,
               "B8 gate at %s: model %.4f != manuscript %.3f" % (sr, got, exp))
    # Table 3 must carry every ESR column that the model produces
    for col in ["ESR10", "ESR40", "ESR60", "ESR80", "ESR100"]:
        row = vig.get("0.1 1/s") or {}
        ok(col in row, "B8 v2_viscosity_vs_shear.csv lacks column %s" % col)
    ok(re.search(r"Ratio \(100/10\)", body) is not None,
       "B8 Table 3 ratio column is not labelled 100/10")

    # B9 Table 5 (vessel states, ESR 10 -> 100) against the model output
    t5 = re.findall(r"^\| (Glomerular capillary|Peritubular capillary|"
                    r"Vasa recta \(medulla\)|Vasa recta, hypoperfused) \| "
                    r"(\d+\.?\d*) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \| "
                    r"([0-9.]+) \| \*\*([0-9.]+)\*\* \|$", body, flags=re.M)
    ok(len(t5) == 4, "B9 Table 5 rows not parsed (got %d)" % len(t5))
    t5name = {"Vasa recta, hypoperfused": "Vasa recta - hypoperfused"}
    for name, _g, de, dt, dv, dc, dw in t5:
        r = fc[t5name.get(name, name)]
        for lbl, got, exp in [("viscosity", de, fnum(r["d_eta"])),
                              ("mean WSS", dt, fnum(r["d_tau"])),
                              ("velocity", dv, fnum(r["d_V"])),
                              ("CFL", dc, fnum(r["d_CFL"])),
                              ("WSS CV", dw, fnum(r["d_WSS_CV"]))]:
            ok(abs(float(got) - exp) < 5e-4,
               "B9 Table 5 %s %s: manuscript %.3f != model %.3f"
               % (name, lbl, float(got), exp))

    # B10 Table 6 (graded excess WSS variability) against the model, for every
    #     ESR column of the table
    t6 = re.findall(r"^\| (Glomerular capillary|Peritubular capillary|"
                    r"Vasa recta \(medulla\)|Vasa recta, hypoperfused) \| "
                    r"([+\-0-9.]+)% \| ([+\-0-9.]+)% \| ([+\-0-9.]+)% \| "
                    r"([+\-0-9.]+)% \| ([+\-0-9.]+)% \|$", body, flags=re.M)
    ok(len(t6) == 4, "B10 Table 6 rows not parsed (got %d)" % len(t6))
    with open(RES / "v2_vessel_states.csv", newline="", encoding="utf-8-sig") as fh:
        _vs = list(csv.DictReader(fh))

    def wsscv(vessel, esr):
        for r in _vs:
            if r["vessel"] == vessel and abs(float(r["ESR_mm_h"]) - esr) < 1e-9:
                return float(r["WSS_CV"])
        return None

    for name, a, b, c_, d_, e_ in t6:
        model = t5name.get(name, name)
        base = wsscv(model, 10.0)
        for esr, got in zip([20, 40, 60, 80, 100], [a, b, c_, d_, e_]):
            exp = 100 * (wsscv(model, float(esr)) / base - 1)
            ok(abs(float(got) - exp) < 0.06,
               "B10 Table 6 %s ESR %d: manuscript %s%% != model %.1f%%"
               % (name, esr, got, exp))

    # B11 the vessel-level ESR grid really spans 10-100 mm/h, and every
    #     modelled k0 stays inside the published clinical interval (which is
    #     the stated justification for anchoring the calibration at 100)
    with open(RES / "v2_vessel_states.csv", newline="", encoding="utf-8-sig") as fh:
        grid_esr = sorted({float(r["ESR_mm_h"]) for r in csv.DictReader(fh)})
    ok(grid_esr[-1] == 100.0, "B11 vessel-state ESR grid tops out at %s, not 100" % grid_esr[-1])
    for e in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
        ok(float(e) in grid_esr, "B11 vessel-state grid is missing ESR %d mm/h" % e)
    with open(RES / "v2_esr_to_k0.csv", newline="", encoding="utf-8-sig") as fh:
        k0rows = list(csv.DictReader(fh))
    for r in k0rows:
        ok(r["vs_published_range_3_05_4_36"] == "inside",
           "B11 modelled k0 is %s the published clinical range at ESR %s"
           % (r["vs_published_range_3_05_4_36"], r["ESR_mm_h"]))

    # ==================================================================
    # METHOD C -- logical / textual
    # ==================================================================
    # C1 no duplicate section headings
    heads = re.findall(r"^#{2,3} (.+)$", s, flags=re.M)
    dups = {h for h in heads if heads.count(h) > 1}
    ok(not dups, "C1 duplicate headings: %s" % dups)

    # C2 no sentence over 75 words in the body (superscripts stripped first)
    plain = re.sub("[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079]", "", body)
    long_sents = []
    for para in plain.split("\n"):
        if para.strip().startswith(("|", "**Table", "**Figure", "    ")):
            continue
        for sent in re.split(r"(?<=[.;])\s+", para):
            words = len(re.findall(r"[A-Za-z][A-Za-z\u2019'\-]*", sent))
            if words > 75:
                long_sents.append((words, sent[:80]))
    warn(not long_sents, "C2 sentences over 75 words: %s" % long_sents)

    # C3 British spelling consistent in ORIGINAL PROSE only.
    # The reference list, italicised cited titles and the journal's own name are
    # excluded: those spellings belong to the sources, not to the author.
    prose = s[:s.index("## References")]
    prose = re.sub(r"\*[^*]+\*", " ", prose)          # drop italicised titles
    prose = prose.replace("Clinical Hemorheology and Microcirculation", " ")
    us = ["hemorheology", "hemodynamic", "hematocrit", "modeling", "behavior",
          "analyze", "center"]
    hits = {u: len(re.findall(r"\b%s\b" % u, prose, flags=re.I)) for u in us}
    ok(all(v == 0 for v in hits.values()),
       "C3 US spelling variants present in author prose: %s" % {k: v for k, v in hits.items() if v})

    # C4 abstract claims are a subset of results claims (spot-check the six)
    for key in ["1.000\u00d7", "1.033", "1.228", "46.0%", "15.2%", "\u00b17%", "10\u2013100"]:
        ok(key in s, "C4 abstract/results claim %r missing from the manuscript" % key)

    # C5 caption labels agree with the body call-outs
    for i in range(1, 8):
        ok(("Figure %d" % i) in body, "C5 Figure %d has no body call-out" % i)

    # C6 no duplicated reference DOI lines
    dois_all = re.findall(r"doi:(10\.[^\s\.]+(?:\.[^\s\.]+)*)", refs_block)
    dupd = {d for d in dois_all if dois_all.count(d) > 1}
    ok(not dupd, "C6 duplicated reference DOIs: %s" % dupd)

    # C7 the surviving-hypothesis sentence is identical in abstract and discussion
    ok("temporal variability of wall shear stress" in s,
       "C7 hypothesis phrase missing")

    # ==================================================================
    # METHOD D -- targeted checks on the third-pass amendments
    #   D re-derives the multiplicative decomposition of the WSS-CV response
    #   from the raw model output (an independent code path from the figure
    #   script), and guards the disclosure that accompanies it.
    # ==================================================================
    import math
    with open(RES / "v2_vessel_states.csv", newline="", encoding="utf-8-sig") as fh:
        vsrows = list(csv.DictReader(fh))

    def state(vessel, esr):
        for r in vsrows:
            if r["vessel"] == vessel and abs(float(r["ESR_mm_h"]) - esr) < 1e-9:
                return r
        return None

    def decompose(vessel, hi=100.0):
        r10, rh = state(vessel, 10.0), state(vessel, hi)
        D = float(r10["D_um"]) * 1e-6
        d10, dh = float(r10["CFL_um"]) * 1e-6, float(rh["CFL_um"]) * 1e-6
        g_f = float(rh["CFL_CV"]) / float(r10["CFL_CV"])            # Eq (9)
        e_f = (D / (D - 2 * dh)) / (D / (D - 2 * d10))              # Eq (8)
        tot = float(rh["WSS_CV"]) / float(r10["WSS_CV"])
        return (100.0 * math.log(g_f) / math.log(tot),
                100.0 * math.log(e_f) / math.log(tot),
                2 * d10 / D, 2 * dh / D, 100.0 * (tot - 1.0))

    # D1 the shear-gate share quoted vessel-by-vessel in Section 3.6 (ESR 10 -> 100)
    for vessel, exp in [("Glomerular capillary", 0.05), ("Peritubular capillary", 0.16),
                        ("Vasa recta (medulla)", 0.84), ("Vasa recta - hypoperfused", 4.62)]:
        gate, geo, _, _, _ = decompose(vessel)
        ok(abs(gate - exp) < 0.06,
           "D1 %s shear-gate share %.2f%% != manuscript %.2f%%" % (vessel, gate, exp))
        ok(abs(gate + geo - 100.0) < 1e-6, "D1 %s shares do not sum to 100%%" % vessel)

    # D2 the geometric shares quoted in the Figure 6 caption
    for vessel, exp in [("Vasa recta (medulla)", 99.2), ("Vasa recta - hypoperfused", 95.4)]:
        gate, geo, _, _, _ = decompose(vessel)
        ok(abs(geo - exp) < 0.06,
           "D2 %s geometric share %.2f%% != caption %.1f%%" % (vessel, geo, exp))
        ok(("%.1f%%" % exp) in s, "D2 caption value %.1f%% absent from the manuscript" % exp)

    # D3 the 2*delta/D values quoted in Section 3.6, at BOTH the reference ESR
    #    and the top of the simulated range
    for vessel, e10, e100 in [("Glomerular capillary", 0.24, 0.34),
                              ("Vasa recta (medulla)", 0.32, 0.45),
                              ("Vasa recta - hypoperfused", 0.42, 0.59)]:
        _, _, r10, r100, _ = decompose(vessel)
        ok(abs(r10 - e10) < 0.006,
           "D3 %s 2*delta/D at ESR 10 is %.3f, manuscript %.2f" % (vessel, r10, e10))
        ok(abs(r100 - e100) < 0.006,
           "D3 %s 2*delta/D at ESR 100 is %.3f, manuscript %.2f" % (vessel, r100, e100))

    # D4 the stale attribution must not reappear
    ok("gating window of Equation (4)" not in s,
       "D4 stale attribution: the shear gate is still credited to Equation (4)")
    ok("emerged from the shear-rate gating" not in s,
       "D4 stale causal claim in Section 4.3")

    # D5 the parameter ledger now carries every Layer-4 term named in the text
    led = (SUB / "04_Supplementary" /
           "Supplementary_Table_S1_Parameter_Ledger.csv").read_text(encoding="utf-8-sig")
    for key in ["cfl_baseline_fraction_delta_over_D", "cfl_aggregation_coefficient",
                "cfl_shear_exponent", "wss_cv_aggregation_sensitivity_dCV"]:
        ok(key in led, "D5 parameter ledger is missing %s" % key)
    ok("SIGN" in led, "D5 the ledger does not state the CFL shear-exponent sign convention")

    # D6 the shipped code documents the sign that it actually implements
    s1 = (SUB / "04_Supplementary" /
          "Supplementary_Code_S1_esr_model_v2.py").read_text(encoding="utf-8")
    ok("NOT SETTLED" in s1,
       "D6 shipped Code S1 does not flag that the CFL shear sign is unsettled")
    ok("CFL_SHEAR_EXP" in s1,
       "D6 shipped Code S1 does not expose the CFL shear exponent as a parameter")
    for src_name in ["Suzuki", "Ong", "Liao", "Salame"]:
        ok(src_name in s1,
           "D6 shipped Code S1 does not cite the %s observation on the sign" % src_name)
    ok(s1 == (HERE / "code" / "esr_model_v2.py").read_text(encoding="utf-8"),
       "D6 shipped Code S1 differs from code/esr_model_v2.py")

    # D7 every Equation cross-reference resolves to a label
    #    (a reference to "Equation (4)" is satisfied by the pair 4a/4b)
    def has_label(lab):
        return lab in eqs or any(e.startswith(lab) and e != lab for e in eqs)

    for m in re.finditer(r"Equations? \(([\dab]+)\)(?: and \(([\dab]+)\))?", body):
        for lab in m.groups():
            if lab:
                ok(has_label(lab), "D7 cross-reference Equation (%s) has no label" % lab)
    for lab in re.findall(r"\(Equation ([\dab]+)\)", s):
        ok(has_label(lab), "D7 cross-reference (Equation %s) has no label" % lab)

    # D8 Figure 6 caption and figure agree on the panel count
    cap6 = captions[captions.index("**Figure 6.**"):captions.index("**Figure 7.**")]
    for lab in ["(a)", "(b)", "(c)"]:
        ok(lab in cap6, "D8 Figure 6 caption lacks panel %s" % lab)

    # ------------------------------------------------------------------
    #   D9-D13  the 10-100 mm/h extension.  Each claim made by the revised
    #   text is recomputed on an independent path that re-imports the model.
    # ------------------------------------------------------------------
    import importlib.util
    _spec = importlib.util.spec_from_file_location("mv2", HERE / "code" / "esr_model_v2.py")
    mv2 = importlib.util.module_from_spec(_spec)
    sys.modules["mv2"] = mv2          # required before exec: @dataclass resolves
    _spec.loader.exec_module(mv2)     # its own module entry during decoration

    _phi, _k0h, _k0n = mv2.calibrate_to_nephrotic_target(lambda *a, **k: None)
    hypo = [v for v in mv2.VESSELS if "hypoperfused" in v.name][0]

    def _cv_at(vessel, esr, anchor):
        D = vessel.D
        s_cal = mv2.k0_scale_from_esr(mv2.ESR_NORMAL, _k0n, _k0h, esr_hi=anchor)
        eta_cal = float(mv2.quemada(mv2.H_TUBE, 8 * vessel.V_ref / D, k0_scale=s_cal))
        dPdl = 32.0 * eta_cal * vessel.V_ref / D ** 2
        s = mv2.k0_scale_from_esr(esr, _k0n, _k0h, esr_hi=anchor)
        V = mv2.solve_velocity(D, dPdl, k0_scale=s)
        gw = 8.0 * V / D
        dl = mv2.cell_free_layer(D, mv2.aggregate_index(esr), gw)
        return mv2.cfl_variability(gw, s) * (D / max(D - 2.0 * dl, 1e-9))

    # D9 the anchor-sensitivity numbers quoted in Section 4.6
    e_a100 = 100 * (_cv_at(hypo, 100.0, 100.0) / _cv_at(hypo, 10.0, 100.0) - 1)
    e_a60 = 100 * (_cv_at(hypo, 100.0, 60.0) / _cv_at(hypo, 10.0, 60.0) - 1)
    ok(abs(e_a100 - 46.0) < 0.15, "D9 anchor-100 excess %.2f%% != 46.0%%" % e_a100)
    ok(abs(e_a60 - 48.3) < 0.15, "D9 anchor-60 excess %.2f%% != 48.3%%" % e_a60)
    ok("48.3%" in s, "D9 the Section 4.6 anchor-sensitivity value 48.3% is absent")

    def _eta_ratio(anchor, gamma=2.71227):
        f = lambda e: mv2.k0_scale_from_esr(e, _k0n, _k0h, esr_hi=anchor)
        return (float(mv2.quemada(mv2.H_TUBE, gamma, k0_scale=f(100.0)))
                / float(mv2.quemada(mv2.H_TUBE, gamma, k0_scale=f(10.0))))

    r_a100, r_a60 = _eta_ratio(100.0), _eta_ratio(60.0)
    ok(abs(r_a100 - 1.097) < 0.001, "D9 anchor-100 low-shear ratio %.4f != 1.097" % r_a100)
    ok(abs(r_a60 - 1.150) < 0.002, "D9 anchor-60 low-shear ratio %.4f != 1.150" % r_a60)
    ok("1.150" in s, "D9 the Section 4.6 anchor-60 viscosity ratio 1.150 is absent")

    # D10 the extrapolated ESR at which the fold threshold would be reached
    _frac = (1.15 - 1.0) / (_k0h / _k0n - 1.0)
    _esr_fold = (math.sqrt(10.0) + _frac * (math.sqrt(100.0) - math.sqrt(10.0))) ** 2
    ok(1000.0 <= _esr_fold <= 1400.0,
       "D10 extrapolated fold-threshold ESR %.0f is not of the order 1.2e3" % _esr_fold)
    ok("1.2 \u00d7 10\u00b3" in s, "D10 the quoted fold-threshold ESR (1.2 x 10^3) is absent")

    # D11 the fixed-flow-rate maximum rise quoted in Section 3.4
    with open(RES / "v2_wss_fixedflow.csv", newline="", encoding="utf-8-sig") as fh:
        ffrows = list(csv.DictReader(fh))
    _ffmax = max(float(r["tau_constQ_ratio"]) for r in ffrows
                 if abs(float(r["ESR_hi"]) - 100.0) < 1e-9)
    ok(abs((_ffmax - 1.0) * 100 - 5.2) < 0.1,
       "D11 fixed-flow max rise %.1f%% != the quoted 5.2%%" % ((_ffmax - 1.0) * 100))
    ok("5.2%" in s, "D11 the fixed-flow value 5.2% is absent from the manuscript")

    # D12 the k0 amplification at the three named ESR points (Section 3.8)
    for esr, exp in [(60.0, 2.2), (80.0, 2.8), (100.0, 3.3)]:
        amp = 100 * (mv2.k0_scale_from_esr(esr, _k0n, _k0h) - 1.0)
        ok(abs(amp - exp) < 0.15,
           "D12 k0 amplification at ESR %g is %.2f%%, text implies %.1f%%"
           % (esr, amp, exp))

    # D13 the graded response is strictly monotone in ESR in every vessel, and
    #     the medullary contrast quoted in Section 3.6 holds
    for vessel in ["Glomerular capillary", "Peritubular capillary",
                   "Vasa recta (medulla)", "Vasa recta - hypoperfused"]:
        seq = [wsscv(vessel, float(e)) for e in range(10, 101, 10)]
        ok(all(b > a for a, b in zip(seq, seq[1:])),
           "D13 WSS CV is not strictly increasing with ESR in %s" % vessel)
    _, _, _, _, exc_g = decompose("Glomerular capillary")
    _, _, _, _, exc_h = decompose("Vasa recta - hypoperfused")
    ok(abs(exc_h / exc_g - 3.0) < 0.1,
       "D13 medullary/glomerular excess ratio %.2f != the quoted 3.0" % (exc_h / exc_g))



    # ------------------------------------------------------------------
    #   D14-D18  the CFL shear-exponent robustness sweep (Section 3.7,
    #   Table 7, Figure 6d, prediction P5).  These checks enforce that the
    #   sign-independence and sign-dependence statements in the manuscript
    #   are exactly what the shipped robustness table contains.
    # ------------------------------------------------------------------
    with open(RES / "v2_cfl_sign_robustness.csv", newline="", encoding="utf-8-sig") as fh:
        rb = list(csv.DictReader(fh))
    vessels4 = ["Glomerular capillary [%]", "Peritubular capillary [%]",
                "Vasa recta (medulla) [%]", "Vasa recta - hypoperfused [%]"]
    ok(len(rb) == len(mv2.CFL_SHEAR_EXP_SCAN),
       "D14 robustness sweep has %d rows, scan defines %d"
       % (len(rb), len(mv2.CFL_SHEAR_EXP_SCAN)))
    by_s = {round(float(r["shear_exp"]), 6): r for r in rb}

    # D14 every excess is positive for every s and every vessel  (existence)
    for r in rb:
        for col in vessels4:
            ok(float(r[col]) > 0.0,
               "D14 excess is not positive: s=%s vessel=%s value=%s"
               % (r["shear_exp"], col, r[col]))

    # D15 for s<0 the worst vessel is the hypoperfused vasa recta; for s>0 it
    #     is the glomerular capillary  (sign-dependence of the target)
    for r in rb:
        s_ = float(r["shear_exp"])
        worst = max(vessels4, key=lambda c: float(r[c]))
        if s_ < -1e-9:
            ok(worst == "Vasa recta - hypoperfused [%]",
               "D15 at s=%s the worst vessel is %s, not the hypoperfused vasa recta"
               % (r["shear_exp"], worst))
        elif s_ > 1e-9:
            ok(worst == "Glomerular capillary [%]",
               "D15 at s=%s the worst vessel is %s, not the glomerular capillary"
               % (r["shear_exp"], worst))
    # the CSV's own max_vessel column must agree with the recomputed argmax
    for r in rb:
        worst = max(vessels4, key=lambda c: float(r[c]))
        ok(r["max_vessel"].strip() == worst.replace(" [%]", ""),
           "D15 max_vessel column (%s) disagrees with argmax (%s) at s=%s"
           % (r["max_vessel"], worst, r["shear_exp"]))

    # D16 the four Table-7 rows quoted in the manuscript reproduce exactly
    t7 = [(-0.24, "Vasa recta - hypoperfused [%]", 112.2),
          (-0.12, "Vasa recta - hypoperfused [%]", 46.0),
          (0.12, "Glomerular capillary [%]", 42.8),
          (0.24, "Glomerular capillary [%]", 106.6)]
    for s_, col, exp in t7:
        got = float(by_s[round(s_, 6)][col])
        ok(abs(got - exp) < 0.15,
           "D16 Table 7 value at s=%+.2f is %.1f%%, manuscript %.1f%%"
           % (s_, got, exp))
        ok("%.1f%%" % exp in s,
           "D16 Table 7 value %.1f%% (s=%+.2f) is absent from the manuscript" % (exp, s_))

    # D17 the normally perfused vasa recta is nearly invariant: span < 1.0 pp
    vr = [float(r["Vasa recta (medulla) [%]"]) for r in rb]
    ok(max(vr) - min(vr) < 1.0,
       "D17 vasa recta (medulla) spans %.2f pp, quoted as 23.8-24.5%%"
       % (max(vr) - min(vr)))
    ok(abs(min(vr) - 23.8) < 0.1 and abs(max(vr) - 24.5) < 0.1,
       "D17 vasa recta span endpoints (%.1f-%.1f) != the quoted 23.8-24.5"
       % (min(vr), max(vr)))

    # D18 the crossover, the new equation label, Table 7 and prediction P5 are
    #     all present in the manuscript text
    for token in ["+0.02", "Equation (7a)", "Table 7", "P5", "Figure 6d"]:
        ok(token in s, "D18 the manuscript does not mention %r" % token)

    # ==================================================================
    # METHOD E -- this round: the amendments made in response to the
    #   third-party review (citation attribution, delta0 provenance, the
    #   Equation-(9) parameters, medullary autoregulation, Section 3.9's
    #   title, and the structured abstract this journal requires).
    # ==================================================================
    # E1 the Westergren-velocity linearity now cites ref 3 alone; ref 4 is
    #    cited for its own later 203-sample MCV study
    ok("n = 32) with a slope of 0.778.\u00b3,\u2074" not in s,
       "E1 the Westergren linearity is still jointly attributed to refs 3 and 4")
    ok("slope 0.778, in a 32-sample series).\u00b3" in s,
       "E1 the Westergren linearity is no longer attributed to ref 3")
    ok("confirmed the ESR\u2013aggregation route in 203 clinical samples" in s,
       "E1 ref 4 is not cited for its own measured finding")

    # E2 the 0.16 D coefficient is disclosed as a modelling choice, with the
    #    resulting absolute widths and the explicit cap
    for tok in ["\u03b4\u2080 = 0.16 D a modelling choice",
                "base widths of 1.28, 1.60 and 2.40 \u00b5m",
                "capped at 2.5 \u00b5m"]:
        ok(tok in s, "E2 the delta0 provenance statement is incomplete: %r" % tok)

    # E3 the measured gate anchor is quoted, and Equation (9) is described as
    #    having four parameters rather than two
    ok("The four parameters of Equation (9)" in s,
       "E3 Equation (9) is still described as having two constants")
    ok("9.2 \u00b1 0.6 s\u207b\u00b9" in s,
       "E3 the measured gate anchor 9.2 +/- 0.6 s-1 is not quoted")

    # E4 the modelled layer is compared with the measured 0.8-3.1 um band
    ok("The reference measured band is 0.8\u20133.1 \u00b5m" in s,
       "E4 the modelled layer is not compared with the measured band")

    # E5 Section 3.9's title now covers both halves of the section
    ok("### 3.9 Calibration: the viscosity rise is mostly plasma-borne, and "
       "haematocrit is the missing covariate" in s,
       "E5 the Section 3.9 title does not cover the haematocrit finding")

    # E6 the medullary autoregulation caveat is present in the Discussion
    ok("Myogenic autoregulation is well developed in the cortex but weak in "
       "the medulla" in s,
       "E6 the medullary autoregulation caveat is missing")

    # E7 the ledger records the two new Layer-4 rows, and flags the baseline CV
    #    as an assumption rather than a measurement
    for key in ["wss_cv_gate_exponent_n", "wss_cv_measured_gate_anchor"]:
        ok(key in led, "E7 the ledger does not record %s" % key)
    ok("ASSUMPTION, not a measurement. Adopted as the mid-point (0.30)" in led,
       "E7 the ledger does not flag the baseline CV as an assumption")

    # E8 the four Eq-(9) parameters and the measured anchor appear together in
    #    the Methods text, so the parameter set is fully traceable
    ok("\u0394CV = 0.22, \u03b3\u0307_s = 20 s\u207b\u00b9 and n = 1.5" in s,
       "E8 Equation (9) is not fully parameterised in the Methods")

    # E9 the manuscript footer version stamp must equal the version declared in
    #    the submission checklist (a stale stamp slipped through in the v0.8
    #    round, so it is policed from now on)
    m_foot = re.search(r"\*Manuscript (v[0-9]+\.[0-9]+)\.", s)
    ok(m_foot is not None, "E9 the manuscript footer carries no version stamp")
    if m_foot:
        _v = m_foot.group(1)
        _rd = (SUB / "00_README_\u6295\u7a3f\u6e05\u5355\u4e0e\u8bf4\u660e.md").read_text(
            encoding="utf-8")
        ok(("\u7a3f\u4ef6\u7248\u672c %s" % _v) in _rd,
           "E9 footer says %s but the checklist declares another version" % _v)

    global checks
    print("=" * 78)
    print("VERIFICATION REPORT   checks run: %d" % checks)
    print("=" * 78)
    if fails:
        print("FAILED ITEMS (%d):" % len(fails))
        for f in fails:
            print("   FAIL  " + f)
    else:
        print("ALL CHECKS PASSED")
    if warns:
        print("WARNINGS (%d):" % len(warns))
        for w in warns:
            print("   warn  " + w)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
