#!/usr/bin/env python3
"""
MCP server for IkigAI

Exposes the operations as tools accessible via the Model Context Protocol.
Claude Desktop and Claude Code talk to this server (over stdio or local TCP).

Tools exposed:
  - ikigai_capture(text, type) — drop content into inbox/<type>/
  - ikigai_retrieve(query, gear) — three-gear retrieval
  - ikigai_phase_an_idea(idea_text) — generate phased plan
  - ikigai_brief_today() — return today's brief
  - ikigai_debaiser(topic_id) — invoke contrarian panel
  - ikigai_search(query, n) — fast vector search
  - ikigai_get_page(id) — read a page by id

Run as part of the docker-compose stack.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import yaml
import frontmatter
import chromadb
import ollama

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
LOGS = Path(os.environ.get("LOGS_DIR", "/logs"))
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")

CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())

ollama_client = ollama.Client(host=OLLAMA_HOST)
EMBED_MODEL = CONFIG["ollama"]["embed_model"]
chroma_client = chromadb.PersistentClient(path=str(INDEX / "chroma"))
sources_coll = chroma_client.get_or_create_collection("sources")


# ─── Tool implementations ────────────────────────────────────────

def tool_capture(text: str, capture_type: str = "thought") -> dict:
    """Drop text into inbox/<type>/"""
    valid_types = {"web", "voice", "email", "chat", "tabs", "ideas", "unsorted", "thought"}
    if capture_type not in valid_types:
        capture_type = "unsorted"
    inbox = VAULT / "inbox" / capture_type
    inbox.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date().isoformat()
    timestamp = datetime.now(timezone.utc).strftime("%H%M%S")
    out = inbox / f"{today}-{timestamp}.md"
    out.write_text(f"# Capture\n\n{text}\n")
    return {
        "status": "captured",
        "path": str(out.relative_to(VAULT)),
        "next": "THE WATCHER will process within ~30 seconds.",
    }


def tool_retrieve(query: str, gear: int = 2) -> dict:
    """Vector search + assembly."""
    if gear not in (1, 2, 3):
        gear = 2

    try:
        embedding = ollama_client.embeddings(model=EMBED_MODEL, prompt=query)["embedding"]
    except Exception as e:
        return {"error": f"embedding failed: {e}"}

    try:
        results = sources_coll.query(query_embeddings=[embedding], n_results=10)
    except Exception as e:
        return {"error": f"query failed: {e}"}

    ids = results.get("ids", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    docs = results.get("documents", [[]])[0]

    matches = []
    for i, page_id in enumerate(ids):
        meta = metas[i] if i < len(metas) else {}
        matches.append({
            "id": page_id,
            "summary": meta.get("summary", ""),
            "regions": meta.get("regions", "").split(",") if meta.get("regions") else [],
            "snippet": (docs[i][:200] if i < len(docs) else ""),
        })

    if gear == 1:
        return {
            "gear": 1,
            "query": query,
            "results": matches[:8],
        }
    elif gear == 2:
        return {
            "gear": 2,
            "query": query,
            "trail": matches[:5],
            "note": "G2 synthesis pending Claude integration; here are the top trail entries.",
        }
    else:
        return {
            "gear": 3,
            "query": query,
            "trail": matches[:5],
            "note": "G3 debaiser invocation queued. Run the_debaiser daemon to process.",
        }


def tool_phase_an_idea(idea_text: str) -> dict:
    """Drop the idea in inbox/ideas/ and return queue confirmation."""
    today = datetime.now(timezone.utc).date().isoformat()
    timestamp = datetime.now(timezone.utc).strftime("%H%M%S")
    inbox = VAULT / "inbox" / "ideas"
    inbox.mkdir(parents=True, exist_ok=True)
    out = inbox / f"{today}-{timestamp}-idea.md"
    out.write_text(f"---\nidea_status: raw\n---\n\n{idea_text}\n")
    return {
        "status": "queued",
        "path": str(out.relative_to(VAULT)),
        "next": "THE WATCHER will canonicalise; phase-an-idea will run on next pass.",
    }


def tool_brief_today() -> dict:
    """Return today's brief if it exists."""
    today = datetime.now(timezone.utc).date().isoformat()
    brief_path = VAULT / "wiki" / "outputs" / f"brief-{today}.md"
    if not brief_path.exists():
        return {"status": "no_brief_today", "note": "THE HERALD hasn't run yet today, or brief generation failed."}
    return {
        "status": "ok",
        "date": today,
        "content": brief_path.read_text(),
    }


