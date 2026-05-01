# IkigAI Schema v0.3

> The contract every page in your vault honours.

The schema is the load-bearing piece. Every page in `wiki/` reads as valid YAML frontmatter plus markdown body. The frontmatter is what enables retrieval, classification, ranking, and compounding visibility. The body is what your future self reads.

Schema versions evolve. v0.2 was structural. v0.3 makes the framework first-class: the four-axis Ikigai is no longer the only lens, it sits alongside the concentric-rings architecture. Lexicon awareness is now in the ingest contract.

---

## 1. Universal frontmatter (every page type)

```yaml
---
# IDENTITY
id: <auto>                          # ulid or yyyymmdd-slug, immutable once assigned
type: source | entity | concept | project | idea | output | dimension | lexicon
title: <human readable>
created: <iso8601>
updated: <iso8601>

# LIFECYCLE
status: inbox | canonical | evergreen | superseded | archived
schema_version: "0.3"
schema_hash: <commit hash of schema/SCHEMA.md when written>

# PROVENANCE — where did this come from, what does it know
derived_from: [page_id, ...]        # parent pages
supersedes: [page_id, ...]          # pages this replaces
contradicts: [page_id, ...]         # pages this disputes
last_reinforced: <iso8601>          # when something else cited this
confidence: 0.0..1.0                # how much you trust this page right now
drivers: [string, ...]              # why this is here, what informed it
biases: [string, ...]               # known angles or limits

# IKIGAI LENS (Brusselbach four-axis + intersections)
ikigai_regions: [<region>, ...]
  # Region values (flat list, not nested):
  #   axes:        love, good_at, world_needs, paid_for
  #   intersect:   passion (love+good), profession (good+paid),
  #                vocation (paid+world), mission (world+love),
  #                centre (all four)
  # Tagged through YOUR lens (see lexicon.md), not the source's encoded one.
  # Empty list is valid — not everything maps. Inbox pages may defer.
compounding_ripples: [page_id, ...] # pages whose regions overlap with this one,
                                    # computed at ingest, refreshed by linkage-scout

# RING ARCHITECTURE (concentric, separate axis from regions)
ring: identity | principle | surface | funding | none
  # Identity = AIthropologist content. Principle = sovereignty. 
  # Surface = which expression channel. Funding = how it's funded.
expression_surface: research | tooling | discourse | practice | none
  # Only meaningful when ring=surface
sovereignty_layers: [data, cognitive, tooling, narrative, epistemic]
  # Only meaningful when ring=principle. Empty otherwise.

# LEXICON AWARENESS (new in v0.3)
lexicon_terms: [<term>, ...]        # terms from me/lexicon.md this page uses
                                    # ingest pipeline reads lexicon when classifying these

# RETRIEVAL
retrieval_score: 0.0..1.0           # rank-influencing score, decays without reinforcement
context_modifiers:                  # situational rank adjustments
  work_strategy: 0.0..2.0
  creative: 0.0..2.0
  research: 0.0..2.0
  relational: 0.0..2.0
surface_count: <int>                # times this surfaced in retrieval
use_count: <int>                    # times this was cited in an output
ignored_count: <int>                # times this surfaced and you didn't engage

# CLASSIFICATION (free-form below ikigai_regions)
tags: [<arbitrary>, ...]
people: [<person_id>, ...]
projects: [<project_id>, ...]
concepts: [<concept_id>, ...]
---
```

---

## 2. Page type extensions

### `source` — captured input

A thing you saw, read, heard, said, or were told. Pre-classification ground truth.

Extra fields:
```yaml
source_type: article | post | video | podcast | conversation | voice_memo | dm | book | personal
source_url: <if applicable>
source_author: <if applicable>
source_date: <when authored, not when captured>
captured_via: inbox | gmail | manual | voice | calendar | mcp
captured_at: <iso8601>
verbatim: <true | false>            # is the body the exact thing said?
```

### `entity` — a stable real-world thing

A person, organisation, product, place, event. Survives across sources.

Extra fields:
```yaml
entity_kind: person | org | product | place | event | role
aliases: [<other names>, ...]      # canonicalisation key
attributes: <free key-value>
relationships: [{type, target, confidence}, ...]
```

### `concept` — an idea or pattern

A thing you think about. Cluster point for sources. Compounds across regions.

