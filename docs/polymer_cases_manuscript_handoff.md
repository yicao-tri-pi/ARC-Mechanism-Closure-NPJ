# npj Computational Materials handoff: polymer mechanism cases

## Cross-case conclusion

Neither case yields a defensible mechanism falsification. Both are valuable
because they separate reproducible property-level statements from mechanism
identification:

| Case | Strongest supported result | Non-identifying step | Tension | Class-D counterexample |
|---|---|---|---|---|
| Wang 2012 | The reported \(\epsilon\) values and multi-decade changes reject a constant-\(\sigma T\tau_s\) composite null in the named rigid-chain samples; an independent errors-in-variables predictive refit remains pending | The deviation cannot identify whether \(D\tau_s\), effective carrier population, collective correlations, or a parallel channel changed; EP-derived D/p and packing mediation add further inverse steps | Same-group EP-model validation, cross-method carrier-population disagreement, and rounded-table correlation reproducibility | None found |
| Han 2023 | Alternating SIPEs show large reported conductivity enhancement; P8–P10 show similar Tg does not determine σ | Dominance of sequence-assisted hopping and unique carrier/path decomposition | Experimental control mismatch, processed-only source layers, missing sequence-wide PFG validation | None found |

This is a positive manuscript result: deductive stress testing prevents a true
descriptive discovery from being diluted by a stronger, unsupported mechanistic
verdict.

## Recommended placement

- **Main text:** use Han 2023 as the primary worked example because official
  source data permit an auditable value-level analysis. Show P8–P10 as a compact
  non-identifiability example and the sequence-control mismatch as a causal-scope
  lesson.
- **Main text, compact second example:** use Wang 2012 to distinguish direct
  σ–τs decoupling from EP-model-derived D/p and from the packing narrative.
- **Supplementary information:** full claim ledgers, scope contracts, source-data
  inventories, EP assumptions, all counterexample candidates and Lean receipts.
- **Motivating example only:** if the main-text case budget is one, retain Wang as
  the opening vignette and keep its full audit in the SI. Do not advertise either
  paper as a “mechanism refuted” case.

## Figure and table plan

1. **Main Fig. X — Wang evidence ladder.** The completed vector figure
   `figures/wang2012_evidence_ladder.svg` separates observation → model inversion
   → mechanism in three panels. Green denotes directly supported observations,
   amber denotes model tension, and blue denotes non-identification. Red is
   deliberately absent because no candidate passed the falsification contract.
   The accompanying text must define the Axis-1 null as the conjunction of
   constant effective carrier population, constant collective correlation and
   \(D\tau_s\), which predicts \(\sigma T\tau_s=\mathrm{constant}\).
2. **Main Fig. Y — P8–P10 non-identifiability panel.** Use
   `figures/han_p8_p10_nonidentifiability.svg`: Tg, conductivity and Li
   concentration/σ-per-molar-Li proxy. Caption must state that the proxy is not a
   mobility estimate and that PEO length, concentration and Mn co-vary.
3. **Main Table 1 — Verdict grammar.** A–D evidence classes, five verdicts,
   minimum evidence and prohibited inference.
4. **Main Table 2 — Cross-case claim matrix.** Claim type, direct observable,
   inference model, alternative models, scope verdict and promotion ceiling.
5. **SI Tables Sx–Sy.** Complete Wang and Han claim/evidence ledgers, provenance
   hashes, workbook coverage and counterexample scope contracts.
6. **SI Fig. Sz — Lean boundary.** Empirical premise box → formal implication →
   kernel-checked conclusion → promotion ceiling; explicitly leave empirical
   premise validation outside the prover.

### Caption for the P8–P10 panel

**Figure Y | Similar glass-transition temperatures do not identify ionic
conductivity.** P8–P10 are alternating single-ion polymers with PEO side-chain
lengths (n=13,17,23). Their reported Tg values span 4 °C, whereas conductivity
at 30 °C spans 4.38-fold. Li concentration changes by 1.57-fold; dividing σ by
concentration leaves a 2.78-fold range. This ratio is shown only as a diagnostic
proxy and is not a mobility or correlation-free transport coefficient. Error
bars are the reported conductivity standard deviations; no inferential test is
performed. Values are from the official supplementary information and public
source-data files for Han et al. (2023).

## Manuscript-ready paragraphs

### Results paragraph: Wang

