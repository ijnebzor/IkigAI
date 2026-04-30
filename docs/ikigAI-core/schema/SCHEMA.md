# IkigAI Schema v0.2

> The contract every page adheres to. Universal. Lives in core/.
> Bump schema_hash on breaking changes; lint flags stale pages.

---

## Universal frontmatter (every page has this)

```yaml
---
# Identity
id: 2026-04-30-<slug>           # immutable, used in [[wikilinks]]
type: source                    # source | entity | concept | project | idea | output
created: 2026-04-30T08:54:00+11:00
updated: 2026-04-30T08:54:00+11:00

# Ikigai regions — flat, explicit list of every region this page touches.
# Both axes (love | good_at | world_needs | paid_for) and intersections
# (passion | mission | profession | vocation | centre) are written
# explicitly. A page tagged [love, world_needs] also carries [mission].
# This is what makes the Venn surface compounding: a single contribution
# lights up every region it touches.
ikigai_regions: []

# Summary — agent-written on ingest. Always present. ≤4 sentences.
# This is what the coach reads when it can't re-read the page.
summary: ""

# Topical tags — free-form, governed by lint
tags: []

# Provenance (the reverse brain-fart trail)
sources_raw: []                 # original URLs / file paths / capture origin
derived_from: []                # [[wikilinks]] to parent claims
supersedes: []                  # [[wikilinks]] to claims this replaces
superseded_by: null             # set when something replaces this
confidence: 0.5                 # 0–1, decays over time, rises with reinforcement
last_reinforced: 2026-04-30
drivers: []                     # why I cared: curiosity, deadline, problem-solving
biases: []                      # cognitive biases flagged on this thought

# Retrieval signal (ADDIE feedback, learned from observed use)
retrieval_score: 0.5            # default 0.5; learned from how the page is used
last_surfaced: null             # last time the system showed this in a coach output
last_used: null                 # last time you cited or expanded on it
context_modifiers: {}           # per-context bumps: {"work-strategy": 0.2}
surface_count: 0                # cumulative surfaces in coach outputs
use_count: 0                    # cumulative explicit uses (cited, expanded)

# Lifecycle
status: inbox                   # inbox | canonical | evergreen | superseded | archived
schema_hash: v0.2
---
```

---

## Type-specific extensions

### `source` — anything ingested
```yaml
source_type: web | chat-paste | voice | book | paper | video | email | image | other
source_url: null
source_date: null               # when the source was created (not when ingested)
captured_from: chrome_phone | gmail_label | voice_memo | manual | etc
extracted_entities: []          # [[wikilinks]] to entity pages
extracted_concepts: []          # [[wikilinks]] to concept pages
fetched_via: normal | tinyfish | manual_paste | n/a
```

### `entity` — people, projects, tools, places, orgs
```yaml
entity_type: person | project | tool | place | org | role
aliases: []
relationships: []               # [{type: works_at, target: [[ph2]]}]
```

### `concept` — ideas, frameworks, methods, recurring themes
```yaml
domain: []                      # [security, ai, music]
maturity: nascent | working | established | foundational
```

### `project` — active project hubs
```yaml
project_status: active | paused | shipped | archived
linked_concepts: []
linked_sources: []
linked_ideas: []                # ideas pending or accepted into this project
```

### `idea` — captured idea pending phasing
```yaml
idea_status: raw | phased | accepted | declined | shipped | parked
phased_plan: null               # [[wikilink]] to the phased-plan output once written
calendar_offered: false
calendar_event_ids: []          # Google Calendar event IDs once accepted
parent_project: null            # [[wikilink]] if this rolls up under a project
```

### `output` — saved coach responses
```yaml
output_type: gear-1 | gear-2 | gear-3 | brief | phased-plan | debaiser-report
in_response_to: ""              # the original query
gear_used: 1 | 2 | 3
voice: warm | helpful | aggressive | roasty | prepaired | accountantability | ijneb-dev
sources_cited: []               # [[wikilinks]]
applied: false                  # ADDIE: did the user act on this?
applied_at: null
outcome_notes: null             # captured on follow-up
```

---

## Ikigai regions — the model

Four axes:
- `love` — what you love
- `good_at` — what you're good at
- `world_needs` — what the world needs
- `paid_for` — what you can be paid for

Five intersections (compositions of axes):
- `passion` = love + good_at
- `mission` = love + world_needs
- `profession` = good_at + paid_for
- `vocation` = world_needs + paid_for
- `centre` = all four (the IKIGAI proper)

**The flat-list rule:** when a page touches multiple regions, list them all explicitly. A page touching love and world_needs writes:

```yaml
ikigai_regions: [love, world_needs, mission]
```

The intersection (`mission`) is written explicitly even though it's derivable, because:
- Filtering becomes one operation, not a join
- `wiki/ikigai/mission.md` rolls up everything tagged `mission` directly
- Single contribution compounds across every region it touches
- Click any region in the viewer → see everything that contributed

**The centre case:**
```yaml
ikigai_regions: [love, good_at, world_needs, paid_for, passion, mission, profession, vocation, centre]
```

This is rare and worth flagging. The `centre.md` rollup page should never have many entries. If it does, either the tagging is too generous or you've actually found your Ikigai. Lint will warn.

---

## Lifecycle states

```
inbox        Just captured. Not yet canonicalised or fully tagged.
             Waiting for the understand pipeline.

canonical    Pipeline ran. Frontmatter complete. Linked into graph.
             This is the working state of most pages.

evergreen    Reinforced ≥5 times. Confidence ≥ 0.8. No decay events
             in the last 60 days. The brain trusts this strongly.

superseded   Replaced by another page. Kept (never deleted) for audit.
             superseded_by points to the replacement.

archived     Manually retired. Out of default retrieval. Still findable
             with --include-archived flag.
```

Promotion rules live in `prompts/lint.md`. Demotion is manual or via supersession.

---

## What this schema deliberately omits

- **No `priority` field.** The brief generator computes priority from regions + retrieval_score + calendar context. Static priority rots.
- **No `tags` taxonomy enforcement.** Free-form. Lint surfaces drift; you decide what to consolidate.
- **No `is_private` flag.** Everything in your vault is private by default. If you publish a slice later, that's a separate concern at the publish step.
- **No `embedding` field.** Embeddings live in the vector index, not the markdown. Recomputable from content; never authoritative.

---

## Migration from v0.1

If you ran the v0.1 prototype:
- `ikigai: {love: bool, ...}` → `ikigai_regions: [list]` (compute intersections explicitly)
- Add `summary` field (default empty string; understand pipeline backfills on next pass)
- Add `retrieval_score` (default 0.5)
- Add `context_modifiers` (default {})
- Add `last_surfaced`, `last_used`, `surface_count`, `use_count`
- Bump `schema_hash` to `v0.2`

Migration script lives at `core/scripts/migrate/v0.1-to-v0.2.py` (not yet built; trivial when needed).
