# Han et al. (2023): claim and evidence audit

Primary source and official supplements: [DOI 10.1038/s41563-023-01693-z](https://doi.org/10.1038/s41563-023-01693-z).

## Verified materials and control structure

P8–P10 are all alternating single-ion polymers with PEO side-chain repeat counts
(n=13,17,23), respectively. Their reported values are:

| Polymer | Sequence | PEO n | Tg (°C) | σ at 30 °C (S cm−1) | Li concentration (mol L−1) | Mn,NMR (kDa) |
|---|---:|---:|---:|---:|---:|---:|
| P8 | alternating | 13 | −32 | ((4.2\pm0.5)\times10^{-5}) | 1.18 | 18.3 |
| P9 | alternating | 17 | −31 | ((1.90\pm0.22)\times10^{-5}) | 0.99 | 21.1 |
| P10 | alternating | 23 | −35 | ((9.6\pm1.3)\times10^{-6}) | 0.75 | 24.2 |

Thus P8/P10 conductivity differs by 4.38× over a 4 °C Tg span, while their Li
concentrations differ by 1.57×. The derived σ/cLi ratio differs by 2.78×, but this
is only a diagnostic proxy: it is not a measured mobility and does not remove ion
correlation or density effects.

The experimental alternating polymer P8 and random/block controls were prepared
through different monomer routes (LSM1 + PEO13-VE versus LSM6 + PEOA). Their Tg
and phase behavior are also not identical: the SI reports −32, −40, −36/+16 and
+15 °C for alternating, random, block and homopolymer cases. In simulation, the
alternating/random/block chains instead share an imposed repeat chemistry and
similar Li concentrations (2.56/2.52/2.46 M); the homopolymer has 8.18 M Li.
Accordingly, the simulation is the cleaner sequence contrast among the first
three models, whereas the experiment is the physically realized but more
chemically confounded contrast.

## Claim ledger

| ID | Minimal proposition | Type | Measurement / inference chain | Main nuisances and assumptions | Verdict |
|---|---|---|---|---|---|
| H1 | Sequence/side-chain/tethered-anion design changes conductivity | Descriptive finite-set ordering | synthesis → composition/thermal characterization → EIS/VTF | route, molecular weight, Tg, phase, Li concentration and water history | **supported (A), scope-limited** |
| H2 | Similar Tg entails similar σ | Necessary implication used as a potential explanation, not an author law | Tg and σ | Tg convention and reduced temperature | **refuted as a general entailment by P8–P10; not a sequence falsifier** |
| H3 | Alternation homogenizes Li spatial distribution | Comparative simulation claim | equilibrated MD → density profile/RDF → dispersion metric | force field, finite cell/time, normalization by different means, no seeds | **supported within model; scope-limited** |
| H4 | Alternation reduces aggregation and favors non-aggregated solvation | Multi-modal association claim | Raman deconvolution + 7Li NMR + MD coordination + DFT binding | peak model, concentration, exchange, chemical shift non-uniqueness, model chemistry | **supported directionally; non-identifying** |
| H5 | Alternation enables site-to-site Li migration | Possibility claim, sometimes rhetorically close to causal dominance | selected MD trajectory/snapshots; extra high-field trajectory in SI | trajectory selection, 4 V nm−1 forcing, no event ensemble/seeds | **plausible and model-supported; dominance non-identifying** |
| H6 | Alternating architecture produces much higher conductivity | Descriptive comparison | EIS/VTF | experimental control chemistry/Tg/phase differences | **supported for reported samples; causal attribution scope-limited** |
| H7 | The simulated diffusion ranking is experimentally validated | Cross-method equivalence | MD MSD; PFG-NMR only for P8 and PEO-2 | finite-size/time, force field, PFG fit, missing sequence-control PFG | **not closed; tension/missing evidence** |
| H8 | Bruce–Vincent values near 0.9 are exact Li transference numbers | Model-dependent interpretation | polarization current + impedance → formula | concentrated/associated single-ion electrolyte assumptions and interfaces | **non-identifying as an exact transport decomposition** |

## Public-data audit

The four official source-data workbooks contain no spreadsheet formulas and are
largely plot-ready processed values. They include density/RDF/Raman/NMR/DFT
summaries, SAXS/DSC traces, VTF points, polarization-current traces, MD MSD and
cycling curves. They do not include raw impedance spectra, Raman replicate
spectra and fit residuals, PFG attenuation series, or MD trajectories/seeds.

This supports figure-value traceability but not end-to-end reproduction. In
particular:

- reported errors can be transcribed, but the source does not expose the
  replicate-level EIS values behind every sequence comparison;
- a plotted Raman curve does not expose deconvolution alternatives or covariance;
- a single reported PFG coefficient is not a re-fittable diffusion experiment;
- a trajectory screenshot establishes an event's possibility, not its frequency
  or dominance.

Machine-readable inventories are in
`evidence/npj_mechanism_audit/derived/han_source_data_inventory.csv` and
`han_p8_p10_verified.csv`.

## Evidence table

| Evidence item | Supported conclusion | Remaining alternatives | Class |
|---|---|---|---|
| P8–P10: 4.38× σ range despite a 4 °C Tg span | Tg alone does not identify conductivity, even within the alternating family | Li concentration, side-chain length, local mobility and correlations co-vary | A+B |
| Alternating/random/block/homopolymer σ at 30 °C: (4.2\times10^{-5},3.5\times10^{-6},6.5\times10^{-7},1.6\times10^{-9}) S cm−1 | Large property ordering in the synthesized set | Sequence is not isolated experimentally | A, scope-limited |
| MD density/RDF and coordination statistics | Alternating model has a more even modeled ion environment among matched simulated sequence variants | Force field, finite cell/time and lack of independent seeds | A within model |
| Raman CIP/AGG ratios 2.40/1.30/0.48/0.20, 7Li NMR trend, coordination and DFT energies | Convergent directional evidence that ion association differs | No modality uniquely maps to free-carrier fraction or causal conductivity contribution | A+B |
| A selected site-to-site trajectory and a 4 V nm−1 SI trajectory | The proposed path can occur in the model | Frequency, unbiased kinetics and dominant transport pathway | B |
| Simulated (D_{Li}): 4.0, 2.1, 1.3, 0.25 ×10−9 cm² s−1; PFG only P8/PEO-2 | Order is model-predicted; P8 scale has an experimental anchor | No experimental PFG sequence ranking | C/missing closure |
| Bruce–Vincent values 0.90–0.95 | Similar operational polarization response in the test cells | Exact Onsager transport number and correlation decomposition | B |

## Counterexample candidates and scope contracts

| Candidate | Scope result | Classification |
|---|---|---|
| P8–P10 similar Tg/different σ | Same alternating family and protocol, but PEO length, Li molarity and Mn co-vary | Valid countermodel to “Tg uniquely determines σ”; not a falsifier of sequence mechanism |
| Experimental random/block controls | Same broad SIPE goal but different monomer route, Tg/phase and architecture | Strong property contrast; causal sequence attribution remains scope-limited |
| Simulated alternating/random/block controls | Matched model chemistry and similar Li molarity | Best internal test of the model's sequence effect; still simulation-domain only |
| Homopolymer simulation | Li concentration 8.18 M versus about 2.5 M | Cross-concentration tension; exclude from clean sequence contrast |
| Other sequenced/rigid polymer-electrolyte families | Different backbones, anions, concentrations and morphologies | Boundary evidence, not falsification |

No independent, scope-matched class-D counterexample was found. Nor does the
paper present an exclusivity theorem that only sequence-assisted hopping can
produce the observation.

## Observation-equivalent countermodels

The conductivity enhancement can arise through different combinations of:

1. higher effective carrier population or weaker association;
2. larger local segmental/side-chain mobility at relevant timescales;
3. a better-connected site network or lower hopping barrier;
4. different distinct-ion correlations or cluster populations;
5. phase/morphology and interfacial changes;
6. concentration and composition differences.

The cluster Nernst–Einstein/Onsager form makes explicit why self-diffusion,
conductivity and an operational transference number need not identify the same
mechanism. Independent cluster/correlation observables are needed to close the
decomposition.

## Lean obligations

| Obligation | Empirical premises | Formal result | Status | Promotion ceiling |
|---|---|---|---|---|
| Equal Tg does not entail equal σ | None for the toy theorem; real samples need a tolerance and scope definition | Two toy materials have identical Tg and unequal σ | Kernel checked | Logical non-entailment only; P8–P10 provide approximate empirical illustration |
| σ factorization is non-injective | Chosen factorization is admissible | Distinct carrier/mobility pairs give identical σ | Kernel checked | B only |
| Scoped witness defeats universal necessity | Exact author quantifier plus validated scope match | Constructive negation of the universal implication | Kernel checked | D only after empirical contract passes |
| A local exception does not erase local support | Domain-specific proposition | Supporting and exceptional points coexist | Kernel checked | No global falsification |

## Current verdict, missing puzzle and next step

**Current verdict.** The conductivity enhancement is directly supported for the
reported materials. The public data and simulations support sequence-dependent
ion environments within their respective scopes. They do not uniquely identify
sequence-assisted site-to-site migration as the dominant causal route. P8–P10
are a clean demonstration of Tg non-identification, but not a sequence
counterexample. No mechanism falsification is justified.

**Missing puzzle.** Does the sequence ranking persist when monomer chemistry,
Li concentration, Tg, molecular weight and phase are jointly matched, and is the
same ranking observed in unbiased event statistics, species-resolved diffusion
and collective transport coefficients?

**Closure experiment.** Pre-register a factorial set of alternating/random/block
polymers with matched composition, concentration and thermal history. Measure
replicate EIS, PFG (D_{Li}/D_{anion}), Raman/NMR association, QENS/BDS local
mobility, SAXS/DSC morphology and concentration-cell/Onsager transport. In MD,
publish seeds/trajectories, unbiased hop counts, residence-time distributions and
finite-size uncertainty. Compare models by out-of-sample predictions rather than
by retrospective narrative fit.
