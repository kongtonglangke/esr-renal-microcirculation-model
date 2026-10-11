# -*- coding: utf-8 -*-
"""Independent cross-check (method X).

Deliberately does NOT import verify_submission.py: it re-derives the same
facts through a different code path (hash equality, pandas recomputation,
DOCX readback, image geometry) so that a common-mode error would show up.
"""
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
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
SUP = SUB / "04_Supplementary"
MS = HERE / "Manuscript_ESR_renal_medulla_hypothesis_v0.1.md"

fails, n = [], 0


def chk(cond, msg):
    global n
    n += 1
    if not cond:
        fails.append(msg)


# X1 byte-identity of the source and the delivered manuscript
h_md = hashlib.sha256(MS.read_bytes()).hexdigest()
h_del = hashlib.sha256((SUB / "02_Manuscript.md").read_bytes()).hexdigest()
chk(h_md == h_del, "X1 02_Manuscript.md sha256 %s != working manuscript %s" % (h_del[:12], h_md[:12]))

# X2 every shipped supplementary code file is byte-identical to its source
pairs = [("Supplementary_Code_S1_esr_model_v2.py", "esr_model_v2.py"),
         ("Supplementary_Code_S2_esr_model_v3.py", "esr_model_v3.py"),
         ("Supplementary_Code_S3_make_all_figures.py", "make_ms_figures.py"),
         ("Supplementary_Code_S4_esr_model_v4_flowcurve.py", "esr_model_v4_flowcurve.py"),
         ("Supplementary_Code_S5_esr_model_v5_calibration.py", "esr_model_v5_calibration.py")]
for shipped, src in pairs:
    a = hashlib.sha256((SUP / shipped).read_bytes()).hexdigest()
    b = hashlib.sha256((HERE / "code" / src).read_bytes()).hexdigest()
    chk(a == b, "X2 %s != code/%s" % (shipped, src))

# X3 Table 7 recomputed straight from the robustness CSV (four quotients)
rows = list(csv.DictReader(open(SUP / "Supplementary_Data_S1_v2_cfl_sign_robustness.csv",
                                newline="", encoding="utf-8-sig")))
by = {round(float(r["shear_exp"]), 3): r for r in rows}
man = MS.read_text(encoding="utf-8")
for s_, col, txt in [(-0.24, "Vasa recta - hypoperfused [%]", "112.2"),
                     (-0.12, "Vasa recta - hypoperfused [%]", "46.0"),
                     (0.12, "Glomerular capillary [%]", "42.8"),
                     (0.24, "Glomerular capillary [%]", "106.6")]:
    val = float(by[s_][col])
    chk(abs(val - float(txt)) < 0.15, "X3 s=%s %s=%.1f != %s" % (s_, col, val, txt))
    chk("+" + txt + "%" in man, "X3 manuscript lacks the Table-7 token +%s%%" % txt)

# X4 sign-independence: every excess positive, at every s, in every vessel
cols4 = ["Glomerular capillary [%]", "Peritubular capillary [%]",
         "Vasa recta (medulla) [%]", "Vasa recta - hypoperfused [%]"]
chk(all(float(r[c]) > 0 for r in rows for c in cols4),
    "X4 some excess is non-positive")
# and the crossover: worst vessel flips between the two groups
worst_neg = {max(cols4, key=lambda c: float(r[c])) for r in rows if float(r["shear_exp"]) < 0}
worst_pos = {max(cols4, key=lambda c: float(r[c])) for r in rows if float(r["shear_exp"]) > 0}
chk(worst_neg == {"Vasa recta - hypoperfused [%]"}, "X4 s<0 worst set %s" % worst_neg)
chk(worst_pos == {"Glomerular capillary [%]"}, "X4 s>0 worst set %s" % worst_pos)

# X5 the delivered DOCX really contains Table 7 / Eq (7a) / the new DOIs
from docx import Document
doc = Document(str(SUB / "02_Manuscript.docx"))
dall = "\n".join(p.text for p in doc.paragraphs) + "\n" + \
       "\n".join(c.text for t in doc.tables for r in t.rows for c in r.cells)
chk(len(doc.tables) == 7, "X5 DOCX tables = %d, expected 7" % len(doc.tables))
for key in ["Equation (7a)", "Table 7", "112.2%", "106.6%", "42.8%",
            "doi:10.1063/1.5127879", "doi:10.1016/j.mvr.2025.104859",
            "does not settle the sign", "P5"]:
    chk(key in dall, "X5 DOCX lacks %r" % key)

