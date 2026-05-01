# S2 — 09 — Google OAuth (Calendar + Gmail)

> One-time setup. After this, THE GATEKEEPER and THE SCRIBE work.
> Estimated time: 30 minutes.

## What we're setting up

Two OAuth scopes, both for the NUC user only:

1. **Gmail** — read + modify on label `IkigAI/Inbox` (THE GATEKEEPER)
2. **Calendar** — full two-way scope on primary calendar (THE SCRIBE)

We use the **installed application** flow (not web app), so credentials are stored locally on the NUC.

## Recommendation: dedicated tooling Google account

Don't use your primary Google account if you can avoid it. Create a dedicated `<your-name>+ikigai@gmail.com` (or a new full account) and forward the Inbox label from your real Gmail. Reasons:
- Token leaks are blast-radius bounded
- You can revoke access without breaking your daily mail
- The IkigAI label can have its own forwarding rules without touching your real inbox rules

If you proceed with your primary, that's your call — just rotate annually.

## Step 1 — Create a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Top bar: **Select a project** → **New Project**
3. Name: `ikigai-personal` (or similar)
4. Org: leave as-is
5. Create

## Step 2 — Enable APIs

In the new project:

1. **APIs & Services → Library**
2. Search `Gmail API` → **Enable**
3. Search `Google Calendar API` → **Enable**

## Step 3 — Configure OAuth consent screen

1. **APIs & Services → OAuth consent screen**
2. **User Type:** External (Google requires this for personal accounts; you'll keep the app in Testing mode so only your own account can use it)
3. Fill in:
   - App name: `ikigAI`
   - User support email: your account
   - Developer contact: your account
4. **Save and continue**
5. **Scopes:** click **Add or remove scopes** and add:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/calendar`
6. **Save and continue**
7. **Test users:** add your tooling Google account email
8. **Save and continue**

Stay in Testing mode. Don't publish — Google will demand verification you don't need.

## Step 4 — Create OAuth credentials

1. **APIs & Services → Credentials**
2. **Create credentials → OAuth client ID**
3. **Application type:** Desktop app
4. Name: `ikigAI-nuc`
5. Create

You'll see a dialog with `client_id` and `client_secret`. Click **Download JSON**. Save as `gmail-credentials.json` for now (you'll reuse for Calendar).

## Step 5 — Drop the credentials on the NUC

```bash
# On your laptop, copy to NUC
scp ~/Downloads/client_secret_*.json <user>@<nuc-tailscale>:~/ikigai-state/secrets/google-credentials.json

# On the NUC
chmod 600 ~/ikigai-state/secrets/google-credentials.json
```

## Step 6 — First-time auth flow (do this on the NUC)

This script generates the access tokens for both Gmail and Calendar and saves them where the daemons expect.

```bash
# On the NUC
source ~/ikigai-state/venv/bin/activate
cd ~/IkigAI
```

Save the following as `~/ikigai-state/scripts/oauth-bootstrap.py`:

```python
"""
Run once on the NUC to authenticate Gmail + Calendar.
Opens a browser locally; if NUC is headless, prints a URL to paste into
a browser on your laptop.
"""
import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SECRETS = Path.home() / "ikigai-state" / "secrets"
CRED = SECRETS / "google-credentials.json"

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]

CAL_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]


def auth(scopes, out_name):
    flow = InstalledAppFlow.from_client_secrets_file(str(CRED), scopes)
    # If running headless: pass open_browser=False, copy the URL it prints, paste into a browser on your laptop
    creds = flow.run_local_server(port=0)
    out = SECRETS / out_name
    out.write_text(creds.to_json())
    out.chmod(0o600)
    print(f"  ✓ saved {out}")


print("== Gmail auth ==")
auth(GMAIL_SCOPES, "gmail-token.json")

print("== Calendar auth ==")
auth(CAL_SCOPES, "calendar-token.json")

print("\nDone. Tokens saved to ~/ikigai-state/secrets/")
```

Run:

```bash
mkdir -p ~/ikigai-state/scripts
# (paste the script above)
chmod +x ~/ikigai-state/scripts/oauth-bootstrap.py
python ~/ikigai-state/scripts/oauth-bootstrap.py
```

If the NUC is headless (no browser):
- The script prints a URL
- Open it on your laptop
- Authenticate with your tooling Google account
- Paste the redirect URL back into the NUC terminal when prompted (use `flow.run_console()` instead of `run_local_server` — adjust script if needed)

## Step 7 — Set up the Gmail label

In Gmail (your tooling account, or your primary if you went that route):

1. Settings → Labels → **Create new label** → name: `IkigAI/Inbox`
2. Settings → Filters → **Create new filter**
   - From: addresses you want IkigAI to ingest from (or "to:me has:attachment", or whatever rule makes sense)
   - Apply label: `IkigAI/Inbox`
   - Skip the inbox: optional, your call
3. To test: send an email matching your filter, verify the label is applied

## Step 8 — Enable the daemons in config.yml

```bash
nano ~/ikigAI-me/config.yml
```

Change:
```yaml
the_gatekeeper:
  enabled: false   # → true
the_scribe:
  enabled: false   # → true
```

## Step 9 — Restart the docker-compose stack

```bash
cd ~/IkigAI/docs/s2
docker compose --profile always --profile with-google up -d
```

## Step 10 — Verify

```bash
docker compose logs -f the-gatekeeper
```

You should see startup logs and (if any unread messages exist on the label) processing output.

```bash
docker compose logs -f the-scribe
```

Should show calendar pull on first run; calendar files appear in `~/ikigAI-me/wiki/calendar/`.

## Token rotation

The OAuth refresh token is long-lived but should rotate annually:

1. Delete `~/ikigai-state/secrets/gmail-token.json` and `calendar-token.json`
2. Re-run `oauth-bootstrap.py`
3. Restart THE GATEKEEPER and THE SCRIBE

## Troubleshooting

**"403 Insufficient Permission"**
- Scopes weren't added in Step 3, or you authenticated before adding them
- Delete tokens, reauth

**"Label not found"**
- Confirm exact label name (case-sensitive). `IkigAI/Inbox` includes a slash — Gmail treats this as a nested label

**"redirect_uri_mismatch"**
- You're using `Web application` instead of `Desktop app`. Recreate as Desktop.

**"Access blocked: Authorization Error"**
- App is in Testing mode but your account isn't in the test users list. Add yourself.

**Token expired and won't refresh**
- This shouldn't happen for Desktop credentials but if it does, delete and reauth

## What this does NOT cover

- Multi-account auth (one Google account at a time per vault)
- Server-side OAuth web flow (we use installed-app)
- Granular Gmail scopes (we use modify on the whole inbox; a future enhancement is to scope to label-only when Google supports it)
