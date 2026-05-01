# /retrieve — the retrieval operation

> Surface what the corpus already knows. Three gears, three depths.

Triggered by: query in any client (PWA search, Claude Desktop MCP call, Claude Code, brief generator). The user's phrasing implies the gear; if not, the system asks.

---

## The three gears

| Gear | Latency | Cost | Where it runs | What it returns |
|---|---|---|---|---|
| **G1 — Links** | <1s | $0 | NUC, local model | Top 10 page hits with one-line context. Pure ranking. No synthesis. |
| **G2 — Synthesis** | 5-15s | low | NUC drafts → Claude polishes | 5-section synthesis: claim, evidence, friction, ripples, open questions. |
| **G3 — Debaiser-on-self** | 30-90s | medium | Claude required | Five analyst voices contradict each other on what the corpus thinks. Lens-checker flags drift. |

Retrieval may go SOTA/cloud. Capture and classification stay local. The principle: where the depth genuinely earns the cost, pay it; everywhere else, run free locally.

---

## Inputs

1. **The query** — natural language.
2. **The intent signal** — gear (if explicit) or rough indicator from phrasing.
3. **The user's current context** — recent captures, current stage, recent retrievals (last 24h).
4. **`me/CLAUDE.md`**, **`me/ikigai.md`**, **`me/lexicon.md`** — always.
5. **The vault index** — vector index over canonical pages, graph index over relationships.
6. **`feedback.jsonl`** — surface/ignore/use signals; used for retrieval-score evolution.

---

## Gear 1 — Links

```
Query: "what have I captured about Mac Studios"

→ Vector top-30 from canonical, filter by retrieval_score > threshold.
→ Re-rank with context modifiers (e.g., if this is a work-strategy retrieval, boost work-strategy modifier).
→ Return top 10 with: title, one-line summary, ikigai_regions tags, last_reinforced, link to page.

No synthesis. No interpretation. Just what's there.
```

Voice: silent. The system surfaces and steps back. The user reads.

---

## Gear 2 — Synthesis (default)

```
Query: "what am I really thinking about Mac Studios"

→ G1 to find the 8-15 most relevant canonical pages.
→ Read them. Extract the claims.
→ NUC's local model writes a structured draft.
→ Claude polishes for clarity, voice, lens-fidelity (uses lexicon).
→ Return 5-section synthesis.
```

The five sections, every time:

1. **Claim** — what does the corpus say, in one paragraph?
2. **Evidence** — which pages support it? Bullet with one-line context per page, page_id linked.
3. **Friction** — where does the corpus disagree with itself? Pages that contradict, or sit in tension.
4. **Ripples** — what regions does this synthesis light up? Which other concepts/projects intersect?
5. **Open questions** — what's missing? What would I need to capture to resolve the friction?

The voice **shows overlap, never direct**. It does not say "you should." It says "the corpus contains X. It also contains Y. They overlap on Z. They diverge on W."

The user remains the thinker. The synthesis is the framework overlay laid over what's already there.

---

## Gear 3 — Debaiser-on-self

```
Query: "what am I really thinking about Mac Studios" + flag: debaiser
or:    "challenge me on Mac Studios"

→ Five voices, plus a lens-checker.
→ Each voice reads the corpus's stance on the topic.
→ Each voice argues a different framing.
→ Lens-checker validates against me/lexicon.md to flag terminological drift.
→ Output: synthesis-of-disagreement with explicit framing tags.
```

The five analyst voices (forked from PoliticalDebAIser, retargeted at the self):

1. **The Optimist** — "the corpus is correctly bullish. Here's why this is a load-bearing investment."
2. **The Pessimist** — "the corpus is wrong about the upside. Here are the cited pages most exposed to motivated reasoning."
3. **The Pragmatist** — "the corpus is right about the want, wrong about the timing. Reframe."
4. **The Sceptic** — "the corpus is reading something into this that isn't there. Show me the actual evidence."
5. **The Outsider** — "the corpus is locked into a frame. Here's a frame it's never tried."

Plus:

6. **The Lens-Checker** — reads `me/lexicon.md`. Flags any voice (including the corpus's own pages) that use a load-bearing term in a way that drifts from the user's defined lens. Lists the drift instances. Does not argue them.

Output structure:

```
## What the corpus says
<2 sentence neutral summary>

## Where the analysts split
- Optimist: <one paragraph>
- Pessimist: <one paragraph>
- Pragmatist: <one paragraph>
- Sceptic: <one paragraph>
- Outsider: <one paragraph>

## Drift detected
<lens-checker findings, or "none">

## Where this lands
<one paragraph: not "you should" but "if you want X, optimist line. if you want Y, sceptic line. lens-checker says watch out for Z.">
```

Gear 3 is the strongest tool in the box. It's expensive. Run it when:

- A concept has been reinforced 5+ times without any contradiction logged.
- You're about to commit (a phased plan, a calendar block, a public post).
- The brief generator suggests it.
- You explicitly ask.

---

## Gear inference (from phrasing)

Heuristics:

- **G1** — "show me", "find", "list", "what was the", "where did I", "links to"
- **G2** — "what do I think about", "summarise", "what's my position on", "tell me about"
- **G3** — "challenge me on", "where am I wrong", "debaiser", "blind spots", "argue both sides"

If unclear, default to G2. If the user's recent context shows three G3 runs in a row, suggest G1 next time ("you've been going deep — want a quick scan?"). If the user's recent context shows ten G1 runs without a G2, suggest G2 ("you've been browsing — want me to synthesise?").

---

## Retrieval-score evolution

Every retrieval logs to `state/feedback.jsonl`:

```json
{"ts": <iso>, "gear": 1|2|3, "query": "...", "surfaced": ["page_id", ...], "cited": ["page_id", ...], "ignored": ["page_id", ...]}
```

The keeper daemon reads this nightly:

- Cited pages: `retrieval_score += 0.05`, `use_count++`.
- Ignored pages (surfaced 3+ times in 30 days, never cited): `retrieval_score *= 0.95`, `ignored_count++`.
- Pages not surfaced in 90 days: `retrieval_score *= 0.98` (gentle decay).

Per-context modifiers track which contexts a page is most useful in (work_strategy, creative, research, relational). The classifier gets sharper over time without the user grading anything.

---

## What retrieval refuses to do

- Recommend. The user remains the thinker.
- Pretend the corpus knows things it doesn't. If the corpus is sparse on a topic, say so.
- Auto-cite. Citations are explicit; if a page wasn't actually used, it doesn't go in `cited`.
- Hide drift. The lens-checker fires every G3. Drift findings are surfaced even when they're inconvenient.
