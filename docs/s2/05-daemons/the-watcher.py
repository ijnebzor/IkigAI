#!/usr/bin/env python3
"""
THE WATCHER

Inbox monitor for ikigAI. Watches `inbox/` for new files via inotify.
For each new file, runs the /understand pipeline (locally via Ollama).
Writes canonical pages to wiki/, updates Chroma + graph indexes,
appends to log.md, leaves a heartbeat file for compose healthchecks.

Naming convention: THE [ROLE] (Digiquarium pattern).
"""

import os
import time
import json
import hashlib
import frontmatter
from pathlib import Path
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml
import ollama
import chromadb
import re

VAULT = Path(os.environ.get("VAULT_DIR", "/vault"))
INDEX = Path(os.environ.get("INDEX_DIR", "/index"))
LOGS = Path(os.environ.get("LOGS_DIR", "/logs"))
SECRETS = Path(os.environ.get("SECRETS_DIR", "/secrets"))
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")

INBOX = VAULT / "inbox"
WIKI = VAULT / "wiki"
LOG = VAULT / "log.md"
HEARTBEAT = LOGS / "the-watcher.heartbeat"

# Load config + me/ files
CONFIG = yaml.safe_load((VAULT / "config.yml").read_text())
CLAUDE_MD = (VAULT / "CLAUDE.md").read_text()
IKIGAI_MD = (VAULT / "ikigai.md").read_text()
LEXICON_MD = (VAULT / "lexicon.md").read_text()

# Ollama client
client = ollama.Client(host=OLLAMA_HOST)
MODEL = CONFIG["ollama"]["model"]
EMBED_MODEL = CONFIG["ollama"]["embed_model"]

# Chroma client
chroma_client = chromadb.PersistentClient(path=str(INDEX / "chroma"))
sources_coll = chroma_client.get_or_create_collection("sources")
concepts_coll = chroma_client.get_or_create_collection("concepts")


def heartbeat():
    HEARTBEAT.touch()


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_log(entry: str):
    timestamp = datetime.now(timezone.utc).isoformat()
    with LOG.open("a") as f:
        f.write(f"\n## {timestamp}\n{entry}\n")


def regions_implied(axes: list) -> list:
    """Add intersection regions when both axes appear."""
    s = set(axes)
    if {"love", "good_at"}.issubset(s):
        s.add("passion")
    if {"love", "world_needs"}.issubset(s):
        s.add("mission")
    if {"good_at", "paid_for"}.issubset(s):
        s.add("profession")
    if {"world_needs", "paid_for"}.issubset(s):
        s.add("vocation")
    if len({"love", "good_at", "world_needs", "paid_for"} & s) == 4:
        s.add("centre")
    return sorted(list(s))


def understand(content: str, source_path: Path) -> dict:
    """
    Run the /understand pipeline against `content` using local Ollama.

    Returns a frontmatter+body dict ready to write to wiki/sources/<id>.md.

    NOTE: This is a simplified local-first implementation. For production,
    invoke prompts/understand.md via Claude when ANTHROPIC_API_KEY is set.
    """
    system = (
        "You are the IkigAI ingest pipeline. "
        "Read the personal vocabulary, ikigai framework, and lexicon below. "
        "Then classify the source content according to the schema v0.3.\n\n"
        f"=== CLAUDE.md (vocabulary) ===\n{CLAUDE_MD[:2000]}\n\n"
        f"=== ikigai.md ===\n{IKIGAI_MD[:2000]}\n\n"
        f"=== lexicon.md ===\n{LEXICON_MD[:2000]}\n\n"
        "Respond ONLY with a JSON object matching this schema:\n"
        "{\n"
        '  "title": "5-10 words, retrieval-friendly",\n'
        '  "summary": "2-4 sentences in your voice as the agent",\n'
        '  "ikigai_axes": ["love"|"good_at"|"world_needs"|"paid_for", ...],\n'
        '  "ring": "identity"|"operating_principle"|"expression_surface"|"funding"|null,\n'
        '  "expression_surface": "research"|"tooling"|"discourse"|"practice"|null,\n'
        '  "sovereignty_layers": ["data","cognitive","tooling","narrative","epistemic"],\n'
        '  "lexicon_terms": ["term1", ...],\n'
        '  "extracted_entities": [...],\n'
        '  "extracted_concepts": [...],\n'
        '  "key_claims": [...],\n'
        '  "drivers": ["curiosity"|"professional-relevance"|...],\n'
        '  "biases": ["recency"|"confirmation"|"none"|...],\n'
        '  "confidence": 0.5,\n'
        '  "tags": [...]\n'
        "}\n"
    )

    prompt = f"Source content:\n\n{content[:8000]}\n\nClassify."

    try:
        response = client.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.2},
            format="json",
        )
        result = json.loads(response["message"]["content"])
    except Exception as e:
        print(f"  ✗ understand failed: {e}", flush=True)
        result = {
            "title": source_path.stem,
            "summary": "Understand pipeline failed; manual review required.",
            "ikigai_axes": [],
            "ring": None,
            "expression_surface": None,
            "sovereignty_layers": [],
            "lexicon_terms": [],
            "extracted_entities": [],
            "extracted_concepts": [],
            "key_claims": [],
            "drivers": ["other"],
            "biases": ["none"],
            "confidence": 0.3,
            "tags": ["needs-review"],
        }

    # Build full frontmatter per schema v0.3
    today = datetime.now(timezone.utc).date().isoformat()
    page_id = f"{today}-{slugify(result.get('title', 'untitled'))}"

    fm = {
        "id": page_id,
        "type": "source",
        "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "ikigai_regions": regions_implied(result.get("ikigai_axes", [])),
        "ring": result.get("ring"),
        "expression_surface": result.get("expression_surface"),
        "sovereignty_layers": result.get("sovereignty_layers", []),
        "lexicon_terms": result.get("lexicon_terms", []),
        "summary": result.get("summary", ""),
        "tags": result.get("tags", []),
        "sources_raw": [str(source_path.relative_to(VAULT))],
        "derived_from": [],
        "supersedes": [],
        "superseded_by": None,
        "confidence": result.get("confidence", 0.5),
        "last_reinforced": today,
        "drivers": result.get("drivers", []),
        "biases": result.get("biases", []),
        "compounding_ripples": [],
        "retrieval_score": 0.5,
        "last_surfaced": None,
        "last_used": None,
        "context_modifiers": {},
        "surface_count": 0,
        "use_count": 0,
        "status": "canonical",
        "schema_hash": "v0.3",
        "extracted_entities": result.get("extracted_entities", []),
        "extracted_concepts": result.get("extracted_concepts", []),
    }

    body = (
        f"# {result.get('title', 'Untitled')}\n\n"
        f"## Summary\n\n{result.get('summary', '')}\n\n"
        f"## Key claims\n\n"
        + "\n".join(f"- {c}" for c in result.get("key_claims", []))
        + "\n\n## Raw notes\n\n"
        + content[:4000]
    )

    return {"fm": fm, "body": body}


