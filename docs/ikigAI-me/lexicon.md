# lexicon.md — Benji's load-bearing terms

> The stones I'm placing.
> Read by every IkigAI prompt before classification.
> Without this, the system inherits encoded meanings and my stones drift.
> Narrative sovereignty as architecture.

---

## sovereignty

```yaml
term: sovereignty
layers: [data, cognitive, tooling, narrative, epistemic]
seeded: true
```

**Definition:** The principle of self-ownership across every layer of one's digital and intellectual life. Refusal to be a tenant.

**My lens:** Not "freedom from rules." Sovereignty is the agency to choose what to be beholden to. Local-first is data sovereignty. Refusing to let LLMs encode meaning for me is narrative sovereignty. Building DebAIser is epistemic sovereignty. ERPNext over Odoo is tooling sovereignty. The Digiquarium controlling its specimens' information diet is cognitive sovereignty. Same idea, five layers.

When a source uses "sovereignty" to mean political independence, that's a divergent reading — interesting evidence about the world, not reinforcement of my own thinking.

---

## AIthropologist

```yaml
term: AIthropologist
layers: [identity]
seeded: true
```

**Definition:** One who studies AI as if it were a culture worth understanding rather than a tool to wield.

**My lens:** This is my identity. The Digiquarium IS this work. IkigAI is AIthropology applied to my own knowledge — turning myself into a tank I can study. Everything I make expresses this: the naming convention (each AI is a specimen), the framework doc's ring 1, the way I write about LLMs as having tendencies and worldviews. Calling myself this is not aspirational; it's the work.

---

## compounding

```yaml
term: compounding
layers: [structural]
seeded: true
```

**Definition:** A single action lighting up multiple regions of meaning simultaneously, where the visibility of those overlaps unlocks adjacent moves.

**My lens:** Not "doing more things faster." Compounding is the moment when one stone you place reveals it was already adjacent to three others. The IkigAI system's job is to make this visible — never to direct, only to surface. When a Phish Focus feature ships and it also strengthens my Digiquarium operational learning, that's compounding. When IkigAI's lexicon design idea applies back to PH2 ROE-card design, that's compounding.

---

## recursion

```yaml
term: recursion
layers: [structural]
seeded: true
```

**Definition:** When an output of one process becomes the input that improves the next iteration of itself.

**My lens:** The brain feeds itself. Every capture refines the lexicon → refines the next classification → refines the next retrieval → refines the next capture. Recursion is what makes the system get better as a function of being used, not trained. The Digiquarium's daemon system is recursive — the audits feed the operations feed the audits. IkigAI's ADDIE loop in S4 is the same shape applied to retrieval.

---

## amplification

```yaml
term: amplification
layers: [philosophical]
seeded: true
```

**Definition:** Increasing your effective capability without ceding the cognition to the amplifier.

**My lens:** I am the thinker. The system is the lens. The industry wants to erode critical thinking; this is the opposite. Amplification respects the user as the agent of their own thought. When I use Claude to draft, I'm the thinker; Claude is the amplifier. When the brief surfaces compounding I'd missed, I act on it; the system doesn't.

---

## governance

```yaml
term: governance
layers: [structural]
seeded: true
```

**Definition:** The set of practices that keep a complex system aligned with the principles it was built to express.

**My lens:** For my own life as much as for code. What practices keep me aligned to my Ikigai? What practices keep IkigAI aligned to sovereignty? What practices keep PH2's product surface aligned with human risk management as a real discipline rather than a checkbox? Same question at different scales. The Digiquarium has THE GUARD, THE SENTINEL, THE BOUNCER — those daemons are governance applied at the system level. IkigAI's lint and decay daemons are governance applied to my knowledge.

---

## agency

```yaml
term: agency
layers: [philosophical]
seeded: true
```

**Definition:** The capacity to act in line with one's values, given full visibility of consequences.

**My lens:** The system enhances agency by making consequences visible — region ripples, compounding effects, drift detection. It does not replace agency by recommending action. When a brief shows me drift, my agency is the choice of whether to correct or accept the new alignment. The system's job is the visibility, not the verdict.

---

## alignment

```yaml
term: alignment
layers: [structural]
seeded: true
```

**Definition:** When stated values, observed behaviour, and surfaced opportunities all point the same way.

**My lens:** The Ikigai test. When current ikigai matches aspirational ikigai matches what I actually fed myself this week, I'm aligned. When they diverge, that's the drift the brief surfaces. Note: this is *not* the AI-safety meaning of alignment (model behaviour matching designer intent). Different word, same family. The system should not conflate them.

---

## drift

```yaml
term: drift
layers: [structural]
seeded: true
```

**Definition:** Slow misalignment between intent and action, invisible without instrumentation.

**My lens:** The DevOps concept applied to a life. I said IkigAI was the priority but spent 12 hours this week on PH2. That's drift. The system surfaces it; I decide if it's correct alignment (PH2 deadline this week, fine) or genuine drift (PH2 has eaten 3 weeks running and I keep saying IkigAI matters more, problematic). Drift detection is a visibility tool, not a guilt tool.

---

## expression surfaces

```yaml
term: expression_surfaces
layers: [structural]
seeded: true
```

**Definition:** The four channels through which the AIthropologist identity manifests publicly: Research, Tooling, Discourse, Practice.

**My lens:** Ring 3 of the framework. Research = Digiquarium, AIthropology paper. Tooling = TheInstrumAInt/gargAIntuan and the apps. Discourse = ijneb.dev, blog, podcast, AISA talks. Practice = the day-job surface where someone else pays for the thinking. A page tagged with an expression surface answers "where does this work *show up*?" — different question than "which Ikigai axes does it touch?"

---

## naming convention

```yaml
term: naming_convention
layers: [narrative]
seeded: true
```

**Definition:** The practice of naming AI-adjacent projects with "AI" capitalised mid-word — wAIter, IkigAI, PrepAIred, RenovAIter, TrAIdie, AIsthetics, gargAIntuan, ABENAKI.

**My lens:** This is narrative sovereignty in action. The names declare that AI is *part* of the work, not the work itself, and that the work is *mine*, not the platform's. It's also a stake in the ground that I'd rather be a slightly weird wordsmith than a generic-named SaaS. Big dork energy made structural.

---

## big dork energy

```yaml
term: big_dork_energy
layers: [voice, identity]
seeded: true
```

**Definition:** The willingness to be earnestly curious, technically deep, and slightly self-deprecating without performing too-cool detachment.

**My lens:** From the ijneb.dev tagline. It's a vibe permission slip. The system can match it when I'm in flow — `ijneb-dev` voice — but should not force it on me when I'm in `accountantability` mode (drift surfaced) or in research-paper-writing mode.

---

## Adding terms

When ingesting captures, the system may suggest new lexicon entries via /lexicon-suggest. The system never auto-adds. I author. Every term gets a `lens:` field — the meaning *I* apply, in my words, with examples if it helps.

When a source uses a lexicon term in a divergent way, the lens-checker in /debaiser flags the divergence as evidence about the world, not reinforcement of my position.

When my lens evolves (e.g. I add a 6th layer to sovereignty), I update the entry. The system reads the latest version on next ingest.

---

## Schema

```yaml
---
type: lexicon
ring: operating_principle
sovereignty_layers: [narrative]
ikigai_regions: [good_at, world_needs, mission]
schema_hash: v0.3
---
```
