# /brief — daily morning brief

> The hook. Every day starts here.
> "What do you want to work on today?" — answered against your real life.

## Inputs
- Today's date and the user's local time
- Active projects (`wiki/projects/` with `project_status: active`)
- Promoted Lab items (ideas with `idea_status: phased` or `accepted`)
- Calendar reality: today + next 7 days (cached from Google Calendar)
- Recent capture activity (last 7 days)
- Linkage-scout queue (overnight discoveries)
- User's voice preference for `morning_brief` context

## Process

### Step 1 — Read the three signals

**Signal A: Active projects.** What's currently in flight? What's the last update on each (most recent reinforcement, recent ideas added, recent outputs)? What's stalled (no activity 14+ days)?

**Signal B: Promoted ideas.** What ideas have phased plans waiting? Are any of them blocked on a previous phase? Which have calendar slots already accepted?

**Signal C: Recent calendar reality.** What did the user actually spend time on in the last 7 days? Match against project pages — did the time match the stated priorities? If not, flag the drift.

Weight all three equally for v1. After 30 days of usage, the system can re-weight based on which signal best predicts engagement (ADDIE).

### Step 2 — Read overnight discoveries

The linkage-scout daemon has run overnight and produced a queue of:
- Newly discovered linkages between previously unconnected pages
- Pages whose `confidence` decayed past a threshold without reinforcement
- Echo-chamber warnings (high-confidence claims with no contradicting sources)

Pick the top 1–3 to surface. Only the genuinely useful — don't pad.

### Step 3 — Read the user's calendar today

What does today look like? Hard commitments (meetings, family, etc.)? Free deep-work blocks? Travel?

The brief's recommendation must respect today's reality. If today is back-to-back, the recommendation is "small drop-in tasks only." If today is wide open, the recommendation can be ambitious.

### Step 4 — Build the options

Aim for 3 options, each from a different active project where possible. Format:

```
— Stage <N> of <Project>
  Focus: <one sentence on what this stage produces>
  You could use that for: <one sentence on why it matters now>
  Effort: <hours>
  Risk: <one sentence on what might go wrong>
```

Pull stages from the project pages directly. If a project has a phased plan, the next stage is obvious. If not, propose a likely next-best move based on the project's recent activity.

### Step 5 — Recommend

Pick one of the three. Justify in two sentences:

```
**My recommendation:** Stage 3 of ABENAKI Lab.
Given your focus on getting the canonicalisation engine clean and your recent
ingest of the rohitg00 LLM Wiki v2 patterns, this slots cleanly into 
2 hours and unblocks Stage 4. Calendar shows a free 7-9pm window tonight.
```

The recommendation should reference *why* — the user's recent context, not generic prioritisation. The brain has the data; use it.

### Step 6 — Offer the calendar slot

If the recommendation maps to an idea with calendar offers pending, surface them. If not, look at today + next 3 days for a fitting slot.

```
**Want me to book it?** Best slot: tonight 7:00–9:00 PM (free, deep-work window).
Reply 'yes' or pick another slot:
  — Thu May 1, 6:30–8:00 PM
  — Sat May 3, 9:00–11:00 AM
```

### Step 7 — Surface overnight discoveries (optional section)

```
**Worth noticing:**
- Two pages on local LLM cost dropped past your reinforcement threshold.
  You may have moved on from the topic — confirm or recapture.
- New linkage: [[swarmvault]] and [[abenaki-segment-6]] both hit
  "schema-driven knowledge work." Worth a Gear 2 retrieval to synthesise?
- Echo chamber forming on [[mac-mini-as-host]] — 4 reinforcements,
  zero contradictions. Want a Gear 3 debaiser pass?
```

Only include this section if there's genuinely something to surface. Empty is fine. Padding is bad.

### Step 8 — Sign off in voice

Match the user's `morning_brief` voice preference. Examples:

**helpful:**
> Have a good day. Drop new captures in `inbox/` whenever they arrive — I'll have today's discoveries ready by tomorrow morning.

**roasty:**
> You've abandoned 4 ideas in the last 30 days. Maybe finish one before starting another? Just sayin'.

**prepaired:**
> Brief delivered. Confidence high on the recommendation. Standing by for direction.

---

## Output format (full)

```markdown
# Brief — <Day, Date>

Good morning. Here are your build options today:

— **Stage 2 of PrepAIred**
  Focus: <…>
  You could use that for: <…>
  Effort: <hours>
  Risk: <…>

— **Stage 3 of ABENAKI Lab**
  Focus: <…>
  You could use that for: <…>
  Effort: <hours>
  Risk: <…>

— **Stage 5 of IkigAI**
  Focus: <…>
  You could use that for: <…>
  Effort: <hours>
  Risk: <…>

**My recommendation given your focus on <X>:** <pick + reasoning, 2 sentences>.

**Best calendar slot:** <slot>. Want me to book it?
Other options: <…>, <…>

---

**Worth noticing:** (only if something genuinely surfaced)
- <discovery>
- <discovery>

---

<voice signoff>
```

---

## Save the brief

Write to `wiki/outputs/brief-<YYYY-MM-DD>.md` with:
- `output_type: brief`
- `gear_used: 0` (briefs aren't a retrieval gear)
- `applied: false` (updated when user accepts a recommendation or books a slot)

Surface to:
- Web viewer brief panel
- MCP-callable from any client
- Optional email push if user has configured it

---

## What NOT to do

- **Don't surface every discovery every day.** Only the top 1–3, only if genuinely useful.
- **Don't recommend across all projects equally.** Recommend based on what fits today and what unblocks the most downstream work.
- **Don't ignore the user's calendar reality.** A 4-hour recommendation on a back-to-back day is wrong. Adjust scope or pick a different option.
- **Don't repeat yesterday's recommendation if the user declined.** Pick something else; note that yesterday's option is still available.
- **Don't pretend recent activity didn't happen.** If the user spent 12 hours on PrepAIred this week and zero on IkigAI, the brief should reflect that — either as confirmation (good focus) or contradiction (you said IkigAI was the priority).
