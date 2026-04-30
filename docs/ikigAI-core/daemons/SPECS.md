# Daemons — Specs Only at v0.2

> What they do, when they run, how they get built in S2.
> No implementation here. These specs are the contract S2 builds against.

---

## inbox-watcher

**Purpose:** processes captures as they land in `inbox/`.

**Trigger:** inotify on `inbox/**/*` (Linux). Polling fallback for non-Linux.

**Flow:**
1. New file detected
2. Read file, identify type from path (chrome / voice / chat-paste / ideas / unsorted)
3. If type `ideas/` → run /phase-an-idea after canonical ingest
4. Otherwise → run /understand pipeline
5. Append to log.md, move processed file to inbox/_archived/<date>/

**Implementation in S2:**
- Python daemon with `watchdog` library
- Containerised, runs as systemd service
- Logs to `state/daemons/inbox-watcher.log`
- Health endpoint at `http://localhost:8901/health`

**Configurable from `me/config.yml`:** poll_interval, retry behaviour, batch size.

---

## scout (linkage-scout)

**Purpose:** nightly graph walk for non-obvious connections.

**Trigger:** cron, default 02:00 local.

**Flow:** see `prompts/secondary.md` → /surface section.

**Implementation in S2:**
- Python script run by cron
- Reads vector + graph indexes
- Writes to `state/scout_queue.jsonl`
- Brief generator reads this in the morning

---

## brief-generator

**Purpose:** daily morning brief.

**Trigger:** cron, time configured in `me/config.yml` (default 07:30 local).

**Flow:** see `prompts/brief.md`.

**Implementation in S2:**
- Reads scout queue, active projects, calendar cache, recent ideas
- Calls /brief prompt against Claude (or local for draft + Claude polish)
- Writes brief to `wiki/outputs/brief-<date>.md`
- Surfaces via web viewer panel and MCP `ikigai_brief_today` tool

---

## decay-keeper

**Purpose:** confidence and retrieval-score lifecycle upkeep.

**Trigger:** cron, weekly Sunday 03:00.

**Flow:** see `prompts/secondary.md` → /lint section.

**Implementation in S2:**
- Python script
- Modifies frontmatter on stale pages
- Promotes pages meeting promotion criteria
- Writes summary to `log.md`

---

## debaiser

**Purpose:** contrarian panel on demand.

**Trigger:**
- User invokes `/debaiser <topic>` from MCP or web
- Auto-flagged when scout detects echo chamber
- Triggered on Gear 3 retrieval

**Flow:** see `prompts/debaiser.md`.

**Implementation in S2:**
- Not a long-running daemon
- Invoked synchronously from retrieve / brief
- Cloud LLM (Claude) required

---

## gmail-watcher

**Purpose:** read-only Gmail pull from configured label.

**Trigger:** poll every 15 minutes, configurable.

**Flow:**
1. OAuth into Gmail with read-only scope
2. List messages with label `IkigAI/Inbox`
3. For each: pull body, strip headers, write to `inbox/gmail/<message-id>.md`
4. Remove the label from the message in Gmail (mark-as-processed)
5. Inbox-watcher takes over

**Implementation in S2:**
- Python with `google-api-python-client`
- OAuth credentials in `me/secrets/google_credentials.json` (gitignored)
- Refresh token cached securely
- Per-account configuration in `me/config.yml`

---

## calendar-sync

**Purpose:** two-way Google Calendar sync.

**Trigger:**
- Read: every 15 minutes, populates `state/cache/calendar.json`
- Write: on demand when user accepts a calendar offer

**Flow:**
1. Read: pull events for today + next 14 days, cache locally
2. Write: when user accepts a /phase-an-idea calendar offer, post event to Google with description linking to the plan page

**Implementation in S2:**
- Same OAuth as gmail-watcher (single Google credentials block)
- Two-way scope
- Event description format: `IkigAI: <plan-id> | <plan-title> | http://nuc.tailnet/wiki/outputs/<plan-id>`
- User's per-calendar mapping in `me/config.yml`

---

## health summary

S2 implements all daemons as systemd services with a single health-check endpoint:

```
GET http://nuc.tailnet:8900/health

{
  "inbox_watcher": "running",
  "scout": "last_run: 2026-04-30T02:00:00, status: ok",
  "brief_generator": "last_run: 2026-04-30T07:30:00, status: ok",
  "decay_keeper": "last_run: 2026-04-28T03:00:00, status: ok",
  "gmail_watcher": "running",
  "calendar_sync": "running",
  "ollama": "running",
  "vector_index": "running",
  "graph_index": "ok"
}
```

This becomes the brain's heartbeat. The web viewer shows it on the home screen.
