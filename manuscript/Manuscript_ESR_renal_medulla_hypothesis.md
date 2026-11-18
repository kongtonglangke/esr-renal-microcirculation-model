# One unresolved constitutive sign decides which renal microvessel an elevated erythrocyte sedimentation rate most loads: a reduced-order haemodynamic model

**Article type:** Original Research Article (computational / theoretical modelling)

**Author:** Yan Wang (ORCID 0000-0002-3474-7984) — Department of Nephrology, Affiliated Hospital of Gansu Medical College, Pingliang, Gansu, China

**Correspondence:** Yan Wang, Department of Nephrology, Affiliated Hospital of Gansu Medical College, Pingliang, Gansu, China

---

## Abstract

**Background.** An elevated erythrocyte sedimentation rate (ESR) is common in chronic kidney disease and predicts adverse renal outcome, yet is read as non-specific inflammation. **Objective.** To test whether the rheology that an elevated ESR indexes mechanically loads the renal microcirculation, and where. **Methods.** We built a four-layer reduced-order model mapping ESR through red-cell aggregate size to a shear-dependent viscosity (Quemada law) and thence to wall shear stress (WSS) and its variability over 10–150 mm h⁻¹, anchored to published measurements and bounded by close packing. **Results.** The intuitive mechanism failed: aggregation affects viscosity only at low shear, the mean WSS is viscosity-independent at fixed pressure gradient, and aggregation thickens rather than thins the cell-free layer. Only WSS temporal variability rose monotonically with ESR, in every vessel and for every value of the one parameter the literature leaves unsettled—the sign of the cell-free-layer/shear relation. **Conclusions.** That sign decides the ranking: at ESR 100 mm h⁻¹ the excess is 37.0% in the hypoperfused medulla against 27.6% in the glomerular capillary under one sign, and 28.4% against 32.9% under the other. The effect is graded and real, but the anatomical contrast is modest.

**Keywords:** erythrocyte sedimentation rate; haemodynamics; erythrocyte aggregation; cell-free layer; wall shear stress; renal medulla; constitutive uncertainty


---

## 1. Introduction

An elevated erythrocyte sedimentation rate (ESR) is among the most frequently requested laboratory abnormalities in clinical nephrology, yet its mechanistic meaning is usually reduced to a non-specific marker of inflammation.¹ That reduction is incomplete even on its own terms: the ESR is a sedimentation measurement whose value is set by plasma protein composition, red-cell aggregation and haematocrit, not by inflammation alone.² An elevated ESR predicts mortality in the general population,³ and in chronic kidney disease (CKD) the association with adverse renal outcome persists after adjustment for conventional inflammatory markers. This raises a question that is anatomical and physical rather than immunological. Does the rheological state that an elevated ESR indexes act on the kidney as a mechanical load on its microcirculation?

The question arose in this service from clinical observation rather than from the haemodynamic literature. Patients without hypertension or diabetes were repeatedly encountered in whom a markedly elevated ESR was the first and most striking laboratory abnormality and in whom renal injury was already present but attributable to no primary glomerular disease; patients with primary glomerular disease in the same service showed only mild ESR elevation. A retrospective case–control study of 80 patients—40 with primary and 40 with secondary renal disease—confirmed the separation: ESR was 42 (16–94) mm h⁻¹ in the secondary group against 16 (10–27) mm h⁻¹ in the primary group (P < 0.001), with an area under the receiver operating characteristic (ROC) curve of 0.747 and a threshold of 69.8–82.0 mm h⁻¹ at 95% specificity.⁴ The inference drawn at the bedside was mechanistic rather than statistical: if the plasma-protein state that raises the ESR also raises whole-blood viscosity at the shear rates prevailing in the renal microcirculation, then the sedimenting abnormality is not a passive marker but a load. The rheological half of that inference already had support in nephrotic syndrome, where whole-blood viscosity is elevated at low shear rates in proportion to fibrinogen,⁵ consistent with the molecular picture in which fibrinogen molecules bridge adjacent red cells and drive aggregation.⁶ What did not exist was any decomposition of the proposed mechanism into its physical links, any quantification of each link, or any test of whether the intuitive chain survives contact with established haemodynamics.

The intuitive chain is easy to state. An elevated ESR is taken to reflect reduced red blood cell (RBC) suspension stability and increased RBC aggregation;⁷,⁸ increased aggregation is thought to make RBCs marginate towards the vessel wall, narrow the lubrication gap between RBCs and the endothelium, and impose an abnormal mechanical load—either through a raised mean wall shear stress (WSS) or through repeated cell–wall contact—that ultimately injures the glomerular or peritubular endothelium. Each arrow in this chain is physically plausible in isolation. Whether the chain as a whole produces a measurable effect at physiological parameter values is a separate question, and it is precisely the question that has never been asked quantitatively.

We therefore set out to build the smallest model that contains the whole chain and can be evaluated with literature-anchored parameters, and to interrogate it for internal consistency, sensitivity, and falsifiable consequences. We treated the study as a numerical experiment with a pre-specified null: if the intuitive chain is correct, the model should show that raising ESR (i) raises blood viscosity appreciably at renal microvascular shear rates, (ii) raises the mean WSS, (iii) reduces the RBC–endothelium gap, and (iv) produces flow heterogeneity or stasis. Because clinical concern attaches to sustained, markedly elevated values rather than to small deviations from the reference range, the model was evaluated not at a single pair of values but across the whole interval from a normal ESR of 10 mm h⁻¹ to 150 mm h⁻¹—the upper value chosen because clinical series contain patients above 120 mm h⁻¹, and flagged where it extrapolates beyond the calibrated range—and the graded dose–response across that interval is reported throughout.

None of the four predicted consequences survived. The model produced instead a different, narrower, and—we argue—more defensible hypothesis: that the rheological state indexed by an elevated ESR acts through the temporal variability of WSS in the low-shear microcirculation, and not through the mean stress or through cell–wall apposition. The central result of the paper, however, is not the magnitude of that effect but the discovery that its anatomical target is not fixed by the model at all. The effect is present in every vessel and at every value of the one constitutive quantity the literature leaves unresolved—the sign of the cell-free-layer/shear-rate relation—yet which vessel is worst is decided entirely by that sign, the ranking reversing between the hypoperfused medulla and the glomerular capillary (Section 3.7). We therefore treat the sign not as a nuisance parameter to be assumed away but as the quantity that one feasible measurement must settle, and we state that measurement as a formal prediction (P5). The remainder of this paper develops the hypothesis, reports the quantitative basis for it, and states the predictions by which it should stand or fall.

---

## 2. Methods

### 2.1 Model overview

We modelled a single representative microvessel as a rigid circular tube carrying a non-Newtonian suspension of RBCs in plasma, and we asked how a change in RBC aggregation propagates from a clinical ESR value to a set of mechanical descriptors at the vessel wall. The model has four layers, each of which was deliberately kept as simple as the literature allows, so that the overall behaviour can be attributed to identifiable constitutive assumptions rather than to numerical detail (Figure 1).

The first layer maps a clinical ESR value to an effective RBC aggregate radius through a Stokes sedimentation relation. The second maps aggregate radius to a shear-dependent blood viscosity through the Quemada constitutive law. The third solves the steady, fully developed flow of that viscosity in a tube, subject to a prescribed organ-level pressure gradient. The fourth constructs the two-layer core/cell-free-layer geometry implied by the flow and evaluates the wall shear stress and its temporal variability. The model is not a computational fluid dynamics (CFD) simulation; it is a reduced-order model designed to be exact for a circular tube and transparent in its assumptions. Escalating to two-phase CFD was judged unnecessary because the results that drive the paper—the shear gating of the aggregation effect, the viscosity-independence of the mean wall shear stress, and the thickening of the layer under axial accumulation—follow from the constitutive law and from mass conservation rather than from the details of the velocity field. A CFD solution would refine the velocity profile and the near-wall cell distribution, but it cannot alter the Quemada high-shear asymptote or the identity $\tau_w$ = D(ΔP/L)/4; the code and parameters are provided so that the judgement can be checked independently.

### 2.2 Layer 1: from ESR to effective aggregate radius, derived from measured data

The ESR is a sedimentation measurement, so the natural physical variable to which it maps is an aggregate size. Rather than assuming that mapping, we derived it from two established relations. The first is Stokes' law for the sedimentation velocity of a single aggregate of radius $R_{\mathrm{agg}}$ in plasma of viscosity $\mu_p$, with $\rho_e$ and $\rho_p$ the erythrocyte and plasma densities:

$$V_s=\frac{2\,(\rho_e-\rho_p)\,g\,R_{\mathrm{agg}}^{2}}{9\,\mu_p}\tag{1}$$

The second is the empirical relation between the Westergren ESR and the true sedimentation velocity, which Higuchi and Watanabe measured to be almost linear (r = 0.990, slope 0.778, in a 32-sample series).⁹ The same group later confirmed the ESR–aggregation route in 203 clinical samples and refined it for mean corpuscular volume.¹⁰ Combined with the hindered-settling correction $V_e=V_s\,(1-\mathrm{Ht})^{n}$ with $n=4.65$ (Richardson–Zaki),¹¹ this fixes the aggregate size parameter α, defined by

$$R_{\mathrm{agg}}=R_{\mathrm{ef}}\,(1+\alpha)\tag{2}$$

from the measured constants of the same study: $\rho_e$ = 1100 kg m⁻³, $\rho_p$ = 1025 kg m⁻³, $R_{\mathrm{ef}}$ = 3.084 × 10⁻⁶ m, and $\mu_p$ = 1.64 × 10⁻³ Pa s. Writing c for the no-aggregation sedimentation velocity (the value of Equation 1 at α = 0), the chain reduces to

$$c=\frac{2\,(\rho_e-\rho_p)\,g\,R_{\mathrm{ef}}^{2}}{9\,\mu_p},\qquad(1+\alpha)^{2}=\frac{V_s}{c}\tag{3}$$

