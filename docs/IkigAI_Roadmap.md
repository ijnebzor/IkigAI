# 🧿 IkigAI: The Personal Coach That Lives On Your Brain
### _A roadmap for building a self-owned, idea-to-action engine grounded in everything you know._

---

## **Purpose**

IkigAI is a personal coach that runs on your always-on home device, ingests anything you send it from anywhere, and helps you turn ideas into action against the life you're actually trying to build.

It owns your knowledge. It explains everything you've ever sent it. It tells you how you got to a thought, what you might be missing, and what to do next. It knows your calendar, your projects, your commitments, and your Ikigai gaps — so when you drop an idea in, it returns a phased plan and offers you the time to start.

You drop ideas in.
The machine canonicalises, links, surfaces, coaches, and schedules.
You make and iterate. Better every day.

---

## **Core Principles**

- **You own everything.**
    Markdown vault on your NUC. Git is the memory trail. No vendor lock-in. Clouds reach in only when you say so.

- **Capture is frictionless.**
    Any device, any medium, share-sheet to inbox. Zero thought between brain fart and saved.

- **Canonicalisation is sacred.**
    The dedup engine is what makes the system functional day one. Multi-key matching across every messy capture converges on one record per concept. Get this right, every retrieval afterwards is sharper.

- **Ikigai regions are the lens.**
    Every page carries every region it touches as a flat, explicit list. A single capture compounds across passion, mission, vocation, profession, centre. Click any region, see everything that contributed.

- **Retrieval has gears.**
    Gear 1 — links only. Gear 2 — synthesis with provenance trail, action, blind spot, biases. Gear 3 — Debaiser-on-self contrarian panel. You choose per query. The system remembers per context.

- **The daily brief is the hook.**
    Every day starts with "what do you want to work on today?" — across active projects, promoted ideas, and recent calendar reality. The system offers options across all your projects (PrepAIred, ABENAKI, IkigAI itself, etc) and recommends based on your focus.

- **Productionised idea flows.**
    Idea in → phased plan out → calendar slots offered → work begins. Notion-shaped, but personalised by your brain rather than tag rules.

- **Local-first inference, cloud where it earns it.**
    Ollama (llama3.2) handles ingest, classification, embeddings, drafts. Claude handles synthesis polish and Debaiser-on-self. MCP exposes everything to any client.

- **Phase 0 is a one-time bridge.**
    Brain dump from messaging apps and tab piles, copy-paste only, never again. From day one of S2 onward, IkigAI is the only destination.

- **Bespoke per user, universal under the hood.**
    Core (schema, prompts, daemons) is shared. Me (vocabulary, vault, calendar links) is yours. Friend's version is a fork point, not a refactor.

---

## **System Architecture Overview**

### **You**

Capture ideas anywhere. Receive briefs in the morning. Ask questions at the depth you choose. Accept or decline scheduling offers. Make and iterate.

### **NUC (always-on host, Tailscale-meshed)**

Runs everything stateful. Linux on your i7. Reachable via Tailscale + SSH from any device you own. MCP server exposes operations as tools to any client.

### **Vault (canonical store)**

Markdown files with explicit frontmatter. Git-tracked. Two indexes derive from it: vector (Chroma or Qdrant — pick at S2) and graph (NetworkX or LightRAG — pick at S2). Vault is truth; indexes are computed.

### **Engines (your three reused production components)**

- **Canonicalisation & dedup engine** — multi-key matching: title, version, content hash, semantic similarity. Confidence-scored merging. Already proven in your council-document work; retargeted at your brain.
- **gargAIntuan multi-agent orchestration** — parallel agent dispatch for classification, linkage, reflection. Job queue with streamed logs. Already productionised; retargeted at personal classification.
- **Context-injection synthesis engine** — Claude with role-aware prompts for retrieval Gear 2 and Gear 3 outputs. Already productionised for B2B personalisation; retargeted at personal coaching.

### **Daemons (always-on Claw workers)**

- **inbox-watcher** — processes captures as they land
- **linkage-scout** — nightly graph walk for non-obvious connections
- **brief-generator** — daily brief at your chosen time
- **decay-keeper** — confidence and retrieval-score upkeep
- **debaiser** — contrarian panel on demand or auto-flagged

### **Google integration (S2)**

Two-way Calendar (read your real schedule, write proposed events you accept). Read-only Gmail label/folder watcher (you forward newsletters / drops to a `+ikigai@` alias or label items, daemon ingests). M365 integration deferred to later phase.

