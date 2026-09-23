# Linear EIS versus second-harmonic NLEIS evidence map

## Scientific target and boundary

This case separates spectral predictive adequacy from practical identification
of electrode allocation inside a fixed equivalent-circuit family. It does not
claim that NLEIS is uninformative or that the selected circuit is physically
unique.

## Inputs and executable design

- Data upstream: `yuefan98/2nd-NLEIS-manuscripts`, commit
  `859a0c75a64925ce15482069e2622643152c76eb`, MIT license.
- Toolbox upstream: `yuefan98/nleis.py`, commit
  `71e472023fbb6b8fe1d7a06d536469c48f6dbe82`, MIT license.
- All 30 paired public spectra:
  `third_party/2nd-NLEIS-manuscripts/Part II/data/`.
- Frozen study contract: `experiments/nleis_joint_fit_contract_v0.1.json`.
- Audit, fitting, aggregation, and rendering code: `scripts/*nleis*.py` and
  `scripts/figures/render_nleis_joint_fit_figure.py`.

## Raw and processed outputs

- Corpus audit: `results/nleis_public_data_audit_v0.1.json`.
- Full 30-spectrum aggregate, including per-start fit records:
  `results/nleis_joint_fit_v0.1.json`.
- Preserved terminal checkpoint shards: `results/nleis_joint_fit_shards/`.
- Hash binding: `evidence/nleis_joint_fit_v0.1_provenance.json`.
- Figures: `figures/nleis_joint_fit*`.
- Formal statement and historical kernel receipt:
  `formal/ImpedanceParityNonidentifiability.lean` and
  `results/impedance_parity_lean_receipt.json`.

## Result that may be claimed

The 30-spectrum study passed the frozen median held-out-error gate (joint EIS
NRMSE 0.024; joint NLEIS NRMSE 0.116). Twenty-six spectra met the eligibility
rule, but only 3/30 achieved the required allocation-range contraction, below
the frozen 20/30 threshold. Thus good held-out prediction did not establish
practical electrode-allocation identification under this model and multistart
rule. Broadened model families and independent physical constraints remain
required for closure.
