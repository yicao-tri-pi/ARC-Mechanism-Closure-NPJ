# Three-paper review packet for Hisa

Status: internal review draft. No external message has been sent.

## 1. Paper topology

| Line | Ownership | Core claim | Current evidence | Hisa review focus |
|---|---|---|---|---|
| ARC-SEED / NMI | Team-led; Yi contributes a bounded verification interface | Physics-traceable and falsifiable hypothesis generation can be audited before promotion | Team-owned claim graph, traces, benchmarks, and expert-evaluation program | Does the interface improve decisions without absorbing the personal papers? |
| ARC-CM / TMLR | Yi-led methodology | Verifier responsibility depends on execution, obligation specification, and formalization fidelity | Fully reproduced 200-case white-box and 240-case grounded-synthetic suites | Are claims calibrated to what the code reads and executes? |
| npj Computational Materials | Yi-led deep science | Predictive agreement can coexist with multiple mechanisms; formal countermodels expose closure needs | NASICON and NLEIS completed bounded studies; polymer case is prospective | Are the mechanism sets and closure claims scientifically credible? |

Nature Communications is no longer an active manuscript route.

## 2. Repository topology

| Repository / branch | Role | Status |
|---|---|---|
| `ARC-CM-TMLR/main@210cfd4` | Hisa-audited TMLR baseline | GitHub, Overleaf, and local baseline were aligned |
| `ARC-CM-TMLR/experiment/real-pair-end-to-end` | Protected RP-001 execution | Active in another window; do not modify or interpret yet |
| `ARC-Mechanism-Closure-NPJ/main` | New npj source of truth | Clean standalone repository; selected artifacts require hash-recorded import |
| `ARC-SEED/contrib/formal-verification-nmi` | Co-author contribution proposal | Isolated worktree based on current team `origin/main` |
| `ARC-Lean-benchmark@4e8c454` | Historical public pilot | Superseded; not a second active TMLR submission |

## 3. TMLR claim after the audit

The headline is not 0% white-box FAR. It is the redistribution of verifier
responsibility between authored white-box obligations and the grounded
synthetic stress suite:

- portfolio FAR: 0% to 12.9%;
- Lean unique catch: 34.2% to approximately 2.9%;
- Lean residual catch: 100% to 18.2%.

The intended interpretation is construction dependence. The paper will label
literal structured comparisons accurately and will not describe absent live
retrieval, CAS, unit reasoning, or forward simulation as implemented features.

## 4. Negative-transference division

TMLR asks whether a temporally sealed certificate can be constructed and
verified without outcome leakage. Its outputs are method traces, verifier
responsibility, and fidelity status.

npj asks which transport assumptions make the earlier claim underdetermined,
which correlation-aware mechanisms remain possible, and which observation
closes the scientific question. Its outputs are a physical hypothesis space,
formal countermodels, transport analysis, and mechanism-specific closure.

The papers may share public sources but not prose, main figures, tables, or an
identical headline claim.

## 5. Requested review

Please review:

1. the three-paper claim boundary;
2. execution/specification/fidelity separation in TMLR;
3. RP-001 outcome isolation after the protected run completes;
4. theorem-to-certificate semantic fidelity;
5. completeness of the polymer transport mechanism set;
6. duplicate-publication risk in the split use of RP-001;
7. whether every headline has evidence beyond authored metadata.

## 6. Current gates

- RP-001 execution and immutable-output audit are pending.
- Its independent fidelity review is pending.
- The npj polymer mechanism library and evidence packet are prospective.
- The TMLR nine-page rewrite waits until the protected run is complete.
- No response or repository update has been sent or pushed externally from this
  implementation pass.
