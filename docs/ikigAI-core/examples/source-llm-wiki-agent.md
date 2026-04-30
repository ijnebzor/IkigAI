---
id: 2026-04-30-llm-wiki-agent
type: source
created: 2026-04-30T08:54:00+11:00
updated: 2026-04-30T08:54:00+11:00

ikigai_regions: [love, good_at, world_needs, paid_for, passion, mission, profession, vocation, centre]

summary: >
  SamurAIGPT/llm-wiki-agent is a Claude Code skill that turns dropped sources
  into a persistent interlinked markdown wiki — auto-creating entity and
  concept pages, flagging contradictions at ingest, and generating a graph
  visualisation. It's the production version of Karpathy's LLM Wiki pattern,
  with the lifecycle additions from the rohitg00 v2 gist. Directly relevant
  to IkigAI's core canonicalisation and linkage approach.

tags: [ai, sovereignty, tool, to-implement, knowledge-management]

sources_raw:
  - https://github.com/SamurAIGPT/llm-wiki-agent
derived_from: []
supersedes: []
superseded_by: null
confidence: 0.7
last_reinforced: 2026-04-30
drivers: [project-research, idea-generation]
biases: []

retrieval_score: 0.5
last_surfaced: null
last_used: null
context_modifiers: {}
surface_count: 0
use_count: 0

status: canonical
schema_hash: v0.2

source_type: web
source_url: https://github.com/SamurAIGPT/llm-wiki-agent
source_date: 2026-04-30
captured_from: chrome_phone
extracted_entities:
  - "[[claude-code]]"
  - "[[obsidian]]"
extracted_concepts:
  - "[[knowledge-graph]]"
  - "[[canonicalisation]]"
  - "[[wiki-pattern]]"
fetched_via: normal
---

# llm-wiki-agent — production Claude Code skill for self-building wiki

## Summary
SamurAIGPT/llm-wiki-agent is a Claude Code skill that turns dropped sources into a persistent interlinked markdown wiki — auto-creating entity and concept pages, flagging contradictions at ingest, and generating a graph visualisation. It's the production version of Karpathy's LLM Wiki pattern, with the lifecycle additions from the rohitg00 v2 gist. Directly relevant to IkigAI's core canonicalisation and linkage approach.

## Key claims
- The wiki *itself* is the artifact; chat answers are throwaway
- Canonicalisation at ingest beats RAG retrieval at query time
- Two-pass graph build: deterministic from `[[wikilinks]]` + semantic for implicit edges
- Works without API key (uses Claude Code's existing auth)
- 1.2k stars, MIT license — mature enough to study and fork

## Connections
- Reinforces: [[canonicalisation]] — multi-key matching is the load-bearing step
- Reinforces: [[wiki-pattern]] — Karpathy's original framing
- Extends: [[abenaki-segment-6]] — IkigAI's planned canonical record pattern
- Pattern in: [[ikigai-core-prompts]] — `/understand` borrows the structure

## Open questions
- How does this scale past ~10k pages? Their stress-test data isn't published.
- Their merge logic for chat-paste content — does it handle anonymisation cleanly?
- Could the inferred-edges layer feed our `linkage-scout` directly?

## Raw notes
> "Most knowledge tools make you search your own notes. This one reads everything you've collected and writes a structured wiki that compounds over time."
> — Their README, captures the IkigAI thesis exactly.

---

<!-- This is what a fully-processed source looks like after running /understand. -->
<!-- Note ikigai_regions hits all 9 (rare!) because this source touches Benji's centre: -->
<!--   loves it (passion), is good at it (passion), world needs it (mission), -->
<!--   paid_for path via productisation (vocation+profession). Genuine centre case. -->
<!-- Confidence 0.7 not 0.5 because primary source (the repo itself) and reinforces existing concepts. -->
