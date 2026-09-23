# Wang et al. (2012): claim and evidence audit

Primary source: [DOI 10.1103/PhysRevLett.108.088303](https://doi.org/10.1103/PhysRevLett.108.088303). Model-validation source: [Wang et al. (2013), DOI 10.1103/PhysRevE.87.042308](https://doi.org/10.1103/PhysRevE.87.042308).

## Scope and measurement chain

The declared experimental domain is five comb-like amorphous polymer
electrolytes containing LiClO4 at 0.3–1.0 wt% (reported O:Li 220:1–540:1), gold
blocking electrodes separated by 54 µm, and broadband dielectric spectroscopy
from (10^{-2}) to (10^7) Hz. DSC was used to identify a single glass
transition. Conductivity and segmental relaxation were fitted from dielectric
spectra. The supplied SI now independently verifies the five structures and
reports Mw/PDI, salt loading, O:Li, Tg, fragility and both decoupling exponents
with uncertainties. Ion diffusivity (D) and mobile-ion fraction (p) were not directly
measured: they were inverted from electrode-polarization parameters using the
Trukhan model, an equal-cation/anion-diffusivity assumption, a Debye-like EP
model, the approximation ΔεEP ≫ εR, and constant normalizations selected to
recover a high-temperature stoichiometric limit.

The resulting chain is:

> dielectric spectrum → fitted σ and τs → electrode-polarization length/time →
> Debye-like EP model → Trukhan inversion → normalized D and p → mechanistic
> interpretation.

The SI derives approximate equivalence between the MacDonald and Trukhan
expressions when ΔεEP ≫ εR, which the authors state is satisfied in practice for
EP. This is an internal equivalence of two inversions under shared assumptions;
it is not an external validation of equal species diffusivity, electrode
independence, Debye behavior or the physical meaning of p.

## Axis 1 as a predictive model comparison

The earlier shorthand “σ is not proportional to τs⁻¹” is insufficient. The
actual conductivity-only null combines three physical premises:

\[
\sigma=\frac{q^2pHD}{k_BT},\qquad D\tau_s=C,\qquad p,H=\mathrm{constant}.
\]

Together they predict \(\sigma T\tau_s=\mathrm{constant}\), or
\(\log(\sigma T)=\alpha-\log\tau_s\). Thus a changing \(\sigma T\tau_s\)
refutes the conjunction, not specifically \(D\tau_s=C\). A temperature-dependent
carrier population or collective correlation factor is an explicit countermodel
even when diffusion remains completely segmentally coupled.

The frozen reanalysis therefore compares a constrained slope β=−1 against a
free slope β with ε=1+β, using an errors-in-variables loss and held-out σ
prediction. The full model, inputs, outputs, loss and decision rule are in
`docs/wang2012_axis1_predictive_research_contract.md`; the executable fitter is
`scripts/fit_wang_axis1_models.py`. Because raw curves, BDS fit covariance and an
exact numerical definition of the paper's “near Tg” fitting window are not yet
available, the new predictive comparison is specified and smoke-tested but not
presented as an independently completed empirical refit.

## Claim ledger

| ID | Minimal proposition | Type and quantifier | Observable / target | Hidden premises and nuisance variables | Author-stated qualification | Verdict |
|---|---|---|---|---|---|---|
| W1 | In the measured rigid-backbone samples, the free-slope model departs from the constrained β=−1 composite null more strongly than in flexible controls | Predictive comparison, five named materials | σ, τs; held-out σ; β and ε | correlated fit errors, fit window, p(T), H(T), salt level, Tg, chemistry | Limited to studied materials; exact raw curves/window unavailable | **supported from reported fits; independent refit pending (A+C)** |
| W2 | The inferred D also decouples from τs | Descriptive but model-mediated | EP-derived D, τs | Debye-like EP, ΔεEP ≫ εR, equal diffusivity, blocking boundary, electrode model, normalization | SI proves only conditional Trukhan–MacDonald equivalence; main text calls the treatment qualitative and notes omitted electrode-material effects | **scope-limited / tension (A+C)** |
| W3 | The mobile-ion fraction changes weakly compared with mobility and does not drive the enhancement | Relative mechanistic attribution | EP-derived p and D | same as W2; p/D tradeoff; ion populations sensed by different methods | Reported disagreement with tracer/Raman/PFG-NMR and simulations; issue left unresolved | **non-identifying (B), with C tension** |
| W4 | Decoupling magnitude correlates with kinetic fragility more strongly than with Tg | Correlation in n=5, not universal implication | ε1/ε2 versus VFT-derived m/Tg | shared τs fit in both axes, chemistry and salt covariation, small n, rounded public inputs | No causal identification claimed; exact reported R² is not reproducible from rounded SI Table I | **supported qualitatively; numerical tension / scope-limited** |
| W5 | Rigid chains frustrate packing, producing loose local structure that facilitates ion motion | Plausible causal narrative | packing/free-volume mechanism | no direct packing/free-volume mediator measurement; carrier and topology alternatives | Framed as a scenario (“may/can”), not an exclusive law | **non-identifying (B)** |
| W6 | Fragility/rigidity is the unique cause of decoupling | Exclusivity | mechanism | would require matched interventions and mediator closure | Not actually asserted by the paper | **not an author claim; do not test as one** |

## Evidence table

| Evidence item | What it supports | What it cannot establish | Class |
|---|---|---|---|
| σTτs changes by roughly 4–6 orders of magnitude in the named rigid systems; SI reports ε1 = 0.75, 0.72 and 0.41 versus 0.16 and −0.01 in the flexible samples | The reported free-slope fit departs substantially from the β=−1 composite null in the named rigid samples | Independent held-out predictive loss without raw curves; whether p, H, Dτs or a parallel channel changed | A+C |
| SI Table I gives all five material identities, Mw/PDI, salt/O:Li, Tg, fragility and ε1/ε2 with errors | Exact public scope and qualitative material ordering | Raw spectra, unrounded fit values or regression covariance | A |
| Article reports R²=0.80/0.78 for fragility and 0.31/0.33 for Tg; unweighted OLS on rounded SI values gives 0.853/0.837 and 0.488/0.502 | Fragility remains more associated than Tg in this five-point table | Exact reproduction of the published R² or causal independence from shared fits | A+C, scope-limited |
| SI derivation shows approximate Trukhan–MacDonald equality for Debye-like EP with ΔεEP ≫ εR | Algebraic agreement of two model formulas under shared premises | External model validity, equal species diffusion or direct self-diffusion/free-ion population | B |
| Same-group 2013 model audit: Macdonald–Trukhan fits degrade as concentration rises, can overestimate D and underestimate n, and empirical normalization lacks firm theoretical justification | The inversion requires an explicit model-validity uncertainty | Failure of the directly measured σ–τs trend; exact bias in every 2012 sample | C |
| Published tracer/Raman/PFG-NMR/simulation trends noted as inconsistent by the 2012 authors | The p interpretation is method/population dependent | A scope-matched counterexample without identical material, salt, concentration, temperature and observable | C |
| Later rigidity studies report strong decoupling in other polymer families | General plausibility and a broader boundary condition | The specific “packing frustration” mediator or universality | A/C, cross-domain |

## Counterexample candidates and scope contracts

| Candidate | Match result | Classification |
|---|---|---|
| Radiotracer evidence for temperature-dependent carrier concentration ([PRL 93, 125901](https://doi.org/10.1103/PhysRevLett.93.125901)) | Different electrolyte systems and observable; probes labeled-ion transport rather than the same EP inverse problem | Tension, not falsification |
| Raman ion-pair populations | Different population sensitivity and often different formulations; speciation does not directly equal electrode-active carrier density | Tension, not falsification |
| PFG-NMR self-diffusion results | Direct species self-diffusion is valuable, but no retrieved study matches all five 2012 polymers, LiClO4 levels, thermal history and temperature grid | Missing closure experiment |
| 2013 failure analysis of EP models | Same model family and authors; includes a PEI–LiTFSI case at N:Li=400:1, comparable dilution scale but different polymer and salt | Strong model tension; not a W1 counterexample |
| Rigid polymers without enhanced conductivity | Rigidity alone is not the published necessary antecedent; packing, carrier density and morphology differ | Boundary condition only |

No class-D counterexample was found. In particular, the paper's packing account is
a plausible explanation rather than a universal necessary implication. Treating
an unmatched rigid polymer as a falsifier would strengthen the author claim
beyond its wording.

## Observation-equivalent countermodels

The W1 observation is compatible with at least:

1. nearly fixed carrier density and a mobility channel weakly coupled to α
   relaxation;
2. temperature-dependent dissociation that offsets segmental slowdown;
3. correlated cluster motion with a changing Haven/collective factor;
4. local side-chain motion or site-to-site hopping below the α-relaxation scale;
5. packing/free-volume changes;
6. mesoscale morphology or interfacial conduction.

Because σ alone supplies one product-like constraint, these models are not
identified without independent species diffusion, speciation, collective
correlation and structural measurements.

## Lean obligations

| Obligation | Empirical premises | Formal result | Status | Promotion ceiling |
|---|---|---|---|---|
| Conductivity factorization is non-injective | σ can be represented by carrier × charge × mobility in the selected model | Two distinct carrier/mobility pairs give the same σ | Kernel checked | B only; no real mechanism chosen |
| Composite Axis-1 null implies an invariant | p and the collective factor are constant and Dτs is constant | σTτs is constant up to q²/kB | Kernel checked | A conditional prediction; empirical premises remain external |
| Axis-1 violation refutes only the conjunction | σTτs differs between two conditions | Not all of constant p, constant collective factor and constant Dτs can hold together | Kernel checked | Does not identify which premise failed |
| Carrier variation can mimic Axis-1 decoupling | Explicit rational countermodel | Dτs remains constant while σTτs changes | Kernel checked | B: σ/τs alone cannot prove diffusion decoupling |
| Observation-equivalent mechanisms defeat unique identification | Packing and at least one distinct admissible mechanism predict the same admitted observation | The observation cannot have a unique mechanistic preimage | Kernel checked | B only; empirical equivalence remains outside Lean |
| One counterexample refutes a universal implication | The author claim is truly universal and the witness passes every scope term | (P(w)\land\neg Q(w)\Rightarrow\neg\forall x(Px\to Qx)) | Kernel checked | D only after empirical scope validation |
| Local support and a local exception may coexist | Claim is not universal | Existence of one supporting and one failing domain point is logically consistent | Kernel checked | Prevents global overclaim; no empirical verdict |

Source: `formal/PolymerMechanismAudit.lean`; receipt:
`results/polymer_mechanism_lean_receipt.json`.

## Current verdict, missing puzzle and next step

**Current verdict.** The reported conductivity/segmental-relaxation decoupling is
supported for the five named materials at the level of the published plots and
ε estimates. An independent errors-in-variables, held-out predictive comparison
remains pending curve digitization or raw data. The finding rejects a composite
constant-p/constant-H/single-timescale null; it does not by itself prove that
diffusion decouples from segmental relaxation. The fragility association is supported only
qualitatively within a small, non-independent sample; its exact reported R² is
not reproduced by the rounded SI inputs. The D/p partition and packing-frustration
mechanism are non-identifying, with a material model-validity tension. Nothing in
the retrieved record warrants “mechanism falsified.”

**Missing puzzle.** Does a direct, species-resolved diffusion and speciation
measurement preserve the reported temperature-dependent decoupling in the same
samples, and does an independent packing mediator explain residual variation
after carrier concentration and local mobility are controlled?

**Closure experiment.** On identical batches and thermal histories, measure
σ/BDS, PFG-NMR or tracer (D_{Li},D_{anion}), Raman/IR speciation, QENS/local
relaxation and density/free-volume or scattering across the same temperature
grid. Fit a joint uncertainty-aware model before comparing packing, carrier and
mobility pathways. Until then, W1 belongs in the main text; W2–W5 require the
limitations/SI treatment.

## Manuscript-ready figure and table package

The vector schematic `figures/wang2012_evidence_ladder.svg` implements the
case-specific publication figure rather than merely proposing one. Its three
independently renderable panels separate: (a) directly observed σ and τs and the
class-A descriptive conclusion; (b) the Trukhan inversion, its equal-diffusivity,
electrode and normalization assumptions, and the D/p outputs; and (c) the
packing-frustration narrative from observation-equivalent alternatives. No
synthetic or digitized numerical data are shown.

**Proposed caption.** **Figure X | Evidence layers in the Wang et al. polymer-
electrolyte case.** **a,** Broadband dielectric spectroscopy directly supports
the reported conductivity–segmental-relaxation decoupling in the measured
materials. **b,** Diffusivity and mobile-ion fraction are model-derived
quantities whose interpretation depends on a Debye-like electrode-polarization
model, ΔεEP ≫ εR, equal cation/anion diffusivity, electrode assumptions and
constant normalization. **c,** Packing frustration is consistent with the observation but
is not uniquely selected over changes in carrier population, local mobility,
ion correlations or morphology. The audit therefore supports the descriptive
claim, assigns the D/p decomposition to non-identifying/model-tension status,
and finds no scope-matched mechanism falsifier.

The table-ready claim ledger is available as
`evidence/npj_mechanism_audit/derived/wang2012_claim_ledger.csv`; it records claim
type, quantifier, observable, target mechanism, scope, nuisance variables,
verdict and promotion ceiling for every audited proposition.

The predictive Axis-1 theory/model matrix is available as
`evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv`.
