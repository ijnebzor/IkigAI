#!/usr/bin/env python3
"""
explode_url_dump.py

Takes a flat text file containing URLs and explodes them into individual
per-URL stub files in inbox/chrome/exploded/, ready for the /understand
pipeline to canonicalise and ingest.

Usage:
    python3 core/scripts/explode_url_dump.py me/inbox/chrome/2026-04-30-phone.md

Behaviour:
  - Reads the input file
  - Extracts every http(s):// URL (regex; handles markdown, raw lists, mixed)
  - Deduplicates within the input
  - Writes one stub per URL to inbox/chrome/exploded/<id>.md
  - Each stub is schema-v0.2 valid, ready for the canonicaliser
  - Idempotent: existing stubs are not overwritten
  - Leaves the original dump in place (audit trail)

Doesn't fetch URLs — that's the canonicaliser's job, with rate limiting
and TinyFish fallback for blocked content.
"""

import re
import sys
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

URL_RE = re.compile(r'https?://[^\s\)>\]"\'`,]+', re.IGNORECASE)


def short_host(url: str) -> str:
    try:
        h = urlparse(url).hostname or "unknown"
        return h.replace("www.", "").replace(".", "-")[:30]
    except Exception:
        return "unknown"


def url_id(url: str, n: int) -> str:
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:6]
    return f"{n:04d}-{short_host(url)}-{h}"


def make_stub(url: str, n: int, source_label: str) -> str:
    today = datetime.now().date().isoformat()
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    return f"""---
id: {today}-{url_id(url, n)}
type: source
created: {now}
updated: {now}

ikigai_regions: []

summary: ""

tags: []

sources_raw:
  - {url}
derived_from: []
supersedes: []
superseded_by: null
confidence: 0.5
last_reinforced: {today}
drivers: []
biases: []

retrieval_score: 0.5
last_surfaced: null
last_used: null
context_modifiers: {{}}
surface_count: 0
use_count: 0

status: inbox
schema_hash: v0.2

source_type: web
source_url: {url}
source_date: {today}
captured_from: {source_label}
extracted_entities: []
extracted_concepts: []
fetched_via: pending
---

# (untitled — pending fetch)

## Summary
> Pending. The canonicaliser will fetch this URL and fill in.

## Raw URL
{url}
"""


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"input file not found: {src}", file=sys.stderr)
        return 1

    text = src.read_text(encoding="utf-8", errors="replace")
    urls = list(dict.fromkeys(URL_RE.findall(text)))

    if not urls:
        print("no URLs found in input", file=sys.stderr)
        return 1

    out_dir = src.parent / "exploded"
    out_dir.mkdir(parents=True, exist_ok=True)

    label = src.parent.name
    written = 0
    skipped = 0
    for n, url in enumerate(urls, start=1):
        path = out_dir / f"{url_id(url, n)}.md"
        if path.exists():
            skipped += 1
            continue
        path.write_text(make_stub(url, n, label), encoding="utf-8")
        written += 1

    print(f"input: {src}")
    print(f"URLs found (deduped within input): {len(urls)}")
    print(f"new stubs written: {written}")
    print(f"already-existed skips: {skipped}")
    print(f"output dir: {out_dir}")
    print()
    print(f"next: run /understand on {out_dir}/*.md")
    print(f"the canonicaliser will then merge any duplicates against existing wiki/sources/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
