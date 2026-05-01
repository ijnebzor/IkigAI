# S2 — 10 — Phase 0 brain dump

> The bulk-import moment. Everything you've been collecting in side surfaces (Chrome tabs, social bookmarks, voice memos, chat-pastes) lands in IkigAI in one sustained session.
> Estimated time: 90 minutes. Worth more.

## Why Phase 0 matters

Phase 0 is the difference between an empty system and a working brain. With no corpus, retrieval returns nothing useful and the daemons have nothing to be smart about. With a Phase 0 dump, every retrieval lands on real material from day one.

This is also the first stress test of your /understand pipeline. Bulk-importing 200 disparate things will surface schema bugs, lexicon gaps, and canonicalisation misfires you'd never find with one-at-a-time captures.

## What goes in

Five surfaces. Do them in this order — easiest first.

### Surface 1 — Chrome tabs (15-20 min per device)

The "tabs as todo list" pattern. Every device, every tab open right now, becomes a source.

**Per-device procedure:**

1. Open the device's Chrome (or Safari)
2. Right-click on any tab → **Bookmark all tabs** → save to a temporary folder `IkigAI/Phase0/<device-name>`
3. Export bookmarks: Chrome menu → Bookmarks → Bookmark manager → ⋮ → Export bookmarks → save HTML
4. Copy the HTML to the NUC: `scp <bookmarks>.html <user>@<nuc>:~/ikigAI-me/inbox/tabs/`

**The chunker:**

THE WATCHER doesn't natively chunk an HTML bookmarks export. Run this once to split:

```python
# ~/ikigai-state/scripts/chunk-bookmarks.py
import sys
from pathlib import Path
from bs4 import BeautifulSoup

src = Path(sys.argv[1])
out_dir = Path.home() / "ikigAI-me" / "inbox" / "tabs"
out_dir.mkdir(exist_ok=True, parents=True)

soup = BeautifulSoup(src.read_text(), "html.parser")
for i, a in enumerate(soup.find_all("a")):
    title = a.get_text(strip=True) or "untitled"
    href = a.get("href", "")
    if not href:
        continue
    safe = "".join(c if c.isalnum() else "-" for c in title[:50]).strip("-")
    out = out_dir / f"tab-{i:04d}-{safe}.md"
    out.write_text(f"# {title}\n\nSource: {href}\n\n_(Phase 0 import — original tab from {src.stem})_\n")
print(f"Chunked {i+1} tabs → {out_dir}")
```

Run:
```bash
python ~/ikigai-state/scripts/chunk-bookmarks.py ~/ikigAI-me/inbox/tabs/<bookmarks>.html
```

Each tab becomes its own file. THE WATCHER will pick them up and run /understand on each. Plan for ~30 seconds/tab if Ollama is on a fresh model — 200 tabs ≈ 100 minutes wall clock for the watcher to chew through. You can watch via `docker compose logs -f the-watcher`.

**Cap:** for v0.3, cap Phase 0 at 200 tabs per device. Anything beyond is probably already-stale browse history. Close the tabs after dumping.

### Surface 2 — Social bookmarks (10-15 min)

Saved Instagram posts, Twitter/X bookmarks, LinkedIn saved articles.

**Instagram:**
- Profile → Saved → ⋮ → Send via DM (to yourself) — or just screenshot the list and grab links
- For each saved post: copy the post URL, write a markdown file with `# <one-line title>\n\n<post URL>\n\n<your reason for saving it>` if you remember
- Drop into `~/ikigAI-me/inbox/web/`

