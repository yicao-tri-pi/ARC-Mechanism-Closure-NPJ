# npj Axis-1 progress note — 2026-09-19

## What changed today

The Wang et al. (2012) "decoupling" axis (Axis 1 of the polymer-electrolyte
mechanism audit) was reframed from a verdict ("the descriptive decoupling is
supported") into a forward-predictive nested-model-comparison problem. This
is a strictly tighter formulation, frozen in
`docs/wang2012_axis1_predictive_research_contract.md`.

The core move: decoupling needs an explicit null to decouple *from*. That
null, M0, is the conjunction of three physical premises — constant effective
carrier population `p`, constant collective correlation factor `H`, and
`D·τs = const` — which together predict the falsifiable invariant
`σ·T·τs = const`, i.e. a slope of exactly −1 for `log(σT)` against `log τs`.
The alternative, M1, is a free-slope model with `ε = 1 + β` as the estimand.
Both σ and τs come from the same dielectric fits, so the primary comparison
uses an errors-in-variables loss rather than naively regressing a
shared-variable quantity. Decision criteria (held-out prediction, CI
excluding zero, fit-window/digitization robustness, effect size in
conductivity decades, and explicit scoping of any causal claim to the
composite null rather than to "diffusion decouples from relaxation") are all
pre-specified.

A second, equally important correction: the SI's own reported ε₁ values
(0.75, 0.72, 0.41, 0.16, −0.01 across the five named materials) are a
continuous sequence, not a clean rigid/flexible binary. Treating "rigid vs.
flexible" as two discrete classes overstates what the data show.

Third, reading four competing theoretical papers (Maitra–Heuer PRL 2007;
Webb/Wang/Miller's chemically specific dynamic-bond-percolation model,
Macromolecules 2015; France-Lanord & Grossman's cluster Nernst–Einstein
model, PRL 2019; Fong et al.'s Onsager/distinct-ion-correlation treatment,
Macromolecules 2020) against the theory-model matrix
(`evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv`) surfaced the
real gap: Wang's packing-frustration story is plausible but is not a closed
forward model. No published bridge function connects a packing observable to
the specific relaxation times/site topology, then to `D_Li`, then to `(p,
H)`, then to `σ`. Each competing theory supplies at most one or two links of
that chain with independently measured inputs.

Fourth, a "true closed-loop" experimental design was sketched: identical
batches, one temperature grid, across BDS/EIS, PFG-NMR/tracer, eNMR/
concentration-cell, Raman/NMR speciation, QENS/MD, and PALS/density — enough
independent channels to actually decompose `D`, `p`, and `H` rather than
inferring all three from a single conductivity curve.

## Current status

Existing artifacts: the axis-1 contract itself; the fitter
`scripts/fit_wang_axis1_models.py` (implements M0/M1, AICc, leave-one-out
predictive RMSE; validated only on synthetic data with a known injected
slope, never yet run on real Wang curves); the Lean formalization
`formal/PolymerMechanismAudit.lean` (8 kernel-checked theorems covering the
composite-null invariant, its non-identifying violation, and an explicit
carrier-variation countermodel — checked, but verifies conditional logic
only, not any empirical claim); the verified SI material table with ε₁/ε₂ and
SDs for all five materials; and the completed six-claim ledger with zero
class-D (falsifying) counterexamples found after a scope-matched literature
search.

**Single biggest gap:** no real temperature-resolved σ(T)/τs(T) curve data
(or BDS fit covariance) has been digitized or obtained yet — the input
schema file still contains only a placeholder row. This blocks the actual
per-material M0/M1 refit and is the one item that turns this from a
specified-but-unrun analysis into a completed empirical result.

## Deliverable produced today

`docs/npj_paper_blueprint_v2.md` — a standalone npj-target manuscript
blueprint built around this Axis-1 reframing (distinct from the broader,
existing `docs/npj_paper_blueprint.md`, which covers six audit cases under
one identifiability framework and treats Wang as one compact example). v2
specifies title/abstract options, a five-figure plan with an honest
per-figure data-availability assessment, three tables, a full
done/written-not-run/not-started inventory, and a priority-ordered TODO list
headed by the digitization blocker above.
