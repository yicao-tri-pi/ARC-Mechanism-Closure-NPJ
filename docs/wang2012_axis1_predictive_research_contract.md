# Wang 2012 Axis 1: predictive research contract

## Why the earlier verdict was insufficient

“The descriptive decoupling is supported” is a verdict, not yet a predictive
scientific proposition. It does not specify which physical assumptions are being
tested, what the model consumes, what it predicts, or what loss determines
failure. The corrected Axis 1 is therefore a nested model-comparison problem.

## Exact research questions

### Primary descriptive question

> For each of the five named Wang materials, and over an explicitly declared
> temperature/relaxation window, does a single-timescale, constant-carrier,
> temperature-invariant-correlation model predict the joint observations
> \(\{\sigma(T),\tau_s(T)\}\) within their uncertainty, or does a free-slope or
> segmented model yield materially better out-of-sample prediction?

This question does not ask whether “packing frustration is true.” It asks whether
a precisely stated null model survives contact with the directly measured
conductivity and relaxation data.

### Mechanism-resolution question

> If the null model fails, which independently measured temperature-dependent
> factor—carrier population, collective ion correlation, local/renewal time,
> path topology, or packing/free volume—predicts the residual conductivity after
> segmental relaxation is accounted for?

### Theory-bridge question

> Can a model map independently measured microscopic inputs to \(D\) and
> \(\sigma\) without calibrating an unconstrained temperature-dependent factor
> to the same conductivity curve it is meant to predict?

## Model M0: the complete-coupling composite null

For material \(i\) and temperature point \(j\), define

\[
\sigma_{ij}=\frac{q^2}{k_B T_{ij}}\,p_{ij}\,H_{ij}\,D_{ij},
\]

where \(p\) is an effective mobile-carrier population and \(H\) is a collective
correlation factor. The scalar Nernst–Einstein treatment used by Wang corresponds
to absorbing or fixing \(H\).

M0 requires all of the following within one material and declared window:

1. \(D_{ij}\tau_{s,ij}=C_i\): one segmental timescale controls diffusion;
2. \(p_{ij}=p_i\): the effective carrier population is temperature invariant;
3. \(H_{ij}=H_i\): the collective correlation factor is temperature invariant;
4. the same species, phase, salt concentration and measurement definition apply
   across the fitted temperature window;
5. no additional parallel conduction channel contributes materially.

These premises imply the directly testable invariant

\[
\boxed{\sigma_{ij}T_{ij}\tau_{s,ij}=A_i}
\qquad
A_i=\frac{q^2p_iH_iC_i}{k_B}.
\]

Equivalently, with \(x_{ij}=\ln\tau_{s,ij}\) and
\(z_{ij}=\ln(\sigma_{ij}T_{ij})\),

\[
M_0:\quad z_{ij}=\alpha_i-x_{ij},
\]

so the predicted slope is exactly \(\beta_i=-1\).

### Inputs, fitted parameter and output

| Item | M0 definition |
|---|---|
| Direct inputs | T, σ(T), τs(T), material identity; uncertainties and covariance from the dielectric fit |
| Fixed physical conditions | polymer architecture, LiClO4 content/O:Li, phase and thermal history |
| Fitted parameter | one material-specific intercept αi; no free slope |
| Predicted output | \(\hat\sigma(T)=\exp(\alpha_i)\tau_s(T)^{-1}/T\) |
| Direct comparison | predicted versus measured σ at every held-out temperature |
| Falsifiable invariant | βi = −1, or equivalently εi = 0 |

M0 is therefore calculable and externally checkable. Its failure rejects the
conjunction of assumptions 1–5. It does not identify which assumption failed.

## Model M1: empirical fractional-coupling alternative

Wang's reported power law can be written without placing τs on both sides of the
regression:

\[
M_1:\quad z_{ij}=\alpha_i+\beta_i x_{ij},
\qquad
\epsilon_i=1+\beta_i.
\]

This is equivalent to

\[
\sigma T\tau_s=A_i\tau_s^{\epsilon_i}.
\]

M1 predicts σ at an unseen temperature from measured τs and fitted
\((\alpha_i,\beta_i)\). It quantifies departure from M0 but is not itself a
microscopic mechanism.

