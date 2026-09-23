# Polymer-electrolyte mechanism audit: evidence manifest

Frozen on 2026-09-19 for the Wang (2012) and Han (2023) case studies. The files in
`sources/` are immutable inputs; `derived/` contains machine-readable summaries
produced by `scripts/audit_polymer_mechanism_cases.py`.

## Canonical sources

| Local file | Public provenance | SHA-256 | Role |
|---|---|---|---|
| `sources/wang2012/wang2012_prl.pdf` | Wang et al., *Phys. Rev. Lett.* 108, 088303 (2012), DOI: [10.1103/PhysRevLett.108.088303](https://doi.org/10.1103/PhysRevLett.108.088303) | `a9da131bd8ce636e45b670ca3e1898343b843765e6e6dee9d5da110228d3af0a` | Primary article supplied by the user |
| `sources/wang2012/wang2012_supporting_information.pdf` | Supporting Information for Wang et al. (2012), supplied by the user from the APS article record | `cdcf9712efff3cb7d3ab500f94a9a7e99a064dfdba3137ffac0eabf1ebaa2413` | Trukhan–MacDonald derivation and Table I material/fit summary |
| `sources/wang2012/wang2013_ep_critique.pdf` | Wang et al., *Phys. Rev. E* 87, 042308 (2013), DOI: [10.1103/PhysRevE.87.042308](https://doi.org/10.1103/PhysRevE.87.042308) | `2070a937967f7fa5fadb1a7e39ee7b5c2bab1b72173afc44cfda8fecb8e441f3` | Same-group validation of the electrode-polarization inference model |
| `sources/han2023/han2023_main.pdf` | Han et al., *Nature Materials* 22, 1423–1430 (2023), DOI: [10.1038/s41563-023-01693-z](https://doi.org/10.1038/s41563-023-01693-z) | `1b17982a2c831d93ce2626f2bd98fc4408d13b246c61c0e9301638a7eaf945dc` | Primary article |
| `sources/han2023/han2023_si.pdf` | Publisher supplementary information for DOI 10.1038/s41563-023-01693-z | `d84aabf65c57aef6ae1b87a5e54afdd5cef26273ad17d17fbfffadf97f5f89e7` | Structures, synthesis, methods, tables and supplementary figures |
| `sources/han2023/han2023_source_data_fig3.xlsx` | Publisher source-data file for Fig. 3 | `6d3407964024149084665774669019241140b7e57b3f8876c49b155348bb5399` | Processed MD/RDF/Raman/NMR/DFT values |
| `sources/han2023/han2023_source_data_fig4.xlsx` | Publisher source-data file for Fig. 4 | `f7ed35e60afbf47abc66043d8a68b8b47b7790182ca3a2aa4a39031456614c68` | Summary values and processed SAXS/DSC traces |
| `sources/han2023/han2023_source_data_fig5.xlsx` | Publisher source-data file for Fig. 5 | `f69a728dd91eea6115b49bc5109223d7752a6d0a8dd995851a668728bdd89f25` | VTF, transference-current and MD-MSD plot data |
| `sources/han2023/han2023_source_data_fig6.xlsx` | Publisher source-data file for Fig. 6 | `9297169c263100d7c055e911f142972944f68604e07a26b2d38b9952a8fe86f` | Cell-cycling plot data |

The APS endpoint initially returned HTTP 401, but the user subsequently supplied
the five-page Supporting Information. Its hash is frozen above. It exposes the
structural table and analytical derivation, but not raw dielectric spectra or
the unrounded regression inputs used for the article's reported R² values.

## Derived artifacts

- `derived/polymer_source_data_audit_v0.1.json`: hashes, workbook inventory and
  field-level audit.
- `derived/han_p8_p10_verified.csv`: P8–P10 values transcribed from the official
  SI and checked against the source-data workbooks where present.
- `derived/han_source_data_inventory.csv`: sheet sizes, populated cells and
  formula counts.
- `derived/wang2012_claim_ledger.csv`: machine-readable claim type, quantifier,
  scope, nuisance, verdict and promotion ceiling for the Wang case.
- `derived/wang2012_counterexample_candidates.csv`: field-by-field scope contract
  for every Wang counterexample candidate; none passes all required terms.
- `derived/wang2012_materials_verified.csv`: Table I material identities, Mw/PDI,
  salt loading, O:Li, Tg, fragility and both decoupling exponents with errors.
- `derived/wang2012_correlation_reanalysis.json`: unweighted OLS check using the
  rounded public Table I values, alongside the article-reported R² values.
- `literature_evidence_register.csv`: primary-source retrieval register with
  material/method scope and A–C classification. No retrieved entry passed the
  class-D scope contract.
- `wang2012_theory_model_matrix.csv`: calculable theory alternatives with their
  independent inputs, model map, output, direct test and unresolved gap.
- `wang_axis1_input_schema.csv`: required schema for direct M0-versus-M1 fitting;
  the included row is explicitly marked as an example and excluded from analysis.

The Han workbooks contain plotted/processed values. They do not contain raw EIS
spectra, Raman fit residuals and replicate spectra, PFG attenuation series, or MD
trajectories/seeds. “Source data available” is therefore not equivalent to raw
measurement or simulation reproducibility.