Wang et al. provide a useful separation between observation and mechanism. A
precise Axis-1 null combines three assumptions: \(D\tau_s\) is constant, the
effective carrier population is temperature invariant, and collective ion
correlations are temperature invariant. Together they predict
\(\sigma T\tau_s=\mathrm{constant}\), or a slope of −1 for
\(\log(\sigma T)\) against \(\log\tau_s\). The reported fractional-coupling
exponents and multi-decade changes in \(\sigma T\tau_s\) oppose this composite
null in the named rigid-backbone electrolytes, although an independent
errors-in-variables, held-out predictive refit awaits digitized or raw curves
with a frozen temperature window. A violation identifies only that at least one
member of the conjunction fails; conductivity and segmental relaxation alone do
not show that diffusion itself decouples. The further decomposition into
diffusivity and mobile-ion fraction is an inverse result from an electrode-
polarization model rather than a direct species-resolved measurement. The SI
shows that the Trukhan and MacDonald expressions are approximately equivalent
for a Debye-like EP response when ΔεEP ≫ εR, but this conditional algebra does
not validate their shared physical premises. The same group later showed that related
Macdonald–Trukhan inversions can deteriorate with concentration and that empirical
normalization lacks a firm theoretical basis. These findings do not invalidate
the reported failure of the composite scaling null. They instead place the D/p
partition in the non-identifying/tension category. Dynamic-bond-percolation,
three-timescale cation diffusion, cluster Nernst–Einstein and Onsager models give
explicit alternative routes to the same conductivity trend. Wang provides no
independently calibrated bridge from packing to renewal/hopping parameters, then
to self-diffusion and collective conductivity; packing frustration is therefore
a plausible, not exclusive, explanation. Moreover, regression on the rounded SI
Table I values preserves the qualitative fragility-over-Tg ordering but does not
reproduce the article's exact R² values, so the numerical correlation remains a
small-n reproducibility tension rather than a causal result.

### Results paragraph: Han

Han et al. report a large conductivity ordering across sequenced single-ion
polymers and provide mutually consistent spectroscopy and simulation signatures
of altered ion environments. The strongest internal non-identifiability test is
P8–P10: similar Tg values coexist with a 4.38-fold conductivity range, so Tg
alone cannot determine transport. This comparison does not isolate sequence,
because all three polymers are alternating while side-chain length, Li
concentration and molecular weight co-vary. Likewise, a selected site-to-site MD
event establishes pathway plausibility but not pathway dominance. We therefore
classify the enhancement as supported within the synthesized set, the modeled
ion-distribution changes as supported within the simulation domain, and the
unique sequence-assisted migration mechanism as non-identifying pending matched
controls and ensemble transport statistics.

### Discussion paragraph: methodological lesson

These cases illustrate why an anomaly, a countermodel and a counterexample must
not be conflated. A countermodel shows that the available observations admit
more than one mechanism; a literature tension shows that an expectation changes
under a different system or measurement chain; only a scope-matched violation
of a declared necessary or universal prediction constitutes falsification. Lean
can certify the conditional implication once its premises are stated, but it
cannot certify material comparability or measurement validity. The publication
gate must therefore join formal proof receipts to empirical scope contracts and
uncertainty, rather than replacing them.

## Artifact map and verification

| Artifact | Purpose | Status |
|---|---|---|
| `docs/npj_paper_blueprint.md` | Updated article architecture and gates | Edited |
| `docs/polymer_mechanism_audit_contract.md` | Frozen definitions and decision rule | Complete |
| `docs/wang2012_mechanism_audit.md` | Wang stage package | Complete |
| `docs/wang2012_axis1_predictive_research_contract.md` | Frozen Axis-1 inputs, forward models, loss and decision rule | Specification complete; empirical refit pending raw/digitized curves |
| `docs/han2023_mechanism_audit.md` | Han stage package | Complete |
| `evidence/npj_mechanism_audit/derived/*.csv/json` | Machine-readable source audit | Generated |
| `formal/PolymerMechanismAudit.lean` | Minimal logical obligations | Lean 4.33.1 kernel checked |
| `results/polymer_mechanism_lean_receipt.json` | Proof provenance and boundary | Return code 0 |
| `evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv` | Competing calculable theories and discriminating measurements | Complete literature matrix |
| `figures/han_p8_p10_nonidentifiability.{svg,png}` | Manuscript-ready diagnostic panel | Vector/raster inspected |
| `figures/wang2012_evidence_ladder.{svg,png}` | Manuscript-ready observation/inference/mechanism schematic | Standalone panels and composite inspected |

No manuscript branch, remote repository, pull request or Overleaf target was
modified. Such publication steps require a separate, explicit authorization and
a designated integration branch.