The SI reports \(\epsilon_1=0.75,0.72,0.41,0.16,-0.01\) for
PPEOSt-b-PSt, PPEOSt, PNBCEM, PPEOCL and PPEOMA. This already shows why a binary
rigid/flexible label is too coarse: the appropriate estimand is a continuous
material-specific ε, followed by a descriptive rigid–flexible contrast.

## Primary loss and model comparison

Both σ and τs are fitted from dielectric spectra, and their errors may be
correlated. Regressing \(\ln(\sigma T\tau_s)\) directly on \(\ln\tau_s\) would
also place the same noisy τs on both axes. The primary fit therefore uses
\(z=\ln(\sigma T)\) versus \(x=\ln\tau_s\) with an errors-in-variables loss:

\[
\mathcal L_i(\alpha,\beta)=\frac12\sum_j
\left[
\frac{(z_{ij}-\alpha-\beta x_{ij})^2}
{s^2_{z,ij}+\beta^2s^2_{x,ij}-2\beta c_{xz,ij}}
+\ln\left(s^2_{z,ij}+\beta^2s^2_{x,ij}-2\beta c_{xz,ij}\right)
\right].
\]

If fit covariance is unavailable, digitization and regression uncertainty must
be propagated by bootstrap and the result labeled support-limited.

### Prespecified outputs

- \(\hat\beta_i\), \(\hat\epsilon_i=1+\hat\beta_i\), and uncertainty;
- predicted σ and residual at each temperature;
- AICc and leave-one-temperature-out predictive loss for M0 and M1;
- influence of every point and sensitivity to the declared fit window;
- a segmented alternative M2 only if its breakpoint rule is frozen before
  fitting, to test whether “near Tg” is a genuine regime rather than a selected
  subset;
- descriptive contrast
  \(\Delta\epsilon=\overline\epsilon_{\rm named\ rigid}
  -\overline\epsilon_{\rm named\ flexible}\), without treating five materials as
  a random population sample.

### Decision rule

Axis-1 decoupling is supported for a named material only if:

1. M1 predicts held-out σ better than M0 by the frozen predictive criterion;
2. the ε interval excludes zero and the practical change across the observed τs
   span is reported in conductivity decades;
3. the conclusion is stable to fit-window and digitization/fit-error sensitivity;
4. no single temperature point determines the sign;
5. the claim remains explicitly about the composite M0, unless p, H and D are
   measured independently.

The analysis is retrospective because the published ε values are already known.
Freezing this contract before curve digitization prevents further outcome-driven
changes but does not make the study prospectively blinded.

## Mechanistic alternatives with calculable outputs

| Model | Required inputs | Computed output | Distinguishing prediction | Main gap |
|---|---|---|---|---|
| M0 complete coupling | τs, constant p/H, one calibration constant | σ(T) | β=−1; Dτs, p and H constant | Strong compound null |
| Mp carrier variation | τs, independently measured p(T), constant H, Dτs=C | σ(T) | σTτs follows p(T) while Dτs remains constant | Spectroscopic species fraction may not equal current-carrying p |
| MH correlation variation | τs, species self-D, collective H(T) | σ(T) | self-D may remain coupled while σ/σNE changes | Requires collective transport, not only PFG self-D |
| MDBP dynamic bond percolation | hopping rate, renewal rate, site topology | D(ω,T) or long-time D | decoupling follows renewal/hopping ratio, not necessarily α relaxation | Mapping renewal rate to measured τs is not automatic |
| MMH Maitra–Heuer | τ1 intrachain, τ2 bound-segment/Rouse, τ3 interchain renewal, N, Re², Dcm | DLi(N,T) | for long chains \(D_M\propto(\tau_{12}\tau_3)^{-1/2}\), where \(\tau_{12}^{-1}=\tau_1^{-1}+\tau_2^{-1}\) | Validated for PEO/LiBF4; predicts cation self-D, not full σ |
| MCS-DBP chemically specific DBP | solvation-site distribution, hopping rates, site-refresh rate from short MD | long-time DLi | stiffness and site density can have competing effects | Force-field/chemistry transfer and collective conductivity remain open |
| McNE cluster Nernst–Einstein | cluster populations αij, cluster charges zij, cluster diffusion Dij | \(\sigma_{cNE}=e^2(Vk_BT)^{-1}\sum z_{ij}^2\alpha_{ij}D_{ij}\) | charged-cluster populations can change σ without a single “free-ion fraction” | Cluster identity/lifetime approximation |
| MOnsager collective transport | charge-resolved collective displacement or all Onsager coefficients | exact linear-response σ and transport decomposition | changing distinct correlations can alter σ without changing self-D | Experimentally demanding complete coefficient set |
| Mpack packing-mediated | independent packing/free-volume metric plus a specified map to hopping/renewal parameters | D and then σ | packing must predict residual transport after τs, p and H are controlled | Wang supplies no quantitative bridge equation |

