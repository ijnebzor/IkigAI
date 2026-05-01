# S2 — 07 — Claude Desktop config

> Connecting Claude Desktop (your phone, your laptop, anywhere on the tailnet) to the IkigAI MCP server running on the NUC.

## What this enables

Once Claude Desktop talks to the NUC's MCP server, you get these tools available in any chat:

- `ikigai_capture` — drop content into the inbox from a phone chat
- `ikigai_retrieve` — three-gear retrieval over your corpus
- `ikigai_phase_an_idea` — submit an idea for phasing
- `ikigai_brief_today` — pull today's brief
- `ikigai_debaiser` — invoke the contrarian panel
- `ikigai_search` — quick vector search
- `ikigai_get_page` — read a specific page by id

## Two connection modes

Pick one. SSH-stdio is simpler and more secure (no open ports on the NUC). HTTP/TCP is more flexible if you also want browser-based clients.

---

## Mode A — SSH stdio (recommended)

Claude Desktop spawns the MCP server over SSH. The MCP server runs *inside the docker-compose stack* on the NUC, but the SSH-bridge connects to it.

### NUC-side: a small SSH-callable wrapper

On the NUC:

```bash
# ~/bin/ikigai-mcp-bridge
#!/bin/bash
exec docker exec -i ikigai-mcp python -u /daemons/mcp-server.py
```

Make it executable:

```bash
chmod +x ~/bin/ikigai-mcp-bridge
```

### Claude Desktop config

On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ikigai": {
      "command": "ssh",
      "args": [
        "<your-tailscale-name>",
        "/home/<nuc-user>/bin/ikigai-mcp-bridge"
      ]
    }
  }
}
```

Replace:
- `<your-tailscale-name>` with the NUC's Tailscale name (e.g. `nuc.tail-abc123.ts.net`)
- `<nuc-user>` with the NUC user whose home holds the bridge script

### Verify SSH works without password

Claude Desktop can't enter SSH passwords. Use SSH keys:

```bash
# On your laptop
ssh-copy-id <nuc-user>@<your-tailscale-name>
ssh <your-tailscale-name>  # should not prompt for password
```

### Restart Claude Desktop

Quit fully, reopen. You should see the tools listed when you check the MCP indicator (lower-right corner of the input).

---

## Mode B — HTTP/TCP (alternative)

Useful if you want browser-based MCP clients later. Less secure if mis-configured (don't bind to public).

### Expose the MCP server on a Tailscale-only port

In `04-docker-compose.yml`, change the `mcp-server` service to bind to the Tailscale interface:

```yaml
  mcp-server:
    <<: *daemon-base
    container_name: ikigai-mcp
    command: ["python", "-u", "/daemons/mcp-server.py", "--http", "--port", "8765"]
    ports:
      - "100.0.0.0/8:8765:8765"   # Tailscale-only, NOT 0.0.0.0
```

Note: docker doesn't natively support binding to a CIDR. The simplest way to enforce tailnet-only is via UFW:

```bash
sudo ufw default deny incoming
sudo ufw allow in on tailscale0
sudo ufw enable
```

Then `0.0.0.0:8765` is fine because the firewall only lets tailnet traffic through.

The `--http` flag isn't implemented in the v0.3 MCP server (which is stdio-only by default). To enable HTTP mode, add a uvicorn wrapper — see `06-mcp-server.py` for stdio-only; HTTP is a future enhancement.

For now, **prefer Mode A**.

---

## Test the connection

Open a new Claude Desktop chat:

> Use the ikigai_brief_today tool and tell me what's in today's brief.

If the MCP server is healthy and the brief exists, Claude returns the brief content. If THE HERALD hasn't run yet, you'll see `{"status": "no_brief_today"}`.

> Capture this thought: "Sovereign systems trade discoverability for trust."

Claude calls `ikigai_capture` with type=`thought`. Within ~30 seconds, THE WATCHER processes the file and you'll see it in `wiki/sources/` after a `ls` on the NUC.

## Troubleshooting

**"Tools not appearing in Claude Desktop"**
- Restart Claude Desktop fully
- Check JSON syntax: `cat ~/Library/.../claude_desktop_config.json | jq`
- SSH manually to confirm: `ssh <tailscale-name> /home/<nuc-user>/bin/ikigai-mcp-bridge` should print MCP server banner to stderr

**"SSH timing out"**
- Tailscale might not be authenticated; check `tailscale status` on both ends
- Firewall: `sudo ufw status` on NUC; allow port 22 from `tailscale0`

**"Docker exec fails — container not running"**
- `docker compose ps` on NUC
- Check `mcp-server` is up
- `docker compose logs mcp-server` — look for crash on boot (usually missing volume mount)

**"Permission denied on docker exec"**
- The NUC user needs to be in `docker` group: `groups | grep docker`
- If not: `sudo usermod -aG docker $USER`, then log out + back in

---

## What this DOES NOT do

- Doesn't handle authentication beyond SSH keys + Tailscale ACLs. That's intentional. The whole IkigAI security model is "the tailnet is the boundary."
- Doesn't multi-tenant. If you eventually have a friend-me/, you'll need a separate MCP server per vault, with the bridge script differing.
