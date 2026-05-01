# S2 — NUC Live, Brain On

> The Saturday-execution kit.
> 6 hours. End state: a working brain on your NUC, reachable from every device, processing real captures.
> You execute this on the NUC itself (probably via Claude Code SSH'd in).
> I built the docs; you provision the hardware and run the scripts.

## What S2 produces

- A NUC running Linux + Tailscale + Docker + Ollama + Python venv
- Vault dir at `~/ikigAI-me/` git-tracked
- Vector index (Chroma) initialised
- Graph index (NetworkX) initialised
- 7 daemons running, named after the Digiquarium pattern (THE WATCHER / SCOUT / KEEPER / HERALD / DEBAISER / GATEKEEPER / SCRIBE)
- An MCP server on the NUC exposing `ikigai_capture`, `ikigai_retrieve`, `ikigai_phase_an_idea`, `ikigai_brief_today`, `ikigai_debaiser`
- Claude Desktop and Claude Code configured to talk to the MCP server over Tailscale
- Google Calendar two-way OAuth scope live
- Gmail read-only OAuth on label `IkigAI/Inbox`
- Phase 0 brain dump complete — Chrome tabs, Insta/Twitter/LinkedIn saved, voice memos transcribed via whisper.cpp, chat-paste quotes, all canonicalised

By the end, you can SSH into the NUC, daemons are healthy, Claude Desktop on your phone runs `ikigai_retrieve` over the dump, and a new article in inbox/ processes within a minute.

## What you need before starting

See `00-prereqs.md`.

## The order

```
00-prereqs.md           Check this first
01-nuc-provision.sh     Linux baseline, Tailscale, Docker, Python
02-ollama-setup.sh      Install Ollama, pull llama3.2, verify
03-vault-init.sh        Clone repo to NUC, set up me/ from your edits
04-docker-compose.yml   The orchestrator
05-daemons/             Source for each daemon (Python)
  the-watcher.py        Inbox monitor, runs /understand
  the-scout.py          Nightly graph walk, finds new linkages
  the-keeper.py         Daily lifecycle upkeep, decay, lint
  the-herald.py         Daily brief generator (07:30)
  the-debaiser.py       Echo-chamber detector + on-demand
  the-gatekeeper.py     Gmail watcher on label
  the-scribe.py         Calendar two-way sync
06-mcp-server.py        Exposes operations as tools
07-claude-desktop-config.md   JSON for Claude Desktop
08-claude-code-config.md      JSON for Claude Code on the NUC
09-google-oauth.md      OAuth setup (Calendar + Gmail)
10-phase-0-playbook.md  The brain dump procedure
11-verify.md            Health checks, smoke tests
RUNBOOK.md              This file (the narrative)
```

## How to execute

The recommended approach: SSH into the NUC, fire up Claude Code in the IkigAI repo, ask it to walk through `s2/` in order. It can read each file, run scripts, react to errors, and adapt.

```bash
# On the NUC
ssh nuc
cd ~/IkigAI
claude
```

Then prompt:

> Walk through docs/s2/ in order. Read RUNBOOK.md first, then 00-prereqs.md. Stop after each step and confirm before proceeding. Show me the output of every command. Don't proceed if anything fails.

You stay in the loop on every step. Claude Code does the typing; you do the verifying.

Estimated time per phase:

| Phase | Time | What |
|-------|------|------|
| 00-01 | 45m | Provision the NUC |
| 02 | 20m | Ollama working |
| 03 | 15m | Vault on disk |
| 04 | 30m | Docker-compose up, daemons running |
| 05 | 60m | Each daemon verified |
| 06 | 30m | MCP server live |
| 07-08 | 20m | Claude clients configured |
| 09 | 30m | Google OAuth |
| 10 | 90m | Phase 0 brain dump |
| 11 | 20m | Verify everything |
| **Total** | **~6h** | |

## What can go wrong

- **Ollama refuses connections** — check firewall, port 11434, host binding (`OLLAMA_HOST=0.0.0.0`)
- **Tailscale ACLs block daemon-to-daemon** — open intra-tailnet traffic
- **Docker volume permissions** — vault dir owned by NUC user, not root
- **Whisper.cpp slow** — small.en is fine; medium is slow; tiny.en is too lossy for voice memos
- **Google OAuth redirect mismatch** — `http://localhost:8080/callback` vs `http://nuc.tailnet/callback`; pick one and stick

Each step doc has its own troubleshooting block.

## What this kit deliberately does NOT do

- **Doesn't deploy a public web server.** Everything is Tailscale-local.
- **Doesn't auto-update.** You decide when to pull schema changes.
- **Doesn't backup.** That's a separate concern (recommended: rsync to a second NUC or a SOC-compliant cloud, your call).
- **Doesn't multi-tenant.** That's S5. This is single-vault.
- **Doesn't replace ABENAKI's existing infra if any** — it's `ikigAI-me/`, separate dir, you decide if/when to merge.

## After S2 ships

You go to S3:
- Three retrieval gears with real classifier
- Web viewer at `http://nuc.tailnet/`
- Brusselbach diagram interactive
- THE HERALD generates daily 07:30 brief
- /phase-an-idea reads idea + vault + projects + calendar, offers slot

S3 is documented in `roadmap-reference.html#s3` and follows the same shape as this packet.
