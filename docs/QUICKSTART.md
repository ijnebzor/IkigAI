# IkigAI v0.2 — Quickstart (S0 + S1, today)

> Two stages. ~3 hours total. Validates the foundation before any infrastructure work.

---

## Before you start

You'll need:
- Claude Desktop or Claude Code on your Mac (for the manual round trip)
- A real source you'd actually capture into IkigAI. Don't pick something fake — the validation only works on real input.

You will NOT need yet:
- The NUC (S2)
- Tailscale (S2)
- Ollama (S2)
- Daemons (S2)

---

## S0 — Foundation (30 min, mostly setup)

### Step 1 — Decide where IkigAI lives

For now (development on your Mac):
```
~/ikigAI/
  ikigAI-core/
  ikigAI-me/
```

Later (S2) the entire `~/ikigAI/` directory gets `rsync`'d to the NUC at the same path. iCloud/Dropbox sync optional but not required — the NUC is the canonical home.

### Step 2 — Unzip the bundle

```bash
mkdir -p ~/ikigAI
cd ~/ikigAI
unzip ~/Downloads/ikigAI-v0.2.zip
```

Resulting structure:
```
ikigAI/
  ikigAI-core/    (universal — leave alone)
  ikigAI-me/      (yours — edit freely)
  README.md
  IkigAI_Roadmap.md
```

### Step 3 — Initialise git for your `me/`

```bash
cd ~/ikigAI/ikigAI-me
git init
git add .
git commit -m "ikigAI-me v0.2 init"
```

Your brain has version control from this moment. Every change tracked. The git history is itself a memory trail.

### Step 4 — Read your CLAUDE.md

Open `~/ikigAI/ikigAI-me/CLAUDE.md`. I've populated it from everything I know about you — projects, tools, people, concepts, voice preferences.

**Read it carefully. Edit anything that's wrong, missing, or stale.**

This is the highest-leverage edit you'll make on the system. Every retrieval, every brief, every phased plan is shaped by what's in this file.

### Step 5 — Read your ikigai.md

`~/ikigAI/ikigAI-me/ikigai.md` has my best guess at your current vs aspirational Ikigai. Adjust where I'm wrong. This file informs every classification call the system makes.

### Step 6 — Read your config.yml

`~/ikigAI/ikigAI-me/config.yml` has voice defaults, working hours, brief cadence, daemon schedules. Adjust anything that doesn't match how you work.

**S0 done.** You have a configured `me/`. No infrastructure yet. Ready to validate.

---

## S1 — Single Round Trip (~1 hour)

The goal here is NOT to ingest a lot. It's to prove the schema works on one real source before you commit to any bulk effort.

### Step 1 — Pick one real source

Something representative. Examples:
- A long article you'd normally tab-stash
- A voice memo you've been meaning to action
- A copy-pasted message from a chat (Phase 0 pattern)
- A project idea you've been circling

Don't pick a smoke-test URL. Pick something that matters.

### Step 2 — Drop it in `inbox/unsorted/`

Save it as a markdown file:
```
~/ikigAI/ikigAI-me/inbox/unsorted/2026-04-30-real-thing.md
```

Plain content, no frontmatter needed. The pipeline writes the frontmatter.

### Step 3 — Run the manual /understand

Open Claude Desktop or Claude Code. New conversation. Paste this:

```
You are running the IkigAI /understand pipeline.

Read these two files first:
1. ikigAI-core/prompts/understand.md (the pipeline spec)
2. ikigAI-me/CLAUDE.md (my personal vocabulary)
3. ikigAI-me/ikigai.md (my current vs aspirational Ikigai)

Then process this source:

[paste the content of your inbox file here]

Output the resulting wiki/sources/<id>.md page in full. Also list:
- New entities you'd propose creating
- New concepts you'd propose creating
- Any contradictions with my existing thinking (you can't see existing
  pages yet, so just flag what would matter)
- Confidence reasoning
```

### Step 4 — Inspect the result

Read the page Claude produced. Check:

- **Title** — retrieval-friendly? 5–10 words?
- **Summary** — 2–4 sentences capturing what matters?
- **ikigai_regions** — does the list match how *you* feel about this content's regions?
- **Tags** — match your vocabulary, not generic?
- **Entities/concepts** — propose the right things?
- **Drivers/biases** — honest, not fabricated?
- **Confidence** — defensible?

If anything's wrong, the schema or vocabulary needs adjustment, not the source.

### Step 5 — Save the page (manually for S1)

Save Claude's output to:
```
~/ikigAI/ikigAI-me/wiki/sources/<the-id-it-generated>.md
```

S2 automates this. For now, manual.

### Step 6 — Run a manual /retrieve at all three gears

Three new Claude conversations, one per gear. Each one paste:

**Gear 1:**
```
You are running IkigAI /retrieve at Gear 1 (links only).

Read ikigAI-core/prompts/retrieve.md and ikigAI-me/CLAUDE.md.

My corpus consists of one page: [paste the source page].

Query: [a question that would naturally retrieve that source].

Return Gear 1 output.
```

**Gear 2:**
Same setup, but ask for Gear 2 with the synthesis structure (answer / trail / action / blind spot / biases).

**Gear 3:**
Same setup, but read `prompts/debaiser.md` too. Ask for the full Debaiser panel.

(Gear 3 will be limited because the corpus is one page — that's fine, you're validating shape, not depth.)

### Step 7 — Adjustments

Anything that felt wrong during S1 → fix in:
- `core/schema/SCHEMA.md` (if the schema's wrong)
- `core/prompts/understand.md` (if the pipeline's wrong)
- `me/CLAUDE.md` (if the vocabulary's wrong)
- `me/ikigai.md` (if the Ikigai axes feel mistagged)

Bump `schema_hash` to `v0.2.1` in any page you've manually edited the schema on.

### Step 8 — Commit

```bash
cd ~/ikigAI/ikigAI-me
git add .
git commit -m "S1 round trip: first real source ingested"
```

**S1 done.** You believe the foundation. You have one real page in the vault. You're ready to commit S2's effort.

---

## What you have now

- A working schema validated on real input
- A `me/` repo configured to your domain
- One real source proving end-to-end pipeline shape
- Confidence to invest the ~6 hours of S2 (NUC + daemons + bulk ingest)

## What's next

S2: provision the NUC, get the daemons running, bulk Phase 0 dump.

When you're ready, say so and I'll write the S2 deployment guide — Tailscale config, Docker Compose for the daemons, Ollama setup, Google OAuth steps, MCP server config, and the bulk-ingest playbook for your existing dump material.