Extra fields:
```yaml
concept_kind: theory | framework | technique | hypothesis | preference
mature: <true | false>             # has this graduated to evergreen
related_concepts: [<concept_id>, ...]
```

### `project` — a thing you're building

A multi-stage commitment. Has phases, deliverables, rings, surfaces.

Extra fields:
```yaml
project_status: inbox | scoping | active | paused | shipped | archived
phases: [{name, status, deliverable}, ...]
deliverables: [<output_id>, ...]
collaborators: [<person_id>, ...]
target_date: <iso8601 | null>
parent_project: <project_id | null>
```

### `idea` — a candidate project

A thing that wants to be a project but hasn't been phased yet. `/phase-an-idea` reads this.

Extra fields:
```yaml
idea_origin: capture | brief | retrieval | dream | walk
trigger_page: <page_id | null>
phase_status: unphased | phasing | phased | promoted_to_project | discarded
phased_plan: <output_id | null>    # if /phase-an-idea has run
```

### `output` — something the system produced

A brief, a phased plan, a synthesis, a debaiser report, a calendar event suggestion.

Extra fields:
```yaml
output_kind: brief | synthesis | debaiser | phased_plan | retrieval | onboarding_snapshot
gear: 1 | 2 | 3 | null              # for retrievals
input_pages: [<page_id>, ...]
prompt_used: <prompt_name>
applied_at: <iso8601 | null>        # when user marked it applied
applied_outcome: <free text | null>
```

### `dimension` — an Ikigai region rollup

The 9 region pages. Auto-maintained but readable.

Extra fields:
```yaml
dimension_id: love | good_at | world_needs | paid_for | passion | mission | profession | vocation | centre
member_pages: [<page_id>, ...]     # everything tagged with this region
density: 0.0..1.0                   # member_pages / corpus_size
last_audit: <iso8601>
```

### `lexicon` — a load-bearing term (new in v0.3)

An entry from `me/lexicon.md`, indexed for retrieval.

Extra fields:
```yaml
term: <string>
lens: <string>                     # short type/category
body: <markdown>
examples: <markdown>
load_bearing_for: [<concept_id>, ...]  # concepts that depend on this term's interpretation
```

---

## 3. Lifecycle states

| State | Meaning | Retrieval default |
|---|---|---|
| **inbox** | Captured, not yet processed | excluded from retrieval |
| **canonical** | Processed, regions tagged, valid | included |
| **evergreen** | Mature, high confidence, surfaced often | boosted |
| **superseded** | Replaced by a newer page | excluded unless asked |
| **archived** | Kept for history, not for retrieval | excluded |

State transitions are explicit. The watcher promotes inbox→canonical after `/understand` runs cleanly. The keeper proposes evergreen after high reinforcement. Supersession is never automatic — only the user (or `/phase-an-idea` and `/debaiser` with confirmation) sets it.

---

## 4. Compounding ripples (new in v0.3)

When a page is created or updated, the ingest pipeline computes which other pages it ripples into. Two pages ripple if they share at least one Ikigai region AND at least one other classifier (concept, project, person, ring, surface).

`compounding_ripples` is the result. The Lens view reads this. The compounding flash overlay reads this. The brief generator uses ripple density to pick "today you should look at X — it ripples into 4 active regions and last reinforced 14 days ago."

The user never sees ripples computed manually. The system always shows them.

---

## 5. Migration from v0.2

v0.2 → v0.3 changes:

1. **Added** `ring`, `expression_surface`, `sovereignty_layers`, `lexicon_terms`, `compounding_ripples` fields.
2. **Added** `lexicon` page type.
3. **Renamed** `ikigai_regions` semantics — same field, but values now also include the explicit centre intersection.
4. **No breaking changes** to existing v0.2 frontmatter — all existing pages remain valid; new fields default to null/empty.

Migration script: see `s2/03-vault-init.sh`. Backfill is non-destructive.

---

## 6. The contract

Every page in `wiki/` MUST have valid v0.3 frontmatter. The watcher rejects pages that don't. There is no soft validation. If `/understand` produces something invalid, it gets rewritten until it's valid before being committed.

**This is not bureaucracy. This is the load-bearing layer.** The system's intelligence comes from being able to query against this contract reliably. Loose frontmatter = loose retrieval = drift.
