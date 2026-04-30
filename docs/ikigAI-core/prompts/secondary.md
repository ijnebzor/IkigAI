# /surface — linkage-scout daemon

> Runs nightly. Walks the graph. Surfaces non-obvious connections.
> Output feeds the next morning's brief.

## Process

### 1. Find candidate page pairs
For each high-confidence page (`confidence ≥ 0.7`, `status: canonical|evergreen`):
- Find pages with overlapping `tags` but no current `[[wikilink]]` connection
- Find pages with overlapping `extracted_entities` but no link
- Find pages in adjacent `ikigai_regions` with semantic similarity ≥ 0.85 but no link

### 2. Score each candidate linkage
- Tag overlap weight 1.0
- Entity overlap weight 1.5
- Region adjacency weight 0.5
- Semantic similarity weight 1.0
- Penalty if either page has been surfaced together in the last 7 days (-0.5)

Top candidates above threshold (configurable per-user, default 2.5) → linkage queue.

### 3. Detect echo chambers
For each high-confidence claim with ≥5 reinforcements:
- Check for any contradicting page in the corpus
- If none exists → flag as echo-chamber candidate
- Surface in next brief: "Want a debaiser pass on this?"

### 4. Detect decay candidates
- Pages where `last_reinforced` > 60 days ago AND `confidence` was previously > 0.7
- Surface as: "You may have moved on from this — confirm or recapture."

### 5. Detect orphans
Pages with `status: canonical` and zero inbound links from sources. Either the entity/concept isn't really live in the user's thinking, or sources weren't properly linked at ingest. Surface for review.

### 6. Output to queue
Write to `state/scout_queue.jsonl` with timestamp, candidate type, page IDs, score. The brief generator reads this file and picks the top 1–3 to surface in the morning.

### 7. Cleanup
Truncate `scout_queue.jsonl` to last 7 days. Older discoveries that weren't surfaced get archived; if they were genuinely useful they'll reappear when corpus changes.

## Cadence

Nightly cron, configurable. Default: 02:00 local time.

---

# /lint — vault health & lifecycle

> Runs daily (separately from scout). Keeps confidence honest.

## Operations

1. **Confidence decay** — pages with `last_reinforced` > 30 days ago: -0.1 confidence (floor 0.2). Append decay note to page footer.

2. **Retrieval-score decay** — pages with `last_surfaced` > 90 days ago: -0.1 retrieval_score (floor 0.1).

3. **Promotion** —
   - `inbox` → `canonical`: ≥2 sources OR ≥3 inbound `[[wikilinks]]` AND no unresolved contradictions
   - `canonical` → `evergreen`: ≥5 reinforcements AND `confidence ≥ 0.8` AND no decay events in 60 days

4. **Schema staleness** — pages with `schema_hash` < current schema version: list for re-ingest.

5. **Tag drift** — tags used <3 times across the vault: surface for consolidation.

6. **Entity drift** — entity pages with no source backlinks: surface for review.

7. **Output to** `log.md` with structured summary. No automatic destructive actions; user decides what to consolidate or archive.

## Cadence

Daily cron, configurable. Default: 03:00 local time, after scout.

---

# /why-did-i-think — provenance trace

> Walk a claim's `derived_from` backwards. Surface the trail. Identify load-bearing nodes and biases.

## Inputs

A claim, a `[[wikilink]]`, or a paraphrase.

## Output format

```
TARGET: <[[wikilink]] or claim text>
Confidence: <X> (reinforced <N> times since <date>)

PROVENANCE TREE:
└─ <claim>
   ├─ derived_from: [[source-A]] (confidence 0.X, captured YYYY-MM-DD)
   │  ├─ source: <URL or origin>
   │  ├─ drivers at capture: [curiosity, problem-solving]
   │  └─ biases flagged: [recency]
   ├─ derived_from: [[concept-B]] (confidence 0.X, reinforced 3x)
   │  └─ derived_from: [[source-C]]  ← LOAD-BEARING
   └─ supersedes: [[earlier-claim]] (date, why)

DRIVERS (across the chain): <union>
BIASES (across the chain): <union>

CONTRADICTIONS:
- [[source-D]] disagrees on <specific point>. Currently weaker (confidence 0.4 vs target 0.7).

WHAT WOULD CHANGE MY MIND:
- A source that establishes <X> with primary evidence
- A direct experience showing <Y>
- Reinforcement that <load-bearing-source> is wrong

CURRENT STANCE: <one sentence honest summary, including remaining doubts>
```

## What NOT to do
- Don't fabricate provenance. If `derived_from` is empty, say so: "This claim has no captured provenance — it may be inherited prior knowledge or never sourced."
- Don't editorialise. Surface the chain; let the user judge.

---

# /onboard — conversational setup (S5 implementation)

> Spec only at v0.2. Built fully in S5 when the friend onboards.

## Conversation flow

1. **Welcome** — explain what IkigAI is in two sentences. No more.

2. **Current Ikigai** — *"Tell me about a typical week. What do you spend most of your time on?"* Listen, infer tentative regions across love/good_at/world_needs/paid_for. Confirm: *"Sounds like your current Ikigai is mostly profession (good_at + paid_for) with some passion (love + good_at) on the side. Does that match?"*

3. **Aspirational Ikigai** — *"Where do you want to be in 12 months? What gap do you want to close?"* Capture as `me/ikigai.md`.

4. **Vocabulary seed** — *"Who are the most important people in your life right now? Top 3 active projects? Recurring topics you think about?"* Build the first version of `me/CLAUDE.md` collaboratively.

5. **Capture preferences** — share-sheet, voice, hotkey, email, share targets — what does the user have access to and want to use?

6. **Coach voice** — sample 2–3 voices on a real example, user picks default. Note context-specific overrides if they have any.

7. **Brief cadence** — daily morning brief, weekly Sunday-evening pattern report, ambient on-app-open, all three? Pick what fits.

8. **First capture** — *"Send me one thing now. A quote, a link, a thought. Anything."* Process it end-to-end. Show the result. Ask: *"Did this land? Anything I should adjust?"* First feedback signal.

9. **Wrap-up** — explain how to use it tomorrow. Set expectation: *"The system gets better the more you use it. The first 30 days, expect rough edges. After that, it'll know you."*

## Time budget

15 minutes for a technical user. 30+ minutes for a non-technical user. Same conversation tree; depth follows user signal. The agent reads cues and goes deeper only when the user wants more detail.

## Output

- `me/CLAUDE.md` populated with vocabulary and preferences
- `me/ikigai.md` populated with current and aspirational Ikigai
- `me/config.yml` populated with capture/voice/cadence preferences
- One real source in `wiki/sources/` from the first capture
- Welcome message in `wiki/outputs/welcome.md`

## Voice

`warm` always. This is the first impression. No matter what voice they pick for ongoing use, onboarding is warm.