## The central theoretical gap

The packing narrative currently joins three separate theoretical layers:

1. generalized entropy/packing theories map chain structure to fragility or τs;
2. DBP, Maitra–Heuer or solvation-site theories map local and renewal dynamics to
   ion self-diffusion;
3. cluster-NE or Onsager theory maps carrier populations and collective motion to
   conductivity.

Wang does not provide the bridge functions

\[
\text{packing observable}\rightarrow(\tau_1,\tau_3,\text{site topology})
\rightarrow D_{Li}
\rightarrow (L^{ij}\text{ or }H,p)
\rightarrow\sigma.
\]

Consequently, packing frustration is compatible with the observed ε but does
not predict ε from independent inputs. The publishable theoretical result is not
that packing is wrong; it is that the proposed explanation is not a closed
forward model and is observation-equivalent to several models that make different
predictions for Dself, H, p and renewal times.

## Theory papers and their role

- Druger, Nitzan and Ratner introduced dynamic bond percolation, with separate
  hopping and host-renewal times ([DOI 10.1063/1.446144](https://doi.org/10.1063/1.446144)); the frequency-dependent extension is
  [DOI 10.1103/PhysRevB.31.3939](https://doi.org/10.1103/PhysRevB.31.3939).
- Maitra and Heuer derived an explicit three-timescale cation-diffusion model and
  long-chain scaling beyond the simplest DBP expression
  ([DOI 10.1103/PhysRevLett.98.227802](https://doi.org/10.1103/PhysRevLett.98.227802)).
- Webb, Wang and Miller built a chemically specific DBP model from short MD
  solvation-site and hopping statistics
  ([DOI 10.1021/acs.macromol.5b01437](https://doi.org/10.1021/acs.macromol.5b01437)).
- Maitra and Heuer showed that self and distinct ion correlations require more
  information than a static ion-pair fraction
  ([DOI 10.1021/jp711563a](https://doi.org/10.1021/jp711563a)).
- France-Lanord and Grossman formulated cluster Nernst–Einstein conductivity
  ([DOI 10.1103/PhysRevLett.122.136001](https://doi.org/10.1103/PhysRevLett.122.136001)).
- Fong et al. set out the full Onsager decomposition and demonstrate why
  Nernst–Einstein reasoning can fail in polymer electrolytes
  ([DOI 10.1021/acs.macromol.0c02545](https://doi.org/10.1021/acs.macromol.0c02545)).
- Dudowicz, Freed and Douglas predict polymer fragility from molecular structure
  and packing within generalized entropy theory, but do not close the ion-
  transport bridge ([DOI 10.1021/jp053693k](https://doi.org/10.1021/jp053693k)).

## Recommended closure experiment

Use identical batches, temperature grid and thermal history for all modalities:

1. BDS/EIS: σ(T), τs(T), full covariance and electrode-thickness dependence;
2. PFG-NMR or tracer: species-resolved self-diffusion DLi and Danion;
3. electrophoretic NMR/concentration cell plus thermodynamic factor: sufficient
   collective transport information to constrain Onsager coefficients;
4. Raman/IR and quantitative NMR: association/coordination populations, treated
   as separate from effective current-carrying population;
5. QENS/NMR exchange or validated MD: τ1, τ2 and τ3 and their temperature
   scaling;
6. PALS, density, scattering or total-scattering-derived packing metrics;
7. matched polymer pairs that vary rigidity while holding salt, O:Li, Tg range,
   molecular weight and phase as nearly fixed as feasible.

The decisive analysis is whether packing improves out-of-sample prediction of
D or σ after τs, carrier population and collective correlations are included.
If it does not, packing is not falsified globally, but it is not supported as the
mediator in the declared matched domain.
