#!/usr/bin/env python3
"""
THE DEBAISER

Echo-chamber detector + on-demand contrarian panel.
Long-running daemon that reads SCOUT's echo-chamber flags and runs a debaiser
pass on the corpus when triggered. Saves output to wiki/outputs/.

Naming convention: THE [ROLE] (Digiquarium pattern).
"""

import os
import json
import time
import yaml
import frontmatter
from pathlib import Path
from datetime import datetime, timezone

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
LOGS = Path(os.environ.get("LOGS_DIR", "/logs"))
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())
DEBAISER_QUEUE = INDEX / "debaiser_queue.jsonl"
SCOUT_QUEUE = INDEX / "scout_queue.jsonl"


def load_pages_for_topic(topic_id: str):
    """Find pages related to the topic by entity/concept overlap."""
    target = None
    related = []
    for sub in ["sources", "concepts", "entities"]:
        d = VAULT / "wiki" / sub
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            try:
                post = frontmatter.load(f)
                if post.metadata.get("id") == topic_id:
                    target = (f, post)
                else:
                    related.append((f, post))
            except Exception:
                continue

    if not target:
        return None, []

    # Score related by overlap
    target_meta = target[1].metadata
    target_entities = set(target_meta.get("extracted_entities", []))
    target_concepts = set(target_meta.get("extracted_concepts", []))

    scored = []
    for f, post in related:
        score = 0
        score += len(target_entities & set(post.metadata.get("extracted_entities", []))) * 2
        score += len(target_concepts & set(post.metadata.get("extracted_concepts", []))) * 2
        if score > 0:
            scored.append((score, f, post))
    scored.sort(key=lambda x: -x[0])
    return target, [(f, p) for _, f, p in scored[:10]]


def run_debaiser_on(topic_id: str):
    """Run the 5-lens panel on a topic. Without Claude API, write a stub."""
    target, related = load_pages_for_topic(topic_id)
    if not target:
        print(f"  ✗ topic not found: {topic_id}", flush=True)
        return

    target_path, target_post = target
    today = datetime.now(timezone.utc).date().isoformat()

    # Stub output structure when Claude API not available
    body = (
        f"# Debaiser pass — {target_post.metadata.get('id', target_path.stem)}\n\n"
        f"## Confirmer\n_(Local model placeholder — wire to Claude for full panel.)_\n\n"
        f"## Contrarian\n_(Pending Claude integration.)_\n\n"
        f"## Source-skeptic\n_(Pending Claude integration.)_\n\n"
        f"## Bias-watcher\n_(Pending Claude integration.)_\n\n"
        f"## Lens-checker\n_(Pending Claude integration.)_\n\n"
        f"---\n\n## Synthesis\n_Stub synthesis. Configure ANTHROPIC_API_KEY for full output._\n\n"
        f"## Related pages considered\n"
        + "\n".join(f"- [[{p[1].metadata.get('id', p[0].stem)}]]" for p in related[:5])
    )

    out_dir = VAULT / "wiki" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"debaiser-{today}-{target_path.stem}.md"

    fm = {
        "id": f"debaiser-{today}-{target_path.stem}",
        "type": "output",
        "output_type": "debaiser-report",
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "in_response_to": target_post.metadata.get("id", target_path.stem),
        "gear_used": 3,
        "voice": "helpful",
        "sources_cited": [p[1].metadata.get("id") for p in related[:5]],
        "applied": False,
        "ikigai_regions": target_post.metadata.get("ikigai_regions", []),
        "summary": f"Debaiser panel on {target_path.stem}.",
        "status": "canonical",
        "schema_hash": "v0.3",
    }
    post = frontmatter.Post(body, **fm)
    out_path.write_text(frontmatter.dumps(post))
    print(f"  ✓ wrote debaiser report to {out_path.relative_to(VAULT)}", flush=True)


def check_queue():
    """Read debaiser_queue.jsonl for explicit /debaiser invocations."""
    if not DEBAISER_QUEUE.exists():
        return
    requests = []
    with DEBAISER_QUEUE.open() as f:
        for line in f:
            try:
                requests.append(json.loads(line))
            except Exception:
                continue
    DEBAISER_QUEUE.unlink()  # consume
    for r in requests:
        topic = r.get("topic_id")
        if topic:
            run_debaiser_on(topic)


def check_echo_chambers():
    """Read SCOUT's echo_chamber flags and process if auto-trigger enabled."""
    if not SCOUT_QUEUE.exists():
        return
    threshold = CONFIG["daemons"]["the_debaiser"]["auto_trigger_threshold"]
    seen_path = INDEX / "debaiser_seen.json"
    seen = set()
    if seen_path.exists():
        seen = set(json.loads(seen_path.read_text()))

    new_to_process = []
    with SCOUT_QUEUE.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
                if rec.get("type") == "echo_chamber":
                    page_id = rec.get("id")
                    if page_id and page_id not in seen:
                        new_to_process.append(page_id)
                        seen.add(page_id)
            except Exception:
                continue

    for page_id in new_to_process[:3]:  # rate-limit auto-runs
        run_debaiser_on(page_id)

    seen_path.write_text(json.dumps(list(seen)))


def main():
    print("═══ THE DEBAISER — daemon ═══", flush=True)
    while True:
        try:
            check_queue()
            check_echo_chambers()
        except Exception as e:
            print(f"  ✗ debaiser error: {e}", flush=True)
        time.sleep(120)


if __name__ == "__main__":
    main()
