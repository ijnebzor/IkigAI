#!/usr/bin/env python3
"""
S2 — 06 — MCP server entry point

The actual implementation lives at 05-daemons/mcp-server.py (it's a daemon,
runs in the same docker-compose stack as the rest, talks to the same vault
and index volumes).

This file exists at this path because the RUNBOOK ordering refers to
"06-mcp-server.py" — keep both filenames working without duplicating the
source. This is a thin re-export shim.

Usage in compose: `command: ["python", "-u", "/daemons/mcp-server.py"]`

If you're reading the source, go to:
    docs/s2/05-daemons/mcp-server.py

That file:
- exposes 7 tools via JSON-RPC stdio (the MCP wire format)
- calls Ollama for embeddings (Gear 1 search) and Chroma for vector lookup
- queues debaiser passes for THE DEBAISER daemon
- writes captures to inbox/<type>/ for THE WATCHER

The compose service `mcp-server` runs that script directly. Claude Desktop
and Claude Code reach this server either:
  - over SSH stdio (recommended; see 07-claude-desktop-config.md Mode A)
  - over HTTP/TCP via the bridge wrapper (Mode B in same doc)

Nothing to run from this file directly.
"""

from pathlib import Path
import sys

CANONICAL = Path(__file__).parent / "05-daemons" / "mcp-server.py"

if __name__ == "__main__":
    print("This is a routing stub. The real MCP server is at:", file=sys.stderr)
    print(f"  {CANONICAL}", file=sys.stderr)
    print("Run via docker-compose, not directly.", file=sys.stderr)
    sys.exit(1)
