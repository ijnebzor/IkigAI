# ikigAI-core/

> Universal. Fork-safe. The bones every IkigAI operator runs.

This directory is the same for every user. Schema, prompt operations, page templates. No personal information. The friend forks the repo, copies this directory verbatim, and writes only into their own `ikigAI-me/`.

## Files

- `schema/SCHEMA.md` — v0.3 page contract; the load-bearing layer
- `prompts/` — every operation prompt; read in this order: understand → retrieve → debaiser → phase-an-idea → brief → onboard → secondary
- `templates/` — frontmatter templates per page type

## Versioning

The schema_hash in every page references the commit hash of `schema/SCHEMA.md` at write time. Schema migrations are explicit; pages can carry an old hash and be valid until upgraded.

## Promise

This directory does not encode anything specific to one user. If it does, it's a bug — file it as drift.
