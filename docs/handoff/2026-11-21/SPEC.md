# Authority and evidence specification

## Repository authority

- **ARC-lean/** is a directory, not a Git repository. `theorem-proving-reasoning` is a dirty historical prototype with origin `Some-random/theorem-proving-reasoning`; its linked evidence worktree is historical and preserved. Do not push Yi's unpublished work to that third-party origin.
- **ARC-CM-TMLR** (`yicao-tri/ARC-CM-TMLR`, main) is the canonical verifier/methods manuscript and E1–E5 evidence line. PR #12 is already merged. Hand-off PRs and older open evidence PRs are not thereby merged. The local root stays on its SBF experiment branch; a clean handoff worktree holds this change.
- **ARC-SEED** (`TRI-AMDD/ARC-SEED`) is the distinct hypothesis-discovery project. `main` is integration authority; `yicao` is Yi's historical manuscript/evidence branch, not a replacement main. Existing #78 targets main; #77 targets yicao. Dirty R37/NComms work remains preserved for scoped review, not silently promoted. A September decision to freeze SEED is historical advice, not proof the current owner authorized archival.
- **ARC-Mechanism-Closure-NPJ** is the standalone scientific-case paper (NASICON, NLEIS, polymer); do not duplicate TMLR benchmark headlines or SEED hypothesis-generation claims. See the copied overlap policy in registry inputs.
- **ARC-Lean-benchmark** is a superseded public Beyond-PDF pilot. Its archive branch is already marked historical; keep its release surface distinct from CM. Public visibility does not prove release approval.
- Suite core and unrelated projects are outside this write scope.

## Canonical retrieval and data

No existing scientific SQLite database was found in the scoped repository/worktree scan (excluding dependency caches, third-party sources and related-work clones). Scientific source truth remains the versioned result files and task archives. `registry/output/arc_lean_seed_evidence.sqlite` is a **new rebuildable evidence index**, canonical for this handoff's retrieval only. It is not a newly measured scientific results master, and never replaces task-specific raw evidence or the SEED production JSON knowledge bundle. Handoff status lives separately outside this database.

Inputs are exact source snapshots with SHA-256 and original locators. The matrix is an uncommitted campaign snapshot; commits/PR merge do not convert it into independently reviewed scientific evidence. Its raw result locators remain in `matrix_cells` and must be resolved against the preserved original worktree/recovery archive. The index stores native metrics without pooling. Missing, null, HOLD, prospective and review states remain visible.

## Claims and boundaries

- A kernel proof establishes the encoded consequence under premises. Scientific source binding, model adequacy and empirical truth require independent checks.
- The 200 white-box and 240 public-data-grounded stress cohorts are generated/template-bound tasks. Their execution is real; the cohorts are synthetic. Design-dependent verifier catch rates do not estimate natural-science reasoning recall.
- E1–E5 are operationally packaged. E1/E2/E3 remain constructed diagnostics; E4 is source readiness without estimable replay; E5 is underpowered/descriptive. Luna judging is agent-assisted, not human sign-off.
- The latest design×task matrix combines separate evidence tiers and native units, with no common total/ranking. Its old README's 77 measured cells and original E2 smoke HOLD are stale relative to the frozen 134-cell audit and completed typed-v3 follow-up. Retain both protocol histories; do not amend failures away. Typed 8B changes decoder and model jointly.
- Selected real sources, scalar certificate checks and author reference replays are not independent real-world population validation. RP-001 is a selected temporal method trace pending independent semantic fidelity review. NPJ physical conclusions stay within pinned-model/public-data scope.

## Preservation, integration and deployment

Recovery inventory/bundles and every dirty worktree archive are retained at `/Users/yicao/Documents/ARC/internship-handoff-20261121/projects/arc-lean-seed/evidence/recovery/`; the recovery receipt hashes and dry-run/convergence records are outside scientific SQL. No raw data, active campaign, ignored runtime, worktree, automation, or unique branch is deleted. Safe cleanup here means fast-forwarding the unused local main refs to fetched origin/main and creating one scoped handoff branch per publication repository. Existing independent open PRs remain explicit scientific/content decisions, not automatically merged.

SSH BatchMode connectivity to kozo-dev-yi works. Bounded path search did not find an existing named Lean/SEED/CM/NPJ checkout under `/home/yi/Projects`, `/home/yi/worktrees`, or `/home/yi/benchmarks`; this is not global absence proof. Delivery mirrors use a new isolated project path so shared ARC services remain untouched. Mirror equality and PR merge status are recorded separately in external HANDOFF.md/status.json.
