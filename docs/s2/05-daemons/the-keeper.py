#!/usr/bin/env python3
"""
THE KEEPER

Daily lifecycle upkeep. Runs at ~03:00 local.
- Decays confidence on stale pages
- Promotes evergreen candidates
- Lints schema drift, dead links, orphans
- Writes lint-<date>.md report
- Surfaces summary to THE HERALD's queue

Naming convention: THE [ROLE] (Digiquarium pattern).
"""

import os
import json
import time
import yaml
import schedule
import frontmatter
import re
from pathlib import Path
from datetime import datetime, timezone, date, timedelta

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
LOGS = Path(os.environ.get("LOGS_DIR", "/logs"))

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())
RETRIEVAL_CFG = CONFIG["retrieval"]


def days_since(iso_date: str) -> int:
    if not iso_date:
        return 9999
    try:
        d = date.fromisoformat(iso_date[:10])
    except ValueError:
        return 9999
    return (date.today() - d).days


def all_pages():
    for sub in ["sources", "concepts", "entities", "projects", "ideas", "outputs"]:
        d = VAULT / "wiki" / sub
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            yield f


def load(f):
    try:
        return frontmatter.load(f)
    except Exception as e:
        print(f"  ✗ {f.name}: {e}", flush=True)
        return None


def save(f, post):
    f.write_text(frontmatter.dumps(post))


def decay_pass():
    """Drop confidence on stale evergreen pages."""
    decayed = 0
    for f in all_pages():
        post = load(f)
        if post is None:
            continue
        last_reinforced = post.metadata.get("last_reinforced")
        confidence = post.metadata.get("confidence", 0)
        surface_count = post.metadata.get("surface_count", 0)

        if (
            confidence > 0.8
            and days_since(last_reinforced) > 90
            and surface_count == 0
        ):
            post.metadata["confidence"] = 0.6
            post.metadata["updated"] = datetime.now(timezone.utc).isoformat()
            save(f, post)
            decayed += 1

    return decayed


def evergreen_pass():
    """Promote pages that meet evergreen criteria."""
    cfg = RETRIEVAL_CFG["evergreen_threshold"]
    promoted = 0
    for f in all_pages():
        post = load(f)
        if post is None:
            continue
        if post.metadata.get("status") == "evergreen":
            continue
        confidence = post.metadata.get("confidence", 0)
        # Counting reinforcements is a stand-in for now: surface_count + 1 if last_reinforced recent
        reinforcements = post.metadata.get("surface_count", 0)
        last_reinforced = post.metadata.get("last_reinforced")
        if last_reinforced and days_since(last_reinforced) < 60:
            reinforcements += 1

        if (
            confidence >= cfg["confidence"]
            and reinforcements >= cfg["reinforcements"]
        ):
            post.metadata["status"] = "evergreen"
            post.metadata["updated"] = datetime.now(timezone.utc).isoformat()
            save(f, post)
            promoted += 1
    return promoted


def lint_pass():
    """Detect drift. Write report. Don't fix automatically."""
    issues = {
        "schema_violations": [],
        "stale_schema": [],
        "orphans": [],
        "dead_links": [],
        "lexicon_gaps": [],
        "missing_summary": [],
    }
    today = date.today().isoformat()

    # Build index of valid wikilinks (page IDs)
    valid_ids = set()
    for f in all_pages():
        post = load(f)
        if post is None:
            continue
        valid_ids.add(post.metadata.get("id", f.stem))

    # Lexicon terms in vault
    lexicon_path = VAULT / "lexicon.md"
    lexicon_terms = set()
    if lexicon_path.exists():
        # crude: pull "## term" headers + ```yaml term: foo blocks
        text = lexicon_path.read_text()
        for m in re.finditer(r"^## (\w[\w_-]*)$", text, re.MULTILINE):
            lexicon_terms.add(m.group(1))
        for m in re.finditer(r"^term:\s*(\S+)$", text, re.MULTILINE):
            lexicon_terms.add(m.group(1))

    for f in all_pages():
        post = load(f)
        if post is None:
            continue
        rel = str(f.relative_to(VAULT))
        meta = post.metadata
        page_id = meta.get("id", f.stem)

        # Mandatory fields
        for k in ["id", "type", "summary", "created", "updated", "status", "schema_hash"]:
            if not meta.get(k):
                issues["schema_violations"].append(f"{rel}: missing {k}")

        # Schema version
        if meta.get("schema_hash") != "v0.3":
            issues["stale_schema"].append(rel)

        # Empty summary
        if not (meta.get("summary") or "").strip():
            issues["missing_summary"].append(rel)

        # Dead wikilinks
        body = post.content or ""
        for m in re.finditer(r"\[\[([^\]]+)\]\]", body):
            link = m.group(1)
            if link not in valid_ids:
                issues["dead_links"].append(f"{rel}: {link}")

        # Lexicon terms used but not defined
        for term in meta.get("lexicon_terms", []):
            if term not in lexicon_terms:
                issues["lexicon_gaps"].append(f"{rel}: {term}")

        # Orphans (no inbound links, canonical, surface_count zero)
        if (
            meta.get("status") == "canonical"
            and meta.get("surface_count", 0) == 0
            and days_since(meta.get("created", "")) > 30
        ):
            # Check if anyone references this id
            referenced = False
            for f2 in all_pages():
                if f2 == f:
                    continue
                t2 = f2.read_text()
                if f"[[{page_id}]]" in t2:
                    referenced = True
                    break
            if not referenced:
                issues["orphans"].append(rel)

    # Write report
    LOGS.mkdir(parents=True, exist_ok=True)
    report_path = VAULT / "state" / f"lint-{today}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# Lint report — {today}\n"]
    for k, v in issues.items():
        lines.append(f"\n## {k.replace('_',' ')} ({len(v)})\n")
        for item in v[:20]:
            lines.append(f"- {item}")
        if len(v) > 20:
            lines.append(f"- _(+{len(v)-20} more, see logs)_")
    report_path.write_text("\n".join(lines))

    return issues


def write_keeper_summary(decayed: int, promoted: int, issues: dict):
    queue = INDEX / "scout_queue.jsonl"
    queue.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "type": "keeper_summary",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decayed": decayed,
        "promoted_evergreen": promoted,
        "lint_violations": sum(len(v) for v in issues.values()),
        "lint_categories": {k: len(v) for k, v in issues.items()},
    }
    with queue.open("a") as f:
        f.write(json.dumps(summary) + "\n")


def run_keeper():
    print(f"═══ THE KEEPER — run at {datetime.now(timezone.utc).isoformat()} ═══", flush=True)
    decayed = decay_pass()
    print(f"  decayed: {decayed} pages", flush=True)
    promoted = evergreen_pass()
    print(f"  promoted evergreen: {promoted} pages", flush=True)
    issues = lint_pass()
    total_issues = sum(len(v) for v in issues.values())
    print(f"  lint violations: {total_issues}", flush=True)
    write_keeper_summary(decayed, promoted, issues)
    print("  ✓ keeper complete", flush=True)


def main():
    print("═══ THE KEEPER — daemon ═══", flush=True)
    sched = CONFIG["daemons"]["the_keeper"]["schedule"]
    parts = sched.split()
    if len(parts) == 5 and parts[0].isdigit() and parts[1].isdigit():
        time_str = f"{int(parts[1]):02d}:{int(parts[0]):02d}"
        schedule.every().day.at(time_str).do(run_keeper)
        print(f"  Scheduled daily at {time_str}", flush=True)
    else:
        schedule.every(24).hours.do(run_keeper)

    run_keeper()
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