### **Capture surfaces**

Phone share-sheet, Mac quick-note hotkey, voice memo (whisper.cpp transcribed), email forward to alias, MCP from Claude Desktop, manual paste. All land in `inbox/` on the NUC via Tailscale-mounted path or sync.

### **Retrieval surfaces**

Web viewer (ABENAKI-shaped UI on the NUC, accessible at `http://nuc.tailnet/`). MCP chat from any client. Daily brief panel. CLI for power use.

---

# 🔱 **Stages**

Each stage produces something you actually use. Hours are honest estimates of *your* effort. Sequenced; no skipping.

---

## **Stage 0 — Foundation**

### **Goal**
Schema, prompts, repo split, all operation specs ready. No infra yet. Validatable end-to-end through Claude manually.

### **Effort**
~2 hours. Today.

### **Components**

1. **Repo split**
    - `ikigAI-core/` — schema, prompts, daemons (specs only at this stage), bin, ui
    - `ikigAI-me/` — your vault, your CLAUDE.md, your ikigai.md
    - `ikigAI-me` imports `core` like a library
    
2. **Schema v0.2**
    - Frontmatter spec with explicit `ikigai_regions` flat list
    - Provenance fields: `sources_raw`, `derived_from`, `supersedes`, `confidence`, `drivers`, `biases`
    - Retrieval signal: `retrieval_score`, `last_surfaced`, `last_used`, `context_modifiers`
    - Lifecycle: `inbox` → `canonical` → `evergreen`, with `superseded` and `archived` terminal states
    - Type-specific extensions for source / entity / concept / project / output / idea
    
