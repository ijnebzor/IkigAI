# /debaiser — adversarial-on-self synthesis

> Run the corpus against itself. Surface where I disagree with myself. Flag where my lexicon has drifted.

This is the operation forked from PoliticalDebAIser, retargeted from political analysis to self-analysis. Same five-voice architecture. Different mission: instead of finding bias in news coverage, find where my own captured corpus has motivated reasoning, blind spots, or terminological drift.

Run when:

- About to commit to something significant (a phased plan, a calendar block, a public output, a financial decision).
- A concept has been reinforced 5+ times in 30 days without any contradiction logged → auto-trigger candidate.
- The brief generator surfaces it.
- The user explicitly asks: "challenge me on X" or "debaiser X".

---

## Inputs

1. **The topic** — concept_id, project_id, or natural-language frame.
2. **The corpus's stance** — all canonical pages tagged with this topic, ranked by retrieval_score.
3. **`me/CLAUDE.md`** — current context, what I'm currently chasing.
4. **`me/ikigai.md`** — current vs aspirational Ikigai. Important: the analysts read this to challenge whether the corpus is pulling toward the aspirational state or away from it.
5. **`me/lexicon.md`** — load-bearing terms. The lens-checker uses this to flag drift.
6. **The contradiction history** — `state/contradictions.jsonl`. Past pages that contradicted earlier ones. Used to spot whether new contradictions are recurring.

---

## The six voices

### 1. The Optimist

Reads the strongest pro-stance pages. Argues the corpus is right and possibly underselling. Lists the load-bearing assumptions. Names the upside scenario the corpus doesn't quite let itself believe.

Tone: confident. Acknowledges the case the other voices will make. Specific.

### 2. The Pessimist

Reads the most cited pages and asks: where's the motivated reasoning? Which sources have a stake in the user agreeing? Which pages reinforce each other in a closed loop?

Tone: not contrarian for sport. Surgical. Names specific page_ids.

### 3. The Pragmatist

Argues the corpus is right about the **want** but wrong about the **timing or scope**. Reframes the question from "should I do this" to "what's the smallest version that tests the assumption."

Tone: builder-grounded. Concrete. Trades off.

### 4. The Sceptic

Argues the corpus is reading something into the data that isn't there. Pulls the actual evidence chain — does this reasoning hold if you remove pages X, Y, Z?

Tone: epistemic. Asks for the load-bearing causal claim explicitly.

### 5. The Outsider

Argues the corpus is locked into a frame and hasn't tried the alternative. Pulls in pages from outside the topic cluster — adjacent concepts, contrasting projects, dimensions the topic hasn't been compared against.

Tone: lateral. Often surprises the user.

### 6. The Lens-Checker

Reads `me/lexicon.md`. For every load-bearing term used in the topic's pages, checks whether the corpus's usage matches the user's defined lens. Flags drift instances with examples.

Tone: flat. No argument. Just facts: "page X uses 'sovereignty' in a way that drifts from the lexicon's definition. Specifically, [drift instance]."

This voice is essential. The whole reason for the lexicon is preventing drift; this is the operation that actually checks.

---

## Output structure

```markdown
# Debaiser: <topic>

## What the corpus says

<2-3 sentence neutral summary of the dominant stance, with retrieval_score-weighted strength>

Pages forming the stance: [<top 5 page_ids>]
Confidence weighted by reinforcement: <score>
Last meaningful contradiction logged: <date | "never">

## The split

### The Optimist
<one paragraph, names specific pages>

### The Pessimist  
<one paragraph, names specific pages>

### The Pragmatist
<one paragraph, names specific pages>

### The Sceptic
<one paragraph, names specific pages>

### The Outsider
<one paragraph, names specific pages>

## Drift detected

<Lens-Checker findings. Either:>
- <term>: page <id> uses <X way>, lexicon defines as <Y way>. Drift: <description>.
- (or) "No drift detected."

## Where this lands

<One paragraph that does NOT recommend. Says: "if you want X, the Optimist case is loudest. If you want Y, the Sceptic case is loudest. The Lens-Checker says watch the [term] drift before committing." User remains the thinker.>

## Suggested follow-up captures

<List of 2-4 things the user could capture next that would resolve the strongest tensions surfaced. Not directives. Information that would settle the contested point.>
```

---

## Auto-trigger threshold

The keeper daemon runs nightly. For each concept with `retrieval_score > 0.7` and `surface_count > 5` and `last_contradiction_logged > 30 days ago`, it adds a `debaiser_candidate: true` flag.

The next morning brief offers a debaiser run on the top 1-2 candidates. The user can run, defer, or dismiss.

This catches echo chambers. The system notices that you've been increasingly confident about something without ever capturing a counter-perspective, and offers to push back on you. The user can refuse. The user usually refuses. Occasionally the user accepts and is glad they did.

---

## What debaiser refuses to do

- Pretend balance when there isn't any. If four voices agree and one disagrees, that gets surfaced honestly — not falsely balanced.
- Manufacture contrarianism. The Pessimist needs evidence; if the corpus is genuinely solid, the Pessimist says so and credits the Optimist.
- Conclude. There is no "and so the right answer is..." line. The user concludes.
- Hide drift. The Lens-Checker is mandatory and runs every time, even on debaiser runs the user expected to validate the stance.

---

## Tone across the whole output

The Debaiser is not the antagonist. It's the framework overlay applied to the user's own corpus. The voice is rigorous, not adversarial. It cares about the user being right more than being challenged. When the corpus is genuinely solid, the Debaiser says so plainly.

The role is to show the user what they actually think — not what they think they think. That requires honesty in both directions.
