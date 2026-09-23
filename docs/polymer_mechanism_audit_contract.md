# Polymer-electrolyte mechanism audit: frozen research contract

## Research objective

The target is not “is the proposed mechanism true?” in the abstract. It is:

> For each published proposition, what do the public measurements and declared
> model class directly support, what remains non-identifiable, what constitutes
> a scope-limited tension, and what—if anything—is falsified inside the authors'
> declared material and measurement domain?

The primary estimand is the **logical and empirical closure status of each
minimal proposition**, not a single verdict on a paper.

## Evidence classes and verdicts

| Evidence class | Required showing | Permitted verdict |
|---|---|---|
| A. Descriptive support | The public observation can be traced to a figure/table/data field with units and scope | `supported` for that observation only |
| B. Model-class non-identifiability | At least two admissible parameterizations or mechanisms are observation-equivalent for the measured target | `non-identifying` |
| C. Anomaly or tension | A credible result disagrees with an expectation but fails at least one scope-matching term or rests on a different measurement/model | `tension` or `scope-limited` |
| D. Mechanism counterexample | A declared universal/necessary prediction is violated by a quality-controlled, scope-matched case | `falsified-within-declared-domain` |

`supported` does not mean unique mechanism. `non-identifying` does not mean the
mechanism is false. `tension` does not mean counterexample. `scope-limited` marks
either a bounded positive result or an exception outside the claimed domain.

## Claim decomposition

Every natural-language claim is reduced to one or more of:

1. descriptive equality/ordering/trend;
2. necessary implication, (P\rightarrow Q);
3. sufficient implication;
4. correlation or monotonic association;
5. exclusivity, “only mechanism M can explain O”;
6. possibility/plausibility, “M may explain O.”

Only (2), (3), or (5) can ordinarily be refuted by a counterexample, and only
when the counterexample matches the antecedent and declared domain. A case that
contradicts a possibility narrative merely narrows its plausible scope.

## Scope-matching contract

A candidate counterexample must record and pass the following fields before it
can receive class D:

| Field | Acceptance rule |
|---|---|
| Material class and architecture | Same declared class, or the claim explicitly quantifies over both classes |
| Salt and anion chemistry | Same salt/anion unless the claim is salt-independent |
| Concentration | Same definition and overlapping range; mass fraction, EO:Li and molarity are not silently interchanged |
| Temperature | Overlapping absolute or reduced-temperature interval, with Tg convention recorded |
| Phase/morphology | Comparable amorphous/crystalline/multiphase status and thermal history |
| Protocol | Same observable or a validated conversion between observables |
| Timescale | Comparable frequency, diffusion time and equilibration window |
| Target quantity | Direct/derived status, units, normalization and uncertainty recorded |
| Data quality | Replication, error, exclusions and provenance adequate for the claim strength |

The audit also checks stratification and aggregation (including Simpson's
paradox), measurement mismatch, model-dependent inversions and nuisance
variables. Failure of one term limits the item to class C unless the original
claim explicitly spans that difference.

## Competing-model envelope

The minimum alternative model set is:

\[
\sigma = nq\mu,
\qquad
\sigma = \frac{q^2}{k_BT V}\sum_{ij} z_i z_j D_{ij},
\]

plus segmental coupling, free-carrier/association changes, cluster correlations,
local side-chain mobility, path connectivity/topology, packing/free volume, and
morphology/interface contributions. Observing conductivity alone cannot select
among these decompositions.

## Literature-based closure attempt

This protocol was fixed before classifying the retrieved candidates.

- **Predictions sought:** direct diffusivity and speciation should covary with the
  proposed carrier/mobility mechanism; packing metrics should mediate a claimed
  rigidity effect; sequence effects should persist in chemistry-, concentration-,
  Tg- and phase-matched comparisons; a claimed dominant hop should appear as a
  reproducible path ensemble rather than a single trajectory anecdote.
- **Retrieval:** primary article, official SI/source data, cited validation paper,
  then primary PFG-NMR/tracer/Raman/QENS/BDS/packing and later polymer-electrolyte
  studies using DOI/title/author keyword combinations.
- **Include:** explicit material formulation, temperature, observable, protocol
  and provenance. **Exclude from falsification:** reviews without new data,
  inaccessible numerical basis, e-mail summaries, unmatched salt/phase or
  method-only disagreement.
- **Database fields:** DOI/URL, version, material, architecture, salt,
  concentration definition/value, temperature/Tg, phase, method/timescale,
  observed variable, inferred variable, model, uncertainty, raw/processed data
  level and scope verdict.
- **Decision rule:** class D only if a published universal/necessary proposition
  and all relevant scope terms are matched, data quality is adequate, and the
  predicted consequent fails. Otherwise report A, B or C without promotion.

## Formalization boundary

Lean checks only conditional logic and countermodel construction. It does not
certify Tg equivalence, sample comparability, the conductivity model, or any
empirical mechanism. Each theorem must therefore ship with empirical premises,
formal statement, kernel status and a promotion ceiling.

## Publication gate

A proposition can enter the main text only if its scope, observable/inference
chain, uncertainty, alternative models and verdict are all explicit. Precise
algebra cannot compensate for unmatched materials, missing raw data, or a
model-dependent measurement inversion.
