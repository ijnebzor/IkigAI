# /understand — the ingest operation

> Read incoming material, classify through MY lens, write a valid v0.3 page.

Triggered by: file landing in `inbox/`, manual run, or MCP call from any client.

---

## Inputs

You receive:

1. **The raw source** (markdown, transcribed audio, pasted text, link contents).
2. **Source metadata** (where it came from, when, by whom — if known).
3. **`me/CLAUDE.md`** — projects, people, concepts, vocabulary, current working context.
4. **`me/ikigai.md`** — current and aspirational Ikigai with concentric-rings architecture.
5. **`me/lexicon.md`** — load-bearing terms with my interpretive lens. Read this BEFORE classifying.
6. **`core/schema/SCHEMA.md`** — the v0.3 contract this output must honour.
7. **The recent corpus** — last ~50 canonical pages, for canonicalisation and supersession detection.

---

## Output

A single valid v0.3 markdown page with frontmatter. Status starts as `canonical` if classification succeeded; `inbox` if anything was unclear.

---

## Process

### Step 1 — read the lexicon first

Before reading the source, read `me/lexicon.md`. The lexicon defines what load-bearing terms mean **to me**. If the source uses any lexicon term, the classification must use my interpretive lens for that term, not the source's encoded one.

**Concrete example.** If the source says "we need data sovereignty in healthcare" and my lexicon defines sovereignty as a five-layer concept (data, cognitive, tooling, narrative, epistemic), the resulting page tags `sovereignty_layers: [data]` explicitly, and `lexicon_terms: [sovereignty]` is set. The classification is wrong if it imports the source's reading of "data sovereignty" as a single undifferentiated concept.

### Step 2 — read the source

Extract the substantive claims. Strip rhetorical flourishes. If the source is a transcript, distil to claims and quotes. Verbatim quotes go in the body with attribution; everything else is paraphrased.

### Step 3 — canonicalise

Search the recent corpus for:
- An entity with this name (or alias) → reference its `id`, do not create a duplicate.
- A concept that captures this idea → reference and reinforce it; bump `last_reinforced`.
- A near-identical source already captured → mark this one as `archived` and link.

If the source contradicts an existing canonical page, set `contradicts: [<old_id>]` on the new page. **Do NOT auto-supersede.** Surface the contradiction in the next brief.

### Step 4 — classify against the four-axis Ikigai

Tag `ikigai_regions` through MY lens. Be honest. The four axes:

- `love` — would I do this anyway? Does this fascinate me?
- `good_at` — am I durably skilled at what this implicates?
- `world_needs` — does the world need this? Be careful not to tag generously here. Most things don't qualify.
- `paid_for` — am I paid (now or credibly soon) for this?

Plus the intersections, included explicitly when they apply:

- `passion` (love + good_at)
- `profession` (good_at + paid_for)
- `vocation` (paid_for + world_needs)
- `mission` (world_needs + love)
- `centre` (all four)

If three of four axes apply, list those three plus the relevant intersection. If all four, list all four plus `centre`.

If nothing applies, leave the list empty. Empty is valid. Not everything is Ikigai-coded.

### Step 5 — classify against the ring architecture

This is separate from regions. The four-circle Ikigai is the test; the rings are the architecture.

- `ring: identity` — this is about being the AIthropologist. Defining who I am.
- `ring: principle` — this is about sovereignty. Set `sovereignty_layers: [...]` listing which layers (data, cognitive, tooling, narrative, epistemic).
- `ring: surface` — this expresses identity through one of the four channels. Set `expression_surface: [research|tooling|discourse|practice]`.
- `ring: funding` — this is about how the work gets funded (salary, NFP, commercialisation, brand-adjacent).
- `ring: none` — most things; doesn't sit on a specific ring.

A page can have a ring AND ikigai_regions. They're orthogonal axes.

### Step 6 — compute compounding ripples

For each canonical page in recent corpus, check if it shares at least one ikigai_region AND at least one other classifier (concept, project, person, ring, surface) with the new page. List those `page_id`s in `compounding_ripples`.

This is what makes the Lens view light up. This is what the brief reads to surface "this thing you're capturing connects to four other things you're already working on." This is the mechanism behind compounding visibility.

If the corpus is empty, ripples are empty. Fine.

### Step 7 — set provenance and confidence

- `derived_from`: [] for raw sources; [<input_page_id>] when a synthesis or output produced this.
- `confidence`: start high (0.85+) for verbatim sources, lower (0.6-0.8) for paraphrased synthesis, lower still (0.4-0.6) for inferred classifications.
- `drivers`: short list of WHY this got captured. ("inbox watch on Twitter saved", "user voice memo at 11pm", "MCP call from Claude Desktop").
- `biases`: known limits. ("source has commercial interest in X", "captured during high-stress week", "was responding to a specific Slack thread context now lost").

### Step 8 — write the body

Markdown. Voice: matter-of-fact, dense, scannable. No filler. Structure:

1. **One-line summary** — what this page IS, in one sentence.
2. **Substantive content** — the claims, quotes, key passages. Verbatim where useful, paraphrased where compression matters.
3. **Why it matters** — one short paragraph relating this to my current work and current Ikigai state. Honest. If it doesn't matter, say so.
4. **Open questions** — things this raises that aren't resolved. Becomes the seed for `/phase-an-idea` later.
5. **Links** — bare-link list to related pages by id, with one-line context per link.

### Step 9 — validate

Before writing, validate the frontmatter against `core/schema/SCHEMA.md`. If anything fails:
- Required field missing → status: inbox, note the gap in `drivers`.
- Region tag is hallucinated → drop it.
- Ring is wrong → none is fine.

Do NOT ship invalid frontmatter to canonical. The watcher rejects it.

---

## Voice and tone

Matter-of-fact. The page is for my future self. Future-me has limited time and reads what's useful. Don't editorialise. Don't motivate. Don't sell.

If the source is voice memo or chat-paste, retain my actual voice — including swearing, half-thoughts, course corrections. Don't sanitise. The lexicon and my prior corpus is what tells you what my voice sounds like.

---

## Edge cases

- **Empty body** — capture as `inbox` status with a `drivers` note. Will be re-run when there's enough to classify.
- **Highly contested topic** — flag with `biases: [contested]` and surface in next debaiser run.
- **Recursive reference** (this page is about a page) — `derived_from` links the parent.
- **The source contradicts the lexicon** — capture the source AND propose a lexicon update in the body (don't write to lexicon directly; surface for user review).
- **The source is from me, talking about me** — `verbatim: true`, `entity_kind: self` if it's an entity-type page about my own state.

---

## What this operation refuses to do

- Tell me what to do. The body has open questions, not directives.
- Tag generously. Empty regions are honest.
- Auto-supersede. Contradictions surface; only I (or a debaiser run) decide.
- Write outside the schema contract. If it can't be valid v0.3, it stays inbox.
