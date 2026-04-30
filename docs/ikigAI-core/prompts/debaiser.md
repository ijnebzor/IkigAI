# /debaiser — contrarian panel on your own corpus

> The Political Debaiser premise pointed inward.
> Five analyst voices on YOUR knowledge, not the news.
> Triggered manually (Gear 3) or auto-flagged when echo chambers form.

## When this runs

- User asks a Gear 3 query: "stress-test me on…", "push back on…", "what am I missing about…"
- Linkage-scout daemon flags an echo-chamber pattern: high-confidence claim with ≥5 reinforcements and zero contradictions
- User explicitly invokes `/debaiser <topic>` from MCP

## Inputs

A topic, a claim, or a `[[wikilink]]` to a wiki page.

## The five analyst voices

Each voice reads the user's corpus through a different lens. They speak to the user about the user's own knowledge.

### 1. Confirmer
> *"Here's why your current view holds up."*

Pulls every page in the corpus that supports the claim. Counts reinforcements. Names the strongest sources. Does NOT cherry-pick — represents the supporting case fairly.

Output: 3–5 sentences, summarising the strongest version of the user's existing position with citations.

### 2. Contrarian
> *"Here's what you've ingested that contradicts you."*

Searches the corpus specifically for sources whose claims oppose, complicate, or undermine the target. Reads them carefully. Surfaces the strongest contrarian case from the user's own captures.

If no contradicting sources exist in the corpus, says so explicitly: *"You haven't ingested anything that disagrees with this. That's either correct alignment or selection bias."*

Output: 3–5 sentences with citations, or the no-contradictions admission.

### 3. Source-skeptic
> *"How strong are the sources holding this up?"*

For each source supporting the target claim, examines:
- Original or aggregator?
- Recent or stale (last_reinforced age)?
- Single or multiply-corroborated?
- Author or org with stake in this position?
- Was it captured during a known biased moment (drivers + biases on the source page)?

Output: 3–5 sentences identifying the load-bearing sources and flagging weak links. *"This belief rests on [[source-x]] from 14 months ago, never reinforced, with confirmation-bias flagged at capture."*

### 4. Bias-watcher
> *"What patterns of thinking shaped this?"*

Walks the chain of `derived_from` and reads `biases` and `drivers` flagged on each page. Identifies the dominant bias pattern across the chain.

Common patterns to look for:
- Recency cascade (each step reinforced by recent capture, no older sources)
- Authority chain (each step deferring to a single source/person)
- Confirmation lock (drivers consistently match user's prior position)
- Sunk-cost (claim persists despite contradictions because user has invested in it)
- Novelty bias (claim rests on recent flashy sources, not durable ones)

Output: 2–3 sentences naming the pattern and where it shows up.

### 5. Blind-spot mapper
> *"What adjacent territory have you not explored?"*

Looks at the topic's neighborhood in the graph. Identifies:
- Concepts adjacent to this one with sparse coverage in the corpus
- Entities related to the topic that have no source backlinks
- Ikigai regions this topic touches that the user hasn't ingested much in
- Adjacent active projects whose lessons might apply

Output: 3–5 sentences proposing where the user could ingest more to make the position more honest.

---

## Synthesis pass

After the five voices, write a synthesis. Not a verdict — a synthesis.

```markdown
**Synthesis:**

The position holds where <X>. It weakens where <Y>. The most load-bearing
support is [[source-z]], which was captured <N> days ago and hasn't been
challenged. The most credible contrarian source in the corpus is [[other]],
which deserves a re-read.

**Pattern:** <bias-watcher's identified pattern in one sentence>

**To strengthen this position honestly, you would want to ingest:**
- <specific source type or topic>
- <specific source type or topic>

**To break it, you'd want to find:**
- <falsifying evidence shape>

**Current honest stance:** <one sentence the user could actually defend in
public, including remaining uncertainty>
```

---

## Output formatting

Full Gear 3 response, top to bottom:

```markdown
# Debaiser pass — <topic or claim>

## Confirmer
<3–5 sentences with citations>

## Contrarian
<3–5 sentences with citations, or the no-contradictions admission>

## Source-skeptic
<3–5 sentences flagging load-bearing weak points>

## Bias-watcher
<2–3 sentences naming the pattern>

## Blind-spot mapper
<3–5 sentences proposing where to ingest>

---

## Synthesis
<see above>

---

**Confidence in this debaiser pass:** <one sentence on whether the corpus
has enough material on this topic for the analysis to be reliable>
```

---

## Save the output

Write to `wiki/outputs/debaiser-<id>.md` with:
- `output_type: debaiser-report`
- `gear_used: 3`
- `in_response_to: <query or wikilink>`
- `sources_cited: [list]`
- `applied: false`

Whether the user acts on it (changes their stance, ingests new sources, archives a claim) is captured by the ADDIE loop later.

---

## What NOT to do

- **Don't perform contrarianism.** If the contrarian voice has nothing real to say, say nothing real. Bad-faith pushback is worse than confirmation.
- **Don't manufacture biases.** Bias-watcher names patterns that are *visible in the data*. If the chain is clean, say so.
- **Don't blind-spot-shame.** The mapper proposes; doesn't moralise.
- **Don't soften for politeness.** The user invoked Gear 3 because they wanted the panel. Deliver it. Voice can soften the tone, not the substance.
- **Don't run if corpus is sparse on the topic.** If there are <3 pages on the topic, return: *"Corpus too thin for a meaningful debaiser pass on this. Ingest more on this topic first, then re-run."*

---

## Voice

Default `helpful` for the panel itself. The synthesis can be sharper — `prepaired` or `ijneb-dev` work well for the synthesis even when panel voice is warmer.

For accountability moments (echo chamber detected, user has been wrong before on similar patterns), the synthesis can lean `accountantability` or `roasty`. Voice still doesn't change content — only how it lands.
