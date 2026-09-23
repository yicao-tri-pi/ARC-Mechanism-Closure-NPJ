# Manuscript package status

Target: npj Computational Materials working draft  
Last evidence integration: 2026-09-22

## Entry points

- `sn-article.tex`: current manuscript.
- `sn-article.pdf`: locally compiled and visually inspected 13-page draft.
- `sn-article-template-original.tex`: untouched Overleaf template snapshot.
- `figures/`: five main-figure assets copied from the evidence repository.

## Evidence state

- NASICON 6,000-pass extension: completed; prospective convergence and
  directional-confirmation gates failed; bounded within-model result.
- EIS/NLEIS 30-spectrum study: completed; held-out error gate passed and
  allocation-contraction rule failed; fixed-circuit result.
- Wang polymer audit: source, formal and implementation layers present;
  empirical curve-level refit pending numerical curves/covariance.
- Negative-transference closure: prospective; no result claimed.
- Independent theorem-to-claim fidelity review: pending for main-text
  scientific promotion.

Orange `PLACEHOLDER` paragraphs in the manuscript are deliberate. They specify
the experiment or review required before a stronger claim can replace them.

## Local build

The verified local build used:

```text
tectonic sn-article.tex --keep-logs --keep-intermediates
```

Generated auxiliary files are excluded from the synchronized package. The PDF
was rendered page-by-page for visual inspection after the final build.

