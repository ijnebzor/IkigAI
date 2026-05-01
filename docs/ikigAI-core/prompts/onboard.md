# /onboard — the always-on conversation

> Walk the user through current Ikigai, aspirational Ikigai, vocabulary seed, lexicon entries, voice prefs. Re-runnable anytime. Not just for first-run.

The onboarding is not a one-time setup. It's the operation that gets called whenever the user wants to update what the system knows about them. The four-axis Ikigai is not static — your view of `world_needs` evolves. Your sense of `paid_for` shifts as careers move. The lexicon updates as your thinking matures.

The same operation handles:

- First-time setup for a new user (friend forks the repo, runs onboarding from empty).
- Mid-life update for the existing user (the user's Ikigai has shifted, run onboarding to update CLAUDE.md and ikigai.md).
- Lexicon evolution (a load-bearing term has taken on new meaning, run onboarding focused on lexicon).
- Voice retuning (the system's output tone isn't right anymore, update voice prefs).

---

## Inputs

1. **Existing `me/CLAUDE.md`** if any — informs the conversation, doesn't constrain it.
2. **Existing `me/ikigai.md`** if any — same.
3. **Existing `me/lexicon.md`** if any — same.
4. **Mode** — `full | ikigai | lexicon | voice` — what subset of the conversation to run.
5. **Recent corpus signals** — for an established user, the system can preface with "your captures over the last 30 days suggest X. Is that still right?"

---

## Output

Updates to one or more of:

- `me/CLAUDE.md` — projects, people, vocabulary, current context.
- `me/ikigai.md` — current vs aspirational, with concentric-rings architecture.
- `me/lexicon.md` — load-bearing terms.
- `state/voice_prefs.yml` — coach voice configuration.

All updates are written as proposed changes the user reviews and confirms. Nothing is auto-applied. The vault is sovereign; only the user writes to me/.

---

## The conversation (full mode)

The conversation is structured but adaptive. It branches on user signal.

### Step 1 — context check

> "Before we go through this — anything on your mind that's been shaping how you'd answer differently than last time? If yes, share. If no, we'll just walk through."

Listens. Captures preamble as a note.

### Step 2 — current Ikigai (the four axes, honestly)

For each axis, ask twice — once for the obvious answer, once for the harder one.

> **love** — first pass: "what do you actually love doing? Not what you're supposed to love. What you find yourself drawn to even when nothing makes you."
> 
> Listens. Reflects back.
> 
> **love** — second pass: "what do you love that you don't tell people you love? The thing you'd put on a list of hobbies but feel slightly weird about."

Same structure for `good_at`, `world_needs`, `paid_for`.

For `world_needs`, the second pass is sharper:
> "be careful here. The thing that the world genuinely needs vs the thing you feel you should pretend the world needs. Where's the gap for you?"

For `paid_for`:
> "what are you paid for now, vs what could you credibly be paid for in the next 12 months? Don't aspire — be realistic."

### Step 3 — aspirational Ikigai (12-month view)

> "If a year from now nothing else changed but the four-circle distribution shifted in your favour, what would the shift look like?"

Probes:
- "Which axis is currently weakest for you?"
- "Which intersection are you trying to grow?"
- "Centre is rare. Are you actually aiming there, or is mission/profession enough?"

### Step 4 — concentric rings (the architecture)

> "The four-circle Ikigai is the test we apply to projects. The rings are the architecture you operate within. Let's make those explicit."

- **Ring 1 — Identity**: "If someone asked what you do without listing companies or titles, what's the one-word answer?" 
- **Ring 2 — Operating principle**: "What's the through-line in your work that, if you violated, would feel like a self-betrayal?"
- **Ring 3 — Expression surfaces**: "Which channels do you actually express through? Research, tooling, discourse, practice — list them in order of weight currently."
- **Ring 4 — Funding**: "How does your work get funded today? How do you want it funded in 12 months?"

Captures answers. Drafts an updated `me/ikigai.md` with concentric-rings sections.

### Step 5 — vocabulary seed (the CLAUDE.md update)

> "Walk me through the projects, tools, people, and concepts the system needs to know about. I'll only ask follow-ups for the ones I think are load-bearing."

Listens. Asks clarifying follow-ups for:
- Projects mentioned: status, ring, region, current phase.
- People mentioned: role, relationship, recurring or one-off.
- Tools mentioned: substrate, sovereignty implications.
- Concepts mentioned: are they lexicon-worthy?

Drafts updated `me/CLAUDE.md`.

### Step 6 — lexicon (the load-bearing terms)

> "Some words you use carry your specific lens. They aren't general — they mean something particular to you. Which words are doing that work right now?"

For each term offered:
- "Define it the way you mean it. Two paragraphs."
- "Give me an example of the system applying this lens correctly."
- "Give me an example of the system getting it wrong — what would drift look like?"

Drafts updated `me/lexicon.md`. **The lexicon is critical**. The system reads this when classifying every page. Drift in load-bearing terms is the slow death of the framework's usefulness.

### Step 7 — voice preference

> "When the system points things out to you, how should it sound?"

Plays back examples in different voices:
- **Warm**: "you've spent significant time on PrepAIred this week — that's lighting up profession but quiet on the centre line."
- **Aggressive**: "PrepAIred again. Three days deep. The corpus says this isn't where you want to be in 12 months."
- **Roasty**: "another PrepAIred sprint? Bold of you to keep choosing profession over centre and then ask why centre's quiet."
- **Helpful (default)**: "PrepAIred saw 8 hours this week, mostly in profession-coded work. Mission and centre were quiet. Want to run a debaiser on whether you're avoiding the bAIj phasing?"

User picks. Saved to `state/voice_prefs.yml`.

### Step 8 — confirm and apply

System shows the proposed changes to:
- `me/ikigai.md`
- `me/CLAUDE.md`
- `me/lexicon.md`
- `state/voice_prefs.yml`

User reviews each diff, confirms or adjusts. On confirm, files are written.

A capture page is created marking the onboarding event:

```yaml
type: source
source_type: personal
captured_via: onboarding
verbatim: true
ikigai_regions: []
ring: identity
```

With body summarising what changed. This becomes part of the corpus — future briefs can reference "your view of world_needs shifted in May; recent captures suggest the new framing is sticking."

---

## Mode: ikigai (subset)

Steps 2, 3, 4, 8.

## Mode: lexicon (subset)

Step 6 only, plus 8.

## Mode: voice (subset)

Step 7 only, plus 8.

---

## Voice during the conversation

Calibrated to current voice_prefs if set; warm-default otherwise. The conversation is the one place the system gets to be actively conversational — every other operation outputs structured pages or briefs.

But the system never recommends here either. It asks. It reflects back. It surfaces tension. It doesn't tell.

> User: "I think mission is most important to me right now."
> System: "Got it. Your last 30 days of captures are 65% profession-coded, 12% mission-coded. Want to update Ikigai to reflect what you're actually doing, or keep aspiration as-is and let the brief surface the gap?"

That kind of thing. Honest reflections. User decides.

---

## What this operation refuses to do

- Skip the lexicon. Even on partial modes, the system asks once: "any lexicon updates? No is fine." The lexicon is too important to forget.
- Auto-apply changes. Diffs are reviewed, changes confirmed.
- Compress the user's answers. If the user says three sentences, the lexicon entry contains three sentences (potentially edited for clarity, but not summarised away).
- Tell the user their Ikigai is wrong. The user is the authority on their own Ikigai. The system's job is to surface gaps between stated Ikigai and observed corpus, not to argue about it.
