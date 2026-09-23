# npj Computational Materials deep-science blueprint v3

Status: working blueprint; prospective claims are explicitly marked.

## Paper identity

### Working title

**When Prediction Does Not Identify Mechanism: AI-Assisted Formal Countermodels and Closure Experiments for Ion Transport**

### Scientific question

Can AI-assisted mechanism enumeration, automatic formalization, and trusted
verification identify the mechanism space left open by an apparently successful
prediction or fit, and specify the observation needed to close that space?

The paper is not a theorem-prover benchmark. It is a materials-science study of
mechanism identifiability. Lean checks consequences of an encoded model; it does
not invent a physical mechanism or establish that the encoded model describes
the world.

### Maximum headline claim

> Across three materials-science settings, predictive agreement remains
> compatible with multiple mechanisms. AI-assisted hypothesis enumeration and
> formal countermodel checking expose the assumptions responsible for this
> non-identifiability and specify observations needed for closure.

This sentence must not enter the abstract until all three cases satisfy the
publication gate below.

## Workflow and responsibility boundary

```text
historical evidence and physical knowledge
  -> physical-mechanism hypothesis library
  -> AI-generated candidate mechanisms, competitors, and claim graph
  -> certificate and formal-obligation generation
  -> alignment and independent fidelity review
  -> Lean proof or non-entailment/countermodel check
  -> numerical and domain admissibility checks
  -> constructive critic proposes a discriminating observation
  -> computation, experiment, or temporally later evidence provides closure
```

- The mechanism library defines scientifically admissible possibilities.
- AI proposes and structures candidates; its output is not scientific gold.
- Lean certifies consequences inside the formalization; it does not discover
  new physics.
- Alignment/fidelity review checks that the theorem says what the scientific
  certificate says.
- Numerical and domain verifiers check witness admissibility.
- Empirical closure decides which mechanism survives in the material system.

## Three deep cases

### Case 1: NASICON kMC

Question: does a similar mean local barrier identify aggregate event kinetics or
long-time conductivity?

Existing evidence:

- held-out compositions contain matched mean-barrier configurations with
  different aggregate initial rates;
- the 3,000-pass block failed its prospective study-level closure gate;
- the 6,000-pass amendment still failed full convergence, and the only pair in
  which both runs passed the primary gate reversed the proposed ordering.

Claim ceiling: a bounded counterexample inside the pinned fitted kMC model and
seed; no general law about experimental pellet conductivity.

Closure requirement: converged paired trajectories, event-network and
correlation diagnostics, and matched-temperature experimental validation.

### Case 2: linear EIS versus second-harmonic NLEIS

Question: does good spectral prediction identify electrode allocation or the
underlying mechanism?

Existing evidence:

- the public release supplies 30 paired EIS/NLEIS spectra;
- Lean checks the sum/difference parity countermodel in the declared two-
  electrode model;
- joint fits pass held-out-error gates, but only 3/30 spectra meet the frozen
  practical-identifiability contraction threshold.

Claim ceiling: predictive adequacy inside a fixed circuit family does not imply
practical parameter identification. The result does not show that NLEIS is
uninformative.

Closure requirement: broadened model families, independent refitting,
uncertainty calibration, and physically constrained electrode attribution.

### Case 3: polymer negative transference

Question: when does immobilizing anions, reducing anion self-motion, or obtaining
a high diffusion-based estimate license a claim about the sign or magnitude of
the true lithium transference number?

The hypothesis library must include at least:

- ideal/uncorrelated Nernst--Einstein transport;
- cation--anion cross-correlations;
- anion--anion correlations through the polymer backbone;
- ion pairing and larger ion clusters;
- chain-length and concentration dependence;
- reference-frame dependence of the reported transference number;
- mismatch between self-diffusion proxies and electrophoretic transport.

The pre-outcome certificate may use only evidence legal at the chosen cutoff.
The Bergstrom et al. 2023 paper and Dryad measurements are outcome references:
they may adjudicate mechanism concordance after execution but must never enter
the verifier input.

Success does not require predicting a negative value. A valid early warning may
show that the sign is underdetermined while cross-correlations remain
unconstrained, or identify the correlation-sensitive observable needed for
closure.

Claim ceiling before independent review: prospective scientific case. Any
current RP-001 execution is a pipeline result until its formalization passes an
independent semantic-fidelity audit.

## Relationship to the TMLR paper

The same public case may appear in both papers with non-overlapping scholarly
contributions:

- TMLR evaluates temporal sealing, certificate derivation, verifier composition,
  and fidelity gates.
- This paper owns the full transport-theory analysis, hypothesis space,
  scientific evidence chain, conditional conclusions, and closure analysis.

The papers must not reuse prose, main figures, result tables, or headline
numbers. The later submission must disclose and cite the earlier one. See
`case_ownership_and_overlap.md`.

## Section plan

1. Prediction versus mechanism identification.
2. AI-assisted hypothesis-to-formalization workflow.
3. NASICON: finite simulation and kinetic promotion ceilings.
4. NLEIS: predictive adequacy versus practical identifiability.
5. Polymer transport: correlation-aware conditions for transference claims.
6. Cross-case synthesis of structural, practical, and specification failures.
7. What formal verification establishes---and does not establish.
8. Closure experiments, limitations, and discussion.

## Publication gate

Each case must provide:

- an exact source claim and bounded target;
- an immutable evidence packet and claim-to-source map;
- at least one domain-credible competing mechanism;
- an executable structured or numerical witness;
- a formal obligation derived from the certificate rather than a defect label;
- independent theorem-to-claim fidelity review;
- numerical, experimental, or historical closure evidence;
- a failure-preserving provenance record;
- an explicit statement of what remains unproven.

No three-case headline is allowed if any case is missing one of these items.

