# docs/ — IkigAI Specification

> The contract. The substrate. The vocabulary. Everything the system reads before it acts.

## Layout

```
docs/
├── ikigAI-core/         # universal, fork-safe
│   ├── schema/          # SCHEMA.md — v0.3 page contract
│   ├── prompts/         # operation prompts
│   │   ├── understand.md
│   │   ├── retrieve.md
│   │   ├── debaiser.md
│   │   ├── phase-an-idea.md
│   │   ├── brief.md
│   │   ├── onboard.md
│   │   └── secondary.md (surface, lint, why-did-i-think, etc.)
│   └── templates/       # frontmatter templates per page type
│       ├── source.md
│       ├── entity.md
│       ├── concept.md
│       ├── project.md
│       ├── idea.md
│       ├── output.md
│       ├── dimension.md
│       └── lexicon.md
└── ikigAI-me/           # bespoke, this user's vault skeleton
    ├── CLAUDE.md         # vocabulary, projects, current context
    ├── ikigai.md         # concentric rings, current vs aspirational
    ├── lexicon.md        # load-bearing terms with my lens
    ├── config.yml        # daemon and routing config
    ├── inbox/            # captures awaiting processing
    ├── state/            # runtime state, feedback log, indexes
    └── wiki/             # the vault: sources, entities, concepts, projects, ideas, outputs, dimensions
```

## Repo split contract (S0 hard requirement)

`ikigAI-core/` is universal and fork-safe. Two friends can use the same core.

`ikigAI-me/` is bespoke. Friend forks, gets their own `me/` skeleton, never refactors core.

Day-1 split. No refactor cost when friend onboards.

## Reading order for new operators

1. `ikigAI-me/ikigai.md` — what this vault is FOR (the user's framework)
2. `ikigAI-me/CLAUDE.md` — who the user is, what they work on
3. `ikigAI-me/lexicon.md` — load-bearing terms with the user's lens (read this BEFORE classifying anything)
4. `ikigAI-core/schema/SCHEMA.md` — what every page must look like
5. `ikigAI-core/prompts/<operation>.md` — the specific operation

## Schema version

v0.3. Adds: `ring`, `expression_surface`, `sovereignty_layers`, `lexicon_terms`, `compounding_ripples` fields. Adds `lexicon` page type. Migration from v0.2 is non-destructive.

## What lives outside docs/

- `index.html`, `app.html`, `roadmap-reference.html` — the PWA. Reads docs for spec; doesn't write to it.
- `s2/` (after S2 build) — deployment scripts, daemon source, MCP server, runbook.
- `manifest.json`, `sw.js` — PWA configuration.

## Status

- v0.3 spec complete (this commit)
- v0.3 PWA shipped (this commit)
- S2 deployment packet — coming in this commit
- S2 deployment execution — Saturday, on user's NUC
