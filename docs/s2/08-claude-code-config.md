# S2 — 08 — Claude Code config

> Configuring Claude Code on the NUC itself (or on your laptop SSH'd in) to talk to the IkigAI MCP server.
> Same MCP target as Claude Desktop, different config location.

## Why Claude Code on the NUC

When you're SSH'd into the NUC and want to:
- Read/edit pages in `~/ikigAI-me/`
- Run `/understand` or `/retrieve` against your real corpus
- Run `git diff` on the vault and reason about what changed
- Add a new daemon and have Claude know the existing daemon shape

...Claude Code with MCP gives you everything inline.

## Install Claude Code

If not already installed on the NUC:

```bash
# Node.js 20+ required
node --version  # should be ≥20

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

## Where the config lives

Claude Code reads MCP servers from `~/.config/claude/mcp.json` on Linux.

```bash
mkdir -p ~/.config/claude
```

## Two ways to wire MCP

Same modes as Desktop, simpler in this case because Claude Code is *on* the NUC — no SSH bridge needed.

### Option 1 — Direct stdio to running container (recommended)

```json
// ~/.config/claude/mcp.json
{
  "mcpServers": {
    "ikigai": {
      "command": "docker",
      "args": ["exec", "-i", "ikigai-mcp", "python", "-u", "/daemons/mcp-server.py"]
    }
  }
}
```

Claude Code runs `docker exec -i ikigai-mcp python /daemons/mcp-server.py` and pipes JSON-RPC over stdio. No network involved.

Works because Claude Code is running as the NUC user, who's in the `docker` group.

### Option 2 — Run a fresh MCP server outside compose

If you don't want Claude Code attached to the long-running daemon container:

```json
{
  "mcpServers": {
    "ikigai": {
      "command": "/home/<nuc-user>/ikigai-state/venv/bin/python",
      "args": ["/home/<nuc-user>/IkigAI/docs/s2/05-daemons/mcp-server.py"],
      "env": {
        "VAULT_DIR": "/home/<nuc-user>/ikigAI-me",
        "INDEX_DIR": "/home/<nuc-user>/ikigai-state/index",
        "OLLAMA_HOST": "http://localhost:11434"
      }
    }
  }
}
```

Each Claude Code session spawns its own MCP server process. Slightly more isolation, slightly more startup latency. Pick based on preference.

## Verify

```bash
cd ~/IkigAI
claude
```

In the chat:

> /mcp

Should list `ikigai` with 7 tools.

> Use ikigai_search to find anything about sovereignty in my corpus.

If the corpus has anything matching, you'll see results. If empty, *"No matches"* is the correct response — not a failure.

## Useful Claude Code workflows on the NUC

### Walk through S2 step-by-step (the recommended approach)

```
cd ~/IkigAI
claude

> Walk through docs/s2/ in order. Read RUNBOOK.md first, then 00-prereqs.md.
> Stop after each step and confirm before proceeding. Show me the output of
> every command. Don't proceed if anything fails.
```

### Add a new daemon

```
> I want to add THE CRITIC daemon. It should run weekly, read all
> outputs marked applied:true, and rate retrieval ranking against actual
> use. Look at how the-keeper.py is structured and propose a new file
> in s2/05-daemons/ following the same shape.
```

### Audit the vault

```
> Read the latest state/lint-*.md and tell me what to clean up.
> Don't fix anything yet — just summarise.
```

### Explore corpus through MCP

```
> Use ikigai_retrieve with query "compounding visibility" gear=2.
> Then use ikigai_get_page on the top result and explain what's in it.
```

## Editing the vault directly

Claude Code edits files in place. When working in `~/ikigAI-me/`, the vault is a separate git repo (set up in 03-vault-init). Commit changes from Claude Code as normal:

```
> After we just added that lexicon entry, commit it to the vault repo.
```

Don't commit secrets. The `.gitignore` in the vault excludes `state/`, `secrets/`, `*.token`, `.env`. Verify with `git status` before push.

## Troubleshooting

**"docker exec fails: No such container: ikigai-mcp"**
- `docker compose ps` — is the MCP container running?
- `docker compose up -d mcp-server` to start

**"MCP server starts but tools don't appear"**
- Check container has read access to volumes: `docker exec ikigai-mcp ls /vault`
- Check `~/.config/claude/mcp.json` is valid JSON: `cat ~/.config/claude/mcp.json | jq`

**"ANTHROPIC_API_KEY not set"**
- Claude Code needs its own key (separate from MCP server's key for cloud retrieval)
- `export ANTHROPIC_API_KEY=sk-ant-...` in `.bashrc` or `.zshrc`
- For docker-compose to also see the key (for daemons that polish via Claude), use a `.env` file in `docs/s2/`:
  ```
  ANTHROPIC_API_KEY=sk-ant-...
  VAULT_DIR=/home/<nuc-user>/ikigAI-me
  INDEX_DIR=/home/<nuc-user>/ikigai-state/index
  LOGS_DIR=/home/<nuc-user>/ikigai-state/logs
  SECRETS_DIR=/home/<nuc-user>/ikigai-state/secrets
  ```

**"Claude Code says corpus is empty even though I added pages"**
- The vector index needs the page added — usually THE WATCHER handles this. Confirm watcher is running and has processed the file.
- Force a reindex: `docker compose restart the-watcher`

---

## Multi-machine note

When you SSH from your laptop to the NUC, Claude Code on the laptop can also use the same MCP server via the SSH-bridge approach (see `07-claude-desktop-config.md`). You don't need Claude Code installed on the NUC; the laptop one will reach the MCP server through SSH.

The on-NUC Claude Code option exists for when you're on-NUC anyway (e.g. doing infra work) and want immediate access without SSH'ing back to your laptop.
