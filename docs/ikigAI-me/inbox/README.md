# inbox/ — captures awaiting processing

THE WATCHER daemon (S2+) inotifies on this directory. Drop any markdown file here and the watcher:

1. Reads the file
2. Runs `/understand` on it
3. Writes the resulting page to `wiki/sources/<id>.md` (or `wiki/ideas/`, `wiki/concepts/`, depending on classification)
4. Commits to git
5. Removes the inbox file

Until S2 is live, captures pile up here for later batch processing.

## Naming

Free-form. The watcher derives the id and slug. Useful prefixes:

- `voice-<date>.md` — voice memo transcript
- `link-<date>-<slug>.md` — link-and-context save
- `chat-<date>.md` — chat-paste (Phase 0 only)
- `idea-<slug>.md` — explicit idea capture
- `note-<date>.md` — anything else

## What goes here

Any thought, link, voice memo, transcript, screenshot+context, paste-from-DM (Phase 0 only). The watcher classifies and routes.

## What does NOT go here

- Meeting transcripts longer than 30 mins (split first)
- Files larger than 500KB (the watcher will reject and ask)
- Anything you're not OK being part of your corpus forever
