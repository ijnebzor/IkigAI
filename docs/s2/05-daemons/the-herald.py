#!/usr/bin/env python3
"""
THE HERALD

Daily morning brief generator. Runs at 07:30 local.
Reads SCOUT discoveries + KEEPER summary + recent activity, calls Claude (or
local Ollama as fallback) to assemble the brief.

Naming convention: THE [ROLE] (Digiquarium pattern).
"""

import os
import json
import time
import yaml
import schedule
import frontmatter
from pathlib import Path
from datetime import datetime, timezone, date, timedelta
from collections import Counter

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
LOGS = Path(os.environ.get("LOGS_DIR", "/logs"))
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())
CLAUDE_MD = (VAULT / "CLAUDE.md").read_text()
IKIGAI_MD = (VAULT / "ikigai.md").read_text()
LEXICON_MD = (VAULT / "lexicon.md").read_text()
BRIEF_PROMPT_PATH = Path("/daemons/prompts/brief.md")
SCOUT_QUEUE = INDEX / "scout_queue.jsonl"


def load_brief_prompt():
    """Try to read brief.md from /daemons/prompts/ if mounted; else use embedded."""
    if BRIEF_PROMPT_PATH.exists():
        return BRIEF_PROMPT_PATH.read_text()
    return (
        "You are THE HERALD. Generate today's morning brief in the user's voice. "
        "Lead with region overlap state. Surface 1-3 SCOUT discoveries if useful. "
        "Recommend one option with reasoning, including a calendar slot offer. "
        "Format as markdown."
    )


def recent_activity_summary():
    """Last 7 days region distribution."""
    cutoff = date.today() - timedelta(days=7)
    region_counter = Counter()
    pages_count = 0

    for sub in ["sources", "ideas", "outputs"]:
        d = VAULT / "wiki" / sub
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            try:
                post = frontmatter.load(f)
                created = post.metadata.get("created", "")
                if not created:
                    continue
                created_date = date.fromisoformat(created[:10])
                if created_date >= cutoff:
                    pages_count += 1
                    for r in post.metadata.get("ikigai_regions", []):
                        region_counter[r] += 1
            except Exception:
                continue

    return {
        "pages_last_7d": pages_count,
        "region_distribution": dict(region_counter),
    }


def active_projects():
    """Pages with type=project, status=active."""
    proj_dir = VAULT / "wiki" / "projects"
    if not proj_dir.exists():
        return []
    out = []
    for f in proj_dir.glob("*.md"):
        try:
            post = frontmatter.load(f)
            if post.metadata.get("project_status") == "active":
                out.append({
                    "id": post.metadata.get("id", f.stem),
                    "title": (post.content or "").split("\n")[0].lstrip("# ").strip()[:80],
                    "regions": post.metadata.get("ikigai_regions", []),
                })
        except Exception:
            continue
    return out


def read_scout_queue():
    """Read latest SCOUT and KEEPER outputs from queue."""
    if not SCOUT_QUEUE.exists():
        return [], None, []
    discoveries, echo_chambers = [], []
    keeper_summary = None
    cutoff = datetime.now(timezone.utc) - timedelta(hours=36)
    with SCOUT_QUEUE.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
                ts = datetime.fromisoformat(rec.get("timestamp", "").replace("Z", "+00:00"))
                if ts < cutoff:
                    continue
                if rec.get("type") == "linkage":
                    discoveries.append(rec)
                elif rec.get("type") == "echo_chamber":
                    echo_chambers.append(rec)
                elif rec.get("type") == "keeper_summary":
                    keeper_summary = rec
            except Exception:
                continue
    discoveries.sort(key=lambda d: -d.get("score", 0))
    return discoveries[:3], keeper_summary, echo_chambers[:3]


