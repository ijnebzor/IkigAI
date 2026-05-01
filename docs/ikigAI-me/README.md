# ikigAI-me/

> Bespoke. This user's vault. Not for friend's eyes.

This directory contains the user's specific instance:

- Their identity, vocabulary, current context (`CLAUDE.md`)
- Their concentric-rings architecture and four-circle position (`ikigai.md`)
- Their load-bearing terminology with their interpretive lens (`lexicon.md`)
- Their daemon config (`config.yml`)
- Their captures (`inbox/`, then routed into `wiki/`)
- Their runtime state (`state/`)
- Their corpus (`wiki/`)

## Friend onboarding

Friend forks the repo. Deletes everything in `me/` except `wiki/dimensions/` (the schema rollup pages stay). Runs `/onboard` from S5. The conversation generates their version of CLAUDE.md, ikigai.md, lexicon.md, config.yml. Their captures fill their inbox. Same core/. Different me/. Two brains, one architecture.

## Privacy

The `me/` directory is single-tenant. Even if you self-host the repo as a public mirror, the friend's `me/` is in a separate repo with its own ACL. Tailscale ACLs keep daemon-served APIs isolated per-vault.

## Don't commit

- `state/voice_prefs.yml` if it contains keys
- `inbox/` items containing PII without consent
- `state/feedback.jsonl` if you'd rather not log retrieval history (it's local-only either way, but you can choose)

`.gitignore` is set accordingly.
