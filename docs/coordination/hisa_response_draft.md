# Draft response to Hisa

Hisa, thank you for the exceptionally careful audit. The fact that you were
able to reproduce the frozen assets, all 440 Lean and language-only outcomes,
the verifier catches, and the subset analyses is very reassuring. I also agree
with your main interpretation: the present suites establish correct execution
of authored obligations, but their unique- and residual-catch rates are not
intrinsic measurements of verifier capability.

I am adopting the white-box-to-stress shift as the central current result. The
0% false-acceptance rate will be presented as coverage of the authored
white-box obligations, not as evidence of open-world reliability. The increase
to 12.9% under the public-data-grounded synthetic stress construction, together
with the redistribution of unique and residual responsibility, is the more
informative finding.

I am also separating three paper lines more explicitly.

1. ARC-SEED remains the team-led Nature Machine Intelligence paper. My role is
   a bounded co-author contribution around the interface between hypothesis
   generation, formal verification, promotion ceilings, and discriminating
   observations. We are no longer pursuing the Nature Communications
   restructuring as an active paper route.
2. ARC-CM/TMLR is my AI-methodology paper. Its question is how evidence,
   structured checks, domain checks, formal verification, alignment, and a
   constructive critic should be composed, and how their responsibilities
   change across white-box, construction-stress, and temporally sealed regimes.
3. The npj Computational Materials paper is the deep-science line. It will use
   NASICON, NLEIS, and a polymer negative-transference case to study the gap
   between predictive agreement and mechanism identification.

Your comments have also changed how I will describe Lean. Lean does not invent
the physical loophole. The intended pipeline is: a literature- and physics-
grounded hypothesis library defines candidate mechanisms; AI proposes and
structures competing explanations; an automatic formalization step generates
the obligation; an independent fidelity gate checks that the theorem represents
the scientific claim; Lean verifies the encoded consequence or countermodel;
and numerical, domain, or empirical evidence determines whether the witness is
physically meaningful. I will avoid language suggesting that a kernel proof
establishes the truth of a real material mechanism.

We currently have an active, protected RP-001 real-pair run in a separate
working window. It uses the negative-transference literature as a temporally
sealed case. I do not want to reinterpret or modify that run while it is in
progress. Once it finishes, I will first freeze the raw outputs, environment,
stdout/stderr, and hashes; check for outcome leakage; and then request an
independent semantic-fidelity review. Until that review passes, the result will
be described only as a pipeline result.

The same public case may ultimately appear in both TMLR and npj, but with a
strict contribution split. TMLR will use it to study temporal sealing,
certificate derivation, verifier composition, and fidelity. The npj paper will
own the full transport-theory analysis: reference-frame dependence,
Nernst--Einstein assumptions, Onsager cross-correlations, ion clustering,
chain-length and concentration effects, and the relation to the later Dryad
observation. The two papers will not reuse prose, main figures, tables, or the
same headline claim, and the overlap will be disclosed explicitly.

I accept the concrete provenance and wording corrections in your audit. In
particular, I will reconcile the reused-versus-new execution registry, fix the
stale result paths, record the exact Mathlib revision, retain complete Lean
stdout and stderr, remove the missing-module import problem and machine-local
path assumptions, rename the untransformed controls accurately, and replace
claims of retrieval/CAS/forward-model/unit reasoning with descriptions of the
literal predicates actually executed.

I have prepared a versioned ScientificClaimCertificate interface so that the
TMLR paper can evaluate the verification methodology while the npj and SEED
lines can consume the same semantic contract without sharing a mutable
codebase. The interface records claim strength, scope, assumptions, competing
mechanisms, observables and reference frames, temporally legal evidence,
formal obligations and their source-node mappings, fidelity status, verifier
receipts, discriminating observations, and empirical closure status.

For your next review, the most helpful questions would be:

- Are the three manuscript claims and case boundaries sufficiently distinct?
- Does the execution/specification/fidelity separation capture your concern?
- After RP-001 completes, is the outcome isolation genuine?
- Does the Lean target faithfully express the scientific certificate?
- Is the polymer transport mechanism set scientifically complete enough to
  support the npj analysis?
- Does the proposed split use of the negative-transference case avoid duplicate
  publication risk?
- Does every headline claim have substantive evidence rather than generator-
  authored metadata?

I would be very glad to use the walkthrough to review those items. Your offer
to draft a one-page ARC-CM/SEED interface specification is also directly aligned
with this structure; I would appreciate collaborating on it after you have seen
the current certificate schema and the frozen RP-001 output.

