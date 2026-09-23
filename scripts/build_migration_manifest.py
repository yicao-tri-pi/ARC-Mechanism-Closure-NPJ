#!/usr/bin/env python3
"""Build the deterministic inventory for the imported npj evidence package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "provenance/migration_manifest.json"
EXCLUDED_PARTS = {".git", ".pytest_cache", "__pycache__", ".venv", "_upstream"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == OUTPUT:
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        files.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    payload = {
        "schema_version": "arc-npj-migration-manifest-1.0",
        "generated_date": "2026-09-22",
        "source_states": [
            {
                "path": "/Users/yicao/Documents/ARC/ARC-lean/theorem-proving-reasoning",
                "git_commit": "705f3bf9f48a46ec264a57a46e515a434ab3f0f5",
                "scope": "Committed NASICON and NLEIS artifacts; selected polymer artifacts imported from the dirty working-tree snapshot and identified as such in the case documentation.",
            },
            {
                "path": "/Users/yicao/Documents/ARC/ARC-lean/related-work/NASICON_KMC_paper_data",
                "git_commit": "69eb10b7c52ddd85e39ebeb882b2e4ea617e7770",
                "license": "MIT",
            },
            {
                "path": "/Users/yicao/Documents/ARC/ARC-lean/related-work/2nd-NLEIS-manuscripts",
                "git_commit": "859a0c75a64925ce15482069e2622643152c76eb",
                "license": "MIT",
            },
            {
                "path": "/Users/yicao/Documents/ARC/ARC-lean/related-work/nleis.py",
                "git_commit": "71e472023fbb6b8fe1d7a06d536469c48f6dbe82",
                "license": "MIT",
                "scope": "Pinned dependency, not vendored.",
            },
        ],
        "codex_search_policy": "Codex attachments and session logs were searched only to locate canonical artifacts. Conversation logs were not copied because they are not scientific data and may contain private context.",
        "copyright_exclusions": "Publisher PDFs and user-supplied article copies are excluded; DOI, role, and SHA-256 metadata are retained in the polymer evidence manifest.",
        "file_count": len(files),
        "files": files,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
