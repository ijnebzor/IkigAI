#!/usr/bin/env python3
"""
THE SCRIBE

Google Calendar two-way sync. Reads upcoming events into wiki/calendar/ as
markdown pages. Writes IkigAI-proposed events (from /phase-an-idea acceptances)
back to Google Calendar.

Naming convention: THE [ROLE] (Digiquarium pattern).
Requires Calendar OAuth credentials at /secrets/calendar-token.json.
"""

import os
import json
import time
import yaml
import frontmatter
from pathlib import Path
from datetime import datetime, timezone, timedelta

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
SECRETS = Path(os.environ.get("SECRETS_DIR", "/secrets"))

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())
CAL_TOKEN = SECRETS / "calendar-token.json"
SYNC_WINDOW = CONFIG["daemons"]["the_scribe"].get("sync_window_days", 14)
PROPOSED_QUEUE = INDEX / "calendar_proposals.jsonl"

CAL_DIR = VAULT / "wiki" / "calendar"
CAL_DIR.mkdir(parents=True, exist_ok=True)


def get_calendar_service():
    if not CAL_TOKEN.exists():
        print(f"  ✗ no token at {CAL_TOKEN}", flush=True)
        return None
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(CAL_TOKEN), [
            "https://www.googleapis.com/auth/calendar",
        ])
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                CAL_TOKEN.write_text(creds.to_json())
            else:
                return None
        return build("calendar", "v3", credentials=creds)
    except Exception as e:
        print(f"  ✗ calendar service init failed: {e}", flush=True)
        return None


def pull_events(service):
    """Pull upcoming events into wiki/calendar/."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=SYNC_WINDOW)
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
        maxResults=100,
    ).execute()
    events = events_result.get("items", [])

    for e in events:
        eid = e["id"]
        summary = e.get("summary", "(no title)")
        start = e["start"].get("dateTime", e["start"].get("date"))
        end_t = e["end"].get("dateTime", e["end"].get("date"))
        description = e.get("description", "")

        out = CAL_DIR / f"{eid}.md"

        fm = {
            "id": f"cal-{eid}",
            "type": "calendar_event",
            "google_event_id": eid,
            "summary": summary,
            "start": start,
            "end": end_t,
            "created": e.get("created", ""),
            "updated": e.get("updated", ""),
            "ikigai_regions": [],
            "status": e.get("status", "confirmed"),
            "schema_hash": "v0.3",
        }

        body = f"# {summary}\n\n**When:** {start} → {end_t}\n\n{description}\n"
        post = frontmatter.Post(body, **fm)
        out.write_text(frontmatter.dumps(post))


def push_proposals(service):
    """Read pending proposals, push to Google Calendar."""
    if not PROPOSED_QUEUE.exists():
        return
    requests = []
    with PROPOSED_QUEUE.open() as f:
        for line in f:
            try:
                requests.append(json.loads(line))
            except Exception:
                continue
    if not requests:
        PROPOSED_QUEUE.unlink()
        return

    succeeded = []
    for r in requests:
        try:
            event = {
                "summary": r["title"],
                "description": r.get("description", ""),
                "start": {"dateTime": r["start"]},
                "end": {"dateTime": r["end"]},
            }
            created = service.events().insert(calendarId="primary", body=event).execute()
            r["google_event_id"] = created["id"]
            succeeded.append(r)
            print(f"    ✓ pushed: {r['title']}", flush=True)
        except Exception as e:
            print(f"    ✗ push failed: {e}", flush=True)

    # Replay any that failed; keep the queue file
    failed = [r for r in requests if "google_event_id" not in r]
    if failed:
        with PROPOSED_QUEUE.open("w") as f:
            for r in failed:
                f.write(json.dumps(r) + "\n")
    else:
        PROPOSED_QUEUE.unlink()

    # Echo successful proposals back to vault
    for r in succeeded:
        out = CAL_DIR / f"{r['google_event_id']}.md"
        fm = {
            "id": f"cal-{r['google_event_id']}",
            "type": "calendar_event",
            "google_event_id": r["google_event_id"],
            "summary": r["title"],
            "start": r["start"],
            "end": r["end"],
            "created": datetime.now(timezone.utc).isoformat(),
            "ikigai_regions": r.get("regions", []),
            "in_response_to": r.get("idea_id"),
            "status": "confirmed",
            "schema_hash": "v0.3",
        }
        post = frontmatter.Post(r.get("description", ""), **fm)
        out.write_text(frontmatter.dumps(post))


def run_scribe():
    service = get_calendar_service()
    if not service:
        return
    pull_events(service)
    push_proposals(service)


def main():
    print("═══ THE SCRIBE — daemon ═══", flush=True)
    print(f"  Sync window: {SYNC_WINDOW} days", flush=True)
    while True:
        try:
            run_scribe()
        except Exception as e:
            print(f"  ✗ scribe error: {e}", flush=True)
        time.sleep(300)  # 5 min


if __name__ == "__main__":
    main()