# X6 the ZIP container of the DOCX is well-formed and non-empty
with zipfile.ZipFile(SUB / "02_Manuscript.docx") as z:
    chk(z.testzip() is None and len(z.namelist()) > 5,
        "X6 02_Manuscript.docx ZIP is corrupt")

# X7 figure geometry: Figure 6 is the 4-panel version (aspect ~5.15:1)
from PIL import Image
w, h = Image.open(SUB / "03_Figures" / "Figure6_medullary_amplification.png").size
chk(w / h > 4.5, "X7 Figure 6 aspect %.2f does not look like the 4-panel layout" % (w / h))

# X8 abstract word count, counted independently
ab = man[man.index("## Abstract"):man.index("**Keywords:**")]
ab = re.sub(r"\(Abstract:.*?\)", "", ab.replace("## Abstract", ""))
chk(len(ab.split()) == 198, "X8 abstract = %d words" % len(ab.split()))

# X9 references 1..28 consecutive, and 24 DOIs
refs = man[man.index("## References"):man.index("## Figure captions")]
nums = [int(x) for x in re.findall(r"^(\d+)\. ", refs, flags=re.M)]
chk(nums == list(range(1, 29)),
    "X9 ref numbering %s" % (nums[:5] + ["..."] + nums[-3:]))
chk(len(re.findall(r"doi:10\.", refs)) == 24,
    "X9 DOI count %d" % len(re.findall(r"doi:10\.", refs)))

# X10 every cached PubMed id is still present in the reference list
meta = json.load(open(HERE / "results" / "refs_verified_metadata.json", encoding="utf-8"))
for pm in re.findall(r"PMID (\d+)", refs):
    chk(pm in meta, "X10 PMID %s has no verified metadata" % pm)


# X11 the title page carries the same title as the manuscript, and the running
#     title respects the 45-character limit
tp = (SUB / "01_Title_Page.md").read_text(encoding="utf-8")
ms_title = man.split("\n")[0].lstrip("# ").strip()
seg = tp.split("## Article title")[1].split("**Short running title")[0]
tp_title = [ln.strip() for ln in seg.split("\n") if ln.strip()][0]
chk(tp_title == ms_title,
    "X11 title page title %r != manuscript title %r" % (tp_title[:60], ms_title[:60]))
rt = re.search(r"\*\*Short running title \(\u2264 45 characters\):\*\* (.+)", tp)
chk(rt is not None, "X11 no running title found")
if rt:
    chk(len(rt.group(1).strip()) <= 45,
        "X11 running title is %d chars: %r" % (len(rt.group(1).strip()), rt.group(1)))

# X12 the cover letter quotes the manuscript title verbatim
cl = (SUB / "05_Cover_Letter.md").read_text(encoding="utf-8")
chk(ms_title in cl, "X12 the cover letter does not quote the manuscript title")
chk("five falsifiable predictions" in cl,
    "X12 the cover letter still states the wrong prediction count")

# X13 the reviewer file holds 12 candidates + 9 reserve names, and the authors
#     of refs 26-28 are among the reserves
rv = (SUB / "07_Suggested_Reviewers.md").read_text(encoding="utf-8")
reserve = rv.split("## Reserve names")[1].split("## Status")[0]
names = re.findall(r"\|\s*\*\*(?:Prof\.|Dr)\s+[^|*]+\*\*", reserve)
chk(len(names) == 9, "X13 reserve list holds %d names, expected 9" % len(names))
for who in ["Ong", "Chen", "Fenech"]:
    chk(who in reserve, "X13 the authors of refs 26-28 are incomplete: %s missing" % who)


# X14 the abstract on the title page must be byte-identical to the manuscript's
ms_ab = man.split("## Abstract")[1].split("**Keywords")[0].strip()
tp_ab = tp.split("## Abstract")[1].split("**Word count")[0].strip()
chk(ms_ab == tp_ab,
    "X14 title-page abstract differs from the manuscript abstract "
    "(%d vs %d words)" % (len(tp_ab.split()), len(ms_ab.split())))
chk("**Word count: 198.**" in tp, "X14 the title page states the wrong abstract word count")

# X15 no stale counts survive anywhere in the delivered text files
for f in sorted(SUB.rglob("*.md")):
    txt = f.read_text(encoding="utf-8")
    for stale in ["197 words", "four predictions", "four falsifiable"]:
        chk(stale not in txt, "X15 %s still contains %r" % (f.name, stale))


# X16 the abstract must be structured - checked here without importing the
#     verify script, so a common-mode omission cannot hide
_labs = [x for x in ["**Background.**", "**Objective.**", "**Methods.**",
                     "**Results.**", "**Conclusions.**"] if x in man]