**Twitter/X:**
- Profile → Bookmarks → for each bookmark, copy URL
- If you have a lot, the [Twitter Bookmarks Exporter](https://github.com/tinacious/Tina-Twitter-Bookmark-Export) (or similar tool) can dump JSON; chunk into individual files
- Drop into `~/ikigAI-me/inbox/web/`

**LinkedIn:**
- Saved articles in your profile dropdown → similar approach
- Drop into `~/ikigAI-me/inbox/web/`

### Surface 3 — Voice memos (20-30 min)

If you have voice memos lying around, this is the time.

**iOS Voice Memos export:**
- Files app → On My iPhone → Voice Memos → select all → Share → Save to Files (or AirDrop to Mac, then to NUC)
- Get the M4A files onto NUC: `scp ~/voice-memos/*.m4a <user>@<nuc>:~/ikigAI-me/inbox/voice/raw/`

**On the NUC, transcribe with whisper.cpp:**

```bash
# ~/ikigai-state/scripts/transcribe-voice.sh
#!/bin/bash
RAW=~/ikigAI-me/inbox/voice/raw
OUT=~/ikigAI-me/inbox/voice
WHISPER=~/whisper.cpp

mkdir -p "$RAW" "$OUT"
for f in "$RAW"/*.m4a "$RAW"/*.mp3 "$RAW"/*.wav; do
  [ -f "$f" ] || continue
  base=$(basename "$f")
  stem="${base%.*}"

  # Convert to wav if needed (whisper.cpp wants 16kHz mono wav)
  if [[ "$f" != *.wav ]]; then
    ffmpeg -i "$f" -ar 16000 -ac 1 "/tmp/${stem}.wav" -y -loglevel error
    src="/tmp/${stem}.wav"
  else
    src="$f"
  fi

  # Transcribe
  "$WHISPER/main" -m "$WHISPER/models/ggml-small.en.bin" -f "$src" -otxt -of "/tmp/${stem}"
  
  # Write to inbox
  if [ -f "/tmp/${stem}.txt" ]; then
    cat > "$OUT/${stem}.md" << EOF
# Voice memo — ${stem}

_(Phase 0 import, transcribed with whisper.cpp small.en)_

$(cat "/tmp/${stem}.txt")
EOF
    rm -f "/tmp/${stem}.txt" "/tmp/${stem}.wav"
    mv "$f" "$RAW/.processed/" 2>/dev/null || mkdir -p "$RAW/.processed" && mv "$f" "$RAW/.processed/"
    echo "  ✓ $stem"
  fi
done
```

```bash
chmod +x ~/ikigai-state/scripts/transcribe-voice.sh
~/ikigai-state/scripts/transcribe-voice.sh
```

Each transcript becomes a markdown file in `inbox/voice/`. THE WATCHER processes them.

### Surface 4 — Chat-pastes (30-45 min, the slow one)

Selected snippets from Slack, Discord, iMessage, WhatsApp, etc.

**The hard rule: NEVER reference the channel, sender, or thread.** Phase 0 is one-way. The system gets your *thoughts as you wrote them*, not a record of who said what to whom.

**Procedure for each conversation:**
1. Open the chat client
2. Scroll through, copy passages that contain *your own thinking* on a topic worth keeping
3. Paste into a new file: `~/ikigAI-me/inbox/chat/2026-04-30-<topic>.md`
4. Format:
   ```markdown
   # <topic>

   <your paste>

   <your paste, more on the topic>
   ```
5. NO `<from John on Slack>`, NO `<channel #engineering>`, NO timestamps that imply a thread

This is tedious. Do it. The corpus will reward you for it forever.

### Surface 5 — Existing notes / docs (15 min)

If you've been keeping notes elsewhere (Obsidian, Apple Notes, Google Docs, Notion):

**Obsidian:** copy the vault — `cp -r ~/Obsidian/<vault> ~/ikigAI-me/inbox/imports/<vault-name>/`. THE WATCHER will recursively process. Bear in mind: *every* note becomes a source. Cap or pre-filter.

**Apple Notes:** export folder by folder — File → Export as PDF (or third-party tools that export markdown). Drop into `inbox/imports/`.

**Google Docs:** Drive → folder → ⋮ → Download → choose markdown — extract the zip into `inbox/imports/`.

**Notion:** Settings → Export → Markdown & CSV — extract zip into `inbox/imports/`.

## During the dump

THE WATCHER is processing in the background. You can monitor:

```bash
docker compose logs -f the-watcher
```

Each file produces a line like:
```
→ Processing inbox/tabs/tab-0042-some-article.md
  ✓ wrote wiki/sources/2026-04-30-some-article.md
```

If you see lots of `✗ understand failed`, Ollama is overwhelmed. Pause your dumping; let the queue drain. Resume after the watcher catches up.

## After the dump

### Sanity check

```bash
ls ~/ikigAI-me/wiki/sources/ | wc -l   # number of canonicalised pages
cat ~/ikigAI-me/log.md | tail -50      # recent ingest events
```

### Run THE SCOUT manually

Instead of waiting for the 02:00 cron:

```bash
docker exec ikigai-the-scout python /daemons/the-scout.py
```

This produces the first compounding-discovery report. You'll see linkages between things you'd dumped from completely different surfaces.

### Run THE KEEPER manually

```bash
docker exec ikigai-the-keeper python /daemons/the-keeper.py
```

Produces the first lint report. Expect dozens of issues from raw imports — that's fine. Fix the schema-violating ones; ignore noise.

### Try a real retrieval

From your phone via Claude Desktop:

> Use ikigai_retrieve to answer: "what have I been thinking about local LLM hosting?"

If you've dumped enough, the trail comes back populated. If it's thin, dump more from the chat-paste surface — that's usually where the thinking lives.

## What Phase 0 deliberately leaves out

- **Email archives** — Gmail's a stream, not a dump. THE GATEKEEPER handles that ongoing.
- **Code repos** — `code-review-graph` and similar tools handle those better. Don't try to ingest a repo as a "source".
- **Calendar history** — THE SCRIBE pulls forward, not backward.
- **Anything ambiguous about consent** — if a chat involves sensitive stuff someone else said, leave it out. Use your own thinking only.

## Done state

You've completed Phase 0 when:
- [ ] At least 50 sources in `wiki/sources/`
- [ ] At least 5 voice memos transcribed (if applicable)
- [ ] At least one chat-paste topic
- [ ] THE SCOUT has produced its first discovery report
- [ ] THE KEEPER has produced its first lint report
- [ ] One real retrieval through MCP returns useful results

This is the floor, not the ceiling. The corpus grows from here every time you capture.
