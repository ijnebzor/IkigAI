# /phase-an-idea — turning an idea into a phased plan

> Read an idea. Read the corpus. Read the framework. Write a plan that respects all three.

This is the operation that converts an `idea` page into a `phased_plan` output. The input is one page; the output is a structured commitment with explicit ring/region lighting at each phase.

Triggered by:

- User explicitly calls `/phase-an-idea <idea_id>` from any client.
- An idea page sits at status `unphased` for >5 days; the brief offers to phase it.
- A capture from inbox arrives marked as type `idea`; the watcher offers to phase immediately.

---

## Inputs

1. **The idea page** — the input. Captures what the user is thinking about.
2. **`me/CLAUDE.md`** — current projects, recent context, what the user is currently chasing.
3. **`me/ikigai.md`** — current and aspirational Ikigai. The plan must explicitly say which ring(s) and region(s) it pulls toward.
4. **`me/lexicon.md`** — for any load-bearing term the idea uses, apply the user's lens.
5. **The corpus** — relevant canonical pages by ikigai_region overlap with the idea.
6. **Calendar cache** — last 14 days of activity, next 30 days of slots. Used for realistic phase timing.
7. **Existing project pages** — the plan must reckon with whether this idea is a new project, a phase of an existing project, or something that should be folded into something already in flight.

---

## Output

A single `output` page of `output_kind: phased_plan`. The body is structured. The frontmatter includes the same Ikigai region tagging as any other page.

---

## Process

### Step 1 — read the idea honestly

What is the user actually proposing? Distil to the load-bearing claim. Strip excitement. Strip "but maybe also..." Focus on the smallest articulable version.

If the idea is incoherent or under-formed, the output is a single section saying so, with 3-5 questions the user would need to answer before phasing was useful. **Do not phase a half-baked idea into a plan that pretends to be ready.**

### Step 2 — locate against the corpus

Pull the 10-20 most relevant canonical pages by region overlap and concept match. Ask:

- Has the user thought about this before? When? How did it resolve?
- What's the strongest case in the corpus FOR this idea? Strongest case AGAINST?
- Is there a contradiction in the corpus on this topic? (If yes — surface BEFORE the plan. The user might want a debaiser run first.)

### Step 3 — locate against the rings and regions

For the idea, identify:

- Which ring(s) does this sit on? (identity, principle, surface, funding, none)
- If surface — which expression channel? (research, tooling, discourse, practice)
- Which Ikigai axes does this touch?
- Which intersections light up?
- Does this pull toward or away from the aspirational ikigai?

This is what gets shown at every phase below.

### Step 4 — locate against existing projects

- Is this already in flight as a project? If so, this is a phase of that project, not a new project.
- Does this duplicate effort with another project? If so, surface and ask.
- Is this a new project? Does it warrant the overhead of being one, or could it live as an output of an existing project?

### Step 5 — phase it

The plan is structured into phases, **each with explicit ring/region lighting**.

```markdown
# Phased plan: <idea title>

## What this is
<one paragraph: load-bearing claim>

## Where this sits
- Ring(s): <list>
- Sovereignty layers (if principle): <list>
- Expression surface (if surface): <single>
- Ikigai axes lit: <list>
- Intersections: <list>
- Pulls toward / away from aspirational: <toward | away | neutral, with reason>

## Compounding ripples
- Connects to: <list of project_ids and concept_ids with one-line context per>
- Could feed into: <list of currently-active projects this would benefit>
- Could conflict with: <projects this might pull effort from>

## Phases

### Phase 1 — <name>
**Goal**: <single sentence>
**Effort**: <Xh, honest>
**Deliverable**: <single concrete thing produced>
**Lights up**: <which regions and rings>
**Open questions blocking this phase**: <list, or "none">
**Calendar offer**: <a real slot from the next 14 days, or "user to schedule">

### Phase 2 — <name>
<same structure>

### Phase 3 — <name>
<same structure, only if it earns its place>

(More phases only if genuinely necessary. Most ideas are 2-3 phases.)

## What this plan does NOT include
<honest list of things the user might expect but aren't here, with reasoning>

## Open questions before commitment
<list of things the user should resolve before starting Phase 1; if zero, say so>

## When to revisit
<one sentence: under what condition would this plan need re-phasing>
```

### Step 6 — calendar offer

For Phase 1, propose 2-3 real slots from the next 14 days against actual calendar availability. The user accepts a slot, declines, or asks for alternatives.

If the user accepts, write a Google Calendar event linking back to the plan output page. Mark the plan as `applied_at: <now>`. The plan is in flight.

If the user declines all slots, the plan stays at status `canonical` but `applied_at: null`. The brief generator may resurface it.

### Step 7 — set provenance

The output page references:
- `derived_from: [<idea_id>, ...]` — at minimum the idea, plus any corpus pages heavily used.
- `input_pages: [<page_id>, ...]` — every page actually read.
- `prompt_used: phase-an-idea`
- The idea page is updated: `phase_status: phased`, `phased_plan: <output_id>`.

---

## Voice

The plan is structured, dense, scannable. No filler. No motivation. The user is committed enough to phase the idea; the plan respects that and gives them the framework, not a pep talk.

If the plan finds the idea genuinely unviable, **say so plainly**. Don't phase to phase. The output can be a single paragraph explaining why this isn't ready and 3-5 captures that would change that.

---

## Edge cases

- **Idea contradicts the aspirational ikigai** — phase it AND surface the contradiction. The user is the thinker; they may have updated their Ikigai without writing it down.
- **Idea is a debaiser candidate** — surface "this concept hasn't had a debaiser run in 30+ days; consider running before phasing." Don't refuse. Suggest.
- **Idea would require deprecating something** — surface explicitly which canonical projects/plans this displaces. Don't auto-deprecate.
- **Idea is centre-coded** (lights all four axes) — flag it. Centre-coded ideas are rare and load-bearing; the user should know.

---

## What this operation refuses to do

- Phase an idea before answering its open questions. Half-baked plans cost more than no plan.
- Hide trade-offs. Every plan names what it costs.
- Tell the user what to do. The plan offers structure; commitment is the user's.
- Auto-create calendar events. The user accepts a slot explicitly before anything is written to Google Calendar.
