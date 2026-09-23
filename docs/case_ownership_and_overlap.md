# Case ownership and overlap policy

This registry prevents the ARC-SEED/NMI, ARC-CM/TMLR, and npj manuscripts from
promoting the same contribution as multiple headline results.

| Case or result | Headline owner | Permitted elsewhere | Prohibited overlap |
|---|---|---|---|
| ARC-SEED hypothesis-generation benchmark | ARC-SEED/NMI | Interface-level reference in TMLR/npj | Reuse as a personal-paper headline |
| 200-case white-box verifier suite | TMLR | Brief method citation in npj | Re-reporting ablation tables in npj |
| 240-case grounded synthetic stress suite | TMLR | Motivation for verifier composition in npj | Reuse of headline rates or main figures in npj |
| NASICON kMC | npj | Aggregated illustration of a formal-verification endpoint | Full scientific narrative or figures outside npj |
| EIS/NLEIS practical identifiability | npj | Aggregated illustration of a formal-verification endpoint | Full scientific narrative or figures outside npj |
| Negative-transference/RP-001 | Split by question | TMLR: method trace; npj: transport science | Shared prose, figures, result tables, or identical headline claim |

## Negative-transference split

### TMLR contribution

- temporal evidence sealing;
- outcome-leakage prevention;
- certificate-derived formalization;
- verifier-composition and leave-one-out behavior;
- independent fidelity-gate design;
- case-level method trace.

TMLR must not claim discovery of the physical mechanism.

### npj contribution

- literature-grounded transport hypothesis space;
- Nernst--Einstein and Onsager assumption audit;
- correlation, cluster, chain-length, concentration, and reference-frame analysis;
- scientific interpretation of the later measurement;
- mechanism-specific discriminating observations and closure logic.

npj must not repeat the TMLR benchmark ablations.

## Publication practice

- Maintain separate figures, tables, and prose.
- Cite and disclose the related manuscript when either paper is submitted after
  the other is public or under review, according to venue policy.
- Record shared public sources and code separately from paper-specific analysis.
- Treat RP-001 as a pipeline result until independent fidelity review passes.

