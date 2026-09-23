# NASICON long-time kMC remote feasibility and budget

Status: SSH smoke test complete. This is an execution-readiness record, not a long-time transport result.

## Platform result

The configured `kozo-dev-yi` host is suitable for CPU kMC: 64 logical CPUs, about 249 GiB total memory, and low load at inspection time. The pinned upstream commit was cloned into an isolated temporary root and a Python 3.10.21 environment was created with the same principal numerical package versions used locally.

One process ran structures 48 and 49 at comp=0.2 and 573 K with a shared seed, one equilibration pass, and three measurement passes. Both gates passed. The complete job used 20.03 seconds wall time and 429,884 KiB maximum resident memory. Each structure attempted 16,384 kMC events and emitted initial/final barrier-rate summaries, instantaneous active-event graph summaries, collective diffusivity, tracer diffusivity, Haven ratio, correlation factor, and Nernst-Einstein conductivity.

The three-pass values are intentionally non-scientific. In particular, structure 49 returned a transient Haven ratio above one, demonstrating that this budget is too short for convergence.

## Input completeness

### Complete for the simulation smoke test

- primitive structure and 8x8x8 event topology;
- 650 initial occupation rows across 13 stored composition parameters;
- fitted KRA and site-energy cluster expansions;
- 6,144-event catalogue and site-to-event update kernel;
- public kMC implementation and initial configurations;
- all ten required input files hash bound in the result;
- nine shared input hashes exactly match the prior held-out scan.

### Missing for a definitive long-time study

- a checkpoint/restart layer and terminal exit manifest for parallel jobs;
- fixed multi-seed and convergence schedules for D_J, D_tracer, Haven ratio, f, and conductivity;
- trajectory-time logging of the barrier distribution rather than only initial/final summaries;
- a periodic-boundary-aware dynamic network/percolation definition; the smoke graph is only an instantaneous occupied-vacant graph;
- frozen rules for negative directional barriers and unstable early-time ratios;
- a pairing verifier for seeds, source rows, temperature, and configuration IDs;
- a failure/retry policy that preserves failed jobs in the denominator.

These are engineering additions around the available model; no new DFT or NEB calculations are required for the proposed kMC confirmation.

## Compute budget from the measured runs

The 30-pass local pilot measured about 40 seconds per structure and projected about 1.1 core-hours per 3,000-pass structure. The completed local production block subsequently measured 1.13-1.20 core-hours per 3,000-pass run (7.02 core-hours across six runs), validating the local extrapolation. The prospective 6,000-pass extension measured 2.33-2.44 core-hours per run (14.27 core-hours total), confirming approximately linear scaling at the longer horizon. The three-pass remote smoke gives a much more conservative naive projection of 2.46-2.81 core-hours because setup and compilation overhead dominate such a short run. Remote planning should therefore use the measured local ranges only as lower references until a longer remote calibration measures host-specific scaling.

| Scope | Approximate runs | Approximate core-hours | Illustrative wall time |
|---|---:|---:|---:|
| Structures 48/49, 5 paired seeds, 573 K | 10 | 11-28 | about 1.1-2.8 h at 10 concurrent jobs |
| One composition, 50 structures, 3 temperatures | 150 | 165-420 | about 5-14 h at 32 concurrent jobs |
| Paper-scale 11 compositions x 50 structures x 3 temperatures | 1,650 | 1,815-4,650 | about 2.4-6.1 days at 32 concurrent jobs |
| Same paper-scale grid with 5 stochastic seeds everywhere | 8,250 | 9,075-23,250 | about 12-30 days at 32 concurrent jobs |

Each measured process used about 0.42 GiB peak memory, so 32 concurrent jobs would require roughly 14 GiB before scheduler and filesystem margin. CPU, not memory, is the primary resource. Barrier/network logging is expected to add 10-30% runtime depending on cadence. Full raw 6,144-event dumps every pass would be wasteful; fixed histograms/quantiles every 10-50 passes plus sparse raw snapshots should keep a selected-pair, five-seed package below roughly 1 GiB.

No dollar estimate is asserted because this host's billing arrangement and instance price are not visible. If the machine is already provisioned, the relevant budget is shared CPU time; otherwise price should be computed from the actual instance contract, not an assumed public on-demand rate.

## Simulation versus experiment

The long-time kMC portion needs only simulation. It can estimate D_J, D_tracer, Haven ratio, f, and bulk Nernst-Einstein conductivity and can test whether matched mean barriers remain separated after trajectory convergence.

Comparison to the published experiment does not require a new wet-lab run if the goal is retrospective consistency with the paper's reported conductivity. The paper reports impedance-derived conductivities at 373, 473, and 573 K and explicitly shows pellet-compacity effects. However, its public data-availability statement points to the computational archive; the repository/Zenodo record does not contain raw impedance spectra. The supplementary PDF supplies plotted/fitted experimental values, not a complete machine-readable raw-EIS replication package.

Therefore:

- **simulation-only claim:** feasible now after adding the logging, checkpoint, convergence, and pairing controls above;
- **retrospective simulation-versus-paper comparison:** feasible using reported/fitted experimental values, with a source-extraction uncertainty and pellet-compacity caveat;
- **new independent physical validation or causal claim about real pellets:** requires new experimental data or access to raw spectra plus density, impurity, grain-boundary, and replicate metadata.

## Recommended next execution gate

The selected pair has now been run under frozen 3,000- and 6,000-pass protocols. The 6,000-pass study still fails its all-run convergence gate, while its only fully converged pair reverses the proposed conductivity ordering. The next justified simulation is therefore not another unversioned length increase. Freeze a broader seed/structure sampling design and an event-network analysis that can distinguish occupancy, connectivity, directional bottlenecks, and correlated-motion explanations. For a physical claim, pair that simulation design with matched-temperature impedance, density, phase-purity, and replicate metadata; otherwise retain the conclusion at the pinned-model level.
