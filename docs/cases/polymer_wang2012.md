# Wang 2012 polymer Axis-1 evidence map

## Computable question

For each named polymer and a preregistered temperature/relaxation window, test
the composite fully coupled model

`constant p + constant H + D*tau_s constant => sigma*T*tau_s constant`

against a free-slope model using held-out prediction and an
errors-in-variables likelihood. The exact contract is
`docs/wang2012_axis1_predictive_research_contract.md`.

## Available artifacts

- Claim/evidence and mechanism audits: `docs/wang2012_mechanism_audit.md` and
  `evidence/npj_mechanism_audit/`.
- Competing forward-model matrix:
  `evidence/npj_mechanism_audit/wang2012_theory_model_matrix.csv`.
- Verified rounded SI material table and reported exponents:
  `evidence/npj_mechanism_audit/derived/wang2012_materials_verified.csv`.
- Executable M0/M1 fitter: `scripts/fit_wang_axis1_models.py`.
- Conditional Lean theorems and explicit carrier-change countermodel:
  `formal/PolymerMechanismAudit.lean`.
- Historical kernel receipt: `results/polymer_mechanism_lean_receipt.json`.
- Evidence-ladder figure: `figures/wang2012_evidence_ladder.*`.

These polymer artifacts were imported from an uncommitted research snapshot in
the source worktree. Their exact imported bytes are frozen by the migration
manifest; they are not represented as belonging to source commit `705f3bf`.

## Current evidence and blocker

The paper-reported exponents and multi-decade variation support rejection of
the composite null within the named systems and reported range. They do not
identify whether the failure lies in `D*tau_s`, carrier population, collective
correlation, or an additional transport channel.

The actual per-material curve refit has **not** been run. Public materials do
not provide temperature-resolved numerical `sigma(T)`, `tau_s(T)`, their fit
covariance, and a frozen fit window. The input schema therefore remains a
placeholder, and the synthetic known-slope check validates only software
plumbing. No empirical M0/M1 result should be claimed until digitization or raw
data acquisition is completed under the frozen contract.

Publisher PDFs and the user-supplied copies are intentionally not redistributed
in this repository. Their DOIs, roles, and SHA-256 identifiers remain recorded
in `evidence/npj_mechanism_audit/README.md`.
