# npj paper blueprint v2 — Wang 2012 Axis-1 predictive-model-comparison manuscript

## Why a v2 file instead of editing `npj_paper_blueprint.md` in place

`docs/npj_paper_blueprint.md` is the blueprint for the **broader multi-case
identifiability-audit paper** (OBELiX composition duplicates, Arrhenius
compensating-shift theorem, NASICON kMC, NLEIS parity, Wang 2012, Han 2023,
all under one A–D/five-verdict framework). That paper's Wang section (4.6) is
one compact worked example among six.

Today's reframing (`docs/wang2012_axis1_predictive_research_contract.md`) is
detailed enough — a full nested-model-comparison contract with an
errors-in-variables loss, a falsifiable invariant, and a named theoretical
bridge-function gap — that it now supports its **own, narrower npj-target
manuscript**: a polymer-electrolyte mechanism paper with Wang 2012 as the
empirical spine, not a compact vignette inside the identifiability paper. This
file is that narrower blueprint. It does not replace
`npj_paper_blueprint.md`; that file's section 4.6 and figures 9–10 should
still cite the Wang case as one example in the identifiability paper, and can
link here for the deeper treatment. Which of the two becomes the actual
submission target is Yi's call — this file makes the standalone option
concrete enough to decide from.

## Title / abstract framing options

1. **"When is conductivity–relaxation decoupling a mechanism, and when is it
   a fitted exponent?"** — leads with the M0/M1 nested-model framing;
   foregrounds the falsifiable β=−1 test. Best if the empirical refit on real
   digitized data is completed before submission — this title promises a
   completed statistical result.
2. **"A missing bridge function: why packing-frustration explanations of
   ion-transport decoupling are not yet closed forward models"** — leads with
   the theory gap (three unconnected theoretical layers: packing→relaxation,
   relaxation→D, D→σ). Safer if the empirical refit stays support-limited,
   because the paper's contribution is the audit + bridge-function argument,
   not a new curve fit.
3. **"Decoupling without a diffusion measurement: an identifiability audit of
   polymer-electrolyte transport claims"** — most consistent with the
   existing identifiability-paper vocabulary (A–D evidence classes, five
   verdicts); best if this paper is explicitly positioned as a companion/deep
   dive to `npj_paper_blueprint.md` rather than a fully independent story.

Recommendation: use framing 2 as the primary title. It matches what is
actually deliverable today (a rigorous audit plus a named theoretical gap
plus a concrete closure design) without overpromising a completed empirical
refit that the raw data does not yet support. Framing 1 becomes the title
**only if** Figure 2/3's real-data refit (see below) is completed first.

### Abstract skeleton (framing 2)

- Sentence 1: Decoupling between ionic conductivity and segmental relaxation
  in polymer electrolytes is a reported and mechanistically interesting
  phenomenon, illustrated by Wang et al. (2012, PRL 108, 088303).
- Sentence 2: We reframe the underlying question as a falsifiable nested
  model comparison — a fully-coupled null (M0: σTτs = const, i.e. β=−1)
  against a free-slope alternative (M1: ε=1+β) — rather than a binary
  rigid/flexible label, and show the published exponents (ε₁ =
  0.75/0.72/0.41/0.16/−0.01) already form a continuum, not two clusters.
- Sentence 3: We show the packing-frustration explanation is compatible with
  this pattern but is not a closed forward model: no published bridge
  function connects a packing observable to the multiple relaxation times,
  hopping/renewal statistics, carrier population and collective correlation
  factor that would be needed to predict ε independently.
- Sentence 4: We formalize the logical structure of this gap in Lean 4 (the
  composite-null invariant, its non-identifying violation, and an explicit
  observation-equivalent carrier-variation countermodel) to keep the
  conditional algebra separate from the empirical claim.
- Sentence 5: We specify and propose a matched-sample closed-loop
  measurement design (BDS/EIS, PFG-NMR/tracer, eNMR/concentration cell,
  Raman/NMR speciation, QENS/MD, PALS/density) able to close the bridge, and
  give the falsifiable prediction each competing mechanistic model makes for
  it.

## Section-by-section narrative arc

### 1. Introduction