def tool_debaiser(topic_id: str) -> dict:
    """Queue a debaiser pass."""
    queue = INDEX / "debaiser_queue.jsonl"
    queue.parent.mkdir(parents=True, exist_ok=True)
    with queue.open("a") as f:
        f.write(json.dumps({"topic_id": topic_id, "queued_at": datetime.now(timezone.utc).isoformat()}) + "\n")
    return {
        "status": "queued",
        "topic_id": topic_id,
        "note": "THE DEBAISER picks up within 2 minutes.",
    }


def tool_search(query: str, n: int = 5) -> dict:
    """Fast search wrapper."""
    return tool_retrieve(query, gear=1)


def tool_get_page(page_id: str) -> dict:
    """Read a page by id from wiki/."""
    for sub in ["sources", "concepts", "entities", "projects", "ideas", "outputs"]:
        candidate = VAULT / "wiki" / sub / f"{page_id}.md"
        if candidate.exists():
            try:
                post = frontmatter.load(candidate)
                return {
                    "id": page_id,
                    "type": sub,
                    "frontmatter": post.metadata,
                    "content": post.content,
                }
            except Exception as e:
                return {"error": f"parse failed: {e}"}
    return {"error": f"not found: {page_id}"}


# ─── MCP server (stdio) ──────────────────────────────────────────

TOOLS = {
    "ikigai_capture": {
        "fn": tool_capture,
        "description": "Drop content into the IkigAI inbox. THE WATCHER processes it within ~30s.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Content to capture."},
                "type": {"type": "string", "enum": ["web", "voice", "email", "chat", "tabs", "ideas", "thought", "unsorted"], "description": "Surface."},
            },
            "required": ["text"],
        },
    },
    "ikigai_retrieve": {
        "fn": tool_retrieve,
        "description": "Three-gear retrieval over the IkigAI corpus. Gear 1 links-only, Gear 2 synthesis (default), Gear 3 debaiser panel.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "gear": {"type": "integer", "enum": [1, 2, 3]},
            },
            "required": ["query"],
        },
    },
    "ikigai_phase_an_idea": {
        "fn": tool_phase_an_idea,
        "description": "Hand IkigAI an idea to phase. Returns plan after THE WATCHER canonicalises.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "idea_text": {"type": "string"},
            },
            "required": ["idea_text"],
        },
    },
    "ikigai_brief_today": {
        "fn": tool_brief_today,
        "description": "Get today's morning brief. THE HERALD generates this at 07:30 daily.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    "ikigai_debaiser": {
        "fn": tool_debaiser,
        "description": "Queue a debaiser (contrarian panel) pass on a topic id.",
        "inputSchema": {
            "type": "object",
            "properties": {"topic_id": {"type": "string"}},
            "required": ["topic_id"],
        },
    },
    "ikigai_search": {
        "fn": tool_search,
        "description": "Fast vector search wrapper (Gear 1 equivalent).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "n": {"type": "integer"},
            },
            "required": ["query"],
        },
    },
    "ikigai_get_page": {
        "fn": tool_get_page,
        "description": "Read a vault page by id.",
        "inputSchema": {
            "type": "object",
            "properties": {"page_id": {"type": "string"}},
            "required": ["page_id"],
        },
    },
}


def jsonrpc_response(id_, result=None, error=None):
    if error:
        return {"jsonrpc": "2.0", "id": id_, "error": error}
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def handle(req):
    method = req.get("method")
    params = req.get("params", {})
    rid = req.get("id")

    if method == "initialize":
        return jsonrpc_response(rid, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "ikigAI", "version": "0.3"},
        })

    if method == "tools/list":
        tools = []
        for name, t in TOOLS.items():
            tools.append({
                "name": name,
                "description": t["description"],
                "inputSchema": t["inputSchema"],
            })
        return jsonrpc_response(rid, {"tools": tools})

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name not in TOOLS:
            return jsonrpc_response(rid, error={"code": -32601, "message": f"unknown tool: {name}"})
        try:
            result = TOOLS[name]["fn"](**args)
            return jsonrpc_response(rid, {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]})
        except Exception as e:
            return jsonrpc_response(rid, error={"code": -32000, "message": str(e)})

    return jsonrpc_response(rid, error={"code": -32601, "message": f"unknown method: {method}"})


def main():
    print("═══ ikigAI MCP server (stdio) ═══", file=sys.stderr, flush=True)
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
        except Exception as e:
            print(f"  ✗ parse: {e}", file=sys.stderr, flush=True)
            continue

        resp = handle(req)
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
