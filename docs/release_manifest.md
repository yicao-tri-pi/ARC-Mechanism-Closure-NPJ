# npj deep-science release manifest

## Repository identity

- Repository: `ARC-Mechanism-Closure-NPJ`
- Branch: `main`
- Purpose: standalone publication repository for NASICON, NLEIS, and polymer
  negative-transference deep science, isolated from ARC-CM/TMLR.
- Planning provenance: the initial documents were reviewed on local branch
  `paper/npj-deep-science` at commit `79b7072`, which was based on development
  commit `705f3bf9f48a46ec264a57a46e515a434ab3f0f5`. No upstream Git history is
  imported into this repository.

## Current release state

- Blueprint: v3, working.
- Shared certificate interface: v0.1, SHA-256
  `92ed510317c166c591b4346a8c89fb59e568422301eefc95c6db97d7f47de1bd`.
- NASICON and NLEIS evidence: inherited from the base development history and
  subject to a fresh hash audit before manuscript use.
- Polymer/RP-001 result: not imported; protected execution is active in a
  separate ARC-CM worktree.
- Remote: intentionally unset until the matching GitHub repository is created.

## Release blockers

- evidence-hash refresh for all three cases;
- independent formalization-fidelity reviews;
- polymer mechanism-library adjudication;
- explicit overlap disclosure with the TMLR manuscript;
- figure/table ownership audit;
- clean manuscript build and visual review.
