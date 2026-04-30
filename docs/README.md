# IkigAI v0.2

A self-owned coach grounded in everything you know.

This is a **two-repo** project. They live as siblings.

```
ikigAI-core/    universal — shared across all users
                schema, prompts, daemons, scripts, templates, ui

ikigAI-me/      personal — yours, single source of truth for your brain
                vault, vocabulary, calendar links, feedback log
```

`me/` imports `core/` like a library. Core upgrades flow downstream to every `me/`. Personal never leaks upstream. When user #2 arrives, they get a `friend-me/` next to your `ikigAI-me/`, sharing the same `core/`. No refactor.

## Get started

1. Both repos go on the NUC at `~/ikigAI/`
2. `cd ikigAI-me && git init && git add . && git commit -m "ikigAI-me v0.2 init"`
3. Open `ikigAI-me/CLAUDE.md`, scan the vocabulary, edit anything missing
4. Drop a single source into `ikigAI-me/inbox/unsorted/`
5. Read `ikigAI-core/prompts/understand.md` and run a manual round trip via Claude
6. Validated? Move to S2 (NUC infra + bulk Phase 0 dump). See `IkigAI_Roadmap.md`.

## What's in this v0.2

- Schema v0.2 with explicit Ikigai regions as a flat list (not derived)
- Three retrieval gears: links / synthesis / debaiser-on-self
- Productionised idea flow: drop idea → phased plan → calendar offer
- Daily brief in the multi-project options format
- Repo split: core vs me from day one
- Provenance fields baked in for the reverse brain fart
- ADDIE feedback hooks (retrieval_score, context_modifiers)
- Specs for all daemons (no infra yet — that's S2)

## What's NOT in v0.2 yet

- Daemon implementations (specs only — S2 builds them)
- MCP server config (S2)
- Web viewer (S3)
- Calendar/Gmail integration (S2)
- Application capture mechanic (S4)
- Onboarding conversation (S5)

This is the foundation. Everything else builds on top.
