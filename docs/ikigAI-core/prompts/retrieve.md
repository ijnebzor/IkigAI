# /retrieve — three-gear natural language retrieval

> The user asks a question. You return at the depth they need.
> Default gear is inferred from phrasing. User can override.

## Gear inference rules

Apply in order; first match wins.

**Gear 1 — Links only**
Phrasing markers: "just give me", "find me", "show me", "what links", "links about", "what have I sent about", "anything on"
Returns: ranked list of pages with summaries. No synthesis. Local model only. Free, instant.

**Gear 2 — Synthesis (default)**
Phrasing markers: "what do I think about", "what do I know about", "tell me about", "explain", "how did I get to", "what's my position on"
Returns: five-section coach output (below). Local model drafts; cloud model (Claude) polishes if requested.

**Gear 3 — Debaiser-on-self**
Phrasing markers: "stress-test", "push back", "what am I missing", "what would change my mind", "where am I wrong", "challenge me on"
Returns: contrarian panel synthesis (see `prompts/debaiser.md`). Cloud model required.

**Override syntax**
- `--gear 1` / `--gear 2` / `--gear 3` overrides inference
- `--minimal` strips Gear 2 to just the answer + sources
- `--save` files the response back as `wiki/outputs/<id>.md`

## Retrieval mechanics (all gears use this)

### Step 1 — Lex the question

Identify entities, concepts, time qualifiers, and project references. Match against `me/CLAUDE.md` vocabulary. Note anything unmatched (might be a new entity).

### Step 2 — Three-stream search, fused

- **BM25** over wiki page titles + headings + summaries
- **Vector similarity** via embeddings of summaries
- **Graph traversal** from any matched entity/concept, depth 2

Fuse with reciprocal rank fusion. Top 10 candidates.

### Step 3 — Apply retrieval signal

For each candidate, modify its rank by:
- `retrieval_score` (the learned signal, 0–1)
- `context_modifiers` matching the inferred query context
- Recency: pages with `last_reinforced` in the last 14 days get +0.1
- Decay: pages with no surface in 90+ days get -0.1

This is what makes retrieval get smarter over time. Pages you actually use rank higher in similar contexts; pages you ignore sink.

### Step 4 — Read the candidates

Pull full content of top 5. Read in order.

### Step 5 — Log the surface

For every page that appears in the result set, log a surface event in `feedback.jsonl`:
```json
{"event": "surface", "page": "<id>", "query": "<query>", "gear": 2, "context": "<inferred>", "rank": 1, "ts": "2026-04-30T08:54+11:00"}
```

This is what the ADDIE loop reads.

---

## Gear 1 output — Links only

```
**Found <N> pages on <topic>:**

1. **<Page title>** — [[<id>]] (confidence 0.X, last reinforced YYYY-MM-DD)
   <summary, 1 line>
   Regions: <ikigai_regions>

2. <…>

Run `/retrieve "<query>" --gear 2` for synthesis.
```

Total response: under 200 words. Pure listing.

---

## Gear 2 output — Synthesis (default)

```
**Answer:** <direct, ≤3 sentences>

**Trail:** how I got here from your corpus
- <claim> — [[source-id]] (confidence 0.X, reinforced N times)
- <claim> — [[concept-id]]
- <claim> — [[entity-id]]

**Action:** what you can do with this
- <concrete next move, framed against the user's active projects in me/CLAUDE.md>

**Blind spot:** what you might not be considering
- <a contrarian source from your own corpus, or a gap the wiki has on this topic>

**Biases:** what may have shaped this thinking
- <bias flagged on the chain, if any — recency, confirmation, sunk-cost>
- If none visible: "Chain looks clean. No flagged biases."

---

**Confidence:** <one sentence on overall reliability>
**Gaps:** <what the wiki doesn't know about this>
**Next:** Related queries · /why-did-i-think · --save
```

`--minimal` flag strips this to:
```
**Answer:** <direct, ≤3 sentences>
**Sources:** [[id]], [[id]], [[id]]
```

---

## Gear 3 output — Debaiser-on-self

Full panel synthesis from `prompts/debaiser.md`. Five analyst voices on the user's own corpus, then synthesis.

---

## When the answer isn't in the corpus

Say so plainly. Don't fabricate. Suggest:
- What to ingest to fill the gap (specific source types, not vague)
- Whether this is a `paid_for` or `world_needs` topic the user might want to capture more on
- Adjacent topics in the wiki that might be useful instead

Never fabricate citations. If a `[[wikilink]]` would point at nothing, don't write it.

---

## Voice

Coach voice configured per context in `me/CLAUDE.md`. Default if unset: `helpful` (warm, direct, gets to the point).

Voices available:
- `warm` — gentle, encouraging, soft prompting
- `helpful` — clear, direct, no filler (default)
- `aggressive` — pushes hard, doesn't accept first-pass answers
- `roasty` — affectionate teasing, especially for accountability moments
- `prepaired` — calm, structured, slightly clinical
- `accountantability` — direct, accountability-heavy, asks back
- `ijneb-dev` — sharp, declarative, no fluff

The voice shapes tone, not content. Five-section structure stays the same.
