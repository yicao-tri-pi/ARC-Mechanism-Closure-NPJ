# Wang 2012 completion audit

Audited 2026-09-19 against the requested Wang-case deliverables. “Complete” here
means that the requested artifact exists and its bounded claim is verified; it
does not promote missing empirical evidence to mechanism closure.

| Requirement | Authoritative artifact/evidence | Status |
|---|---|---|
| Optimized research question | `docs/npj_paper_blueprint.md`, “Frozen Wang-case research questions” WQ1–WQ5 | Complete |
| Axis-1 forward model, loss and decision rule | `docs/wang2012_axis1_predictive_research_contract.md`; executable `scripts/fit_wang_axis1_models.py` | Contract and fitter complete; empirical refit awaits digitized/raw σ(T), τs(T), covariance and frozen fit window |
| Blueprint adds deductive/literature stress test and five verdicts | `docs/npj_paper_blueprint.md`, auditable objective, literature route, case contract and publication gate | Complete |
| Exact claim decomposition | `evidence/npj_mechanism_audit/derived/wang2012_claim_ledger.csv`, six claims with type, quantifier, observable, mechanism and scope | Complete |
| Measurement/inference chain, assumptions, nuisances and author limitations | Claim ledger fields plus `docs/wang2012_mechanism_audit.md` | Complete |
| Evidence table and provenance | `docs/wang2012_mechanism_audit.md` and `evidence/npj_mechanism_audit/README.md`; main, SI and 2013 validation PDFs hashed | Complete |
| Fragility, packing and EP sub-audits | W2–W5 in claim ledger and narrative audit | Complete within public evidence |
| Scope-matched counterexample search | `wang2012_counterexample_candidates.csv`, six candidates × material/salt/concentration/temperature/phase/protocol/timescale/target/data-quality fields | Complete; zero class-D matches |
| Explicit no-falsifier verdict | Wang audit current verdict and figure panel c | Complete |
| Observation-equivalent countermodels | Six-model list in Wang audit; non-injective/unique-identification Lean theorems | Complete |
| Lean statements and proof boundaries | `formal/PolymerMechanismAudit.lean`; eight kernel-checked theorems, including the Axis-1 composite null and explicit carrier-change countermodel; empirical premises explicitly external | Complete |
| Machine-verifiable Lean receipt | `results/polymer_mechanism_lean_receipt.json`, return code 0, Lean 4.33.1 | Complete |
| Publication-ready table | Machine-readable claim ledger and Markdown claim/evidence tables | Complete |
| Publication-ready figure | `figures/wang2012_evidence_ladder.svg` and `.png`; all three panels independently renderable | Complete |
| Manuscript-ready paragraph/caption/placement | `docs/polymer_cases_manuscript_handoff.md` and final section of Wang audit | Complete |

## Validation record

- Claim ledger: 6 rows × 13 named fields; parsed with Python `csv.DictReader`.
- Counterexample register: 6 rows × 15 named fields; parsed with Python
  `csv.DictReader`.
- SI material table: 5 rows × 12 named fields; parsed with Python
  `csv.DictReader`. The supplied PDF hash is
  `cdcf9712efff3cb7d3ab500f94a9a7e99a064dfdba3137ffac0eabf1ebaa2413`.
- Rounded-table regression check: fragility R² = 0.853/0.837 and Tg R² =
  0.488/0.502, compared with article-reported 0.80/0.78 and 0.31/0.33.
- SVG: XML-valid and visually inspected at original resolution; PNG rendered at
  400 dpi. Figure SHA-256: `ffb847bbfed7e61558eb52de5a008f29c4152544a9d5b7c76fb8fd587a3d14ce`
  (SVG) and `49cbf933169b9988872a18ed8f6756247c22cdf50bf0483ca6ed5e692be1f117`
  (PNG).
- Lean source SHA-256:
  `39c8409049e7363686a58a5a56fdb28dc3b30d9a770bcb6c8ae43d83e226593c`,
  matching the kernel receipt.
- The Axis-1 fitter imports successfully in the project environment
  (`numpy 2.5.3`, `scipy 1.18.1`); a synthetic known-slope smoke test recovers
  the injected fractional-coupling exponent. This validates implementation
  plumbing, not the Wang empirical result.
- `git diff --check` returns no whitespace errors.

## Resolved source gap and residual empirical limitation

The user-supplied five-page SI resolves the earlier HTTP-401 source gap. It
verifies the structures and Table I values and exposes the Debye, equal-mobility
and ΔεEP ≫ εR premises behind the conditional Trukhan–MacDonald equivalence.
The remaining limitation is narrower: raw dielectric spectra and unrounded
regression inputs are not present. Consequently, the article's exact R² values
cannot be reproduced from the rounded public table, while the qualitative
fragility-over-Tg ordering and bounded W1 conclusion remain supported.