- Open with the reported phenomenon and why it matters (design rule:
  "decouple conductivity from segmental relaxation to beat the Tg–σ
  trade-off").
- State plainly that "decoupling" as usually stated is underspecified: it
  needs a null model to decouple *from*. Introduce M0 informally.
- Preview the three-part contribution: (i) nested-model reframing with a
  falsifiable invariant; (ii) an audit showing the packing narrative is
  observation-equivalent to several other mechanisms; (iii) a bridge-function
  gap diagnosis plus a concrete closure design.
- State explicitly, near the end of the introduction, which parts of the
  paper are a completed empirical result versus a specified-but-not-yet-run
  analysis (per the epistemic-honesty constraint governing this whole
  project) — do this early so no later section over-claims by omission.

### 2. The reframed predictive question (theory section)

- Reproduce, tightened for a general audience, the M0/M1 definitions,
  errors-in-variables loss, and decision rule from
  `docs/wang2012_axis1_predictive_research_contract.md`.
- State the falsifiable invariant β=−1 (σTτs=const) and why this is a
  stronger, more checkable statement than "σ and τs decouple."
- Introduce ε=1+β as the continuous estimand, explicitly rejecting the
  rigid/flexible binary using the SI's own five values.
- State the mechanism-resolution and theory-bridge questions (already framed
  in the contract) as the paper's second and third-tier questions — this is
  what elevates the paper above a single re-fit.

### 3. Methods

- 3.1 Wang 2012 data provenance: what is public (SI Table I, ε₁/ε₂ with SDs
  for all 5 materials — `evidence/npj_mechanism_audit/derived/wang2012_materials_verified.csv`)
  versus what is not yet extracted (temperature-resolved σ(T), τs(T) points
  and their fit covariances — needed for the per-material M0/M1 refit itself).
- 3.2 Nested model comparison: M0 vs M1 vs a frozen-breakpoint M2; AICc and
  leave-one-temperature-out predictive loss; errors-in-variables likelihood
  when covariance is available, bootstrap otherwise. Cite
  `scripts/fit_wang_axis1_models.py` and state precisely what it has been
  validated on (a synthetic dataset with a known injected slope) versus what
  it has not (the real Wang curves).
- 3.3 Formal verification as a rigor device, not a mechanism prover: describe
  `formal/PolymerMechanismAudit.lean`'s eight kernel-checked theorems (the
  composite-null invariant, its non-identifying violation, the explicit
  carrier-variation countermodel, non-injectivity of σ=n q μ factorization,
  and the universal/local-exception boundary lemmas). State the promotion
  ceiling for each explicitly in-text, not just in supplement — this is the
  paper's main methodological novelty candidate (few if any npj mechanism
  papers ship a machine-checked receipt for their conditional logic).
- 3.4 Scope-matching / literature-closure protocol: the pre-registered fields
  and decision rule from `docs/polymer_mechanism_audit_contract.md`, applied
  to the six counterexample candidates in
  `evidence/npj_mechanism_audit/derived/wang2012_counterexample_candidates.csv`.
- 3.5 Theory matrix construction: how
  `evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv` was built
  (declared scope, inputs, model map, output, main gap per competing model).

### 4. Results

- 4.1 The published ε values form a continuum, not a rigid/flexible binary
  (Figure 3 territory) — supported directly from SI Table I, no new fitting
  required.
- 4.2 M0 is rejected in the composite sense in the named rigid-chain
  materials; state exactly what is and is not shown by this (rejects the
  *conjunction* of Dτs=const, p=const, H=const — does not by itself show
  which failed). This is the paper's core epistemic move, already written up
  narratively in `docs/wang2012_mechanism_audit.md` and
  `docs/polymer_cases_manuscript_handoff.md`; Results should state whether it
  is reporting the **published**-fit version of this claim (available now)
  or the **independently refit** version (pending raw/digitized data).
- 4.3 The D/p decomposition (EP-model-inverted) is non-identifying and in
  tension with the same group's own 2013 model-validity paper (Wang et al.
  2013, PRE 87, 042308) — reuse the audit's W2/W3 rows.
- 4.4 The fragility correlation is qualitatively but not numerically
  reproducible from the rounded public table (R² 0.853/0.837 vs published
  0.80/0.78 for fragility; 0.488/0.502 vs 0.31/0.33 for Tg) — cite
  `evidence/npj_mechanism_audit/derived/wang2012_correlation_reanalysis.json`
  verbatim; this is a small, honest, already-computed result.
