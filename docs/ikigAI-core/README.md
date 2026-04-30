# ikigAI-core/

The universal layer of IkigAI. Shared across every user.

```
schema/        SCHEMA.md — the contract every page adheres to
prompts/       Operation prompts (the brain of every daemon)
templates/     Page templates with valid v0.2 frontmatter
daemons/       Specs for every daemon (S2 implements them)
scripts/       Utilities (URL exploder, etc)
bin/           CLI entry points (S2 builds these)
ui/            Web viewer (S3 builds this)
examples/      A demo "me" so new users see it work before configuring
```

## Contract with `me/`

`me/` consumes `core/`:
- Reads schema from `core/schema/SCHEMA.md`
- Reads prompts from `core/prompts/*.md`
- Reads daemon specs from `core/daemons/SPECS.md`
- Uses templates from `core/templates/`
- Calls scripts from `core/scripts/`

`me/` never modifies `core/`. Personal customisation lives in `me/CLAUDE.md`,
`me/ikigai.md`, and `me/config.yml`.

## Versioning

Schema: `v0.2` (in SCHEMA.md frontmatter).

When core ships v0.3, lint flags every `me/wiki/**/*.md` page with
older `schema_hash`. Migration scripts in `core/scripts/migrate/`
update those pages.

## Dependencies

The prompts in `core/prompts/` are model-agnostic. Implementations in
S2 will choose:
- Local model (Ollama llama3.2) for understand drafts, classification, embeddings
- Cloud model (Claude) for Gear 2 polish, Gear 3 debaiser, daily brief

This split is a `me/config.yml` choice. Core just describes what each
prompt expects and produces.

## Forking

When user #2 onboards in S5:
- They get their own `friend-me/` next to `ikigAI-me/`
- Both `me/`s import the same `core/`
- Their CLAUDE.md is theirs
- Their data never crosses into yours

If `core/` improves, both `me/`s benefit immediately. If your `me/`
schema drifts experimentally, friend's `me/` is untouched.