Substituting the measured constants gives c = 0.948 µm s⁻¹. The hindered-settling factor in that step was evaluated at the haematocrit of the source study (0.40), whereas the vessel calculations below use 0.42; the resulting small extrapolation is noted in Section 4.6. Because the Westergren relation is near-linear, this chain implies (1 + α) ∝ √ESR essentially exactly, so the √ESR scaling used in earlier versions of this model is recovered rather than replaced. We state clearly that this is an algebraic consequence of Equations (1) and (3) rather than an independent validation; its empirical content lies entirely in the measured Westergren linearity, which is a falsifiable statement about real blood. What the derivation provides is (i) a measured rather than assumed route from ESR to aggregate size, and (ii) absolute values of α, which were previously undefined. We also retained the haematocrit correction of the aggregation index (AI) measured in the same study, HAI = AI − 0.284 (Ht − 0.40),⁹ which turns out to carry an important clinical implication (Section 3.9).

### 2.3 Layer 2: from aggregation to blood viscosity

The shear-thinning and aggregation dependence of whole-blood viscosity was described by the Quemada equation,

$$\eta=\eta_p\left(1-\frac{kH}{2}\right)^{-2}\tag{4a}$$

$$k=\frac{k_0+k_\infty\sqrt{\dot\gamma/\dot\gamma_c}}{1+\sqrt{\dot\gamma/\dot\gamma_c}}\tag{4b}$$

where $\eta_p$ is the plasma viscosity, H is the tube haematocrit, γ̇ is the shear rate, and k₀, k∞ and $\dot\gamma_c$ are the aggregation, deformability and critical shear-rate parameters, respectively.¹² The parameters were taken from a haematocrit-dependent parameterisation standard in blood-flow modelling,¹³ and, where available, from directly measured clinical values. Aggregation affects viscosity through k₀, which increases as red cells aggregate; deformability affects it through k∞; the crossover between the two regimes is set by $\dot\gamma_c$. The functional form of Equation (4) is what makes the model's central result possible: because the aggregation contribution enters through k(γ̇), and because k(γ̇) → k∞ as γ̇ grows, the effect of aggregation is intrinsically confined to low shear rates.

### 2.4 Layer 3: single-vessel haemodynamics

For steady, fully developed flow in a tube of diameter D subject to a pressure gradient ΔP/L, the wall shear stress is

$$\tau_w=\frac{D\,(\Delta P/L)}{4}\tag{5}$$

and, for a locally Newtonian fluid of apparent viscosity η, the mean velocity and wall shear rate are

$$V=\frac{D^{2}(\Delta P/L)}{32\,\eta},\qquad\dot\gamma_w=\frac{8V}{D}\tag{6}$$

For a non-Newtonian fluid, Equations (5) and (6) were solved self-consistently: at each pressure gradient, the shear rate implied by the velocity was fed back into Equation (4) until convergence. Equation (5) is exact for any axisymmetric tube flow with a uniform wall shear stress and is independent of the fluid's constitutive law. This is a substantive point rather than a technicality: under a fixed organ pressure gradient, the mean WSS cannot be altered by changing blood viscosity, because it is set entirely by the vessel geometry and the driving pressure. Any hypothesis that attributes renal injury to an elevated mean WSS driven by haemoconcentration or aggregation is therefore inconsistent with elementary tube haemodynamics, unless the pressure gradient itself changes.

Two boundary conditions were considered. Under a fixed pressure gradient, the flow rate is allowed to fall as viscosity rises. Under a fixed flow rate (representing perfect renal autoregulation), the velocity is held constant and the pressure gradient is allowed to rise. Both were evaluated, because the physiologically relevant regime is intermediate and the two bracket the range of possible WSS responses. All shear rates quoted in this paper are pseudo shear rates, γ̇ = 8V/D, i.e. the wall shear rate of a Newtonian fluid with the same mean velocity. This is the definition used in the shear-gating measurement that anchors Equation (9),¹⁴ so the model and that measurement are commensurable; for a shear-thinning suspension the true wall shear rate exceeds 8V/D, and the absolute shear rate at which the aggregation effect becomes negligible would shift in proportion, but neither the gating nor the vessel ranking depends on the distinction.

### 2.5 Layer 4: cell-free layer geometry and WSS temporal variability

Flow of RBCs in a microvessel produces a cell-free layer (CFL) adjacent to the wall, with a core of higher haematocrit and near-wall plasma. The two-layer core/plasma description remains the standard reduced representation of this flow, and its competing variants have recently been compared systematically.¹⁵ We represented the layer with the standard two-layer construction: given a tube haematocrit H and a core haematocrit $H_{\mathrm{core}}$, mass conservation of RBCs fixes the CFL thickness δ through

$$H\,\pi R^{2}=H_{\mathrm{core}}\,\pi\,(R-\delta)^{2}\tag{7}$$



The gap available for a flowing RBC to approach the endothelium was then taken as the distance from the outermost core surface to the wall. We emphasise that Equation (7) carries an important and counter-intuitive consequence: because aggregation raises the core haematocrit by drawing cells axially, and because mass conservation is enforced, an increase in aggregation increases δ. That is, aggregation moves the RBC-rich core away from the wall. This prediction is not an artefact of the model; it is the expected behaviour of any two-layer description of a marginating suspension, and it agrees with direct microvascular measurements showing that the CFL thickens when aggregation is increased.⁸,¹⁶,¹⁷

Two elements of this construction need to be stated explicitly, because the spatial result of the model turns on them. The first is the absolute width of the layer. We wrote

$$\delta=\delta_0(D)\,f_A(A)\,f_\gamma(\dot\gamma),\qquad\delta_0=0.10\,D,\qquad f_\gamma=\left(\frac{\dot\gamma}{100\ \mathrm{s^{-1}}}\right)^{s}\tag{7a}$$