chk(len(_labs) == 5, "X16 structured-abstract labels present: %d/5" % len(_labs))

# X17 the parameter ledger grew with the newly documented Layer-4 terms, and
#     the two new rows parse as CSV with a non-empty source
_s1_txt = (SUP / "Supplementary_Table_S1_Parameter_Ledger.csv").read_text(
    encoding="utf-8-sig")
_s1_rows = list(csv.DictReader(io.StringIO(_s1_txt)))
chk(len(_s1_rows) >= 42,
    "X17 parameter ledger has %d rows (expected >= 42)" % len(_s1_rows))
chk("wss_cv_gate_exponent_n" in _s1_txt, "X17 ledger missing the gate exponent n")
chk("wss_cv_measured_gate_anchor" in _s1_txt, "X17 ledger missing the gate anchor")
chk(all(r.get("source", "").strip() for r in _s1_rows),
    "X17 some ledger rows have an empty source cell")

# X18-X20 the public-repository export must mirror the submission record
_export = HERE / "github_upload" / "esr-renal-microcirculation-model"
chk(_export.is_dir(), "X18 the GitHub export folder is missing")
if _export.is_dir():
    _figdir = _export / "figures"
    _nfig = 0
    for _f in sorted((SUB / "03_Figures").glob("*.png")):
        _e = _figdir / _f.name
        chk(_e.is_file() and
            hashlib.sha256(_f.read_bytes()).hexdigest() ==
            hashlib.sha256(_e.read_bytes()).hexdigest(),
            "X18 export figure differs from the submission figure: %s" % _f.name)
        _nfig += 1
    chk(_nfig == 7, "X18 exported figures found: %d (expected 7)" % _nfig)

    # X19 text results are mirrored; the verification log is a run artefact and
    #     is therefore excluded from the comparison
    _pr = HERE / "results"
    _er = _export / "results"
    _names = ["v2_anchors.json", "v2_cfl_sign_robustness.csv",
              "v2_esr_to_k0.csv", "v2_foldchange.csv", "v2_foldchange_by_esr.csv",
              "v2_param_sensitivity.csv", "v2_shear_gating.csv",
              "v2_vessel_states.csv", "v2_viscosity_vs_shear.csv",
              "v2_wss_fixedflow.csv", "v3_constants.json",
              "v3_layer1_measured_mapping.csv", "v3_scaling_check.csv",
              "v4_flow_curve.csv", "v4_fold_slope.csv", "v4_headline.json",
              "v4_root_count.csv", "v5_calibration.json"]
    _bad = [nm for nm in _names
            if not (_er / nm).is_file() or
            (_pr / nm).read_bytes().replace(b"\r\n", b"\n") !=
            (_er / nm).read_bytes().replace(b"\r\n", b"\n")]
    chk(not _bad, "X19 export results differ from the project: %s" % _bad[:4])
    chk(len(list(_er.glob("*"))) >= 24,
        "X19 export results/ holds only %d files" % len(list(_er.glob("*"))))

    # X20 the export carries the manuscript verbatim (line endings normalised)
    _em = _export / "manuscript" / "Manuscript_ESR_renal_medulla_hypothesis.md"
    chk(_em.is_file() and
        _em.read_bytes().replace(b"\r\n", b"\n") ==
        MS.read_bytes().replace(b"\r\n", b"\n"),
        "X20 export manuscript text differs from the working manuscript")
    chk((_export / "supplementary" /
         "Supplementary_Table_S1_Parameter_Ledger.csv").is_file(),
        "X20 export is missing the parameter ledger")

    # X21 the public repository must carry the archival DOI, never a placeholder
    _rd = (_export / "README.md").read_text(encoding="utf-8")
    chk("10.6084/m9.figshare.34333371" in _rd,
        "X21 repository README lacks the archival DOI")
    chk("DOI-pending" not in _rd and "DOI pending" not in _rd,
        "X21 repository README still carries a DOI placeholder")
    _cf = (_export / "CITATION.cff").read_text(encoding="utf-8")
    chk('doi: "10.6084/m9.figshare.34333371"' in _cf,
        "X21 CITATION.cff lacks the doi field")


print("=" * 70)
print("INDEPENDENT CROSS-CHECK   checks run: %d" % n)
print("=" * 70)
if fails:
    print("FAILED (%d):" % len(fails))
    for f in fails:
        print("   FAIL  " + f)
else:
    print("ALL CROSS-CHECKS PASSED")
