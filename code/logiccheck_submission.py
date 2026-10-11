# -*- coding: utf-8 -*-
"""Logic / narrative-consistency check (method 3).

Nothing here recomputes the physics: it asks whether the manuscript is
internally coherent -- every cross-reference resolves, every number quoted in
more than one place agrees, every prediction is defined and used, and no
unconditional claim about the medullary localisation survives anywhere.
"""
import json
import re
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
MS = HERE / "Manuscript_ESR_renal_medulla_hypothesis_v0.1.md"

s = MS.read_text(encoding="utf-8")
body = s[s.index("## 1. Introduction"):s.index("## Declarations")]
caps = s[s.index("## Figure captions"):s.index("## Tables (in the body")]
disc = s[s.index("## 4. Discussion"):s.index("## Declarations")]

fails, n = [], 0


def chk(cond, msg):
    global n
    n += 1
    if not cond:
        fails.append(msg)


# L1 every "Section N.M" cross-reference resolves to a real heading
heads = set(re.findall(r"^#{2,3} (\d+\.\d+)", s, flags=re.M))
for ref in sorted(set(re.findall(r"Sections? (\d+\.\d+)", s))):
    chk(ref in heads, "L1 dangling cross-reference to Section %s" % ref)

# L2 every prediction P1..P5 is defined once and cited at least once
defined = re.findall(r"\*\*P(\d) \(", s)
chk(sorted(defined) == ["1", "2", "3", "4", "5"],
    "L2 predictions defined: %s (expected P1..P5)" % sorted(defined))
chk(len(defined) == len(set(defined)), "L2 a prediction is defined more than once")
for p in ["P1", "P2", "P3", "P5"]:
    chk(s.count(p) >= 2, "L2 prediction %s is defined but never referenced again" % p)
chk("five predictions" in s, "L2 the text does not say the list holds five predictions")

# L3 the headline pair 46.0% / 15.2% is quoted consistently where it appears
chk(s.count("46.0%") >= 3, "L3 46.0%% appears only %d times" % s.count("46.0%"))
chk(s.count("15.2%") >= 3, "L3 15.2%% appears only %d times" % s.count("15.2%"))
# the abstract pair must be the default-sign pair, not the reversed one
ab = s[s.index("## Abstract"):s.index("**Keywords:**")]
chk("46.0%" in ab and "15.2%" in ab,
    "L3 the abstract does not carry the default-sign pair")
chk("3.0-fold" in s, "L3 the 3.0-fold medullary/glomerular contrast is absent")

# L4 no unconditional medullary-localisation claim survives: wherever the
#    medulla is called the most-affected vessel it must be conditioned on the
#    sign, and the phrase "the localisation is established" must be negated.
_COND = ["under the", "whereas", "conditional", "not claim", "do not",
         "if ", "reverses", "the sign", "when ", "either sign"]
for sent in re.split(r"(?<=\.)\s+(?=[A-Z(])", s):
    low = sent.lower()
    if re.search(r"medulla (is|was) the most", low) or \
       "medullary localisation is established" in low:
        chk(any(k in low for k in _COND),
            "L4 unconditional medullary claim: %s" % sent.strip()[:100])

# L5 the reversed-sign counterfactual is stated with its own numbers
chk("42.8%" in s and "106.6%" in s and "112.2%" in s,
    "L5 the reversed-sign / extreme-s values are incomplete")

# L6 statements file word-counts agree with the manuscript actually shipped
st = (SUB / "06_Statements_and_Declarations.md").read_text(encoding="utf-8")
refs = s[s.index("## References"):s.index("## Figure captions")]
nref = len(re.findall(r"^\d+\. ", refs, flags=re.M))
chk(str(nref) in st, "L6 statements file does not record the true reference count (%d)" % nref)
nfig = len(re.findall(r"\*\*Figure (\d)\.\*\*", caps))
chk(str(nfig) in st or ("%d figures" % nfig) in st,
    "L6 statements file does not record the true figure count (%d)" % nfig)

# L7 every Figure / Table call-out in the body is inside the defined ranges
for m in sorted(set(re.findall(r"Table (\d)", body)), key=int):
    chk(1 <= int(m) <= 7, "L7 body calls Table %s but only 7 exist" % m)
for m in sorted(set(re.findall(r"Figure (\d)", body)), key=int):
    chk(1 <= int(m) <= 7, "L7 body calls Figure %s but only 7 exist" % m)

# L8 the abstract, the results and the caption give the same default-sign order
chk("hypoperfused medulla" in ab and "glomerular capillary" in ab,
    "L8 the abstract does not name both ends of the default-sign contrast")
