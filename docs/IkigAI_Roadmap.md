# IkigAI — Roadmap

> Six stages, ~18 hours, three weeks.
> Each stage produces a working state. None is throw-away.
> Schema v0.3.

The full curriculum/spec lives in `roadmap-reference.html` (rendered) and the per-stage detail in `docs/`. This file is the markdown overview.

---

## What this builds

A second brain on a NUC behind Tailscale, with a PWA build-tracker on GitHub Pages. The PWA tracks the build itself; once shipped (S5), the day-to-day brain lives on the NUC.

- **The lens:** Brusselbach Ikigai concentric rings — identity (AIthropologist), operating principle (sovereignty, 5 layers), expression surfaces (research/tooling/discourse/practice), funding architecture
- **The test:** four-circle Ikigai (love · good_at · world_needs · paid_for) applied to every page
- **The compounding visibility model:** every action shows which regions it lights up; the system surfaces but never directs
- **The lexicon:** load-bearing terms with the user's interpretive lens — narrative sovereignty as architecture
- **Three retrieval gears:** local-only (G1), local + cloud polish (G2 default), cloud-required debaiser panel (G3)

---

## The stages

### S0 — Foundation (Today, 2h)

> Schema, prompts, repo split, lexicon. No infra yet. Validatable end-to-end through Claude manually.

Components:
- Repo split: `ikigAI-core/` (universal) and `ikigAI-me/` (yours)
- Schema v0.3: rings + regions, lexicon-aware, `compounding_ripples` field, `lexicon` page type
- Operation prompts: understand, retrieve, debaiser, phase-an-idea, brief, surface, lint, onboard
- Page templates: source, entity, concept, project, idea, output, lexicon
- Personal vocabulary: `CLAUDE.md` populated from GitHub crawl (12 own projects, ijneb studios, PH2 day-job, ISC² CC, podcast)
- Lexicon: `me/lexicon.md` seeded with sovereignty (5 layers), AIthropologist, compounding, recursion, amplification, governance, agency, alignment, drift, expression surfaces, naming convention, big dork energy
- Ikigai aspiration: `me/ikigai.md` with current vs aspirational + ring architecture
- Config: `config.yml` with voice routing, brief cadence, daemon schedules

**Checkpoint:** You can read `CLAUDE.md` and recognise the contract. Pasting any source plus the understand prompt into Claude returns a properly-shaped page that respects your lexicon.

**Deliverable:** ikigAI v0.3 bundle deployed to public GitHub Pages.

### S1 — Single Round Trip (Today, 1h)

> Validate the schema with one real source through the full pipeline manually before any infra.

Components:
- Pick one real source (article, voice memo, chat-paste, or idea)
- Drop in `inbox/unsorted/` as markdown — no frontmatter needed
- Run /understand manually through Claude with `CLAUDE.md` + `ikigai.md` + `lexicon.md` context
- Save the resulting page to `wiki/sources/<id>.md`
- Run /retrieve at all three gears against the corpus-of-one
- Adjust schema/lexicon if any field felt wrong; bump `schema_hash`
- Commit to git

**Checkpoint:** You believe the foundation is right. The lexicon catches when a source uses a load-bearing word in a different sense than yours.

**Deliverable:** Schema v0.3.x post-feedback fixes, one real page committed.

### S2 — NUC Live, Brain On (This week, 6h)

> The heart of the build. Daemons follow Digiquarium THE [ROLE] naming. Reachable via Tailscale. Phase 0 brain dump complete.

The Saturday-execution kit lives in `docs/s2/`. Read `docs/s2/RUNBOOK.md` first.

Components:
- NUC provisioned: Linux, Tailscale, Docker, Python venv (`01-nuc-provision.sh`)
- Ollama installed, llama3.2 + nomic-embed-text pulled and verified (`02-ollama-setup.sh`)
- Vault dir at `~/ikigAI-me/`, git-tracked separately from main repo (`03-vault-init.sh`)
- Vector index initialised (Chroma)
- Graph index initialised (NetworkX)
- 7 daemons via docker-compose (`04-docker-compose.yml`):
  - **THE WATCHER** — inbox-watcher, inotify on `inbox/`, runs /understand
  - **THE SCOUT** — nightly graph walk, finds new linkages, queues echo-chamber flags
  - **THE KEEPER** — daily lifecycle upkeep, decay, lint
  - **THE HERALD** — daily 07:30 brief generator
  - **THE DEBAISER** — echo-chamber detector + on-demand contrarian panel
  - **THE GATEKEEPER** — Gmail watcher on label `IkigAI/Inbox`
  - **THE SCRIBE** — Calendar two-way sync
