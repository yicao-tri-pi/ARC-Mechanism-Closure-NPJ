# NASICON kMC evidence map

## Scientific target and boundary

This case asks whether a similar mean local migration barrier identifies the
aggregate event rate or long-time conductivity inside the pinned public kMC
model. It does not make a general claim about experimental pellets.

## Inputs and executable design

- Public upstream: `caneparesearch/NASICON_KMC_paper_data`, commit
  `69eb10b7c52ddd85e39ebeb882b2e4ea617e7770`, MIT license.
- Redistributed input snapshot: `third_party/NASICON_KMC_paper_data/`.
- Discovery and held-out case data: `data/nasicon_barrier_deep_case_v0.1.json`.
- Frozen contracts: `experiments/nasicon_*contract*.json`.
- Execution and aggregation scripts: `scripts/*nasicon*.py`.
- Contract/integrity tests: `tests/test_nasicon_*.py`.

The input snapshot includes the fitted event-model inputs and
`kmc/mc_results.h5`. The original scripts still require a Git checkout at the
pinned commit so that the commit guard remains meaningful; see
`third_party/README.md` for the bootstrap command.

## Raw and processed outputs

- Six 3,000-pass trajectory shards:
  `results/nasicon_production_shards/`.
- Six 6,000-pass amended trajectory shards:
  `results/nasicon_extended_shards/`.
- Execution progress logs: `results/nasicon_*_logs/`.
- Aggregate and sensitivity results: `results/nasicon_*.json`.
- Publication and diagnostic figures: `figures/nasicon_*`.
- Formal statement and historical kernel receipt:
  `formal/NasiconBarrierNonidentifiability.lean` and
  `results/nasicon_barrier_lean_receipt.json`.

## Result that may be claimed

The held-out initial-rate test passed both frozen channels. The subsequent
3,000-pass study completed all six runs but failed its study-level convergence
gate. The 6,000-pass amendment also completed all six runs but only four runs
passed the primary gate. Its paired conductivity ratios were 0.766, 1.094, and
0.604. Seed 155921 was the only pair for which both runs passed the full primary
gate, and it reversed the proposed ordering.

Therefore the admissible result is a bounded ordering counterexample inside
the pinned fitted kMC model and seed, plus a failure-preserving record showing
that the broader conductivity closure gate did not pass. It is not evidence
for a universal opposite ordering or experimental conductivity.