chk("hypoperfused vasa recta" in caps, "L8 Figure 6 caption omits the default-sign worst vessel")

# L9 the discussion no longer claims the medullary result is model-independent
chk("model-independent fact" in s and "conditional on" in s,
    "L9 the conditional framing of the medullary result is incomplete")

# L10 the third-party critique points that were accepted are visible: the
#     unresolved sign, the decisive experiment, and the CFD non-escalation
chk("why we did not escalate to cfd" in s.lower(),
    "L10 the CFD non-escalation rationale is missing")
chk("the single measurement that would decide the question" in s.lower(),
    "L10 the decisive-experiment statement is missing")

# L11 no stale artefacts from the previous version survive
for stale in ["25 references", "1..25", "v0.5", "six tables", "10\u201360 mm h"]:
    chk(stale not in s, "L11 stale token %r is still present" % stale)


# L12 the title itself must foreground the sign-dependence as the core result
title = s.split("\n")[0]
chk("unresolved constitutive sign" in title,
    "L12 the title does not foreground the unresolved sign: %r" % title[:90])
chk("decides which renal microvessel" in title,
    "L12 the title does not state that the sign decides the target vessel")

# L13 the abstract must carry the sign-first framing, not a caveat framing
chk("That sign alone decides the anatomical target" in ab,
    "L13 the abstract does not state that the sign decides the target")

# L14 the prediction count must be five everywhere (P5 was added last round)
chk("four predictions" not in s, "L14 the text still says 'four predictions'")
chk("four falsifiable predictions" not in s,
    "L14 the text still says 'four falsifiable predictions'")
chk(s.count("five predictions") >= 2,
    "L14 'five predictions' appears only %d times" % s.count("five predictions"))

# L15 the two promoted sections must name the sign in their headings
chk("The most exposed segment depends on the sign" in s,
    "L15 the Section 3.7 heading lost its sign framing")
chk("whose anatomical target is decided by one unresolved sign" in s,
    "L15 the Section 4.1 heading lost its sign framing")
chk("central result of the study" in s,
    "L15 Section 3.7 no longer declares itself the central result")
chk("principal deliverable" in s,
    "L15 Section 4.1 no longer calls the unresolved sign the model's deliverable")


# L16 the abstract must be structured into five labelled parts (this journal's
#     requirement); a single unlabelled paragraph must fail this check
chk(sum(lb in ab for lb in ["**Background.**", "**Objective.**", "**Methods.**",
                            "**Results.**", "**Conclusions.**"]) == 5,
    "L16 the abstract is not structured into five labelled parts")

# L17 Section 3.9 must advertise the haematocrit finding in its heading, since
#     the section reports both the calibration and the under-determination
chk("haematocrit is the missing covariate" in s,
    "L17 the Section 3.9 heading does not cover the haematocrit finding")

# L18 the methods must no longer describe Equation (9) as having two constants
chk("The two constants of Equation (9)" not in s,
    "L18 Equation (9) is still described as having two constants")

# L19 the repository README must state the same version as the manuscript and
#     quote the headline numbers exactly as the model produces them
_rm = HERE / "github_upload" / "esr-renal-microcirculation-model" / "README.md"
chk(_rm.is_file(), "L19 the repository README is missing")
if _rm.is_file():
    _rt = _rm.read_text(encoding="utf-8")
    for _needle in ["v0.8", "10\u2013100 mm h\u207b\u00b9", "46.0%",
                    "112.2%", "106.6%", "23.8\u201324.5%"]:
        chk(_needle in _rt,
            "L19 repository README is missing %r" % _needle)
    chk("github.com/" in _rt, "L19 repository README carries no repository URL")

# L20 the archival DOI must be the same string in the manuscript and in the
#     public repository README, and no placeholder may survive anywhere
_ARCH = "10.6084/m9.figshare.34333371"
chk(_ARCH in s, "L20 manuscript does not quote the archival DOI")
chk("will be deposited in a public archive" not in s,
    "L20 manuscript still carries the pre-DOI promise sentence")
if _rm.is_file():
    _rrt = _rm.read_text(encoding="utf-8")
    chk(_ARCH in _rrt, "L20 repository README does not quote the archival DOI")
    chk("DOI-pending" not in _rrt and "DOI pending" not in _rrt,
        "L20 repository README still carries a DOI placeholder")


print("=" * 70)
print("LOGIC / NARRATIVE CHECK   checks run: %d" % n)
print("=" * 70)
if fails:
    print("FAILED (%d):" % len(fails))
    for f in fails:
        print("   FAIL  " + f)
else:
    print("ALL LOGIC CHECKS PASSED")
