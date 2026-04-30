# /phase-an-idea — productionised idea flow

> Idea in. Phased plan out. Calendar offered. Work begins.
> The verb of IkigAI is *productionising idea flows*. This prompt is that verb.

## Inputs

A page in `wiki/ideas/` with `idea_status: raw` (just-captured idea), or an idea description passed inline.

## Process

### Step 1 — Read the idea fully

What is the user trying to do? What's the desired end state? What's implicit vs explicit? Don't add scope; clarify what's there.

### Step 2 — Pull context from the user's corpus

Across the whole wiki, gather:

- **Adjacent prior work** — pages tagged with overlapping concepts, similar entities, or shared regions
- **Skills the user already has** that apply (read `me/CLAUDE.md` skill markers + concept pages with `maturity: established`)
- **Tools the user already uses** that fit this idea
- **Active projects** that might absorb this, or that this might unblock
- **Past ideas** that look like this — were they shipped, parked, or abandoned? Why?
- **Past biases** the user has shown on adjacent topics

This is the unfair advantage. The brain knows what the user knows. The plan starts where they actually are, not at zero.

### Step 3 — Read the user's current state

- **Active projects** in `wiki/projects/` with `project_status: active`
- **Recent ideas** that haven't yet been phased (signal of bandwidth)
- **Calendar load** for the next 14 days (read via Google Calendar daemon)
- **Current Ikigai** vs **aspirational Ikigai** in `me/ikigai.md` — does this idea move toward aspirational?

### Step 4 — Write the phased plan

Use the same structure this very document was written in. Specifically:

```markdown
# <Idea name>

## Purpose
<one paragraph: what this idea is, why now, what it gets the user>

## Where it sits in your Ikigai
<which axes/intersections this touches; whether it moves toward aspirational>

## Existing leverage
<what the user already has that applies — skills, tools, prior work, adjacent
projects. Be specific: cite [[wikilinks]]>

## Phases

### Stage 0 — Foundation
**Goal:** <what's true at end of stage>
**Effort:** <hours>
**Components:** <bulleted>
**Dependencies:** <what must be true before starting; usually nothing for S0>
**Deliverable:** <the artefact>

### Stage 1 — <next>
… same shape …

### Stage N — <final>
… same shape …

## Total timeline
<sum of effort, mapped to user's calendar reality>

## What stays constant
<the no-refactor guarantees: what's a contract that won't break across stages>

## Calendar offer
<proposed Phase 1 slots against the user's actual availability,
prioritising deep-work blocks if the user has them in CLAUDE.md preferences>
```

### Step 5 — Be honest about cost

Estimate hours like you would for someone you respect: realistically, slightly conservative, not optimistic. If a stage feels like it'll take 8 hours, say 8, not 4. The user is going to schedule against this.

If the idea will take longer than the user's recent throughput suggests they have bandwidth for, say so. Suggest:
- Parking until a specific bandwidth window opens
- Compressing scope (which sub-stages can defer?)
- Replacing an active project (which one is delivering least?)

### Step 6 — Identify the load-bearing dependency

Across the whole plan, which stage is the one that everything else depends on? Mark it. The user will protect this slot above others.

### Step 7 — Flag the risks

What might go wrong? Be specific. Pull from past biases the user has shown — if they tend to underestimate infra time, flag that. If they tend to scope-creep, flag that. The brain has the data; use it.

### Step 8 — Write the page

Save the phased plan as `wiki/outputs/<idea-id>-plan.md` with:
- `output_type: phased-plan`
- `in_response_to: <idea-id>`
- frontmatter linking back to the idea page

Update the idea page:
- `idea_status: phased`
- `phased_plan: [[<output-id>]]`

### Step 9 — Propose the calendar offer

Look at user's Google Calendar for the next 14 days. Find blocks ≥ 90 minutes that don't break stated boundaries (working hours, deep-work preferences from `me/CLAUDE.md`).

Propose:
- 1 slot for Phase 1, kickoff
- 1–2 slots for Phase 1 continuation if Phase 1 is >3 hours

Surface the offer in the brief or directly in the response:

```
**Phase 1 ready to start.** I see these slots in your calendar:

— Wed May 6, 7:00–9:00 PM (deep-work window, no conflicts)
— Sat May 9, 9:00–11:30 AM (your preferred Saturday morning slot)
— Mon May 11, 6:30–8:00 PM (after dinner, light cognitive load before)

Recommended: Sat May 9. Largest contiguous block, matches your historical 
preference for kickoff-day-Saturday on similar projects. Want me to book it?
```

User accepts → daemon writes the event to Google Calendar with description linking to the plan page.

### Step 10 — Update the idea status

If user accepts a calendar offer:
- `idea_status: accepted`
- `calendar_offered: true`
- `calendar_event_ids: [<google_event_id>]`

If user declines:
- `idea_status: phased` (stays as plan, not accepted)
- `calendar_offered: true` (don't re-pester)
- Note the decline reason in the idea page if user provided one

If user picks a different time:
- Same as accept, but with their slot

---

## What NOT to do

- **Don't write a phased plan that's bigger than the idea warrants.** A 30-minute task gets a single-stage plan. Don't bloat to look smart.
- **Don't use generic phase names.** "Stage 1: Discovery" is meaningless. Use specific outcomes: "Stage 1: Whisper.cpp installed, first transcript pipelined."
- **Don't ignore the user's recent failures.** If they've abandoned 3 ideas in a row that matched this pattern, surface that. Maybe this one needs a smaller scope or different framing.
- **Don't propose calendar slots that fight the user's stated preferences.** Read `me/CLAUDE.md` for working hours, Sabbath days, deep-work blocks, family commitments.
- **Don't propose Phase 2+ slots.** Only Phase 1. Each subsequent phase gets re-proposed after the previous ships, against fresh calendar reality.

---

## Voice

Same voice rules as `retrieve.md`. Default `helpful`. Tone shapes how the plan reads, not its structure.

For accountability-heavy moments (idea is repeating a past pattern, scope is too big, user is over-committed), the voice can default to `roasty` or `accountantability` — but the structure stays the same.
