# ESR → renal microcirculation: a reduced-order haemodynamic model

[![DOI](https://img.shields.io/badge/DOI-10.6084%2Fm9.figshare.34333371-blue)](https://doi.org/10.6084/m9.figshare.34333371)
[![License: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](#licence)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Reproducible](https://img.shields.io/badge/results-deterministic-brightgreen)](#reproducibility)

Companion repository for the manuscript

> **Wang Y.** *One unresolved constitutive sign decides which renal microvessel an elevated
> erythrocyte sedimentation rate most loads: a reduced-order haemodynamic model.*
> Submitted to *Clinical Hemorheology and Microcirculation*.

This repository is the *complete model repository* referred to in the paper's
Data and Code Availability statement. It contains every line of code, every parameter
value, every numerical output and every figure, so that each number in the paper can be
recomputed and each judgement can be checked. An archived, citable snapshot lives at
<https://doi.org/10.6084/m9.figshare.34333371>.

---

## 1. What the model does

A four-layer **reduced-order** (laptop-scale) model that carries the erythrocyte
sedimentation rate (ESR) through the constitutive chain

```
ESR  ──►  red-cell aggregate size  ──►  shear-dependent viscosity (Quemada law)
     ──►  microvascular pressure–flow state  ──►  wall shear stress (WSS)
                                               └─►  temporal variability of WSS
```

and then asks **where in the renal microcirculation the effect is largest**, at
physiological diameters, pressures and haematocrit.

| Layer | Physical content | Script |
|:--|:--|:--|
| 1 | ESR → aggregate size, anchored to measured aggregation-index → ESR mappings | `code/esr_model_v3.py` |
| 2 | Quemada non-Newtonian viscosity; aggregation effect intrinsically confined to low shear | `code/esr_model_v2.py` |
| 3 | Core / cell-free-layer (CFL) two-layer construction, mass conservation, shear gating of WSS variability | `code/esr_model_v2.py` |
| 4 | Pressure–flow curve, fold / stasis detection, inverse calibration of the viscosity kernel | `code/esr_model_v4_flowcurve.py`, `code/esr_model_v5_calibration.py` |
| Figures | All seven manuscript figures | `code/make_ms_figures.py` |

Vessels: glomerular capillary, peritubular capillary, vasa recta (normally perfused),
vasa recta (hypoperfused). ESR is swept over **10–100 mm h⁻¹** against a reference of
10 mm h⁻¹.

## 2. Headline result

Two statements survive every robustness test, and they are of different kinds.

**(a) Sign-independent — the effect exists and is graded.** The ESR-driven rise in the
temporal variability of wall shear stress is positive **in every vessel and at every value
of the one parameter the literature leaves unsettled** — the shear exponent *s* of the
cell-free-layer relation δ ∝ γ̇ ˢ, scanned over −0.24 … +0.24. In the hypoperfused medulla
the excess relative to ESR 10 mm h⁻¹ rises from 6.5% at ESR 20 to 17.1% at 40, 26.8% at 60,
36.4% at 80 and 46.0% at 100.

**(b) Sign-dependent — the anatomical target is not fixed by the model.** *Which* vessel is
most loaded is decided entirely by the sign of *s*, with a crossover at *s* ≈ +0.02:

| *s* | most loaded vessel | excess at ESR 100 |
|:--|:--|:--|
| −0.24 … 0.00 | vasa recta, hypoperfused (medulla) | 112.2% … 26.1% |
| +0.06 … +0.24 | glomerular capillary | 31.3% … 106.6% |

The normally perfused vasa recta is almost invariant across the whole range (23.8–24.5%),
because its wall shear rate (≈109 s⁻¹) lies close to the 100 s⁻¹ reference of the CFL
relation, so that the shear factor is ≈1 whatever the sign. Full sweep:
`results/v2_cfl_sign_robustness.csv`.

The literature reports this sign inconsistently (see §4 of the manuscript and the
`cfl_shear_exponent` row of the parameter ledger), which is why the model treats it as an
explicit free parameter rather than asserting a value.

## 3. Repository layout

```
.
├── code/
│   ├── esr_model_v2.py             # Layers 2–3: viscosity, vessels, CFL, WSS variability
│   ├── esr_model_v3.py             # Layer 1: ESR → aggregate-size mapping (measured anchors)
│   ├── esr_model_v4_flowcurve.py   # Layer 4: pressure–flow curve, fold/stasis; Figure 7
│   ├── esr_model_v5_calibration.py # Layer 4: inverse calibration; Supplementary Table S2
│   ├── make_ms_figures.py          # builds Figures 1–6
│   ├── utils/md2docx.py            # manuscript build helper (Markdown → DOCX)
│   ├── utils/md2html.py            # manuscript build helper (Markdown → HTML)
│   ├── verify_submission.py        # QC method 1 – structure / numbers / text
│   ├── crosscheck_submission.py    # QC method 2 – independent cross-check (shares no code with 1)
│   └── logiccheck_submission.py    # QC method 3 – cross-references / narrative consistency
├── results/                        # every numerical output of the paper
├── figures/                        # Figures 1–7 (PNG; TIFFs are generated but not tracked)
├── supplementary/                  # parameter ledger (Table S1), calibration table (S2) and note (S1)
├── manuscript/                     # manuscript source (Markdown) + HTML preview
├── reproduce.sh                    # re-runs the whole pipeline
├── requirements.txt
├── CITATION.cff
└── LICENSE
```

## 4. Quick start

```bash
git clone https://github.com/kongtonglangke/esr-renal-microcirculation-model.git
cd esr-renal-microcirculation-model

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

./reproduce.sh                     # ~1 minute; rewrites results/ and figures/
```

Or run the stages individually:

```bash
python code/esr_model_v2.py            # Layers 2–3   -> results/v2_*
python code/esr_model_v3.py            # Layer 1      -> results/v3_*
python code/esr_model_v4_flowcurve.py  # Layer 4      -> results/v4_*
python code/esr_model_v5_calibration.py# Layer 4      -> results/v5_*
python code/make_ms_figures.py         # Figures 1–7  -> figures/
```

## 5. Reproducibility

* Every published number is produced by the scripts above; no value was entered by hand.
* Re-running the pipeline reproduces `results/` **bit-for-bit except for the single run
  timestamp** in `results/v2_package_versions.json` (verified with a recursive diff against
  the committed output). `./reproduce.sh` normalises text output to LF line endings, so a
  re-run leaves a clean `git status` apart from that one timestamp.
* The pipeline is deterministic: no random seeds, no stochastic sampling.
* `results/verification_3x3_log.txt` is the log of the multi-method internal check that was
  run three consecutive times before submission (three mutually independent checkers:
  structure/numbers/text, an independent cross-check that shares no code with the first,
  and a cross-reference/narrative consistency check).
* The QC scripts are shipped for transparency. They validate the *submission package*
  (cover letter, reviewer suggestions, typeset files), which is not distributed here, so in
  this repository they exit immediately with a notice; all numerical results they verify are
  present under `results/`.

## 6. Inputs and parameters

All model parameters, with their source and their epistemic status (measured anchor vs.
assumption), are tabulated in the manuscript's Supplementary Table S1 (parameter ledger).
Those that are literature-anchored carry a DOI and/or a PubMed identifier. Two modelling
choices are stated explicitly rather than hidden:

* the cell-free-layer scale δ₀ = 0.16 *D*, chosen so that the absolute layer thickness falls
  inside the measured range 0.8–3.1 µm for the vessel diameters used;
* the shear exponent *s*, left free and scanned, because the literature does not settle its
  sign.

## 7. Citation

```bibtex
@software{wang_esr_renal_model_2026,
  author  = {Wang, Yan},
  title   = {ESR-renal-microcirculation-model: a reduced-order haemodynamic model of
             ESR-driven wall-shear-stress variability in the renal microcirculation},
  year    = {2026},
  version = {0.8},
  doi     = {10.6084/m9.figshare.34333371},
  url     = {https://github.com/kongtonglangke/esr-renal-microcirculation-model}
}
```

The archived snapshot is citable at **https://doi.org/10.6084/m9.figshare.34333371**.
Please also cite the manuscript (see `CITATION.cff`).

## 8. Licence

* **Code** (`code/`): MIT — see `LICENSE`.
* **Manuscript text and figures** (`manuscript/`, `figures/`): CC BY 4.0.

## 9. Versioning

The repository content corresponds to manuscript version **v0.8**.

The snapshot is archived and citable independently of later edits:
**https://doi.org/10.6084/m9.figshare.34333371** (figshare, 11 October 2026).
The same content is marked by a release tag in this repository:

```bash
git tag -a v0.8 -m "Manuscript v0.8"
git push origin v0.8
```

If the content changes substantively, archive a new version at figshare and update both the
DOI badge at the top of this file and the `doi` field in `CITATION.cff`.

## 10. Use of generative AI

Consistent with the manuscript's declaration: generative AI (DeepSeek) was used to assist
with code development, manuscript drafting and language polishing. All scientific
decisions, parameter choices, interpretation of results and the final content are the
author's own, and every quantitative result in the paper was recomputed and independently
cross-checked by the scripts in `code/`.

## 11. Contact

**Yan Wang** — Department of Nephrology, Affiliated Hospital of Gansu Medical College,
Pingliang, Gansu, China.
Issues and questions are welcome via the GitHub issue tracker.
