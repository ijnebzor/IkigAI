#!/usr/bin/env python3
"""
THE GATEKEEPER

Gmail watcher. Polls a label (default: IkigAI/Inbox) for unread messages.
Drops bodies into inbox/email/ for THE WATCHER to process.
Marks messages as read after processing.

Naming convention: THE [ROLE] (Digiquarium pattern).
Requires Gmail OAuth credentials at /secrets/gmail-token.json.
"""

import os
import json
import time
import yaml
import base64
from pathlib import Path
from datetime import datetime, timezone
from email import message_from_bytes

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
SECRETS = Path(os.environ.get("SECRETS_DIR", "/secrets"))

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())

GMAIL_TOKEN = SECRETS / "gmail-token.json"
GMAIL_CRED = SECRETS / "gmail-credentials.json"
LABEL_NAME = CONFIG["daemons"]["the_gatekeeper"].get("label", "IkigAI/Inbox")
INTERVAL = CONFIG["daemons"]["the_gatekeeper"].get("interval_seconds", 60)


def get_gmail_service():
    if not GMAIL_TOKEN.exists():
        print(f"  ✗ no token at {GMAIL_TOKEN} — run 09-google-oauth setup", flush=True)
        return None
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials.from_authorized_user_file(str(GMAIL_TOKEN), [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.modify",
        ])
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                GMAIL_TOKEN.write_text(creds.to_json())
            else:
                print("  ✗ credentials invalid; reauth needed", flush=True)
                return None
        return build("gmail", "v1", credentials=creds)
    except Exception as e:
        print(f"  ✗ gmail service init failed: {e}", flush=True)
        return None


def find_label_id(service, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for l in labels:
        if l["name"] == label_name:
            return l["id"]
    return None


def fetch_messages(service, label_id):
    resp = service.users().messages().list(
        userId="me",
        labelIds=[label_id, "UNREAD"],
        maxResults=20,
    ).execute()
    return resp.get("messages", [])


def get_message_body(service, msg_id):
    msg = service.users().messages().get(userId="me", id=msg_id, format="raw").execute()
    raw = base64.urlsafe_b64decode(msg["raw"])
    parsed = message_from_bytes(raw)
    subject = parsed.get("Subject", "(no subject)")

    body_text = ""
    if parsed.is_multipart():
        for part in parsed.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body_text = payload.decode(part.get_content_charset() or "utf-8", errors="replace")
                    break
    else:
        payload = parsed.get_payload(decode=True)
        if payload:
            body_text = payload.decode(parsed.get_content_charset() or "utf-8", errors="replace")

    return subject, body_text


def write_to_inbox(msg_id, subject, body):
    inbox = VAULT / "inbox" / "email"
    inbox.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date().isoformat()
    safe_subject = "".join(c if c.isalnum() else "-" for c in subject[:40]).strip("-")
    fname = f"{today}-{msg_id[:8]}-{safe_subject}.md"
    out = inbox / fname
    out.write_text(f"# {subject}\n\n{body}\n")
    return out


def mark_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()


def run_gatekeeper():
    service = get_gmail_service()
    if not service:
        return
    label_id = find_label_id(service, LABEL_NAME)
    if not label_id:
        print(f"  ✗ label '{LABEL_NAME}' not found in Gmail", flush=True)
        return

    messages = fetch_messages(service, label_id)
    if not messages:
        return
    print(f"  → {len(messages)} unread message(s) on label {LABEL_NAME}", flush=True)
    for m in messages:
        try:
            subject, body = get_message_body(service, m["id"])
            out = write_to_inbox(m["id"], subject, body)
            mark_read(service, m["id"])
            print(f"    ✓ wrote {out.relative_to(VAULT)}", flush=True)
        except Exception as e:
            print(f"    ✗ {m['id']}: {e}", flush=True)


def main():
    print("═══ THE GATEKEEPER — daemon ═══", flush=True)
    print(f"  Label: {LABEL_NAME}", flush=True)
    print(f"  Interval: {INTERVAL}s", flush=True)
    while True:
        try:
            run_gatekeeper()
        except Exception as e:
            print(f"  ✗ gatekeeper error: {e}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