- 4.5 The theory-bridge gap: none of the four competing mechanistic papers
  supplies packing-observable → (τ1,τ3,site topology) → D_Li → (p,H) → σ in
  one calibrated chain; each supplies one or two links only. This is the
  paper's most novel results-section claim and is fully supported by the
  existing theory-matrix CSV without requiring new computation.

### 5. Discussion

- What "solid evidence for decoupling" should mean going forward — separate
  the falsifiable statistical claim (β≠−1) from the mechanism claim
  (packing causes it), explicitly warning against conflating the two, which
  is the error the reframing corrects.
- Consequence for the field: continuous ε means fragility-based
  classification into two families understates the real design space; more
  materials on the same curve will not close the bridge-function gap without
  independent D/p/H measurements.
- The closed-loop measurement design (Figure 5) as the paper's testable
  prediction / call-to-action section — state what each of the four
  candidate mechanistic models (Mp, MH, MDBP/MMH/MCSDBP, McNE/MOnsager)
  predicts for the closure experiment's independent D, p, H channels, so the
  proposal is itself falsifiable rather than a generic "more experiments
  needed."
- Explicit limitations: single research group's five materials, small-n
  fragility correlation, no independently obtained raw curves yet, Lean
  receipts verify conditional logic only.

## Figure plan (final structure)

After reading the docs, the user's candidate 5-figure list survives with one
change: the theory-matrix figure (candidate 4) and the closed-loop-design
figure (candidate 5) are kept as proposed, and candidate 1 (conceptual causal
chain) is kept as Figure 1 because it is the figure that makes the "missing
bridge function" argument legible before any data appears. No reordering is
needed; the honest status assessment differs sharply figure-to-figure.

### Figure 1 — Conceptual causal chain and where Wang's data constrains it

- **Panels:** (a) a directed chain: chain packing/free-volume → relaxation
  modes (τ1 intrachain, τ2 bound-segment/Rouse, τ3 interchain renewal, site
  topology) → D_Li → (carrier population p, collective correlation H) → σ.
  Each arrow annotated with which competing model (MMH, MDBP/MCSDBP, McNE,
  MOnsager, Mpack) supplies it. (b) overlay showing which nodes/arrows Wang
  2012's own data actually constrain (σ(T), τs(T) — the two rightmost nodes
  and the arrow between them) versus which are asserted narratively but
  unmeasured (everything left of D_Li).
- **Data/model output needed:** none — this is a schematic derived from
  reading the theory-model matrix and the axis1 contract's "central
  theoretical gap" section, not a data figure.
