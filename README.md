# IkigAI

> Your brain, coached.
> A self-owned system that reads everything you send it, links it to everything else, and helps you turn ideas into action.

**Live:** [ijnebzor.github.io/IkigAI](https://ijnebzor.github.io/IkigAI/)

---

## What this is

IkigAI is a personal coach grounded in everything you know and read. It runs on your home device, ingests anything you send it from anywhere, and helps you turn ideas into action against the life you're actually trying to build.

The lens is the four-axis Brusselbach Ikigai: **love · good_at · world_needs · paid_for**. Every captured thing gets placed in the regions it touches, so a single contribution compounds across passion, mission, vocation, profession, and the centre.

Retrieval has three gears:
- **Gear 1 — Links only.** Pure search across your own corpus.
- **Gear 2 — Synthesis.** Answer + provenance trail + action + blind spot + biases.
- **Gear 3 — Debaiser-on-self.** Five analyst voices on your own knowledge, pushing back.

The system watches what you actually use and learns what to surface for you. You don't grade it; it watches you grade implicitly.

## What's in this repo

```
index.html                  Landing page
app.html                    The build-tracker app (this is what runs on GitHub Pages)
roadmap-reference.html      Long-form curriculum / spec document
manifest.json + sw.js       PWA setup
docs/                       Schema v0.2 spec, prompts, templates
  IkigAI_Roadmap.md         Full roadmap as markdown
  QUICKSTART.md             How to run S0 + S1 today
  ikigAI-core/              Universal layer: schema, prompts, daemons, scripts
  ikigAI-me/                Personal layer: vault skeleton (forkable for any user)
```

The app on GitHub Pages tracks the build itself. Once IkigAI is shipped (Stage 5), the day-to-day app lives on your NUC behind Tailscale.

## Architecture, in one diagram

```
                    YOU (any device, anywhere)
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         CAPTURE         RETRIEVE        REFLECT
              │               │               │
              └───────────────┼───────────────┘
                              │
                  Tailscale + MCP/SSH
                              │
              ╔═══════════════╧═══════════════╗
              ║   NUC (i7) — always on        ║
              ║   inbox-watcher · scout       ║
              ║   brief-generator · debaiser  ║
              ║   markdown vault              ║
              ║   Ollama + Claude             ║
              ╚═══════════════════════════════╝
```

## Stages

| Stage | When | Effort | What |
|---|---|---|---|
| S0 — Foundation | Today | 2h | Schema, prompts, repo split |
| S1 — Round Trip | Today | 1h | One real source through the pipeline |
| S2 — NUC Live | This week | 6h | Daemons, indexes, MCP, Phase 0 dump |
| S3 — Coach Experience | This week | 4h | Three gears, web viewer, daily brief |
| S4 — Learning Loop | Week 2 | 3h | ADDIE close, retrieval-score evolution |
| S5 — Friend-Ready | Week 3 | 2h | Bespoke proven scalable |

See `docs/IkigAI_Roadmap.md` for the full spec, or open `roadmap-reference.html` for the rendered curriculum.

## Why public

The code isn't sensitive — your data lives on your device. Sovereignty is the point. The repo is public so anyone can fork their own IkigAI when v0.2 stabilises.

## Built with

- [RenovAIter](https://github.com/ijnebzor/RenovAIter) bones — single-file SPA architecture, Drive sync, PWA setup, mobile-first patterns
- ijneb.dev design tokens — `#0d0d0d` background, `#c8f135` accent, JetBrains Mono + Syne + DM Sans

## License

MIT (forkable, modifiable, redistributable).

---

*Schema v0.2 · 2026*