def index_page(page_id: str, summary: str, content: str, regions: list):
    """Write to Chroma."""
    try:
        embedding = client.embeddings(model=EMBED_MODEL, prompt=summary)["embedding"]
        sources_coll.upsert(
            ids=[page_id],
            embeddings=[embedding],
            metadatas=[{"regions": ",".join(regions), "summary": summary[:500]}],
            documents=[content[:2000]],
        )
    except Exception as e:
        print(f"  ✗ index failed: {e}", flush=True)


def write_source(payload: dict, source_path: Path):
    """Write to wiki/sources/<id>.md."""
    sources_dir = WIKI / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    out_path = sources_dir / f"{payload['fm']['id']}.md"
    post = frontmatter.Post(payload["body"], **payload["fm"])
    out_path.write_text(frontmatter.dumps(post))
    return out_path


def process_one(path: Path):
    """Process one inbox file end-to-end."""
    if not path.is_file():
        return
    if path.suffix not in {".md", ".txt", ".html"}:
        print(f"  skip non-text: {path.name}", flush=True)
        return

    print(f"→ Processing {path.relative_to(VAULT)}", flush=True)
    try:
        content = path.read_text()
    except UnicodeDecodeError:
        print(f"  ✗ binary or non-UTF-8: {path.name}", flush=True)
        return

    payload = understand(content, path)
    out = write_source(payload, path)
    index_page(
        payload["fm"]["id"],
        payload["fm"]["summary"],
        content,
        payload["fm"]["ikigai_regions"],
    )

    # Move processed input to inbox/processed/
    processed_dir = path.parent / ".processed"
    processed_dir.mkdir(exist_ok=True)
    path.rename(processed_dir / path.name)

    append_log(
        f"INGEST: `{out.relative_to(VAULT)}` "
        f"regions={payload['fm']['ikigai_regions']} "
        f"confidence={payload['fm']['confidence']}"
    )
    print(f"  ✓ wrote {out.relative_to(VAULT)}", flush=True)


class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        # Wait briefly for write to settle
        time.sleep(0.5)
        try:
            process_one(Path(event.src_path))
        except Exception as e:
            print(f"  ✗ error: {e}", flush=True)
            append_log(f"ERROR: {event.src_path} — {e}")


def initial_sweep():
    """On boot, process anything sitting in inbox/."""
    print("→ Initial sweep", flush=True)
    for surface in INBOX.iterdir():
        if not surface.is_dir() or surface.name.startswith("."):
            continue
        for f in surface.iterdir():
            if f.is_file():
                try:
                    process_one(f)
                except Exception as e:
                    print(f"  ✗ {f.name}: {e}", flush=True)


def main():
    print("═══ THE WATCHER ═══", flush=True)
    print(f"Watching: {INBOX}", flush=True)
    print(f"Wiki dir: {WIKI}", flush=True)
    print(f"Ollama:   {OLLAMA_HOST}", flush=True)

    INBOX.mkdir(parents=True, exist_ok=True)
    WIKI.mkdir(parents=True, exist_ok=True)

    initial_sweep()

    observer = Observer()
    handler = InboxHandler()
    for surface in ["web", "voice", "email", "chat", "tabs", "ideas", "unsorted"]:
        d = INBOX / surface
        d.mkdir(exist_ok=True)
        observer.schedule(handler, str(d), recursive=False)

    observer.start()
    try:
        while True:
            time.sleep(15)
            heartbeat()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
