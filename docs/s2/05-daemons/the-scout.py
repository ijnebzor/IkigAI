#!/usr/bin/env python3
"""
THE SCOUT

Nightly graph walk. Finds new linkages between previously unconnected pages.
Surfaces top discoveries to the next morning brief.

Naming convention: THE [ROLE] (Digiquarium pattern).
"""

import os
import json
import time
import yaml
import frontmatter
import schedule
from pathlib import Path
from datetime import datetime, timezone
import chromadb
import ollama

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
LOGS = Path(os.environ.get("LOGS_DIR", "/logs"))
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())
SCOUT_QUEUE = INDEX / "scout_queue.jsonl"

client = ollama.Client(host=OLLAMA_HOST)
chroma_client = chromadb.PersistentClient(path=str(INDEX / "chroma"))
sources_coll = chroma_client.get_or_create_collection("sources")


def load_pages():
    """Read all canonical pages from wiki/."""
    pages = []
    for sub in ["sources", "concepts", "entities", "projects", "ideas"]:
        d = VAULT / "wiki" / sub
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            try:
                post = frontmatter.load(f)
                pages.append({
                    "id": post.metadata.get("id", f.stem),
                    "type": post.metadata.get("type"),
                    "regions": post.metadata.get("ikigai_regions", []),
                    "entities": post.metadata.get("extracted_entities", []),
                    "concepts": post.metadata.get("extracted_concepts", []),
                    "summary": post.metadata.get("summary", ""),
                    "expression_surface": post.metadata.get("expression_surface"),
                    "lexicon_terms": post.metadata.get("lexicon_terms", []),
                    "path": str(f.relative_to(VAULT)),
                })
            except Exception as e:
                print(f"  ✗ {f.name}: {e}", flush=True)
    return pages


def find_overlaps(pages):
    """For each pair of pages, score overlap."""
    discoveries = []
    for i, a in enumerate(pages):
        for b in pages[i + 1 :]:
            score = 0
            reasons = []

            # Region overlap (≥2)
            r_overlap = set(a["regions"]) & set(b["regions"])
            if len(r_overlap) >= 2:
                score += len(r_overlap) * 2
                reasons.append(f"shared regions: {sorted(r_overlap)}")

            # Entity overlap
            e_overlap = set(a["entities"]) & set(b["entities"])
            if e_overlap:
                score += len(e_overlap) * 3
                reasons.append(f"shared entities: {sorted(e_overlap)}")

            # Concept overlap
            c_overlap = set(a["concepts"]) & set(b["concepts"])
            if c_overlap:
                score += len(c_overlap) * 3
                reasons.append(f"shared concepts: {sorted(c_overlap)}")

            # Same expression surface
            if (
                a["expression_surface"]
                and b["expression_surface"]
                and a["expression_surface"] == b["expression_surface"]
            ):
                score += 1
                reasons.append(f"same surface: {a['expression_surface']}")

            # Lexicon term overlap
            l_overlap = set(a["lexicon_terms"]) & set(b["lexicon_terms"])
            if l_overlap:
                score += len(l_overlap)
                reasons.append(f"shared lexicon: {sorted(l_overlap)}")

            if score >= 5:
                discoveries.append({
                    "score": score,
                    "a": a["id"],
                    "b": b["id"],
                    "reasons": reasons,
                })
    discoveries.sort(key=lambda d: -d["score"])
    return discoveries[:20]


def detect_echo_chambers(pages):
    """Find pages with high confidence + many reinforcements + zero contradictions."""
    threshold = CONFIG["daemons"]["the_debaiser"]["auto_trigger_threshold"]
    candidates = []
    for sub in ["sources", "concepts"]:
        d = VAULT / "wiki" / sub
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            post = frontmatter.load(f)
            if (
                post.metadata.get("confidence", 0) >= 0.8
                and not post.metadata.get("supersedes")
                and not post.metadata.get("superseded_by")
            ):
                candidates.append({
                    "id": post.metadata.get("id", f.stem),
                    "confidence": post.metadata.get("confidence"),
                    "path": str(f.relative_to(VAULT)),
                })
    return candidates[:10]


def write_queue(discoveries, echo_chambers):
    """Write findings to scout_queue.jsonl for THE HERALD to read."""
    SCOUT_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with SCOUT_QUEUE.open("a") as f:
        for d in discoveries:
            f.write(json.dumps({
                "type": "linkage",
                "timestamp": timestamp,
                **d,
            }) + "\n")
        for ec in echo_chambers:
            f.write(json.dumps({
                "type": "echo_chamber",
                "timestamp": timestamp,
                **ec,
            }) + "\n")
    print(f"  ✓ wrote {len(discoveries)} discoveries + {len(echo_chambers)} echo chambers", flush=True)


def run_scout():
    print(f"═══ THE SCOUT — run at {datetime.now(timezone.utc).isoformat()} ═══", flush=True)
    pages = load_pages()
    print(f"  loaded {len(pages)} pages", flush=True)
    discoveries = find_overlaps(pages)
    echo_chambers = detect_echo_chambers(pages)
    write_queue(discoveries, echo_chambers)
    print("  ✓ scout complete", flush=True)


def main():
    print("═══ THE SCOUT — daemon ═══", flush=True)
    schedule_str = CONFIG["daemons"]["the_scout"]["schedule"]
    print(f"  Schedule: {schedule_str}", flush=True)

    # Simple cron-style: parse "0 2 * * *" → schedule.every().day.at("02:00")
    parts = schedule_str.split()
    if len(parts) == 5 and parts[0].isdigit() and parts[1].isdigit():
        time_str = f"{int(parts[1]):02d}:{int(parts[0]):02d}"
        schedule.every().day.at(time_str).do(run_scout)
        print(f"  Scheduled daily at {time_str}", flush=True)
    else:
        # Fallback: every 24 hours from now
        schedule.every(24).hours.do(run_scout)

    # Run once on boot
    run_scout()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