3. **Operation prompts (specs)**
    - `understand` — ingest pipeline (canonicalise → classify → link → frontmatter)
    - `retrieve` — three-gear retrieval, gear inferred from phrasing
    - `debaiser` — contrarian panel, five analyst voices on your own corpus
    - `surface` — linkage-scout daily walk
    - `brief` — daily morning brief generator with project-options pattern
    - `phase-an-idea` — idea → phased plan → calendar offer
    - `lint` — decay, contradictions, promotion
    - `onboard` — conversational setup (deferred to S5, spec'd here)
    
4. **Page templates**
    - source.md, entity.md, concept.md, project.md, idea.md, output.md
    - Each carries the universal frontmatter plus type-specific fields
    
5. **Ikigai dimension pages**
    - `wiki/ikigai/{love,good_at,world_needs,paid_for}.md` — axes
    - `wiki/ikigai/{passion,mission,profession,vocation,centre}.md` — intersections
    - Each rolls up everything tagged with that region

### **What you do NOT create**
- No infrastructure
- No daemons running
- No vault content yet beyond templates and skeletons

### **Checkpoint**
You can read CLAUDE.md and recognise the contract. You can paste any source plus the `understand` prompt into a Claude chat and a properly-shaped page comes back.

### **Deliverable**
`ikigAI-v0.2.zip` you `git init` and commit on the NUC.

---

## **Stage 1 — Single Round Trip**

### **Goal**
Validate the schema with one real source through the full pipeline manually before any infra. Catch schema bugs cheap.

### **Effort**
~1 hour. Today or tomorrow.

### **Components**

1. **One real source picked** — a long article you'd normally tab-stash, or one voice memo, or one chat-paste. Representative of how you'll use the system.

2. **Manual ingest** — paste source + `understand` prompt into Claude. Resulting markdown lands in `inbox/`. You inspect: does the canonicalisation hold? Are the regions right? Is the summary useful? Are the entities the right ones?

3. **Manual retrieval, all three gears**
    - Gear 1 — "what do I know about [topic]" returns the page with summary
    - Gear 2 — synthesis with provenance trail
    - Gear 3 — Debaiser panel runs against just that one page (the trail is short but the shape is right)

4. **Schema feedback loop** — anything that felt wrong gets fixed in the schema before S2.

### **What you do NOT create**
- Don't ingest more than one source. Validate shape, not volume.
- Don't try to bulk-anything yet.

### **Checkpoint**
You believe the foundation is right. You'd bet S2's effort on this schema.

### **Deliverable**
Schema v0.2.1 (post-feedback fixes) and one real page in `inbox/`.

---

## **Stage 2 — NUC Live, Brain On**

This is the heart of the build. Everything depends on this stage.

### **Goal**
NUC running everything stateful. Reachable from your devices via Tailscale. Phase 0 brain dump complete and canonicalised.

### **Effort**
~6 hours. This week. One sitting if possible.

### **Components**

#### Part A — NUC provisioning

1. Linux confirmed (Ubuntu LTS recommended; whatever you're already on works)
2. Tailscale installed on NUC and your devices, mesh confirmed
3. Docker + Docker Compose for daemon containerisation
4. Ollama installed natively on NUC, llama3.2 pulled (your Model Wars winner)
5. Vault dir created at `~/ikigAI-me/` with the v0.2 layout
6. Vector index initialised (Chroma — simplest local, swappable later)
7. Graph index initialised (NetworkX in `state/graph.json`, LightRAG layered later if needed)
8. SSH config from your Mac and laptop to the NUC verified

#### Part B — Engines deployed (the three reused production components)

1. **Canonicalisation & dedup engine** containerised on NUC
    - Multi-key matching: title fuzzy, version, SHA256 content hash, semantic via embeddings
    - Confidence-scored merging
    - Configured to run on every inbox file
    
2. **gargAIntuan orchestrator** containerised on NUC
    - Job queue
    - Parallel agent dispatch for classification + linkage + reflection
    - Streamed logs accessible via SSH
    
3. **Context-injection synthesis engine** containerised on NUC
    - Configured for Gear 2 (synthesis) and Gear 3 (Debaiser) calls to Claude API
    - API key in environment, not in repo
    - Logs every Claude call with token spend per call

#### Part C — Daemons running

1. `inbox-watcher` — inotify on `inbox/`, triggers understand pipeline (canonicalise → classify → link → write to `wiki/`)
2. `decay-keeper` — cron, daily, confidence and retrieval-score upkeep

#### Part D — MCP server

1. MCP server exposing operations as tools:
    - `ikigai_capture` — drop content into inbox
    - `ikigai_retrieve` — three-gear retrieval
    - `ikigai_phase_an_idea` — idea → phased plan
    - `ikigai_brief_today` — daily brief on demand
    - `ikigai_debaiser` — contrarian panel
2. Configured in Claude Desktop and Claude Code on your devices via Tailscale URL

#### Part E — Google integration

1. Google Calendar OAuth, two-way scope
2. Gmail OAuth, read-only on a single label `IkigAI/Inbox` across whichever Gmail accounts matter
3. Daemon: Gmail watcher polls labelled items, pulls into `inbox/`, removes label
4. Daemon: Calendar reader caches today + next 7 days for brief generator

#### Part F — Phase 0 brain dump

1. **Chrome tabs** — Android long-press → Select all → Share → Copy. Paste into `inbox/dump-chrome-android.md`. Repeat per device.
2. **Saved Instagram / Twitter / LinkedIn** — copy salient items (URL + your reason for saving) into `inbox/dump-social.md`.
3. **Quotes from messaging apps** — copy individual items you want preserved into `inbox/dump-chats.md`. **Never reference the channel, sender, or thread.** This is the one-way bridge.
4. **Voice memos** — whisper.cpp pass over your folder, transcripts into `inbox/voice/`.
5. Watcher processes everything as it lands. Canonicalisation engine merges duplicates. Classifier tags Ikigai regions. Linker builds the graph.

### **What you do NOT create**
- No web viewer yet (S3)
- No coach voice yet (S3)
- No daily brief delivery yet (S3, but data is being prepared)
- No application loop yet (S4)

### **Checkpoint**
- You SSH into the NUC, see daemons running healthy
- You open Claude Desktop on your phone, use `ikigai_retrieve` over the dump
- You paste a new article into the inbox folder via Tailscale-mounted path; it processes within a minute
- You query "what have I been thinking about Mac Studios" and get back canonicalised pages from your past dumps

### **Deliverable**
A working brain. Real corpus. Reachable from every device. Daemons quiet, indexes warm.

---

## **Stage 3 — Coach Experience**

This is when it stops being infrastructure and starts being a coach.

### **Goal**
Three retrieval gears live. Web viewer running. Daily brief delivered. Coach voice configured. Productionised idea flows working — drop an idea, get a phased plan with calendar offers.

### **Effort**
~4 hours. This week, after S2.

### **Components**

#### Part A — Three-gear retrieval

1. Gear inference from phrasing (rules + LLM classifier fallback)
    - "Just give me…" / "find me…" → Gear 1
    - "What do I know / think about…" / "How did I get to…" → Gear 2
    - "Stress-test me on…" / "Push back…" / "What am I missing on…" → Gear 3
2. Per-context gear preference learned (you can override; system remembers)
3. Gear 1 returns ranked links + summaries (pure local, instant, free)
4. Gear 2 returns five-section coach output (local draft, Claude polish optional)
5. Gear 3 runs Debaiser panel (Claude required, slower, deliberate)

#### Part B — Web viewer

1. Static-served from NUC at `http://nuc.tailnet/` (or Tailscale Funnel for HTTPS)
2. ABENAKI-shaped sidebar nav over your wiki structure
3. Brusselbach Ikigai diagram interactive — click any region, see everything tagged
4. Search across the whole vault with snippet highlighting (your existing pattern)
5. ijneb.dev tokens applied (#0d0d0d, #c8f135, JetBrains Mono + Syne)
6. "Brief" panel always accessible — today's recommended work

#### Part C — Daily brief

1. `brief-generator` daemon runs every morning at your chosen time
2. Reads three signals: active projects, promoted ideas, recent calendar (7-day rolling)
3. Weights equally at first; learns over time
4. Outputs a brief in this shape:
    ```
    Good morning. Here are your build options today:
    
    — Stage 2 of PrepAIred
        Focus: <what>. You could use that for <why>.
    
    — Stage 3 of ABENAKI Lab
        Focus: <what>. You could use that for <why>.
    
    — Stage 5 of IkigAI
        Focus: <what>. You could use that for <why>.
    
    My recommendation given your focus on <X>: <pick + reasoning>.
    Open calendar slots today: <list>. Want me to book <recommended>?
    ```
5. Brief delivered to web viewer panel, MCP-callable from any client, optional email push

#### Part D — Coach voice

1. Voice configurations: `warm`, `helpful`, `aggressive`, `roasty`, plus your existing `prepaired`, `accountantability`, `ijneb-dev`
2. Voice picked per context (work tasks default `prepaired`, personal default warm, financial default `accountantability`, accountability moments default roasty)
3. Voice override per query

#### Part E — Productionised idea flow

1. New page type `idea` in `wiki/ideas/`
2. `phase-an-idea` operation:
    - Reads the idea
    - Pulls everything in vault relevant to it
    - Reads your active projects, current Ikigai axes, calendar load
    - Writes a phased plan in IkigAI's own format (this document is the template)
    - Identifies dependencies, what each phase delivers
    - Proposes calendar slots for Phase 1 of the new idea against your real availability
3. You accept calendar offers via the brief panel; daemon writes events to Google Calendar with description linking to the idea page

### **What you do NOT create**
- No application/outcome capture yet (S4)
- No friend onboarding (S5)
- No M365 integration yet (later)

### **Checkpoint**
- Daily brief lands in your morning, recommends across your projects, offers calendar slots
- You drop a fresh idea into `inbox/ideas/`; within minutes you have a phased plan
- You open the web viewer on your phone, click `mission`, see everything you've ever sent that touched mission
- Gear 3 retrieval on a load-bearing belief returns a Debaiser panel that surfaces something you'd genuinely missed

### **Deliverable**
A coach. A real one. Yours.

---

## **Stage 4 — Learning Loop**

### **Goal**
The system learns from how you use it. Application captured. Outcomes observed. Retrieval ranking moves with reality, not just decay.

### **Effort**
~3 hours. Week 2.

### **Components**

1. **Application capture mechanic**
    - When a coach output gets acted on, you tell it (or it asks 24 hours later)
    - Three capture modes: explicit `applied:<output-id>` note, agent follow-up DM, calendar event completion as implicit signal
    - All three layered; explicit dominates

2. **Outcome observation**
    - When an applied idea ships / fails / iterates, capture that back as a source
    - Outcome links back to the original idea page, supersedes if learnings change the plan

3. **Retrieval-score evolution**
    - Surface events logged
    - Citations in coach outputs reinforce
    - Ignored surfaces decay
    - Per-context modifiers learned (this source ranks higher in `work-strategy` context, lower in `creative`)

4. **Linkage-scout daemon active**
    - Nightly walk, finds high-confidence pages with sparse connections
    - Proposes linkages to a `for-your-attention` queue
    - Daily brief surfaces top-3

5. **Debaiser auto-trigger**
    - When a load-bearing claim accumulates >5 reinforcements without contradiction, debaiser runs unprompted
    - Output goes into the next morning's brief: "I think you might be in an echo chamber on X"

### **What you do NOT create**
- Still no friend handoff (S5)

### **Checkpoint**
- A page you cited in a coach output two weeks ago shows visibly higher rank in fresh retrievals on related queries
- The system has caught at least one echo-chamber pattern and surfaced it in a morning brief
- Linkage-scout has proposed at least one connection that genuinely surprised you

### **Deliverable**
A system that gets better the more you use it, without you grading anything.

---

## **Stage 5 — Friend-Ready**

### **Goal**
Onboarding conversation built. Bespoke proven scalable by spinning up a second `me`. Friend's first capture lands cleanly.

### **Effort**
~2 hours. Week 3, when a friend's ready.

### **Components**

1. **Conversational onboarder** (operation prompt)
    - Walks new user through current Ikigai → aspirational Ikigai → vocabulary seed → capture preferences → coach voice → brief cadence
    - Builds their `friend-me/CLAUDE.md` collaboratively
    - 15 minutes for a technical user, longer for a non-technical one — same conversation tree, depth follows user signal

2. **Second `me` repo created**
    - `friend-me/` next to `ikigAI-me/` on shared infra (or their own NUC)
    - Same `core/` import
    - Their vault, their tags, their voice
    - First capture from them validates the friend lands cleanly

3. **Multi-tenant access surface**
    - MCP server reads `me` from auth context
    - Tailscale ACL keeps friend's vault fully isolated
    - Daemons run per-vault

4. **Comparison pass**
    - Their experience vs yours noted
    - Anything that needs governance / operationalising surfaces here
    - Core gets the upgrade; their `me` and yours both benefit

### **What you do NOT create**
- Don't productise. This is proof-of-concept for bespoke-at-scale, not a launch.
- Don't open beyond your friend.

### **Checkpoint**
- Your friend captures their first thing
- Their first retrieval works
- Their daily brief, in their voice, lands the next morning
- You haven't refactored anything in your own setup to make theirs work

### **Deliverable**
Two people, one core, two brains. Bespoke scales.

---

# 🧭 **The IkigAI Cognitive Loop**

```
1. You capture a thought, link, voice memo, quote — from anywhere.
2. Inbox-watcher picks it up on the NUC.
3. Canonicalisation engine merges with existing records or creates new.
4. gargAIntuan orchestrator runs classification, linkage, reflection
   in parallel.
5. Page lands in vault with Ikigai regions, summary, provenance,
   linkages.
6. Linkage-scout walks the graph that night, finds non-obvious
   connections.
7. Brief-generator builds tomorrow's options across your projects,
   weighted by your focus.
8. Morning: you read the brief on your phone or web viewer.
9. You pick what to work on. Calendar event lands in Google Cal.
10. You retrieve at the gear that fits — links, synthesis, or coach.
11. You act on what landed.
12. Application capture closes the ADDIE loop.
13. Outcome observed; retrieval_score and context_modifiers update.
14. Tomorrow's brief is shaped by today's reality.
```

This is the engine. It runs whether you're at the keyboard or not.

---

# 📅 **Total Timeline**

```
Today               S0 + S1     ~3h     foundation + manual round trip
This week           S2 + S3    ~10h     NUC live, coach experience
Week 2              S4          ~3h     learning loop closes
Week 3              S5          ~2h     friend-ready
─────────────────────────────────────────
TOTAL                          ~18h     within your 20h budget
```

S0 starts now. The rest is sequenced; nothing skipped.

---

# 🎯 **What Stays Constant Across All Stages**

- The vault is plain markdown. Yours forever. Portable to anything that reads markdown.
- The frontmatter shape is the contract. Schema versioning means upgrades migrate, never break.
- Every engine is replaceable. Canonicaliser, classifier, synthesiser — all swappable behind their interfaces.
- Local-first. Cloud reaches in only when it earns it.
- The data is yours. Always. Even if every cloud you use today disappears tomorrow.

That's the no-refactor guarantee, and it's the same one ABENAKI promised in December — now backed by tooling and patterns the OSS community shipped between then and now.

---

*Schema v0.2 · Roadmap v1.0 · 2026-04-30*
*This document was written by the kind of system it describes.*
