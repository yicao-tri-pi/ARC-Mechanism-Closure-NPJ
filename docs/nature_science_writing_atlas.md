# Nature/Science writing atlas for the mechanism-closure paper

Status: editorial analysis completed 2026-09-22. This is a writing and figure-
architecture reference, not an evidence source for the three case results.

## Selection rule

The comparison set is restricted to Nature Portfolio and Science-family
venues. Papers were selected because they solve at least one of the manuscript's
editorial problems: connecting computation to a physical mechanism, combining
AI with scientific reasoning, separating prediction from understanding, or
turning a materials workflow into a compact figure narrative.

| Paper | Venue | Reusable writing move | Boundary for our paper |
|---|---|---|---|
| Deng et al., [Fundamental investigations on the sodium-ion transport properties of mixed polyanion solid-state battery electrolytes](https://www.nature.com/articles/s41467-022-32190-7) | Nature Communications (2022) | Opens from an unresolved physical variable, moves from local migration units to aggregate transport, and closes with experiment--simulation agreement. Each main figure advances one scale of the causal chain. | Our NASICON result is not an equivalent validation study: it audits a pinned kMC ordering and currently lacks matched experimental closure. |
| Wang et al., [Design principles for NASICON super-ionic conductors](https://www.nature.com/articles/s41467-023-40669-0) | Nature Communications (2023) | Combines a large design space, controlled computation, literature data and synthesis; Fig. 1 joins structure, workflow and search space before presenting performance. | We use this as the positive design-principle contrast. We do not claim our matched-pair audit yields a general NASICON design rule. |
| Han et al., [Sequencing polymers to enable solid-state lithium batteries](https://www.nature.com/articles/s41563-023-01693-z) | Nature Materials (2023) | Uses a design--mechanism--device arc: concept, chemistry, dissociation, transport pathway and cell performance. The abstract states a concrete intervention and a quantitative outcome. | Our polymer section is an inference audit, not a new polymer synthesis or device-performance paper. |
| Cornelio et al., [Combining data and theory for derivable scientific discovery with AI-Descartes](https://www.nature.com/articles/s41467-023-37236-y) | Nature Communications (2023) | Defines the unresolved methodological gap before naming the system; distinguishes empirical fit from derivability; shows the discovery cycle and the implemented subsystem early. | A derivation from axioms is still conditional on the adequacy of those axioms. Our fidelity and empirical-closure gates address this additional boundary. |
| Jung et al., [Machine-guided path sampling to discover mechanisms of molecular self-organization](https://www.nature.com/articles/s43588-023-00428-z) | Nature Computational Science (2023) | Presents an explicit closed learning cycle: trajectories update a quantitative mechanism, which guides new sampling. Results are organized around what each feedback step adds. | Our loop proposes discriminating observations but has not yet completed experimental feedback for every case. |
| Krenn et al., [On scientific understanding with artificial intelligence](https://www.nature.com/articles/s42254-022-00518-3) | Nature Reviews Physics (2022) | Frames the field with a memorable contrast between prediction and understanding, then decomposes understanding into operational dimensions. | We turn that high-level distinction into falsifiable gates for ion-transport studies. |
| Messeri and Crockett, [Artificial intelligence and illusions of understanding in scientific research](https://www.nature.com/articles/s41586-024-07146-0) | Nature (2024) | Leads with a risk created by successful tools, not with tool novelty; the argument is organized around identifiable failure modes. | We avoid a general critique of AI and test bounded failure modes with executable cases. |
| Schmidt and Lipson, [Distilling free-form natural laws from experimental data](https://www.science.org/doi/10.1126/science.1165893) | Science (2009) | A compact problem--method--demonstration narrative: the algorithmic advance is justified by recovery of interpretable laws from observations. | Symbolic recovery alone does not establish mechanistic uniqueness; our paper asks what competing models remain observation-equivalent. |

## Structural pattern extracted from the exemplars

The strongest papers do not begin with a software inventory. They establish a
scientific tension in the first paragraph, state a single intervention in the
second, and make the consequence measurable in the third. Their main figures
form an argument rather than a gallery:

1. **Problem and causal map.** A domain object and a workflow appear together.
2. **First bounded result.** A direct observable demonstrates the gap.
3. **Mechanistic discrimination.** Competing explanations are separated by a
   controlled calculation or measurement.
4. **External or cross-scale closure.** A different observable, experiment or
   device confirms what the earlier inference could not.
5. **Generalization and limits.** The final figure or discussion names the
   design rule and its domain.

Nature-style titles and abstracts also place the scientific object before the
implementation detail. Quantitative results are paired with the domain in which
they hold. Limitations are not hidden in a generic final paragraph; they are
encoded in the result verbs (``is compatible with'', ``does not identify'',
``within the pinned model'') and in figure captions.

## Translation into this manuscript

### Pitch

> Predictive agreement is routinely treated as mechanistic evidence in ion-
> transport research, yet the same observable can be produced by different
> event networks, electrode allocations or correlation structures. We combine
> physics-guided AI hypothesis enumeration, formal countermodels and numerical
> stress tests to make this ambiguity executable. In NASICON and nonlinear
> impedance cases, prospectively frozen gates show that prediction can remain
> adequate while the proposed mechanism or parameter allocation is not
> identified. A polymer-electrolyte audit then localizes the missing observables
> needed to distinguish segmental coupling, carrier population and collective
> correlations. The result is a closure workflow that converts mechanistic
> uncertainty into a specific next measurement without asking formal proof to
> stand in for physics.

### Main-figure logic

| Figure | Narrative job | Current state |
|---|---|---|
| 1 | Scientific workflow and responsibility boundary | Complete schematic |
| 2 | NASICON: finite convergence and an ordering reversal within the pinned kMC model | Complete; empirical closure pending |
| 3 | NLEIS: held-out prediction versus allocation contraction | Complete; external attribution pending |
| 4 | Polymer: observation, inverse model and mechanism are different evidence layers | Complete audit schematic; curve refit and negative-transference execution pending |
| 5 | Cross-case evidence matrix and the missing closure gate | Complete, explicitly includes failed/pending gates |

### Abstract ceiling for the present draft

The present evidence supports two executable non-identifiability results and one
source-grounded mechanism audit. It does **not** yet support the stronger claim
that the full AI-to-empirical-closure cycle has succeeded in all three systems.
Until the experiment roadmap is completed, the abstract must describe the
polymer component as an audit and the cross-case workflow as a tested framework
with prospective closure steps.