- MCP server on NUC exposing operations as tools (7 tools: capture, retrieve, phase_an_idea, brief_today, debaiser, search, get_page)
- MCP configured in Claude Desktop and Claude Code (`07-claude-desktop-config.md`, `08-claude-code-config.md`)
- Google Calendar two-way OAuth scope (`09-google-oauth.md`)
- Gmail read-only OAuth on label
- Phase 0 brain dump (`10-phase-0-playbook.md`):
  - Chrome tabs from each device (URL exploder)
  - Saved Instagram/Twitter/LinkedIn
  - Quotes from messaging apps (NEVER reference channel/sender/thread)
  - Voice memos via whisper.cpp small.en
  - Watcher processes everything; canonicalisation merges duplicates
- Verification (`11-verify.md`)

**Checkpoint:** SSH into NUC, daemons healthy. Claude Desktop on phone runs `ikigai_retrieve` over the dump. New article in inbox processes within a minute. Query "what have I been thinking about <topic>" returns canonicalised pages from past dumps.

**Deliverable:** A working brain. Real corpus. Reachable from every device.

### S3 — Coach Experience (This week, 4h)

> Three retrieval gears with real classifier. Web viewer. Daily brief. Coach voice. Productionised idea flow with calendar offers.

Components:
- Gear inference from phrasing (rules + LLM classifier fallback)
- Per-context gear preference learned
- Gear 1 — local Ollama, instant, free
- Gear 2 — local draft + Claude polish (default)
- Gear 3 — Debaiser-on-self panel via Claude (5 voices on your corpus)
- Web viewer static-served from NUC at `http://nuc.tailnet/`
- Brusselbach Ikigai diagram interactive with live region fill
- Search across whole vault with snippet highlighting
- Brief panel always accessible — today's recommended work
- THE HERALD daily 07:30 brief polished
- Brief format: stage options, recommendation with reasoning, calendar offer
- Coach voice configurable per context
- /phase-an-idea reads idea + vault + projects + ikigai + calendar
- Calendar offer: propose Phase 1 slots against real availability
- Accept slot writes Google Calendar event

**Checkpoint:** Daily brief lands in your morning, recommends across projects, offers calendar slots. Drop fresh idea, get phased plan. Click region in lens, see everything tagged. Gear 3 surfaces something you missed.

**Deliverable:** A coach. A real one. Yours.

### S4 — Learning Loop (Week 2, 3h)

> The system learns from how you use it. Application captured. Outcomes observed. Retrieval ranking moves with reality.

Components:
- Application capture: explicit `applied: <output-id>` note
- Application capture: 24-hour follow-up DM from agent
- Application capture: calendar event completion as implicit signal
- Outcome observation: shipped/failed/iterated captured as source
- Outcome links back to original idea page; supersedes if learnings change plan
- `retrieval_score` evolution: surface events logged in `feedback.jsonl`
- Citations reinforce; ignored surfaces decay
- Per-context modifiers learned
- THE SCOUT active nightly — top discoveries surface in next brief
- Debaiser auto-trigger on >5 reinforcements without contradiction
- Lexicon teachable: when you disagree with a region tag, system updates interpretation

**Checkpoint:** A page cited two weeks ago shows visibly higher rank in fresh retrievals. System has caught at least one echo-chamber pattern. THE SCOUT proposed at least one connection that genuinely surprised you.

**Deliverable:** A system that gets better the more you use it, without grading anything.

### S5 — Friend-Ready (Week 3, 2h)

> Onboarding conversation built. Bespoke proven scalable. Friend's first capture lands cleanly.

Components:
- /onboard upgraded to first-class always-on operation
- Walks user through current Ikigai → aspirational → vocabulary seed → lexicon
- Captures preferences → coach voice → brief cadence
- Re-runnable: user can reshape system as they reshape themselves
- `friend-me/` created next to `ikigAI-me/`, same `core/` import
- Multi-tenant MCP: server reads `me` from auth context
- Tailscale ACL keeps friend's vault isolated
- Daemons run per-vault
- Comparison pass: their experience vs yours, governance gaps surfaced

**Checkpoint:** Friend captures their first thing. Their first retrieval works. Their daily brief in their voice lands next morning. You haven't refactored anything.

**Deliverable:** Two people, one core, two brains. Bespoke scales.

---

## After S5

The system is yours forever. The daemons run on your NUC, the vault lives on your hardware, the corpus grows every time you capture. There is no S6 — just maintenance and the occasional schema-bump as your thinking evolves.

The lexicon grows. The framework gets re-tested through /onboard quarterly. The voices get tuned. The DEBAISER catches echo chambers you didn't know you were forming. The HERALD shows you drift before it becomes a year-long pattern.

It's not a product. It's a tool you built for yourself, with bespoke-per-user architecture so a friend can fork later. The friend gets their own. The compounding stays visible. The thinking stays yours.
