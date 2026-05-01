# Secondary operations (v0.3)

> Smaller, supporting prompts.
> Most live as MCP tools after S2; some run as cron-driven daemons.

---

## /surface

Bidirectional discovery. The user asks "what should I look at?" without naming a topic.

### Read first
- `me/CLAUDE.md`, `me/ikigai.md`, `me/lexicon.md`
- Last 30 days of activity
- THE SCOUT's queue

### Process
1. Find pages with `last_surfaced` >60 days, `confidence` >0.6 (forgotten gold)
2. Find pages with high `surface_count` but low `use_count` (false signal — drop their score)
3. Find recent pages with high overlap to active projects (under-leveraged)
4. Find regions that have gone quiet vs aspirational (drift)
5. Pick top 5; rank by likely surprise + utility

### Output
```markdown
**Five things you might re-engage with:**

1. **[[page]]** — <why surface, what it connects to now>
   Lights up: <regions>
2. ...
```

Voice: same as `brief`.

---

## /lint

The cleanup operation. Flags drift, doesn't fix it.

### Read first
The whole `wiki/` tree.

### Run nightly
Default: 02:00 local, by THE KEEPER daemon.

### Checks

**Schema:** Every page has `id`, `type`, `summary`, `created`, `updated`, `ikigai_regions`, `status`, `schema_hash`.

**Region implication:** If `ikigai_regions` includes both `love` and `good_at` but not `passion`, flag.

**Stale schema:** Any page with `schema_hash != v0.3` queues for migration.

**Orphans:** Sources/ideas with no inbound links, status `canonical` for >30 days, surface_count zero.

**Bidirectionality:** A → [[B]] but B has no link back. Both should mention each other; flag missing back-links.

**Dead wikilinks:** `[[X]]` that points to nothing.

**Tag drift:** New tags appearing in `<3 pages with no consolidation note.

**Confidence drift:** `confidence > 0.8` AND `last_reinforced > 90 days` AND `surface_count == 0` → drop to 0.6, note in log.

**Lexicon coverage:** Pages with `lexicon_terms` referencing a term not in `me/lexicon.md` → flag for user to author.

**Echo chambers:** Confidence >0.8, reinforcements >5, contradictions = 0 → queue for THE DEBAISER.

### Output
`state/lint-<date>.md` with sections: schema_violations, orphans, bidirectionality, dead_links, tag_drift, confidence_drift, lexicon_gaps, echo_chambers.

Surface count in next morning's brief if >0.

---

## /why-did-i-think

Trace the genesis of a current claim.

### Inputs
A claim, page id, or wikilink.

### Process
Walk `derived_from` chain to root. Read each page. Reconstruct the trail.

### Output
```markdown
# Why I think <claim>

## The trail
1. **<root source>** ([[id]], <date>)
   <summary>
   <drivers, biases captured at the time>

2. **<derived>** ([[id]], <date>)
   Built on (1). <how it shifted the claim>
   <drivers, biases>

3. **<current>** ([[id]], <date>)
   Built on (2). <where you are now>

## The pattern
<bias-watcher style: which patterns shaped the trail?>

## What's been tested
<which steps had contrarian challenges, which didn't>

## What's still untested
<weakest steps in the chain — most likely points of failure>
```

Voice: `prepaired` — clinical, structured.

---

## /onboard

See `prompts/onboard.md` — first-class always-on operation.

---

## /lexicon-suggest

When THE WATCHER sees a load-bearing term used in 3+ sources without an entry in `me/lexicon.md`, propose adding it.

### Process
1. Read the term across sources
2. Identify the user's apparent meaning vs encoded meaning
3. Draft a candidate entry

### Output
```markdown
**Lexicon suggestion:**

You've used "**<term>**" in <N> recent sources. Across them, your usage
seems to mean <user-apparent-meaning>, which differs from the
encoded reading of <encoded-meaning>.

Suggested entry:
```yaml
term: <term>
definition: <neutral definition>
lens: <user-apparent meaning, with example>
seeded: true
```

Want to keep, edit, or skip?
```

Surfaced in brief, never forced.

---

## /debaiser-on-demand

Wrapper around `prompts/debaiser.md` for explicit invocation. Single MCP tool, accepts topic or page id.

---

## /idea-flow-check

Run weekly (Sunday evening). Looks at:
- Ideas captured this week
- Ideas phased this week
- Ideas accepted into calendar this week
- Ideas declined / parked
- Phase 1 stages actually started
- Phase 1 stages shipped

### Output
```markdown
# Idea flow — week of <date>

**Captured:** <N>
**Phased:** <M>
**Accepted to calendar:** <K>
**Started:** <J>
**Shipped:** <L>

**Conversion rates:**
- Capture → Phase: <pct>
- Phase → Accept: <pct>
- Accept → Start: <pct>
- Start → Ship: <pct>

**Stuck:** <ideas in 'phased' >14 days>
**Stalled:** <ideas in 'accepted' but never started, slot passed>
**Patterns:** <which kinds of ideas convert; which don't>
```

Surfaced in Sunday evening brief.

---

## /apply

When user marks an output as applied:
1. Update output's `applied: true`, `applied_at: <ts>`
2. Bump `retrieval_score` of all `sources_cited` in the output
3. Log to `state/feedback.jsonl` for ADDIE
4. After 24h, daemon prompts: "How did it go?"

User responds → write outcome as new source → link to original idea → update idea status if shipped/iterated.
