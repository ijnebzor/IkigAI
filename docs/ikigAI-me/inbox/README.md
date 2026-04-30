# inbox/

Drop anything. The pipeline triages.

## Subfolders

- `chrome/` — browser tab dumps, copied URL lists
- `social/` — Instagram / Twitter / LinkedIn saves (one-time Phase 0 dump only)
- `voice/` — voice memo transcripts (whisper.cpp output)
- `chat-paste/` — copy-paste content from messaging apps (one-time Phase 0 only)
- `gmail/` — fed by Gmail label watcher (S2)
- `ideas/` — captured ideas, will route to phase-an-idea
- `unsorted/` — when you can't be bothered. The pipeline figures it out.

## What gets accepted
Anything text-ish. The pipeline handles dedupe and canonicalisation.

## What does NOT go in
- Live messaging app exports (one-time Phase 0 paste only)
- Anything referencing channels, senders, threads
- Secrets (stripped at ingest anyway, but don't include them)

## After ingest
The pipeline writes structured pages to `wiki/`, then leaves the inbox file
in place with a footer note. Move ingested files to `inbox/_archived/`
once you trust the result.
