# ARC Mechanism Closure — npj Computational Materials

Standalone repository for the Yi-led deep-science paper on mechanism
identifiability in ion-transport research.

## Scientific question

Can AI-assisted mechanism enumeration, automatic formalization, and trusted
verification identify the mechanism space left open by an apparently successful
prediction or fit, and specify the observation needed to close that space?

The planned paper integrates three bounded scientific cases:

1. NASICON kMC: finite simulation, kinetic promotion ceilings, and a bounded
   ordering counterexample;
2. linear EIS versus second-harmonic NLEIS: predictive adequacy versus practical
   electrode-allocation identifiability;
3. polymer negative transference: correlation-aware conditions under which
   immobilized-anion or diffusion-based reasoning does not determine true
   lithium transference.

Lean checks consequences of an encoded scientific model. It does not invent a
physical mechanism or prove that the encoded model describes the world.

## Authoritative documents

- `docs/npj_deep_science_blueprint_v3.md`: paper identity, cases, and gates;
- `docs/claim_evidence_ledger.md`: supported versus prospective claims;
- `docs/experiment_registry.md`: completed, running, and planned experiments;
- `docs/case_ownership_and_overlap.md`: boundary with ARC-SEED/NMI and
  ARC-CM/TMLR;
- `docs/interfaces/scientific_claim_certificate.schema.json`: versioned
  cross-paper data interface;
- `docs/coordination/`: internal Hisa review packet and unsent response draft.

## Repository boundary

This repository has a clean history and is not a fork of
`Some-random/theorem-proving-reasoning`. Scientific artifacts will be imported
only through explicit, hash-recorded provenance. The upstream development
repository remains a historical source for selected NASICON and NLEIS
artifacts; it is not the publication repository for this paper.

The repository is local-only until its matching GitHub repository is created.

