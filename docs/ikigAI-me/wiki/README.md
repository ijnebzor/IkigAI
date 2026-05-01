# wiki/ — the corpus

> Everything captured, classified, retained, retrievable.

## Layout

- `sources/` — raw inputs (articles, voice memos, chat-pastes, etc.)
- `entities/` — people, orgs, products, places, events
- `concepts/` — ideas, frameworks, hypotheses
- `projects/` — multi-stage commitments
- `ideas/` — candidate projects awaiting `/phase-an-idea`
- `outputs/` — what the system produced (briefs, syntheses, debaiser reports, phased plans)
- `dimensions/` — auto-maintained Ikigai region rollups (don't hand-edit)
- `people/` — symlinked subset of entities/ for convenience

All pages valid v0.3 frontmatter. The watcher rejects pages that don't validate.

## Don't manually create dimension pages

`wiki/dimensions/` are auto-maintained by the keeper daemon. Members are computed nightly from canonical pages tagged with the corresponding region.

## Naming

Pages use ulid or yyyymmdd-slug as id. The id is the filename. Cross-references use `[[<page_id>]]`. Title in frontmatter is human-readable.
