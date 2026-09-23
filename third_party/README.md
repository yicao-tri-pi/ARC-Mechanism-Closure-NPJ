# Third-party data and reproducibility pins

## Included MIT-licensed snapshots

1. `NASICON_KMC_paper_data`
   - source: https://github.com/caneparesearch/NASICON_KMC_paper_data
   - commit: `69eb10b7c52ddd85e39ebeb882b2e4ea617e7770`
   - included: fitted inputs, `kmc/mc_results.h5`, and the two Python model
     modules required by the archived runs
   - license: `third_party/NASICON_KMC_paper_data/LICENSE`
2. `2nd-NLEIS-manuscripts`
   - source: https://github.com/yuefan98/2nd-NLEIS-manuscripts.git
   - commit: `859a0c75a64925ce15482069e2622643152c76eb`
   - included: all 30 paired spectra used by the audit and fit study
   - license: `third_party/2nd-NLEIS-manuscripts/LICENSE`

The fitting toolbox is not vendored because it is a separately maintained
software dependency:

- source: https://github.com/yuefan98/nleis.py.git
- commit: `71e472023fbb6b8fe1d7a06d536469c48f6dbe82`
- license: MIT

The archived execution scripts deliberately verify Git commits. To rerun them,
materialize the pinned checkouts under `_upstream/`:

```bash
bash scripts/bootstrap_upstreams.sh
```

The copies under `third_party/` are immutable evidence snapshots and are
validated by content hashes; they are not a substitute for the Git commit guard
during a scientific rerun.

## Papers and publisher source files

Publisher PDFs for Wang 2012, its supporting information, the 2013
electrode-polarization critique, and Han 2023 are not redistributed here. The
evidence manifest records their DOIs, roles, and hashes so a reviewer can bind
a lawfully obtained copy to the audit. Derived tables and claim ledgers are
included. This avoids silently treating user-supplied or publisher-hosted files
as redistributable source code.
