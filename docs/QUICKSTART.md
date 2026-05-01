# IkigAI — Quickstart (S0 + S1, today)

> Two stages. Roughly 3 hours total. Validates the foundation before any infrastructure work.

---

## Before you start

You'll need:
- Claude Desktop, Claude Code, or another LLM client (for the manual round trip)
- A real source you'd actually capture into IkigAI — don't pick something fake; the validation only works on real input

You will NOT need yet:
- The NUC (S2)
- Tailscale (S2)
- Ollama (S2)
- Daemons (S2)

---

## S0 — Foundation (2h, mostly setup + reading)

### Step 1 — Decide where IkigAI lives on your Mac

For now (development before NUC ships):

```
~/ikigAI/
  ikigAI-core/        # cloned/copied from this repo's docs/ikigAI-core/
  ikigAI-me/          # cloned/copied from this repo's docs/ikigAI-me/, then bespoke'd
```

```bash
mkdir -p ~/ikigAI
cd ~/ikigAI

# Pull this repo
git clone https://github.com/ijnebzor/IkigAI.git ./repo
cp -r ./repo/docs/ikigAI-core ./
cp -r ./repo/docs/ikigAI-me ./
```

Eventually `ikigAI-me/` becomes its own git repo (private). For S0–S1 it's just files on your Mac.

### Step 2 — Edit `ikigAI-me/CLAUDE.md`

This is YOUR personal vocabulary. The version in the repo is mine. Make it yours:

- Identity, location, day job
- Active projects with repos
- Key people (only those you'd want the system to recognise)
- Skill markers
- Time/capacity (working hours, deep-work blocks, family-protected times)
- Voice prefs (default: helpful for retrieval, prepaired for plans, ijneb-dev for briefs — change per taste)

### Step 3 — Edit `ikigAI-me/ikigai.md`

Anchor the framework to *your* current state.

- **Ring 1 — Identity:** what you are. (Mine: AIthropologist.)
- **Ring 2 — Operating principle + sovereignty layers:** which layers you actually engage. (Mine: all five.)
- **Ring 3 — Expression surfaces:** name yours: research / tooling / discourse / practice. (Some surfaces may be empty for you; that's fine.)
- **Ring 4 — Funding:** salary, NFP, commercialisation, speaking, etc.
- **Current vs aspirational:** describe today's typical week and where you want to be in 12 months
- **Portfolio test:** map your active projects through the four-circle Ikigai test

### Step 4 — Edit `ikigAI-me/lexicon.md`

Add at least 3-5 of YOUR load-bearing words with the lens YOU apply.

The seeded ones (sovereignty, AIthropologist, compounding, etc.) are mine. Some may match your usage — keep those. Most won't — replace.

For each:
- `term:`
- `definition:` (neutral, dictionary-ish)
- `lens:` (your interpretive meaning, in your words, with examples)

### Step 5 — Read the prompts

In order:

1. `ikigAI-core/prompts/understand.md` — what /understand does
2. `ikigAI-core/prompts/retrieve.md` — three-gear retrieval
3. `ikigAI-core/prompts/brief.md` — daily brief structure
4. `ikigAI-core/prompts/onboard.md` — the always-on intake conversation
5. Skim the others (debaiser, phase-an-idea, secondary)

You're not running these yet — you're absorbing the contract.

### Step 6 — Read the schema

`ikigAI-core/schema/SCHEMA.md`. Especially the universal frontmatter and the type-specific extensions. You'll be filling these in by hand in S1.

**Checkpoint:** You can read your own `CLAUDE.md`, `ikigai.md`, and `lexicon.md` and recognise yourself in them. The schema feels right for the kind of thinking you do.

---

## S1 — Single round trip (1h)

### Step 1 — Pick a real source

An article you'd actually want IkigAI to remember. Or a voice memo (transcribe manually). Or a chat snippet. Real, not test.

Drop the raw content (URL + selected text, or the full transcript) into `~/ikigAI/ikigAI-me/inbox/unsorted/<slug>.md`. No frontmatter; just the content.

### Step 2 — Run /understand manually

Open Claude Desktop or Claude Code. Paste:

```
You are the IkigAI ingest pipeline. Read these three files in order, then process the source.

=== CLAUDE.md ===
<paste the contents of ikigAI-me/CLAUDE.md>

=== ikigai.md ===
<paste the contents of ikigAI-me/ikigai.md>

=== lexicon.md ===
<paste the contents of ikigAI-me/lexicon.md>

=== Source ===
<paste the inbox file>

=== Instructions ===
Apply the /understand pipeline as documented in ikigAI-core/prompts/understand.md. Return a single markdown file ready to save to wiki/sources/<id>.md, including:
- v0.3 frontmatter (id, type, ikigai_regions, ring, expression_surface, sovereignty_layers, lexicon_terms, summary, all the rest)
- # Title
- ## Summary
- ## Key claims
- ## Raw notes
```

### Step 3 — Inspect the output

Did it:
- [ ] Tag the right Ikigai regions?
- [ ] Pick the right ring + expression surface?
- [ ] Catch any lexicon terms used in the source? Apply your lens correctly?
- [ ] Identify entities/concepts that match your `CLAUDE.md`?
- [ ] Flag any contradictions if you have any other pages already?

If yes: foundation is solid.
If no: which step is failing? Adjust the prompt OR your `CLAUDE.md`/`ikigai.md`/`lexicon.md` content. Re-run.

### Step 4 — Save the page

`~/ikigAI/ikigAI-me/wiki/sources/<id>.md`.

### Step 5 — Run /retrieve at all three gears

For Gear 1, you can do this manually with grep + read.

For Gear 2 and Gear 3, paste the same context block plus the full prompt from `ikigAI-core/prompts/retrieve.md`, ask a question your one-page corpus could partially answer, and inspect.

### Step 6 — Bump schema if needed

If you found a field that felt wrong, edit `ikigAI-core/schema/SCHEMA.md`. Update `schema_hash` in your sole page. Commit.

### Step 7 — Commit

```bash
cd ~/ikigAI/ikigAI-me
git init -q
git add .
git commit -m "S1 round trip: first real source ingested"
```

**Checkpoint:** You believe the foundation is right. The lexicon catches when a source uses a load-bearing word in a different sense than yours.

---

## After S0 + S1

You go to S2. That's where the NUC, Tailscale, daemons, MCP, and Phase 0 dump happen. The packet for that lives in `docs/s2/` — start with `RUNBOOK.md`.

Do S2 in one sustained session (~6 hours, probably a Saturday). Compressing it produces flaky daemons. Trust the runbook order.

---

## What to do if S0/S1 doesn't feel right

- **Schema feels wrong:** rewrite the field that's bugging you, bump `schema_hash`, re-run S1
- **Prompt feels generic:** rewrite the operation prompt to use YOUR voice and YOUR examples
- **Lexicon feels thin:** add 5 more terms, with lenses; re-run S1 against a source where they're load-bearing
- **CLAUDE.md feels generic:** add specifics — names, project URLs, working hours, voice prefs
- **You're not sure if S1 worked:** the bar isn't perfection; it's "the foundation feels right enough to commit infrastructure to"

The point of S0/S1 is to surface schema bugs cheap, before you commit 6 hours of NUC infra to them.