with the whole expression subject to the packing bound derived immediately below (Equation (7c). The prefactor and the aggregation slope were chosen jointly with that bound, not for their absolute values alone. A prefactor of 0.16 D, used in an earlier version of this work, places the hypoperfused vasa recta at a core haematocrit of 1.24 at the reference ESR and is therefore inadmissible; the same is true of any prefactor above about 0.12 D once the aggregation factor is applied. At 0.10 D the predicted widths at the reference ESR are 0.61, 0.85 and 1.49 µm in the 8, 10 and 15 µm vessels, all inside the measured band of 0.8–3.1 µm once the vessel diameter is allowed for,¹⁸ rising by about 1.23-fold at ESR 100 mm h⁻¹. No vessel reaches the packing bound below ESR 150 mm h⁻¹; at the top of the grid the hypoperfused vasa recta reaches it exactly ($H_{\mathrm{core}}$ = 0.950) and can thicken no further (Supplementary Data S1). The factor $f_A$ is a monotone function of the aggregation amplification A with a slope of 0.06 per unit A, chosen to reproduce the measured thickening of the layer with aggregation;¹⁶,¹⁷ that slope is a modelling choice and its influence on the ranking is quantified in Section 3.7. The second is $f_\gamma$, the shear-rate dependence of the layer, and here the literature does not give a single sign. Suzuki and colleagues, measuring in both microvessels and glass capillaries of exactly the size range used here, found the layer to thicken as flow velocity increased (*s* > 0);¹⁶ in vivo arteriolar measurements found the layer to be enhanced by flow reduction combined with aggregation (*s* < 0);¹⁹ a particle simulation resolves the two observations as non-monotonic, the layer thinning as shear rises at low shear rates and thickening again at high shear rates;²⁰ and the most recent in vitro study reports one sign in plasma and the other in a non-aggregating medium, and states that the dependence remains debated.²¹ Two further studies add quantitative detail without settling the sign: the layer width has been expressed as a function of rheological parameters at microvascular bifurcations,²² and cell-resolved CFD has been validated against measured layer formation in a contracting microchannel.²³ We therefore treat *s* as a free parameter rather than a fixed constant. The whole main analysis uses *s* = −0.12, the aggregation-dominated value; Section 3.7 reports the complete vessel ranking as a function of *s*, and we are explicit in Section 4.6 about which conclusions survive a change of sign and which do not.

Equation (7) fixes the core haematocrit once the layer width is set,

$$H_{\mathrm{core}}=\frac{H}{\left(1-2\delta/D\right)^{2}}\tag{7b}$$

and therefore also bounds that width from above. A core haematocrit cannot exceed the haematocrit of close-packed red cells, $H_{\max}$, so the construction is admissible only where $H_{\mathrm{core}}$ ≤ $H_{\max}$, that is where

$$\delta\leq\frac{D}{2}\left[1-\sqrt{\frac{H}{H_{\max}}}\right]\tag{7c}$$

With H = 0.42 and $H_{\max}$ = 0.95 this limits the layer to 2δ/D ≤ 0.335, or 2.5 µm in the 15 µm vasa recta. The bound is a physical admissibility condition rather than a numerical safeguard: a parameterisation that violates it returns a core haematocrit above 1, so the diagnostic quantity is the $H_{\mathrm{core}}$ returned by Equation (7b), which we report for every vessel at every simulated ESR (Supplementary Data S1) so that the condition of Equation (7c) can be checked directly.

The final model element concerns the temporal behaviour of the CFL and the wall stress. Microvascular CFLs are not steady; they fluctuate in width on sub-second timescales, and these fluctuations modulate the instantaneous wall shear stress. Because the flow is not steady, the stress experienced by the endothelium has a mean and a fluctuating component, and it is the fluctuating component that can differ between rheological states even when the mean is unchanged. To keep the model reproducible rather than verbal, the two variability steps are written explicitly. Because the mean wall shear stress is fixed by the pressure gradient and the vessel diameter (Equation (5), a fluctuating layer cannot modulate it through the mean. What the layer does modulate is the shear rate within the near-wall plasma layer, $\dot\gamma_{\mathrm{near}}$ = 2 $V_{\mathrm{core}}$/(D/2 − $\delta_{\mathrm{inst}}$), where $V_{\mathrm{core}}$ is the core velocity. Differentiating at fixed core velocity and expressing the result as a coefficient of variation,

$$CV_\tau=CV_\delta\,\frac{2\delta}{D-2\delta}\tag{8}$$

so a fractional fluctuation of the layer becomes a fractional fluctuation of the near-wall shear with the geometric sensitivity 2δ/(D − 2δ). The numerator is 2δ and not D because the absolute sensitivity of the near-wall gap to a fluctuation in δ scales with δ itself and vanishes as δ → 0; the form D/(D − 2δ) used in an earlier version over-stated the transfer by D/2δ, which is 3.8-fold in the hypoperfused vasa recta and 6.6-fold in the glomerular capillary. Equation (8) is first-order in δ and is used as such throughout. The cell-free-layer variability was itself written as a saturating, shear-gated function of the aggregation amplification A, defined as the ratio of the aggregation-dependent zero-shear parameter to its value at the reference ESR of 10 mm h⁻¹:

$$CV_\delta(\dot\gamma,A)=CV_0+\Delta CV\,(A-1)\left[1+\left(\frac{\dot\gamma}{\dot\gamma_s}\right)^{n}\right]^{-1}\tag{9}$$

with CV₀ = 0.30 (the mid-range of the 0.2–0.6 baseline observed in vivo), ΔCV = 0.22, $\dot\gamma_s$ = 20 s⁻¹ and n = 1.5. Equations (8) and (9) are the complete specification of this layer: given the shear rate from Layer 3 and the amplification from Layer 2, the wall-stress coefficient of variation follows with no further input and no per-vessel tuning. The four parameters of Equation (9) are the only phenomenologically assigned quantities in the model, and they were not fitted: they were fixed so that the predicted gating reproduces the experimental observation that RBC aggregation raises cell-free-layer variability at low shear rates (9.2 ± 0.6 s⁻¹) but not at moderate or high shear rates (>45 s⁻¹).¹⁴,²⁴ Of the four, only the gating threshold is anchored to a measured value; the two magnitude parameters are assumptions. Experimental work additionally shows that CFL variation directly alters arteriolar wall shear stress.¹⁴,¹⁸ The absolute magnitude of Equation (9), as distinct from its shear gating, is the largest uncertainty within this layer (Section 4.6).

### 2.6 Parameter anchoring and calibration

Every parameter was assigned to one of three evidence tiers and recorded in a parameter ledger (Supplementary Table S1): measured (taken directly from a published measurement), modelling choice (a standard formulation with a conventionally accepted value), or assumption (a value with no direct measurement, flagged as the largest source of uncertainty).

The viscosity kernel was validated before use. We took a published parameter set measured in clinical blood samples and compared the model's predicted relative viscosity curve against the measured curve from the same study.²⁵

Because the mapping from ESR to k₀ is not directly measurable, we did not assume it. Instead we performed an inverse calibration: we took an independently published clinical whole-blood viscosity increment (low-shear +41%, high-shear +25% in nephrotic syndrome⁵) and asked what combination of plasma-viscosity increase and k₀ increase would reproduce it. Two observations and two unknowns make this a determinate inverse problem, and we solved it numerically. We then checked that the recovered k₀ fell inside the range measured directly in clinical samples.²⁵

*ESR range and anchoring of the aggregation step.* The model was evaluated on a grid of ESR values from 10 to 150 mm h⁻¹. The mapping from ESR to the k₀ amplification is a shape function anchored at two values of ESR: unity at the reference ESR of 10 mm h⁻¹, and the calibrated amplification (1.033×) at 100 mm h⁻¹. The anchor is placed at 100 rather than at the top of the simulated grid because it is the value at which the calibration target is attained; results between 100 and 150 mm h⁻¹ involve an amplification beyond the anchor and an implied k₀ above 4.36, the highest value measured in clinical samples,²⁵ and are reported as an extrapolation. The extrapolation is included because markedly elevated ESR values are common in the population from which the clinical question arose—7 of 80 patients in the case–control series⁴ had an ESR above 120 mm h⁻¹—and a model that stopped at 100 would not describe them. The upper anchor is a modelling choice, and we made it deliberately: placing it lower—at 60 mm h⁻¹, as an earlier version of this work did—forces the modelled k₀ above 4.36, the highest value measured in clinical samples,²⁵ for every ESR above 60, and therefore extrapolates the constitutive law beyond measured physiology. Anchoring it at the top of the range keeps every modelled k₀ inside the measured interval [3.05, 4.36]. The choice has little effect on the quantity that carries the paper's conclusion, because that conclusion rests on cell-free-layer geometry rather than on the magnitude of the viscosity; we quantify the insensitivity in Section 4.6.

### 2.7 Sensitivity analysis

To quantify how much of the result depends on the particular parameter set, the entire calculation was repeated with four published Quemada parameterisations spanning the observed clinical range of k₀. Results were compared as viscosity ratios (elevated- versus normal-aggregation) across the shear-rate range 0.3–1000 s⁻¹.

### 2.8 Software and reproducibility

The model was implemented in Python 3.13 (NumPy, SciPy, pandas, Matplotlib). The model runs in under three seconds on a laptop and requires no specialist CFD software. All code, parameter tables, and numerical output are provided as supplementary material to support exact reproduction.

---

## 3. Results

### 3.1 Layer 1 is a derivation, not an assumption, and it yields absolute aggregate sizes

Replacing the assumed Stokes scaling with the measured chain of Section 2.2 gives the aggregate-size parameter α as a function of ESR (Table 1, Figure 2). At the constants measured by Higuchi and Watanabe,⁹ α rises from 1.21 at ESR 2 mm h⁻¹ to 3.95 at ESR 10 mm h⁻¹, 11.13 at ESR 60 mm h⁻¹ and 14.66 at ESR 100 mm h⁻¹, corresponding to effective aggregate radii $R_{\mathrm{agg}}$ = $R_{\mathrm{ef}}$(1+α) of 6.8, 15.3, 37.4 and 48.3 µm respectively. These are the first absolute aggregate-size values the model has produced; earlier versions carried an arbitrary reference radius and were therefore only able to make statements about relative change.

A power-law fit to the derived relation returns an exponent of exactly 0.5000, i.e. (1 + α) ∝ $ESR^{0.5}$, identical to the √ESR scaling that the earlier version assumed. We emphasise that this agreement is an algebraic identity, not an empirical discovery: the chain is proportional at every step, so the exponent is 0.5 by construction. The scientific content of the replacement is that the scaling no longer requires a free assumption—it follows from Stokes' law and from a measured, falsifiable linearity in real blood (r = 0.990). The maximum deviation from a pure square-root law across ESR 2–100 mm h⁻¹ is correspondingly zero by identity, and we do not present it as evidence.

**Table 1.** Layer-1 mapping derived from measured constants.⁹

| ESR (mm h⁻¹) | $V_e$ (µm s⁻¹) | $V_s$ (µm s⁻¹) | HAI | α (measured chain) | $R_{\mathrm{agg}}$ (µm) |
|---:|---:|---:|---:|---:|---:|
| 2 | 0.432 | 4.65 | 0.517 | 1.214 | 6.83 |
| 5 | 1.081 | 11.62 | 0.545 | 2.501 | 10.80 |
| 10 | 2.161 | 23.24 | 0.569 | 3.951 | 15.27 |
| 20 | 4.322 | 46.48 | 0.596 | 6.002 | 21.59 |
| 30 | 6.483 | 69.73 | 0.615 | 7.575 | 26.45 |
| 40 | 8.644 | 92.97 | 0.629 | 8.902 | 30.54 |
| 60 | 12.967 | 139.45 | 0.651 | 11.127 | 37.40 |
| 80 | 17.289 | 185.94 | 0.668 | 13.003 | 43.19 |
| 100 | 21.611 | 232.42 | 0.682 | 14.656 | 48.28 |

The HAI values implied by the mapping are all above the minimum physiological value b = 0.426 reported in the same study, which confirms that the model is being evaluated inside the range in which the underlying regression was fitted, rather than extrapolated beyond it.

### 3.2 The viscosity kernel reproduces the published curve of the same study

Substituting a published clinical parameter set into Equation (4) and comparing the predicted relative viscosity against the measured curve from the same study gave agreement within ±7% across the shear-rate range 0.1–100 s⁻¹ at a haematocrit of 0.42 (Table 2): predicted/measured ratios were 0.98, 1.05, 1.07 and 1.03 at 0.1, 1, 10 and 100 s⁻¹ respectively (Figure 3).

This is a consistency check, not an independent validation, and the distinction matters for how much the comparison can be asked to carry. The parameter set and the reference curve come from the same publication, so agreement demonstrates that the implementation returns the source's own curve when fed the source's own parameters; it does not demonstrate transportability to blood from another laboratory. Agreement was in addition obtained at H = 0.42, whereas the mean haematocrit reported by that study was 0.44. At the reported value the fit is systematically worse (ratios 1.40, 1.32, 1.22, 1.11), which shows that the reported mean carries non-negligible uncertainty and justifies adopting H = 0.42, but it also means that one free choice enters before the agreement is obtained. A genuinely independent check would require a viscosity–shear curve measured in a different laboratory at a haematocrit stated to two decimal places and spanning the renal microvascular shear range; we did not find one, and we therefore do not claim external validation (Section 4.6). What the comparison establishes is narrower and still useful: the component on which every downstream result depends behaves as its source law requires.

**Table 2.** Consistency check of the viscosity kernel against the curve of the source study (H = 0.42).

| Shear rate (s⁻¹) | Model relative viscosity | Measured relative viscosity | Ratio |
|---:|---:|---:|---:|
| 0.1 | 19.55 | 20.0 | 0.98 |
| 1 | 10.52 | 10.0 | 1.05 |
| 10 | 5.25 | 4.9 | 1.07 |
| 100 | 3.32 | 3.23 | 1.03 |

### 3.3 The aggregation effect is strongly shear-rate gated

Increasing ESR from 10 to 100 mm h⁻¹ produced a viscosity increase that fell steeply with shear rate (Table 3). At 0.1 s⁻¹ the ratio was 1.33; at 2.7 s⁻¹, 1.10; at 14 s⁻¹, 1.05; and at 2000 s⁻¹, 1.004. The effect fell below +10% above a shear rate of approximately 3 s⁻¹, and below +2% above approximately 70 s⁻¹ (Figure 4). The same gating applies to the clinically salient intermediate values: the ratio at 2.7 s⁻¹ was 1.06 at ESR 60 and 1.08 at ESR 80.

**Table 3.** Anchored whole-blood viscosity (mPa·s) at H = 0.42 as a function of ESR and shear rate.

| Shear rate (s⁻¹) | ESR 10 | ESR 40 | ESR 60 | ESR 80 | ESR 100 | Ratio (100/10) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 37.95 | 43.11 | 45.78 | 48.23 | 50.55 | 1.332 |
| 0.52 | 20.77 | 22.48 | 23.31 | 24.06 | 24.74 | 1.191 |
| 2.71 | 11.00 | 11.48 | 11.70 | 11.89 | 12.07 | 1.097 |
| 14.13 | 6.60 | 6.74 | 6.80 | 6.86 | 6.90 | 1.046 |
| 73.56 | 4.78 | 4.82 | 4.84 | 4.86 | 4.88 | 1.021 |
| 383.1 | 4.02 | 4.03 | 4.04 | 4.05 | 4.05 | 1.009 |
| 1995 | 3.70 | 3.70 | 3.71 | 3.71 | 3.71 | 1.004 |

The gating was identical in direction across all four published parameter sets tested (Table 4). At 0.3 s⁻¹ the viscosity ratio varied between 1.207 and 1.234; at 1000 s⁻¹ it varied between 1.006 and 1.011. The absolute magnitude depends on the calibration target, but the qualitative conclusion—that aggregation matters at low shear and is negligible at high shear—is robust to the choice of parameter set.

**Table 4.** Sensitivity of the viscosity ratio (elevated/normal aggregation) to the Quemada parameter set.

| Parameter set | 0.3 s⁻¹ | 1 s⁻¹ | 3 s⁻¹ | 10 s⁻¹ | 100 s⁻¹ | 1000 s⁻¹ |
|---|---:|---:|---:|---:|---:|---:|
| Standard parameterisation, H = 0.42 | 1.234 | 1.148 | 1.093 | 1.054 | 1.018 | 1.006 |
| Measured clinical set | 1.219 | 1.152 | 1.102 | 1.062 | 1.022 | 1.007 |
| Clinical lower bound (k₀ = 3.05) | 1.207 | 1.163 | 1.121 | 1.081 | 1.031 | 1.011 |
| Clinical upper bound (k₀ = 4.36) | 1.223 | 1.151 | 1.099 | 1.059 | 1.020 | 1.007 |

### 3.4 The mean wall shear stress does not respond to ESR

Across the four representative vessels—glomerular capillary, peritubular capillary, medullary vasa recta, and a hypoperfused vas rectum—the mean wall shear stress was identical at all ESR values from 10 to 150 mm h⁻¹ (ratio 1.000× in every case; Table 5). This is the exact analytic consequence of Equation (5): under a fixed organ pressure gradient, $\tau_w$ depends only on vessel diameter and driving pressure. Absolute values were 3.86 Pa in the glomerular capillary, 1.63 Pa in the peritubular capillary, 0.49 Pa in the vasa recta, and 0.077 Pa in the hypoperfused vas rectum (Figure 5). Because these values were unchanged while the apparent viscosity varied between 3.80 and 7.79 mPa·s, the model demonstrates that there is no pathway from blood viscosity to mean WSS at fixed driving pressure. In the fixed-flow-rate scenario, which represents perfect autoregulation, the mean WSS rose by at most 5.2% (in the hypoperfused vasa recta) at ESR 100 mm h⁻¹—several-fold less than the accompanying change in its variability (Section 3.6).

**Table 5.** Vessel-level states at fixed organ pressure gradient. Every column after the first is a dimensionless ratio of the value at ESR 100 mm h⁻¹ to the value at ESR 10 mm h⁻¹ (X₁₀₀/X₁₀); the wall shear rate is the baseline value at ESR = 10 mm h⁻¹.

| Vessel | Baseline wall shear rate at ESR 10 (s⁻¹) | η₁₀₀/η₁₀ | τ₁₀₀/τ₁₀ | V₁₀₀/V₁₀ | δ₁₀₀/δ₁₀ | **CV₁₀₀/CV₁₀** |
|---|---:|---:|---:|---:|---:|---:|
| Glomerular capillary | 1016 | 1.006 | 1.000 | 0.994 | 1.225 | **1.276** |
| Peritubular capillary | 407 | 1.010 | 1.000 | 0.990 | 1.225 | **1.284** |
| Vasa recta (medulla) | 109 | 1.020 | 1.000 | 0.981 | 1.227 | **1.302** |
| Vasa recta, hypoperfused | 10.9 | 1.074 | 1.000 | 0.931 | 1.234 | **1.370** |

### 3.5 Aggregation thickens, rather than thins, the cell-free layer

In every vessel the CFL thickened monotonically as ESR rose, by 1.22–1.23-fold from ESR 10 to ESR 100 (Table 5). In absolute terms the glomerular CFL widened from 0.61 to 0.74 µm, the peritubular CFL from 0.85 to 1.04 µm, the normally perfused medullary CFL from 1.49 to 1.82 µm, and the hypoperfused medullary CFL from 1.96 to 2.42 µm. The reference measured band is 0.8–3.1 µm for vessels of 10–50 µm; the modelled layer lies inside it in the three larger vessels, sits below its lower edge in the 8 µm glomerular capillary—where reported layer widths are in fact smaller than in arterioles—and reaches the packing bound of Equation (7c) only in the hypoperfused vasa recta and only at the top of the simulated grid—$H_{\mathrm{core}}$ = 0.950 at ESR 150 mm h⁻¹, where the layer can thicken no further (Supplementary Data S1). The direction of this change is the opposite of that assumed by the intuitive mechanism. Because the model enforces mass conservation of RBCs in the core (Equation (7), axial accumulation of aggregated cells necessarily withdraws cells from the near-wall region; the RBCs therefore move away from, not towards, the endothelium. This is consistent with direct microvascular measurements, in which the CFL thickens when aggregation is increased.¹⁶,¹⁷ The consequence for the original hypothesis is unambiguous: whatever an elevated ESR does to the renal endothelium, it does not do it by pressing RBCs onto the wall.

### 3.6 Temporal WSS variability is the only monotonic response, and it is modestly larger in the hypoperfused medulla

The single quantity that increased monotonically with ESR in every vessel was the temporal coefficient of variation of the wall shear stress (WSS CV). From ESR 10 to 100 mm h⁻¹ the increase was similar in all four vessels, and modest: 1.276× in the glomerular capillary, 1.284× in the peritubular capillary, 1.302× in the normally perfused vasa recta and 1.370× in the hypoperfused one (Table 5). In absolute terms the WSS CV of the hypoperfused medulla rose from 0.106 at ESR 10 mm h⁻¹ to 0.145 at ESR 100 mm h⁻¹, and to 0.155 at ESR 150 mm h⁻¹. The excess response relative to the glomerular capillary was therefore 1.09-fold in the normally perfused medulla and 1.34-fold in the hypoperfused medulla (Figure 6)—a difference in the same direction as the intuitive expectation but an order of magnitude smaller than a segment-specific mechanism would need. Beyond ESR 100 mm h⁻¹ the contrast rises only marginally, to 1.35-fold at 120 mm h⁻¹, and then falls to 1.24-fold at 150 mm h⁻¹, because the hypoperfused layer reaches the packing bound while the cortical layer does not: the medullary excess saturates at 46.1% while the glomerular excess continues to 37.2%. Because the mean WSS is constant (Section 3.4), the increase occurs at a fixed mean stress: the endothelium of the hypoperfused medulla is exposed to the same average force but to a progressively more fluctuating one as ESR rises.

The response is graded rather than thresholded (Table 6). In the hypoperfused medulla the excess rises from 6.5% at ESR 20 mm h⁻¹ to 16.1% at 40, 23.9% at 60, 30.7% at 80, 37.0% at 100 and 46.1% at 150; the cortical vessels follow the same monotone form at four-fifths of that magnitude. The relation is smooth, with no sharp threshold, and grows nearly linearly in ESR above about 40 mm h⁻¹. The burden attributable to aggregation is therefore small at ordinary ESR values and material only at the markedly elevated values that prompt clinical investigation: below 40 mm h⁻¹ it stays under 13% in every vessel, whereas at 80 mm h⁻¹ and above it exceeds 30% in the hypoperfused medulla.

**Table 6.** Excess wall-shear-stress variability relative to the reference ESR of 10 mm h⁻¹, as a function of ESR and vessel.

| Vessel | ESR 20 | ESR 40 | ESR 60 | ESR 80 | ESR 100 | ESR 120 | ESR 150 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Glomerular capillary | +5.1% | +12.5% | +18.2% | +23.2% | +27.6% | +31.6% | +37.2% |
| Peritubular capillary | +5.2% | +12.8% | +18.8% | +23.9% | +28.4% | +32.6% | +38.4% |
| Vasa recta (medulla) | +5.5% | +13.5% | +19.8% | +25.3% | +30.2% | +34.7% | +41.0% |
| Vasa recta, hypoperfused | +6.5% | +16.1% | +23.9% | +30.7% | +37.0% | +42.8% | +46.1% |

The renal medulla receives only about 6% of renal blood flow, operates at a tissue oxygen tension near 8 mmHg, and is perfused by vasa recta of 12–18 µm diameter—vessels that are intrinsically slow-flowing and therefore intrinsically low-shear.²⁶⁻²⁹ The medullary microcirculation is also the segment in which, at low perfusion, RBC aggregation has been identified as a principal driver of injury, and in which pericyte-mediated capillary constriction is now recognised as a route to no-reflow.³⁰ The model places the largest excess in the same segment, and the reason can be stated explicitly rather than fitted. The response is the product of the two factors of Equations (8) and (9), and the geometric factor dominates: the shear gate of Equation (9) supplies 0.6% of the logarithmic increase in the normally perfused vasa recta and 5.6% in the hypoperfused one, against less than 0.05% in the glomerular capillary, so the geometric factor of Equation (8) carries 94.4–99.4% of the increase. That factor is larger in the medulla because the cell-free layer occupies a larger fraction of the lumen there—2δ/*D* is 0.20 in the normally perfused vasa recta and 0.26 in the hypoperfused one at the reference ESR of 10 mm h⁻¹, rising to 0.24 and 0.32 at ESR 100 mm h⁻¹, against 0.15 and 0.19 in the glomerular capillary. Because Equation (8) makes the sensitivity proportional to 2δ/*D* rather than to a stronger power of it, however, a layer that is 1.7 times relatively thicker in the medulla yields an excess only about 1.3 times larger; the amplification saturates as the layer approaches the packing bound.

One qualification applies to the whole of this section and is quantified in Section 3.7. The medullary excess is carried by the geometric factor 2δ/(*D* − 2δ), and that factor is larger in the medulla only because the baseline layer there is modelled as thicker at low shear. Whether the layer really is thicker at low shear is itself unsettled (Section 2.5). The rank order reported above is therefore conditional, and we now state the condition.

### 3.7 The most exposed segment depends on the sign of an unresolved constitutive relation

This section carries what we regard as the central result of the study: that the existence of the effect is model-robust, while its anatomical target is not.

Section 3.6 reports the rank order of the vessels under one choice of the exponent *s* of Equation (7a). Because that choice is not settled by measurement (Section 2.5), the entire calculation was repeated across *s*. The usable window is narrower than the range of exponents the literature can be read to support, and the reason is Equation (7c): at |*s*| above about 0.15 the cell-free layer of at least one vessel reaches the packing bound at some ESR in the grid, can thicken no further, and returns a saturated—and therefore uninformative—fold change. We therefore report *s* from −0.12 to +0.12, over which the packing constraint is respected in every vessel at every simulated ESR, and we note that within this window the ordering is monotone in *s*, so no behaviour is lost by not extending it. Two statements then separate cleanly.

First, the existence of the effect is robust. For every value of *s*, and in each of the four vessels, the wall-stress coefficient of variation rises monotonically with ESR and is higher at 100 than at 10 mm h⁻¹. Changing the sign of *s* alters the magnitude assigned to a given vessel but never removes the effect, because the rise is driven by the aggregation factor $f_A$ of Equation (7a), which is independent of *s*.

Second, the identity of the most exposed segment is determined entirely by *s* (Table 7, Figure 6d). For *s* < 0 the hypoperfused vasa recta is the most affected vessel and the cortical vessels the least, the ratio between the hypoperfused medulla and the glomerular capillary being 1.34 at the default *s* = −0.12. The ranking crosses over at *s* ≈ +0.04, and for *s* > 0 the glomerular capillary becomes the most affected vessel while the hypoperfused medulla becomes the least. The contrast between the two candidates is small—1.34-fold at one end of the window and 0.86-fold at the other—and this is itself a result: the sign decides which vessel leads, but it cannot produce a large anatomical difference, because Equation (8) makes the sensitivity linear in 2δ/*D* and the packing bound of Equation (7c) prevents the medullary layer from becoming thick enough for the geometric factor to dominate. The normally perfused vasa recta is the most stable of the four (29.6–30.2%), its wall shear rate of 109 s⁻¹ lying close to the 100 s⁻¹ reference of Equation (7a), so that $f_\gamma$ ≈ 1 whatever the sign.

**Table 7.** Excess wall-shear-stress variability at ESR 100 relative to ESR 10 mm h⁻¹, as a function of the cell-free-layer shear exponent *s* of Equation (7a).

| *s* | Glomerular capillary | Peritubular capillary | Vasa recta (medulla) | Vasa recta, hypoperfused | Most affected vessel |
|---|---:|---:|---:|---:|---|
| **−0.12 (default)** | +27.6% | +28.4% | +30.2% | **+37.0%** | hypoperfused vasa recta |
| −0.06 | +28.5% | +29.0% | +30.0% | +34.2% | hypoperfused vasa recta |
| 0.00 | +29.6% | +29.7% | +29.9% | +31.9% | hypoperfused vasa recta |
| +0.06 | **+31.1%** | +30.4% | +29.7% | +30.0% | glomerular capillary |
| +0.12 | **+32.9%** | +31.3% | +29.6% | +28.4% | glomerular capillary |

The practical consequence is that the medullary localisation of Section 3.6 must be read as a prediction conditional on *s* < 0, not as a model-independent fact. Neither the magnitude nor the sign-independence of the effect is at issue; what the sign decides is which of two vessels leads, and by how much—which, within the admissible window, is little. The single measurement that would decide the question is therefore the shear-rate dependence of the cell-free layer in vasa recta, and we state it as a prediction rather than leave it as a caveat (Section 4.5, P5).

### 3.8 No self-arresting stasis within the physiological range

We searched the model for multiple operating points—a fold in the flow curve Q(ΔP/L) that would indicate a self-arresting stasis, in which a falling velocity raises viscosity, which further lowers velocity. At the tube haematocrit used throughout the model (H = 0.42) the self-consistent operating point was unique at every pressure gradient from 5 × 10⁴ to 10⁷ Pa m⁻¹, and the flow curve was strictly monotone (Figure 7a). The same uniqueness held at H = 0.30 and H = 0.45, so the result does not depend on the haematocrit chosen, and it held for both the normal and the clinically calibrated aggregation amplification (1.033×, the value attained at the calibration anchor of 100 mm h⁻¹).

A fold appeared only when the aggregation amplification was pushed above the calibrated value: multiple operating points first occurred at an amplification of about 1.15× at H = 0.42, i.e. about 1.12 times the calibrated 1.033×, and at a closely similar value at H = 0.30 and H = 0.45. The controlling quantity is therefore not haematocrit but proximity to the packing singularity of the Quemada law: the fold condition is that the effective zero-shear parameter approach k·H/2 → 1, and in this parameterisation that requires roughly 10–15% more amplification than the clinical calibration supplies (Figure 7b). Extrapolated along the aggregation mapping, reaching that amplification would require an ESR of the order of 1.2 × 10³ mm h⁻¹, far outside any physiological value. Within the calibrated range, and within the ±10-percentage-point uncertainty band of the calibration itself (Supplementary Note S1), the operating point is unique. We therefore find no support for spontaneous viscosity-driven stasis at the aggregation states that the clinical data support. Stasis in the renal microcirculation would require an additional mechanism—an already-low perfusion pressure, vessel collapse, or leukocyte adhesion—rather than aggregation acting through the flow–viscosity feedback alone.

### 3.9 Calibration: the viscosity rise is mostly plasma-borne, and haematocrit is the missing covariate

The inverse calibration returned a plasma-viscosity multiple of 1.228 and a required k₀ amplification of only 1.033× (from 4.208 to 4.346). In other words, reproducing the observed clinical viscosity increment required the plasma viscosity to rise by 23% but the aggregation parameter to rise by only about 3%, and that 3% is the whole of the cellular contribution at the calibration anchor (ESR 100 mm h⁻¹); at ESR 60 mm h⁻¹ it is 2.2% and at ESR 80 mm h⁻¹, 2.8%. The recovered k₀ of 4.35 fell inside the directly measured clinical range of 3.05–4.36, which is an independent consistency check on the anchoring.

This result has two consequences. First, it means that a substantial fraction of the viscosity change seen clinically when ESR is high is attributable to fibrinogen-driven plasma viscosity rather than to RBC aggregation.⁶ Second, and more importantly for the hypothesis, it means that ESR alone under-determines the rheology: two patients with the same ESR can differ in how much of their rheological load is plasma-borne and how much is cell-borne. Any clinical use of ESR as a rheological proxy must account for this.

The measured haematocrit correction of the aggregation index quantifies a second, independent source of under-determination.⁹ Because the aggregation index scales with haematocrit at a measured rate of 0.284 per unit Ht, reading an uncorrected index as though it were haematocrit-corrected biases the inferred aggregation state by a factor $(1+\Delta\mathrm{AI}/\mathrm{AI}_0)^{4}-1$, where $\Delta\mathrm{AI}=0.284\,\Delta\mathrm{Ht}$ and $\mathrm{AI}_0$ is the corrected index of the state concerned. At a representative elevated state, an uncorrected index in a patient with a haematocrit of 0.42 over-estimates the aggregation state by 17%; at 0.45, by 46%; and at 0.48, by 81%. Haematocrit, not ESR, is therefore the missing covariate in any attempt to use the ESR as a rheological proxy, and this is a quantitative statement derived from measurement rather than from the model.

---

## 4. Discussion

### 4.1 A revised hypothesis whose anatomical target is decided by one unresolved sign

The model does not support the intuitive chain. Each of its four predicted consequences failed in a specific, interpretable way: the viscosity effect is confined to low shear; the mean WSS is viscosity-independent; the cell-free layer thickens rather than thins; and no stasis arises at physiological haematocrit. Rather than discard the haemodynamic idea, we used these failures to constrain it, and they point to a single surviving pathway.

We propose the following hypothesis. The rheological state indexed by an elevated ESR mechanically loads the renal microcirculation principally by increasing the temporal variability of the wall shear stress, and the effect is conditional on hypoperfusion. The mean wall shear stress is unchanged and the RBC–endothelium gap widens rather than narrows, whatever the sign of the cell-free-layer/shear relation. The anatomical target is the one element of the hypothesis that is not sign-independent, and it is here that the model's most consequential result lies. Under the aggregation-dominated sign the hypoperfused medulla is the most exposed segment and the high-shear cortical circulation the least; under the migration-dominated sign the order reverses and the glomerular capillary becomes the most exposed (Section 3.7). Because both signs are represented in the primary literature (Section 2.5), the model cannot—and does not—assert which is realised. What it does instead is sharper: it shows that the entire anatomical question collapses onto a single measurable constitutive exponent, that both candidate targets are already sites of interest in ischaemic renal injury, and that no other modelling choice has a comparable effect on the conclusion. The unresolved sign is thus not a weakness of the model. It is the model's principal deliverable: the quantity that converts a long-standing qualitative disagreement into a decidable experiment.

Two features make this hypothesis both more precise and more defensible than the original. First, it is segment-specific: it does not require the implausible claim that an elevated ESR perturbs the glomerulus—a high-shear environment in which the aggregation effect on viscosity is below 1%—but only that it perturbs whichever segment carries a large baseline cell-free-layer fraction, which in this renal geometry is limited to a small number of candidate vessels. Second, it identifies a specific physical channel: not the magnitude of the force but its unsteadiness. Endothelial mechanotransduction is known to depend on the temporal character of the applied stress and not only on its mean,³¹ so a 37% increase in the variability of the WSS at a fixed mean (at ESR 100 mm h⁻¹, under the aggregation-dominated sign) is a physically meaningful perturbation even though the mean is unchanged.

A third feature is the grading of the response, which is where the model speaks to clinical intuition. Clinical concern attaches to sustained, markedly elevated ESR values rather than to modest deviations from the reference range, and the model predicts that shape without having been constrained to it. The excess wall-stress variability in the hypoperfused medulla rises smoothly and nearly linearly with ESR, with no sharp threshold (Table 6). The clinical interpretation of a given ESR is therefore not a step function but a steep gradient, and the model locates the region of that gradient in which the rheological load becomes mechanically material.

### 4.2 The three structural reasons the intuitive mechanism fails

It is worth stating plainly why the intuitive chain fails, because each failure is generic and would apply to any similar hypothesis. Aggregation affects blood viscosity only at low shear, because the Quemada law—like every established constitutive model of blood—returns to a shear-independent high-shear asymptote governed by RBC deformability rather than aggregation. In a tube with a fixed driving pressure, the mean wall shear stress is a purely geometric quantity. And a marginating suspension concentrates cells in the core, which, by mass conservation, thickens the cell-free layer. None of these three statements depends on the particular parameter values chosen; they are structural features of the physics. A hypothesis that predicts the opposite must therefore be supported by evidence that one of these structural statements is violated in vivo, and we are not aware of such evidence.

### 4.3 The medullary prediction, and why it is conditional

The medulla was not an input to the model, but neither is its primacy a robust output, and the two points must be kept apart. Slow medullary flow acts in two ways: the aggregation effects on viscosity and on cell-free-layer variability are confined to low shear rates, and a slow-flowing vessel carries a cell-free layer occupying a larger fraction of its lumen, so a fluctuation of given absolute size perturbs the near-wall gap more strongly. The second effect carries most of the medullary excess (Section 3.6) but rests on a modelling choice rather than a measurement, and its size is bounded by Equation (7c). The consequence is quantitative and modest: the hypoperfused medulla leads the glomerular capillary by 1.34-fold at *s* = −0.12, and the ranking reverses at *s* ≈ +0.04 (Section 3.7). The medullary localisation is therefore a prediction of the model, contingent on *s* < 0, and its magnitude is not large enough to carry a claim of anatomical specificity on its own. What does not depend on the sign is the general form of the conclusion: the model converges on a small set of low-shear candidate segments, both of which—the hypoperfused medulla and, under the opposite sign, the glomerular capillary—are sites at which the renal microcirculation is already of interest in ischaemic injury, and in which pericyte-mediated capillary constriction has been shown to produce no-reflow.³⁰

One caveat attaches specifically to the medulla. Myogenic autoregulation is well developed in the cortex but weak in the medulla, where perfusion is governed more by metabolic and countercurrent factors than by a myogenic reflex.²⁷,²⁸ The medullary circulation therefore sits nearer the fixed-pressure-gradient end of the bracket used in Section 2.4, where a rise in viscosity lowers flow and hence shear rate. That acts in the same direction as the effect reported here, so taking the fixed-flow case as the upper limit is conservative for the medullary claim.

### 4.4 Relation to prior work

Two strands of prior work support the revised hypothesis. On the microvascular side, three direct measurements converge on it. Increasing RBC aggregation thickens the cell-free layer⁸,¹⁶,¹⁷—the opposite of the intuitive expectation. Red-cell aggregation, rather than red-cell adhesion to the endothelium, is the dominant determinant of in vivo microvascular flow,⁷ and cleavage of the endothelial glycocalyx has recently been shown to increase aggregation, which supplies a route by which endothelial injury and the sedimenting abnormality could reinforce each other.³² And the cell-free layer fluctuates in width on short timescales, with the fluctuations modulating arteriolar wall shear stress.¹⁴,¹⁸ Critically, aggregation increases the variability of the cell-free layer at low shear rates but not at moderate or high shear rates,²⁴ which is exactly the gating our model requires and which we encoded as a constraint rather than derived. On the renal side, the association between a raised ESR and renal injury was documented in the case–control series that motivated this work⁴ and whole-blood viscosity is elevated at low shear in nephrotic syndrome,⁵ while viscosity has since been linked to cardiovascular events and to mortality in CKD and end-stage renal disease;³³,³⁴ no mechanism was proposed; the present work supplies a quantitative candidate mechanism that is consistent with those observations. The principal novelty of this paper is not the idea that haemodynamics may matter in renal disease—that is old—but two things: the decomposition of the idea into measurable links, with the demonstration that only one of them survives; and the finding that the surviving link's anatomical target is governed by a single constitutive sign that the existing literature reports in both directions, so that an unresolved qualitative controversy is replaced by one decisive measurement rather than by an assumption. A modelling study can contribute no more usefully than by showing which measurement would make it obsolete.

### 4.5 Falsifiable predictions

The hypothesis is only as valuable as the experiments it invites. We state five predictions, in order of decreasing ease of testing.

**P1 (microfluidic, decisive for the sign of the mechanism).** In a microchannel perfused with blood at controlled aggregation, increasing aggregation will increase the cell-free layer thickness and will not increase the RBC–endothelium contact frequency. This is a direct, low-cost test; the prediction is already supported by prior microvascular work¹⁶,¹⁷ and its confirmation would close the question raised by the intuitive mechanism.

**P2 (microfluidic, decisive for the gating).** The increase in cell-free-layer variability produced by aggregation will be confined to low shear rates and will be absent above approximately 20–50 s⁻¹. This follows directly from the shear gating expressed in Equation (9) and from the experimentally observed gating of cell-free-layer variability.²⁴

**P3 (imaging, decisive for the medullary claim).** In an experimental preparation in which medullary perfusion can be reduced, an increase in RBC aggregation will increase the temporal variability of wall shear stress in vasa recta and in cortical capillaries, but by a larger factor in the vasa recta (37.0% against 27.6% at ESR 100 mm h⁻¹ in the model, Table 6) and by a larger factor still under reduced perfusion. The cortical increase is part of the prediction and not a null: the model requires the effect to be present everywhere and only its ranking to depend on the sign (Section 3.7).

**P4 (clinical, provisional).** If the hypothesis is correct, then in a renal cohort the association between ESR and outcome should be (i) stronger for markers of medullary injury or perfusion than for cortical markers, though the modelled difference is small enough that a study powered only for the ranking would need to be large; (ii) attenuated by adjustment for plasma viscosity and fibrinogen, which would identify the plasma-borne fraction of the rheological load; (iii) steeper at the high end of the ESR range than at the low end, because the mechanical load is predicted to grow nearly linearly with ESR above about 40 mm h⁻¹ rather than to appear abruptly at a threshold; and (iv) demonstrable only when the elevation is sustained. The last requirement follows from the physics rather than from the model: the quantity computed here is a steady-state load, and a single measurement cannot distinguish a transient from a sustained one. A design in which ESR is documented over at least six months would therefore test the hypothesis in the form in which it arose clinically, and it is the design we would propose for a first prospective study. This prediction is deliberately weak, because the model computes a mechanical load and not an outcome, and it therefore supports no quantitative claim about a clinical ESR threshold—including the 69.8–82.0 mm h⁻¹ diagnostic threshold of the case–control series,⁴ which was derived for a different question.

Refutation of P1 or P2 would falsify the revised mechanism as stated. Refutation of P3 would remove the medullary specificity and leave only the generic claim that aggregation perturbs low-shear microvascular flow. P5 is different in kind: it does not test the mechanism but decides its anatomical target, and it is the only one of the five that the present literature cannot already answer.

**P5 (microvascular, decisive for the sign).** The shear-rate dependence of the cell-free layer in vasa recta, measured across roughly 5–1000 s⁻¹, will establish whether the layer is thicker at low shear (*s* < 0) or at high shear (*s* > 0). This is the single measurement that determines which of two vessels the hypothesis names (Section 3.7): at the aggregation-dominated sign the hypoperfused medulla carries the largest excess (37.0% at ESR 100 mm h⁻¹, 1.34-fold the glomerular value), and at the migration-dominated sign the glomerular capillary does (32.9%, 1.16-fold the hypoperfused medullary value). It should be said plainly that this measurement now discriminates between two similar alternatives rather than between two very different ones; what it still decides is which vessel a mechanistic claim would name, and that is worth deciding before any clinical prediction is attached to either. The measurement requires only the preparations already used in the vasa recta literature, and we regard it as the highest-value experiment the model identifies. We note that the primary literature currently reports both signs¹⁶,¹⁹⁻²¹ and that if, as one simulation suggests,²⁰ the dependence is non-monotonic, then the segment-specific prediction would have to be re-derived from the measured curve rather than merely re-signed.

### 4.6 Limitations

The limitations fall into three groups, and we state each by what it could change.

*Model calibration.* Three choices set the absolute magnitude of the predicted load, and none of them is measured. First, the ESR-to-aggregation mapping, although derived from measured constants rather than assumed (Section 2.2), is not an independent validation: because the Westergren ESR–velocity relation is near-linear, the √ESR scaling follows algebraically from Stokes' law and that linearity, so the empirical content of the step rests entirely on the measured linearity, which we have not re-measured. The absolute aggregate sizes in Table 1 are therefore anchored but provisional; the source study also characterised blood at haematocrits up to 0.40 against the 0.42 modelled here, a small extrapolation. Second, the calibration target is a single published viscosity increment in nephrotic syndrome,⁵ and the amplification is anchored at ESR 100 mm h⁻¹; a target drawn from diabetic kidney disease, or an anchor at 60 mm h⁻¹, would change the low-shear viscosity ratio—from 1.097 to 1.150 at 2.7 s⁻¹ on the lower anchor—without changing the gating. Third, the model of WSS temporal variability has four parameters of which only the gating threshold is anchored to a measured value (9.2 ± 0.6 s⁻¹);¹⁴,²⁴ the baseline coefficient of variation and the aggregation sensitivity are assumptions, and a larger experimental dataset would move the absolute magnitudes of Tables 5 and 6. None of these choices changes the sign of the response or its monotonicity in ESR.

*Vessel ranking.* The ranking rests on two further choices. The baseline layer width is modelled as a power law in shear rate, δ ∝ $\dot\gamma^{\,s}$, with *s* = −0.12 recorded in Supplementary Table S1 as an assumption; its sign is the pivot of the ordering, moving the largest excess from the hypoperfused medulla (37.0%) to the glomerular capillary (32.9%) while leaving the normally perfused vasa recta almost unchanged (29.6–30.2%). The admissible window of *s* is narrower than the range of behaviours the literature reports, because Equation (7c) caps the layer at the packing limit (Section 3.7); the ordering is therefore reported only where it is physically admissible. The vessel geometry is a single rigid circular tube with a sharp core/layer interface; a diffuse interface would reduce the effective δ entering Equation (8) and hence the geometric factor 2δ/(*D* − 2δ), which would reduce rather than inflate the medullary advantage. These are legitimate simplifications for a reduced-order model, but they mean that the ranking should be read as a ranking and not as a measurement.

*Clinical interpretation.* Three boundaries apply. The endpoint is not computed: the model quantifies mechanical load, not injury, and there is no constitutive law relating a change in wall-stress variability to endothelial damage or loss of renal function, so everything downstream of "the endothelium experiences a more variable stress" remains hypothesis. And the load computed here is a steady-state one, whereas a clinical ESR is usually a single measurement that cannot distinguish a transient from a sustained elevation—which is why P4 is framed around sustained rather than single values. Finally, all computations were performed by a single analyst with no independent re-implementation, and independent replication of the code is desirable before any of these numbers is used quantitatively.

---

## 5. Conclusions

The intuitive mechanism linking an elevated erythrocyte sedimentation rate to renal injury—that increased red-cell aggregation presses cells onto the endothelium—does not survive quantitative examination with literature-anchored parameters. Aggregation affects blood viscosity only below a shear rate of a few reciprocal seconds; the mean wall shear stress is independent of viscosity under a fixed pressure gradient; and aggregation thickens rather than thins the cell-free layer. What remains, and what we propose as a testable hypothesis, is that an elevated ESR acts through the temporal variability of the wall shear stress in the low-shear microcirculation. The magnitude of that effect is graded rather than thresholded, and becomes mechanically material only at markedly elevated ESR values: across ESR 10–150 mm h⁻¹ the modelled excess in wall-stress variability in the hypoperfused medulla runs from 6.5% to 46.1%, against 5.1% to 37.2% in the glomerular capillary. The stronger and more general result is structural. The existence and the ESR-grading of the effect hold in every vessel and at every value of the cell-free-layer/shear exponent that the packing constraint admits, whereas the identity of the most exposed vessel is fixed by the sign of that exponent alone, reversing between the hypoperfused medulla and the glomerular capillary at a crossover near *s* = +0.04. The price of that robustness is honesty about its size: the anatomical contrast is about 1.3-fold, too small to found a claim of specificity on, and the model is explicit that what the sign decides is which of two vessels a mechanistic statement would name. A reduced-order model can do no more than this, and it need do no less: it has converted a long-standing qualitative disagreement about the direction of a constitutive relation into a single experiment, which we state as prediction P5, whose outcome would decide the anatomical target of the hypothesis without any further modelling. The hypothesis is narrower than the original, it is consistent with existing microvascular measurements, and it makes five predictions that are experimentally accessible. If they hold, an inexpensive and ubiquitous laboratory test may carry mechanistically interpretable information about renal microvascular risk; if they fail, the haemodynamic interpretation of the ESR in renal disease should be abandoned. Either outcome is informative, which is the property a hypothesis should have. A modelling study can contribute no more usefully than by showing which measurement would make it obsolete.

---

## Declarations

**Ethics approval and consent to participate.** Not applicable; this study used no human or animal subjects.

**Consent for publication.** Not applicable.

**Availability of data and materials.** All model code, parameter tables, and numerical output are provided as supplementary material (Supplementary Codes S1–S5, Supplementary Tables S1–S2, Supplementary Note S1, Supplementary Data S1). Supplementary Protocol S1 sets out the bench validation of predictions P1 and P2. The complete model repository is openly available in a public archive: https://doi.org/10.6084/m9.figshare.34333371.

**Competing interests.** The author declares no competing interests.

**Funding.** The author received no financial support for the research, authorship and/or publication of this article.

**Authors' contributions.** Yan Wang is the sole author and was responsible for all aspects of the work, per the CRediT taxonomy: Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing – original draft; Writing – review and editing; Visualization. The author approved the final manuscript.

**Declaration of generative AI and AI-assisted technologies.** During the preparation of this work the author used DeepSeek in order to develop and debug the Python analysis code and to assist with language editing. After using this tool, the author reviewed and verified all code, output and text, and takes full responsibility for the content of the publication.

---

## References

1. Bray C, Bell LN, Liang H, Haykal R, Kaiksow F, Mazza JJ, Yale SH. Erythrocyte sedimentation rate and C-reactive protein measurements and their relevance in clinical medicine. *WMJ*. 2016;115(6):317–321. PMID 29094869.

2. Umemura H, Fukuda Y, Miyashita T, Nakayama T. Elucidation of the mechanism and significance of the erythrocyte sedimentation rate from clinical laboratory data. *Acta Med Okayama*. 2022;76(4):447–455. doi:10.18926/AMO/63904. PMID 36123160.

3. Fest J, Ruiter R, Mooijaart SP, Ikram MA, van Eijck CHJ, Stricker BH. Erythrocyte sedimentation rate as an independent prognostic marker for mortality: a prospective population-based cohort study. *J Intern Med*. 2019;285(3):341–348. doi:10.1111/joim.12853. PMID 30537394.

4. Wang Y, Bai J, Gao Y, Lei X. Efficacy of abnormal increase of erythrocyte sedimentation rate in the diagnosis of secondary renal diseases in nephropathic patients. *China Medicine* (in Chinese). 2020;15(10):1589–1592. doi:10.3760/j.issn:1673-4777.2020.10.024.

5. McGinley E, Lowe GDO, Boulton-Jones M, Forbes CD, Prentice CR. Blood viscosity and haemostasis in the nephrotic syndrome. *Thromb Haemost*. 1983;49(3):155–157. doi:10.1055/s-0038-1657351. PMID 6410531.

6. Semenov AN, Lugovtsov AE, Shirshin EA, Yakimov BP, Ermolinskiy PB, Bikmulina PY, et al. Assessment of fibrinogen macromolecules interaction with red blood cells membrane by means of laser aggregometry, flow cytometry, and optical tweezers combined with microfluidics. *Biomolecules*. 2020;10(10):1448. doi:10.3390/biom10101448. PMID 33076409.

7. Baskurt OK, Meiselman HJ. RBC aggregation: more important than RBC adhesion to endothelial cells as a determinant of in vivo blood flow in health and disease. *Microcirculation*. 2008;15(7):585–590. doi:10.1080/10739680802107447. PMID 18608991.

8. Bishop JJ, Popel AS, Intaglietta M, Johnson PC. Rheological effects of red blood cell aggregation in the venous network: a review of recent studies. *Biorheology*. 2001;38(2–3):263–274. doi:10.1177/0006355X2001038002003003. PMID 11381180.

9. Higuchi M, Watanabe N. A rapid and accurate method for estimating the erythrocyte sedimentation rate using a hematocrit-corrected optical aggregation index. *PLoS One*. 2022;17(7):e0270977. doi:10.1371/journal.pone.0270977. PMID 35819942.

10. Higuchi M, Watanabe N. Determination of the erythrocyte sedimentation rate using the hematocrit-corrected aggregation index and mean corpuscular volume. *J Clin Lab Anal*. 2023;37(6):e24877. doi:10.1002/jcla.24877. PMID 37003619.

11. Richardson JF, Zaki WN. Sedimentation and fluidisation: Part I. *Trans Inst Chem Eng*. 1954;32:35–53.

12. Quemada D. Rheology of concentrated disperse systems and minimum energy dissipation principle. *Rheol Acta*. 1977;16(1):82–94. doi:10.1007/BF01516932.

13. Cokelet GR. The rheology of human blood. In: Fung YC, Perrone N, Anliker M, eds. *Biomechanics: Its Foundations and Objectives*. Prentice-Hall; 1972:63–103.

14. Namgung B, Ong PK, Johnson PC, Kim S. Effect of cell-free layer variation on arteriolar wall shear stress. *Ann Biomed Eng*. 2011;39(1):359–366. doi:10.1007/s10439-010-0130-3. PMID 20652744.

15. Salame M, Fenech M. A two-phase core-plasma model for microvascular blood flow: comparative analysis of hemodynamic models. *PLoS One*. 2026;21(1):e0327948. doi:10.1371/journal.pone.0327948. PMID 41481754.

16. Suzuki Y, Tateishi N, Soutani M, Maeda N. Flow behavior of erythrocytes in microvessels and glass capillaries: effects of erythrocyte deformation and aggregation. *Int J Microcirc Clin Exp*. 1996;16(4):187–194. doi:10.1159/000179172. PMID 8923151.

17. Maeda N, Suzuki Y, Tanaka J, Tateishi N. Erythrocyte flow and elasticity of microvessels evaluated by marginal cell-free layer and flow resistance. *Am J Physiol*. 1996;271(6 Pt 2):H2454–H2461. doi:10.1152/ajpheart.1996.271.6.H2454. PMID 8997305.

18. Kim S, Kong RL, Popel AS, Intaglietta M, Johnson PC. A computer-based method for determination of the cell-free layer width in microcirculation. *Microcirculation*. 2006;13(3):199–207. doi:10.1080/10739680600556878. PMID 16627362.

19. Ong PK, Namgung B, Johnson PC, Kim S. Effect of erythrocyte aggregation and flow rate on cell-free layer formation in arterioles. *Am J Physiol Heart Circ Physiol*. 2010;298(6):H1870–H1878. doi:10.1152/ajpheart.01182.2009. PMID 20348228.

20. Liao CT, Chen YL. Shear-induced non-monotonic viscosity dependence for model red blood cell suspensions in microvessels. *Biomicrofluidics*. 2019;13(6):064115. doi:10.1063/1.5127879. PMID 31768201.

21. Salame M, Fenech M. Key contributors to cell-free layer formation: an experimental investigation of hematocrit and shear rate gradient. *Microvasc Res*. 2025;162:104859. doi:10.1016/j.mvr.2025.104859. PMID 40846133.

22. Köry J, Maini PK, Pitt-Francis JM, Byrne HM. Dependence of cell-free-layer width on rheological parameters: combining empirical data on flow separation at microvascular bifurcations with geometrical considerations. *Phys Rev E*. 2022;105(1-1):014414. doi:10.1103/PhysRevE.105.014414. PMID 35193324.

23. Gracka M, Lima R, Miranda JM, Student S, Melka B, Ostrowski Z. Red blood cells tracking and cell-free layer formation in a microchannel with hyperbolic contraction: a CFD model validation. *Comput Methods Programs Biomed*. 2022;226:107117. doi:10.1016/j.cmpb.2022.107117. PMID 36122496.

24. Ong PK, Jain S, Kim S. Temporal variations of the cell-free layer width may enhance NO bioavailability in small arterioles: effects of erythrocyte aggregation. *Microvasc Res*. 2011;81(3):303–312. doi:10.1016/j.mvr.2011.02.002. PMID 21345341.

25. Marcinkowska-Gapińska A, Maciejewska B, Majewska A, Kawałkiewicz W, Urbaniak-Olejnik M, Loba W, et al. Can assessment of rheological properties of whole blood and plasma be useful in the diagnosis of tinnitus? A pilot study. *Int J Environ Res Public Health*. 2023;20(3):1977. doi:10.3390/ijerph20031977. PMID 36767344.

26. Brezis M, Rosen S. Hypoxia of the renal medulla—its implications for disease. *N Engl J Med*. 1995;332(10):647–655. doi:10.1056/NEJM199503093321006. PMID 7845430.

27. Pallone TL, Edwards A, Mattson DL. Renal medullary circulation. *Compr Physiol*. 2012;2(1):97–140. doi:10.1002/cphy.c100036. PMID 23728972.

28. Edwards A, Silldorff EP, Pallone TL. The renal medullary microcirculation. *Front Biosci*. 2000;5:E36–E52. doi:10.2741/edwards. PMID 10833463.

29. Evans RG, Smith DW, Lee CJ, Ngo JP, Gardiner BS. What makes the kidney susceptible to hypoxia? *Anat Rec (Hoboken)*. 2020;303(10):2544–2552. doi:10.1002/ar.24260. PMID 31566903.

30. Freitas F, Attwell D. Pericyte-mediated constriction of renal capillaries evokes no-reflow and kidney injury following ischaemia. *eLife*. 2022;11:e74211. doi:10.7554/eLife.74211. PMID 35285797.

31. Chiu JJ, Chien S. Effects of disturbed flow on vascular endothelium: pathophysiological basis and clinical perspectives. *Physiol Rev*. 2011;91(1):327–387. doi:10.1152/physrev.00047.2009. PMID 21248169.

32. Abbasi M, Jin M, Rashidi Y, Bureau L, Tsvirkun D, Misbah C. Glycocalyx cleavage boosts erythrocytes aggregation. *Sci Rep*. 2024;14(1):24340. doi:10.1038/s41598-024-75012-0. PMID 39420024.

33. Celik T, Yilmaz MI, Balta S, Ozturk C, Unal HU, Aparci M, et al. The relationship between plasma whole blood viscosity and cardiovascular events in patients with chronic kidney disease. *Clin Appl Thromb Hemost*. 2017;23(6):663–670. doi:10.1177/1076029616634888. PMID 26907084.

34. Jung JH, Chae YJ, Lee DH, Cho YI, Ko MM, Park SK, Kim W. Changes in whole blood viscosity during hemodialysis and mortality in patients with end-stage renal disease. *Clin Hemorheol Microcirc*. 2017;65(3):285–297. doi:10.3233/CH-16183. PMID 27767962.

## Figure captions

**Figure 1.** Structure of the four-layer reduced-order model. A clinical ESR value is mapped in Layer 1 to an effective aggregate size through measures of sedimentation; Layer 2 converts aggregation into a shear-dependent blood viscosity through the Quemada law; Layer 3 solves the resulting flow in a single representative microvessel under a prescribed organ pressure gradient; and Layer 4 constructs the two-layer core/cell-free-layer geometry and evaluates the wall shear stress and its temporal variability. The shaded panel states the outcome of the model: only the temporal variability of the wall shear stress responds monotonically, it does so in every vessel, and it is largest in the low-shear, hypoperfused medulla by a factor of about 1.3. Tissue injury itself is not computed.

**Figure 2.** Layer 1 derived from measured sedimentation data rather than assumed. (a) The aggregate size factor 1 + α obtained from the measured constants agrees with a pure √ESR law by construction (the fitted exponent is exactly 0.5000). (b) The haematocrit-corrected aggregation index implied by the mapping remains above the minimum physiological value b = 0.426 reported in the source study. (c) Neglecting the haematocrit correction biases the inferred aggregation state by +17% at a haematocrit of 0.42, +46% at 0.45 and +81% at 0.48.

**Figure 3.** Consistency check of the viscosity kernel against the curve of its source study. (a) The Quemada model with a published clinical parameter set reproduces a measured whole-blood relative-viscosity curve. (b) The ratio of model to measured viscosity lies within ±7% across 0.1–100 s⁻¹ at a haematocrit of 0.42.

**Figure 4.** Shear-rate gating of the aggregation contribution to blood viscosity. (a) The ratio of the viscosity at ESR 100 to that at ESR 10 as a function of shear rate; the effect falls below +10% above approximately 3 s⁻¹ and is negligible at the shear rates of the glomerular capillary. (b) The same calculation with four published Quemada parameter sets shows that the gating is robust to the choice of parameter set, while the absolute magnitude is set by the calibration target.

**Figure 5.** Vessel-level ratios X₁₀₀/X₁₀ at a fixed organ pressure gradient. The mean wall shear stress is exactly invariant (1.000× in every vessel), the viscosity and velocity change only marginally, the cell-free layer thickens in every vessel, and the wall-shear-stress coefficient of variation increases monotonically, most strongly in the hypoperfused vasa recta.

**Figure 6.** Wall-shear-stress temporal variability, its decomposition, and its dependence on the sign of the cell-free-layer/shear relation. (a) The coefficient of variation of the wall shear stress increases monotonically with ESR over 10–150 mm h⁻¹ in every vessel. (b) At the default exponent (*s* = −0.12) the excess variability at ESR 100 relative to ESR 10 is 27.6% in the glomerular capillary, 28.4% in the peritubular capillary, 30.2% in the normally perfused vasa recta and 37.0% in the hypoperfused vasa recta. (c) Decomposition of each excess into the geometric factor of Equation (8) (coloured segments) and the shear gate of Equation (9) (hatched segments), expressed as shares of the logarithmic increase; the geometric factor accounts for 94.4% of the increase in the hypoperfused medulla and 99.4% in the normally perfused vasa recta, whereas the shear gate contributes between 0.05% and 5.6%. (d) The same excess recomputed as a function of the cell-free-layer shear exponent *s* of Equation (7a), over the window in which the packing constraint Equation (7c) is respected in every vessel. The rise is positive in every vessel for every value of *s*; the rank order crosses over at *s* ≈ +0.04, the hypoperfused vasa recta being the most affected vessel for *s* < 0 and the glomerular capillary for *s* > 0, while the normally perfused vasa recta (wall shear rate ≈109 s⁻¹, close to the 100 s⁻¹ reference of Equation (7a) is the most stable of the four. Panel labels are placed within the artwork; descriptions are given here.

**Figure 7.** The pressure–flow curve and the absence of self-arresting stasis. (a) Flow rate Q as a function of the pressure gradient ΔP/L at the tube haematocrit used throughout the model (H = 0.42), for the normal aggregation state, the clinically calibrated state (amplification 1.033×, the value attained at ESR 100 mm h⁻¹) and a stress test at 1.5×. The curve is strictly monotone and single-valued over the whole physiological range, so no fold and no stasis branch exists. (b) The fold criterion, the maximum of |d ln η / d ln γ̇|, as a function of tube haematocrit. A fold requires this quantity to exceed unity, which in this parameterisation happens only when the effective zero-shear parameter approaches the packing singularity k·H/2 → 1; numerically the first multiple operating point appears at an amplification of about 1.15×, i.e. about 12% above the calibrated 1.033×, and the threshold is almost independent of haematocrit. Reaching that amplification along the aggregation mapping would require an ESR of the order of 1.2 × 10³ mm h⁻¹. Haematocrit alone is therefore not the controlling variable.


---


