# state/ — runtime state

Created and managed by daemons. Mostly gitignored.

Files:
- `feedback.jsonl` — every surface event for ADDIE retrieval ranking
- `lint-<date>.md` — daily KEEPER lint reports
- `fetch.log` — THE WATCHER's HTTP fetch attempts
- `vector_index/` — Chroma vector store (large; never committed)

This README is committed so the dir survives `git clean`.
