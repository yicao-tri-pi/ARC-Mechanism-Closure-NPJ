#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
upstream_root="${repo_root}/_upstream"
mkdir -p "${upstream_root}"

clone_at_commit() {
  local url="$1"
  local destination="$2"
  local commit="$3"
  if [[ ! -d "${destination}/.git" ]]; then
    git clone --filter=blob:none "${url}" "${destination}"
  fi
  git -C "${destination}" fetch origin "${commit}"
  git -C "${destination}" checkout --detach "${commit}"
}

clone_at_commit \
  https://github.com/caneparesearch/NASICON_KMC_paper_data.git \
  "${upstream_root}/NASICON_KMC_paper_data" \
  69eb10b7c52ddd85e39ebeb882b2e4ea617e7770

clone_at_commit \
  https://github.com/yuefan98/2nd-NLEIS-manuscripts.git \
  "${upstream_root}/2nd-NLEIS-manuscripts" \
  859a0c75a64925ce15482069e2622643152c76eb

clone_at_commit \
  https://github.com/yuefan98/nleis.py.git \
  "${upstream_root}/nleis.py" \
  71e472023fbb6b8fe1d7a06d536469c48f6dbe82

printf '%s\n' "Pinned upstream checkouts are ready under ${upstream_root}."