- **Status:** MISSING (not yet drawn), but fully specifiable now. Everything
  needed to draw it is already written out in
  `docs/wang2012_axis1_predictive_research_contract.md` ("Wang does not
  provide the bridge functions...") and
  `evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv` (the
  `model_map`, `inputs`, `output`, `main_gap` columns for each of the nine
  rows). The existing `figures/wang2012_evidence_ladder.svg` is a related but
  different figure (it separates observation/inversion/mechanism in three
  panels for the identifiability paper) and is a useful visual-style
  reference, not a substitute.
- **How to produce it:** a new vector figure (SVG, consistent with the
  existing `wang2012_evidence_ladder.svg` style) built directly from the
  matrix CSV; no digitization or new computation required. Roughly 1–2 hours
  of diagramming.

### Figure 2 — The empirical core: σT·τs vs T (or log σT vs log τs) per polymer, M0 vs M1, held-out prediction

- **Panels:** one small-multiple panel per material (5 panels) or one
  combined log–log plot with 5 colors: x = log τs(T), y = log(σT); M0 line
  (slope fixed at −1) vs M1 fitted line; leave-one-temperature-out predicted
  points with error bars; residual sub-panel.
- **Data needed:** per-material, per-temperature σ(T) and τs(T) with
  uncertainties/covariance from the BDS fit — i.e., rows conforming to
  `evidence/npj_mechanism_audit/wang_axis1_input_schema.csv`
  (`material,T_K,sigma_s_cm,tau_s_s,primary_window,sigma_log_se,tau_log_se,cov_log_sigma_tau`).
- **Current status: MISSING — this is the single biggest blocker for the
  whole manuscript.** The schema file currently contains only one
  `EXAMPLE_ONLY_DELETE_BEFORE_ANALYSIS` placeholder row
  (`evidence/npj_mechanism_audit/wang_axis1_input_schema.csv`). No real
  temperature-resolved σ(T)/τs(T) curve data has been digitized or obtained
  as raw data from Wang et al. (2012). `scripts/fit_wang_axis1_models.py`
  exists, runs, and has been validated only on synthetic data with a known
  injected slope (per `docs/wang2012_completion_audit.md`, "validates
  implementation plumbing, not the Wang empirical result").
- **How to produce it:** (1) obtain the real curves — either request raw
  data/digitized points from the authors, or digitize Fig. 1–3 of Wang et al.
  (2012) and the SI Arrhenius/decoupling plots using WebPlotDigitizer (a
  manual, per-point extraction from the published PDF figures — legitimate
  but introduces digitization uncertainty that must be propagated, as the
  contract already anticipates via bootstrap when fit covariance is
  unavailable); (2) freeze the "primary window" (near-Tg fitting range) rule
  *before* looking at the digitized values, per the contract's own
  anti-outcome-driven-changes clause; (3) run
  `scripts/fit_wang_axis1_models.py` on the resulting CSV; (4) report the
  errors-in-variables fit if digitization-derived covariance is available,
  otherwise the bootstrap/unweighted mode with that limitation stated in the
  caption.

### Figure 3 — Per-material ε with confidence intervals, ordered by a rigidity/Tg-proxy, showing the continuous structure

- **Panels:** (a) forest-plot style: ε₁ and ε₂ per material with SD error
  bars, ordered by fragility m (or Tg), showing continuum
  0.75→0.72→0.41→0.16→−0.01 rather than two discrete clusters; (b) model
  comparison per material (ΔAICc or held-out log-likelihood, M0 vs M1 vs any
  frozen-breakpoint M2) once Figure 2's data exists.
- **Data needed for panel (a):** ε₁, ε₂ and their SDs per material — **this
  data already exists** in
  `evidence/npj_mechanism_audit/derived/wang2012_materials_verified.csv`
  (columns `epsilon1,epsilon1_sd,epsilon2,epsilon2_sd`, all five materials).
  Panel (a) is buildable **today** with no new data collection.
- **Data needed for panel (b):** the same per-temperature curves as Figure
  2 — MISSING, same blocker.
- **Status:** panel (a) READY NOW; panel (b) blocked on the same raw-data gap
  as Figure 2.
- **How to produce panel (a):** a short plotting script reading
  `wang2012_materials_verified.csv` directly (no script currently exists for
  this specific plot — the closest existing artifact, the correlation
  reanalysis JSON, computes R² but does not plot). This is a same-day task.

### Figure 4 — Theory-model matrix as a figure

- **Panels:** a compatibility/requirement grid: rows = the nine models in
  `wang2012_theory_model_matrix.csv` (M0, M1, MDBP, MDDH, MMH, MCSDBP, MCORR,
  MCNE, MOnsager, MPACK — ten rows including M0/M1 themselves, or exclude
  M0/M1 and keep the eight mechanistic alternatives), columns = {declared
  scope matches Wang's materials?, independent-input status, what it would
  additionally require to be tested against Wang's data, current
  compatible/excluded/untested verdict given the evidence tiers in
  `docs/wang2012_mechanism_audit.md`}.
- **Data needed:** already fully present in
  `evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv` (10 rows ×
  10 columns, including `main_gap` and `relevance_to_wang`).
- **Status:** READY NOW as a table; turning it into a figure (e.g., a
  color-coded grid rather than a CSV/table) is a same-day visualization task,
  not a data-collection task.
- **How to produce it:** direct rendering of the existing CSV into a
  color-coded matrix (green = compatible with current evidence tier, amber =
  untested/needs independent input not yet measured, none currently coded
  red/excluded because no model has been falsified). Consider whether this
  is better shown as Table 3 (see below) rather than a figure — see note in
  Tables section.

### Figure 5 — Proposed closed-loop experimental design (schematic + "what each measurement pins down")

- **Panels:** (a) schematic of the seven proposed measurement modalities
  (BDS/EIS; PFG-NMR/tracer; eNMR/concentration cell + thermodynamic factor;
  Raman/IR + quantitative NMR; QENS/NMR exchange or MD; PALS/density/
  scattering; matched-rigidity polymer pairs) arranged around the same
  causal chain from Figure 1; (b) a table-figure hybrid: rows = measurement,
  columns = {which node/arrow in Figure 1's chain it pins down, what
  independent variable it adds, what each competing mechanistic model
  predicts it will show}.
- **Data needed:** none — this is a proposed design, explicitly framed in
  the contract as future work ("Recommended closure experiment" section of
  `docs/wang2012_axis1_predictive_research_contract.md`).
- **Status:** MISSING as a figure, but fully specified in prose already; a
  same-day diagramming task, and the only figure in the set that is
  deliberately never going to be "data-complete" before submission — it is
  the paper's forward-looking falsifiable-prediction centerpiece, consistent
  with the instruction to frame it as a call-to-action rather than a result.
- **How to produce it:** vector diagram, reusing the Figure 1 chain layout as
  a base; the "what it predicts" column can be populated directly from the
  `distinguishing prediction` column already drafted in the mechanistic-
  alternatives table of the axis1 contract (Mp/MH/MDBP/MMH/MCSDBP/McNE/
  MOnsager rows).

## Tables

- **Table 1 — Per-material data/parameter inventory (Wang 2012 SI).**
  Columns: material, abbreviation, Mw/PDI, LiClO4 wt%, O:Li, Tg, fragility m,
  ε₁±SD, ε₂±SD. **Status: READY NOW** — directly from
  `evidence/npj_mechanism_audit/derived/wang2012_materials_verified.csv`, no
  further work needed beyond Markdown/LaTeX formatting.
- **Table 2 — M0 vs M1 (vs M2) model comparison statistics per material.**
  Columns: material, β̂, ε̂±CI, AICc(M0), AICc(M1), ΔAICc, leave-one-
  temperature-out RMSE(M0 vs M1), fit-window sensitivity flag, digitization-
  uncertainty flag. **Status: MISSING** — same blocker as Figure 2; cannot be
  populated until real σ(T)/τs(T) curves exist. `scripts/fit_wang_axis1_models.py`
  already emits exactly this schema of output (alpha/beta/epsilon/loss/aicc/
  rmse per fit_model call plus a LOO routine) — the script is the direct
  producer of this table once fed real data.
- **Table 3 — Theory-mechanism requirement matrix.** Adapt directly from
  `wang2012_theory_model_matrix.csv`; columns: model, primary source, DOI,
  declared scope, required independent inputs, computed output, direct
  discriminating test, main gap. **Status: READY NOW**, reuse/reformat only.
  (This may replace Figure 4 rather than duplicate it — a single well-
  designed table can carry this content more precisely than a color grid;
  recommend keeping it as Table 3 and dropping Figure 4 as a separate panel,
  or keeping a simplified compatibility-only version as Figure 4 and the full
  detail as Table 3. Author's call at drafting time.)
- **Supplement table — full claim ledger.** Already exists at
  `evidence/npj_mechanism_audit/derived/wang2012_claim_ledger.csv` (6 claims
  W1–W6 with type, quantifier, observable, target, nuisance variables,
  verdict). **Status: READY NOW.**
- **Supplement table — counterexample scope-matching scorecards.** Already
  exists at
  `evidence/npj_mechanism_audit/derived/wang2012_counterexample_candidates.csv`
  (6 candidates). **Status: READY NOW.**

## What we have vs. what's missing — file-by-file inventory

**(a) Done and verified**

- `formal/PolymerMechanismAudit.lean` — 8 theorems, kernel-checked (Lean
  4.33.1), receipt at `results/polymer_mechanism_lean_receipt.json`, return
  code 0. Verifies conditional logic only (composite-null invariant, its
  non-identifying violation, an explicit rational carrier-variation
  countermodel, non-injective conductivity factorization, and
  universal/local-exception boundary lemmas) — does NOT verify any empirical
  claim about real polymers.
- `evidence/npj_mechanism_audit/derived/wang2012_materials_verified.csv` —
  five materials' SI Table I values including ε₁/ε₂ with SDs, checked against
  the supplied SI PDF (hash recorded in
  `docs/wang2012_completion_audit.md`).
- `evidence/npj_mechanism_audit/derived/wang2012_correlation_reanalysis.json`
  — rounded-table R² recomputation, explicitly flagged as not matching the
  article's exact reported R² (honest small-n reproducibility tension).
- `evidence/npj_mechanism_audit/derived/wang2012_claim_ledger.csv` and
  `.../wang2012_counterexample_candidates.csv` — complete, scope-matched, zero
  class-D matches found.
- `figures/wang2012_evidence_ladder.{svg,png}` — existing three-panel
  observation/inversion/mechanism schematic for the identifiability paper;
  usable as a style reference for this paper's Figure 1/5 but not a direct
  substitute.

**(b) Code/specification written, not yet run on real data**

- `scripts/fit_wang_axis1_models.py` — implements M0/M1 fitting, AICc,
  leave-one-out predictive RMSE, and both errors-in-variables and unweighted
  fallback modes. Validated only on synthetic data with a known injected
  slope (smoke test). Has never been run on a real Wang 2012 curve because
  none exists in the repo yet.
- `evidence/npj_mechanism_audit/wang_axis1_input_schema.csv` — schema is
  defined; contains only a placeholder row explicitly named
  `EXAMPLE_ONLY_DELETE_BEFORE_ANALYSIS`.
- `docs/wang2012_axis1_predictive_research_contract.md` — the full forward
  model, loss, decision rule and mechanistic-alternatives table are frozen
  and ready to apply the moment real data exists.

**(c) Not started**

- Digitizing Wang et al. (2012)'s actual σ(T) and τs(T) curves (main text
  Figs. and/or SI Arrhenius/decoupling plots) with per-point uncertainty —
  **the single biggest blocker for the entire manuscript** (blocks Figure 2,
  Figure 3 panel (b), and Table 2 in full).
- Obtaining or estimating BDS fit covariance between σ and τs (needed for the
  errors-in-variables loss to run in its intended mode rather than the
  unweighted/bootstrap fallback).
- Freezing the exact numerical definition of the "near Tg" primary fitting
  window before looking at digitized values (contract requires this to avoid
  outcome-driven window selection).
- Drawing Figure 1, Figure 4/Table 3 rendering, and Figure 5 as actual vector
  graphics (all data-ready, purely a diagramming task).
- Any attempt at the recommended closed-loop experiment itself (PFG-NMR,
  eNMR, Raman/NMR, QENS/MD, PALS) — explicitly future work / call-to-action,
  not a paper blocker, since Figure 5 is designed to be a proposal, not a
  result.

## TODO list (priority order)

1. **[BLOCKING, highest priority] Digitize or otherwise obtain real
   temperature-resolved σ(T) and τs(T) for the five Wang 2012 materials.**
   Why it blocks the paper: without this, Figure 2 and Table 2 cannot exist
   and Figure 3 stays half-finished (panel (a) only); the paper's entire
   empirical core is otherwise just a re-statement of the published ε values.
   How: WebPlotDigitizer on the published main-text/SI figures if raw data
   cannot be obtained from the authors; propagate digitization uncertainty by
   bootstrap per the contract's own fallback clause; record provenance
   (which figure, which axis calibration) for each digitized point.
2. **Freeze the primary-fitting-window rule in writing before touching the
   digitized values.** Why: prevents the exact outcome-driven-selection
   problem the contract was written to avoid; without a frozen rule, any
   fit result is vulnerable to a "why this window" challenge in review. How:
   a short dated addendum to the axis1 contract, committed before running
   the fitter on real numbers.
3. **Run `scripts/fit_wang_axis1_models.py` on the resulting real CSV; record
   whether errors-in-variables mode activates (i.e., whether usable
   sigma_log_se/tau_log_se/cov_log_sigma_tau were recoverable) or whether it
   falls back to unweighted mode.** Why: this produces Table 2 and Figure 2/3b
   directly; also the first real test of whether the fitter's synthetic-data
   validation generalizes. How: existing script, no new code needed unless
   the real CSV reveals an edge case (e.g., fewer than 3 primary-window
   points for a material).
4. **Build the Figure 3(a) forest plot from the already-complete
   `wang2012_materials_verified.csv`.** Why: this is the cheapest and most
   citeable "already-supported" result in the paper and can be produced
   independent of items 1–3. How: a short new plotting script (does not
   exist yet); same-day task.
5. **Draw Figure 1 (causal-chain schematic) and Figure 4/Table 3
   (theory-matrix rendering) directly from
   `wang2012_theory_model_matrix.csv` and the axis1 contract's gap
   discussion.** Why: these carry the paper's most novel non-empirical
   argument (the missing bridge function) and are fully specifiable now,
   independent of the digitization blocker — useful to complete early so
   reviewers see the paper's contribution even if Figure 2/3b lag. How:
   vector diagramming, reusing `wang2012_evidence_ladder.svg`'s visual
   conventions.
6. **Draw Figure 5 (closed-loop design schematic + prediction table-figure).**
   Why: this is the paper's forward-looking centerpiece and, unlike 1–4, has
   no data dependency at all — could be done in parallel with item 1. How:
   vector diagram; predictions column populated directly from the
   mechanistic-alternatives table already in the axis1 contract.
7. **Attempt to obtain independently measured p, H or D for at least one
   Wang 2012 material (literature search for a matched-composition PFG-NMR
   or tracer study), even before running the full closed-loop design.** Why:
   would let the paper report at least one real (rather than purely
   proposed) bridge-function data point in Discussion, strengthening the
   call-to-action framing. How: extend the existing scope-matched literature
   search already documented in `docs/wang2012_mechanism_audit.md`
   ("Counterexample candidates and scope contracts") — note it has already
   searched and found no scope-matched closure; this item is asking to check
   again closer to submission time in case new literature has appeared.
8. **Decide Table 3 vs Figure 4 duplication** (see Tables section) and
   finalize which one carries the theory-matrix detail, to avoid a redundant
   main-text figure and table saying the same thing.
9. **Decide which title/abstract framing (1, 2, or 3 above) to commit to**,
   which is gated on whether item 1 succeeds before the target submission
   window — if the real-data refit is not completed in time, framing 2 is
   the safe choice.

## Style/structural conventions from the four competing-theory papers

Two of the four DOIs resolved to accessible abstracts via `WebFetch`; the
other two (both ACS/Macromolecules) returned HTTP 403 and could not be
fetched — their structural cues below rely only on what is already recorded
in `wang2012_theory_model_matrix.csv` and the axis1 contract, and are marked
as such.

- **Maitra & Heuer, PRL 2007 (10.1103/PhysRevLett.98.227802) — SOURCED via
  WebFetch abstract.** States its forward model in the abstract itself: an
  explicit closed-form expression for the cation diffusion constant D_Li
  invoking Rouse dynamics, whose leading result is a chain-length dependence
  of D_Li checked against experiment "without requiring entanglement
  effects." Structural cue for this paper: lead with the single explicit
  equation for the target observable, then show one discriminating
  comparison against data as the headline result — this is the model this
  npj paper should follow for its own M0/M1 equations in the introduction.
- **France-Lanord & Grossman, PRL 2019 (10.1103/PhysRevLett.122.136001) —
  SOURCED via WebFetch abstract.** States the forward model as a modified
  Nernst–Einstein expression with ionic aggregates as the elementary carrier,
  and leads with a specific counterintuitive experimental fact it explains
  (negative cation transference numbers at high concentration) rather than a
  generic validation. Structural cue: a mechanistic conductivity paper gains
  credibility fastest by explaining one specific, previously puzzling
  published number, which argues for foregrounding the fragility-correlation
  reproducibility check (section 4.4) or a similarly concrete number in this
  paper's own results, not just the abstract ε values.
- **Webb, Wang & Miller, Macromolecules 2015 (10.1021/acs.macromol.5b01437)
  — NOT ACCESSIBLE (HTTP 403); description below is INFERRED from
  `wang2012_theory_model_matrix.csv`'s `model_map`/`output`/`main_gap`
  fields and the axis1 contract's mechanistic-alternatives table, not from
  the paper itself.** Per those secondary sources, it builds a chemically
  specific dynamic-bond-percolation model from short-MD solvation-site and
  hopping statistics, predicting long-time D_Li. Cannot verify its actual
  figure order or exact abstract wording.
- **Fong et al., Macromolecules 2021 (10.1021/acs.macromol.0c02545) — NOT
  ACCESSIBLE (HTTP 403); description below is INFERRED from the same two
  secondary sources.** Per those, it sets out a full Onsager transport-
  coefficient decomposition and argues Nernst–Einstein reasoning can fail in
  polymer electrolytes. Cannot verify its actual figure order or exact
  abstract wording.

General npj Computational Materials / npj-family mechanism-paper convention
(from general familiarity with the venue, not sourced from this search — an
inferred, not verified, convention): such papers typically open Figure 1 with
a schematic of the proposed mechanism/model class before any data, then place
the primary data-model comparison as Figure 2, and reserve a
broader-context/outlook figure for last. This paper's proposed Figure
1→2→3→4→5 order (schematic → core empirical comparison → per-material
structure → competing-theory context → forward-looking design) matches that
convention.