def assemble_brief():
    today = date.today().isoformat()
    activity = recent_activity_summary()
    projects = active_projects()
    discoveries, keeper, echo_chambers = read_scout_queue()
    voice = CONFIG["voice"]["morning_brief"]

    lines = [f"# Brief — {datetime.now().strftime('%A, %d %B %Y')}\n"]

    # Region state
    lines.append("\n## Where you've been compounding\n")
    if activity["region_distribution"]:
        sorted_regs = sorted(activity["region_distribution"].items(), key=lambda x: -x[1])
        lines.append("This week's heaviest fills:")
        for r, c in sorted_regs[:6]:
            lines.append(f"- **{r.replace('_', ' ')}**: {c}")
        all_axes = {"love", "good_at", "world_needs", "paid_for"}
        quiet = all_axes - set(activity["region_distribution"].keys())
        if quiet and sum(activity["region_distribution"].values()) >= 3:
            lines.append(f"\nQuiet axes: {', '.join(sorted(quiet))}. Drift, or correct alignment?")
    else:
        lines.append("No activity in the last 7 days.")

    # Active projects + recommendation
    lines.append("\n\n## Build options today\n")
    if projects:
        for p in projects[:3]:
            regs = ", ".join(p["regions"][:4])
            lines.append(f"- **{p['title']}** — regions: {regs}")
        lines.append(f"\n**Recommendation:** see active projects above. Pick one whose region matches a quiet axis if drift correction matters this week.")
    else:
        lines.append("No active project pages yet. Capture one or run `/onboard` to seed.")

    # Discoveries
    if discoveries:
        lines.append("\n\n## Worth noticing\n")
        for d in discoveries:
            lines.append(f"- New linkage: [[{d['a']}]] ↔ [[{d['b']}]] — {'; '.join(d.get('reasons', [])[:2])}")
        if echo_chambers:
            for ec in echo_chambers[:1]:
                lines.append(f"- Echo chamber forming on [[{ec['id']}]] (confidence {ec['confidence']}). Consider /debaiser.")

    # Keeper summary
    if keeper:
        lines.append("\n\n## Maintenance\n")
        if keeper.get("decayed", 0):
            lines.append(f"- {keeper['decayed']} pages decayed (stale evergreen)")
        if keeper.get("promoted_evergreen", 0):
            lines.append(f"- {keeper['promoted_evergreen']} pages promoted to evergreen")
        if keeper.get("lint_violations", 0):
            lines.append(f"- {keeper['lint_violations']} lint issues — see latest state/lint-*.md")

    # Voice signoff
    lines.append("\n\n---\n")
    if voice == "ijneb-dev":
        lines.append("Drop new captures whenever — I'll have tomorrow's discoveries ready by morning.")
    elif voice == "roasty":
        lines.append("Don't drift. The plan was the plan. Get on it.")
    elif voice == "accountantability":
        lines.append("Brief delivered. No bullshit. Ship something today.")
    elif voice == "prepaired":
        lines.append("Brief delivered. Standing by.")
    else:
        lines.append("Have a good day.")

    return "\n".join(lines)


def write_brief(content: str):
    today = date.today().isoformat()
    out_dir = VAULT / "wiki" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"brief-{today}.md"

    fm = {
        "id": f"brief-{today}",
        "type": "output",
        "output_type": "brief",
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "ikigai_regions": [],
        "summary": "Daily brief for " + today,
        "voice": CONFIG["voice"]["morning_brief"],
        "applied": False,
        "status": "canonical",
        "schema_hash": "v0.3",
        "tags": ["brief", "daily"],
    }
    post = frontmatter.Post(content, **fm)
    out_path.write_text(frontmatter.dumps(post))
    return out_path


def run_herald():
    print(f"═══ THE HERALD — run at {datetime.now(timezone.utc).isoformat()} ═══", flush=True)
    try:
        brief = assemble_brief()
        out = write_brief(brief)
        print(f"  ✓ brief written to {out.relative_to(VAULT)}", flush=True)
    except Exception as e:
        print(f"  ✗ herald failed: {e}", flush=True)


def main():
    print("═══ THE HERALD — daemon ═══", flush=True)
    sched = CONFIG["daemons"]["the_herald"]["schedule"]
    parts = sched.split()
    if len(parts) == 5 and parts[0].isdigit() and parts[1].isdigit():
        time_str = f"{int(parts[1]):02d}:{int(parts[0]):02d}"
        schedule.every().day.at(time_str).do(run_herald)
        print(f"  Scheduled daily at {time_str}", flush=True)
    else:
        schedule.every(24).hours.do(run_herald)

    # Run once on boot for verification
    run_herald()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
