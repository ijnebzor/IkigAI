# IkigAI

> A tool I built for myself.
> The framework overlays your information and your goals.
> Compounding becomes visible.
> You act on what was already there.

**Live:** [ijnebzor.github.io/IkigAI](https://ijnebzor.github.io/IkigAI/)

---

## What this is

You give it what you know. You give it where you're going. The framework — Brusselbach Ikigai, four axes, five intersections, four concentric rings — overlays. Compounding becomes visible. You act on what was already there.

The system never tells you what to do. It just makes the compounding visible — so a single action ripples across regions you didn't know it touched, and frictionless next-moves emerge from the visibility itself.

You remain the thinker. The system is the lens. Your information stays yours. Your stones stay aligned.

**The industry wants to erode your critical thinking. This is the opposite.**

## How it sees the world

Two axes, separately tagged, never conflated.

**The framework, structurally** — concentric rings (architecture):
- **Ring 1.** Identity — AIthropologist
- **Ring 2.** Operating principle — sovereignty (5 layers: data, cognitive, tooling, narrative, epistemic)
- **Ring 3.** Expression surfaces — research / tooling / discourse / practice
- **Ring 4.** Funding — salary / NFP corp / commercialisation / speaking

**The four-circle Ikigai** — a *test*, not the architecture:
- love · good_at · world_needs · paid_for
- intersections: passion (L+G), mission (L+W), profession (G+P), vocation (W+P), centre (all four)

A single move can hit multiple regions at once. The system surfaces every one.

## Three retrieval gears

| Gear | Where | Voice |
|------|-------|-------|
| **G1 — Links only** | Local Ollama, instant, free | Pure listing |
| **G2 — Synthesis** | Local draft + cloud polish | Answer + trail + compounds with + blind spot + lens check |
| **G3 — Debaiser-on-self** | Cloud (panel size requires it) | Five lenses on your own corpus |

Retrieval may go SOTA / cloud when the answer earns it. Everything else local.

## The lexicon

Your load-bearing words, with the interpretive lens *you* apply. Lives in `me/lexicon.md`. Read by every prompt before classification.

This isn't a feature. It's narrative sovereignty as architecture. Without it, the system inherits encoded meanings and your stones drift.

## What's in this repo

```
index.html                  The landing
app.html                    The build-tracker (PWA on GitHub Pages)
roadmap-reference.html      Long-form spec / curriculum
manifest.json + sw.js       PWA setup
docs/
  ikigAI-core/              Universal: schema, prompts, templates
    schema/SCHEMA.md        v0.3 contract
    prompts/                understand · retrieve · debaiser · phase-an-idea · brief · onboard · secondary
  ikigAI-me/                Personal vault (forkable shape)
    CLAUDE.md               Your vocabulary
    ikigai.md               Your framework — current vs aspirational
    lexicon.md              Your stones
    wiki/                   sources · entities · concepts · projects · ideas · outputs
  s2/                       The Saturday-execution kit (NUC provisioning, daemons, MCP)
```

The app on GitHub Pages tracks the build itself. Once shipped (S5), the day-to-day brain lives on the NUC behind Tailscale.

## Stages

| Stage | When | Effort | What |
|-------|------|--------|------|
| S0 — Foundation | Today | 2h | Schema v0.3, prompts, repo split, lexicon seeded |
| S1 — Round Trip | Today | 1h | One real source through the pipeline manually |
| S2 — NUC Live | This week | 6h | Daemons (THE WATCHER, SCOUT, KEEPER, HERALD, DEBAISER), MCP, Phase 0 dump |
| S3 — Coach Experience | This week | 4h | Three gears, web viewer, daily brief, idea-flow |
| S4 — Learning Loop | Week 2 | 3h | ADDIE close, retrieval-score evolution |
| S5 — Friend-Ready | Week 3 | 2h | Onboarding always-on, friend-me/ multi-tenant |

Open `roadmap-reference.html` for the rendered curriculum or `docs/IkigAI_Roadmap.md` for the markdown.

## The bones

I stand on the shoulders of giants and I name them:

- **[RenovAIter](https://github.com/ijnebzor/RenovAIter)** — single-file SPA shape, Drive sync, PWA setup, localStorage-first state
- **[The Digiquarium](https://github.com/ijnebzor/thedigiquarium)** — daemon naming convention (THE [ROLE]), Ollama-on-Windows-host pattern, Docker-compose orchestration, ISO 27001 + NIST CSF v2 audit pattern
- **[PoliticalDebAIser](https://github.com/ijnebzor/PoliticalDebAIser)** — five-lens contrarian panel, here pointed inward at one's own corpus
- **[PrepAIred](https://github.com/ijnebzor/prepaired)** + **[AABB](https://github.com/ijnebzor/AccountantAbilityBuddy)** — the BYOK pattern, single-file HTML, mobile-first vibe
- **ABENAKI** — the December thinking that became this
- **The framework** — Brusselbach Ikigai concentric rings, applied to a real portfolio

None of these is the thing. The thing is yours.

## Why public

Code isn't sensitive — your data lives on your device. Sovereignty is the point. The repo is public so anyone can fork their own when the schema stabilises.

This is not a product. It has never been a product. It is a tool I built for myself, with bespoke-per-user architecture so a friend can fork later without refactoring anything.

## License

MIT.

---

*Schema v0.3 · 2026*
