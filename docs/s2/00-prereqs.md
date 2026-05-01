# S2 — 00 — Prerequisites

> Read first. Don't skip. The whole packet assumes these are true.

## Hardware

- [ ] An Intel NUC (or equivalent x86_64 mini-PC) with:
  - [ ] Minimum 16GB RAM (32GB recommended for llama3.2 + daemons)
  - [ ] Minimum 256GB SSD
  - [ ] Wired Ethernet preferred (Ollama doesn't love wifi instability)
  - [ ] Power: always-on; brain runs 24/7

## OS

- [ ] Ubuntu 22.04 LTS or 24.04 LTS (these scripts assume apt)
- [ ] Sudo access for the NUC user (don't run as root)
- [ ] SSH enabled and reachable from your laptop on local network

## Network

- [ ] Tailscale account ([login.tailscale.com](https://login.tailscale.com))
- [ ] Tailscale auth key ready (Settings → Keys → Generate auth key, reusable, ephemeral=no)
- [ ] Decided your NUC's tailnet name (e.g. `nuc.tailnet` — gets a `*.ts.net` URL too)

## Identity / Auth

- [ ] Google account for Calendar + Gmail OAuth (recommend a separate "tooling" account, not your primary)
- [ ] GitHub account already linked (for cloning the IkigAI repo)
- [ ] An Anthropic API key (or willing to add later for cloud retrieval gears)

## Software you'll install (the scripts handle most of this)

- Docker + docker-compose plugin
- Python 3.11+ + venv
- Git
- Ollama
- whisper.cpp (compiled local; `small.en` model)
- Node.js 20+ (for any tooling that needs it; Claude Code prereq)

## Mental prerequisites

- [ ] You've already done S0 + S1. The schema feels right. The lexicon has at least 5 seeded terms. Your `me/CLAUDE.md` knows your active projects.
- [ ] You've decided which capture surfaces matter most to you (chrome share / voice / gmail label / chat-paste). At minimum, voice + manual file drop.
- [ ] You've blocked roughly 6 hours. This isn't a 90-minute job; trying to compress it produces flaky daemons.
- [ ] You're comfortable SSHing into a Linux box and reading bash. If not, run the scripts via Claude Code which can explain each step.

## What this packet assumes

- The NUC is a single-user device. The user owning the vault is the same as the user running Docker.
- You're the only person who will ever access this vault. Multi-tenancy is a S5 concern.
- The repo on GitHub is `ijnebzor/IkigAI`. If you've forked, swap names accordingly throughout.
- You intend to keep the NUC powered on. Daemons that never run aren't useful.

## Sanity check before you start

```bash
# On your laptop
ssh <user>@<nuc-ip>            # works
ssh <user>@<nuc-ip> 'whoami'    # returns your user, not root
ssh <user>@<nuc-ip> 'free -h'   # shows ≥16GB RAM
ssh <user>@<nuc-ip> 'df -h /'   # shows ≥100GB free
```

If any of those fail, fix before proceeding.

## A note on security

You are the only user. The vault is on your own hardware on a Tailscale-private network. The MCP server doesn't bind to public interfaces. The OAuth credentials live in `~/.config/ikigai/secrets/` with `chmod 600`.

That said:
- Don't put the NUC on a public IP.
- Don't share the Tailscale auth key.
- Don't commit secrets to the repo (`.gitignore` already excludes `secrets/`, `*.token`, `.env`).
- Rotate the OAuth tokens annually or after any suspicion of compromise.
- If you ever sell or decommission the NUC: `shred -u` the vault dir before wipe.

OK. If everything above is true, proceed to `01-nuc-provision.sh`.
