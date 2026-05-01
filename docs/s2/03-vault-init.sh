#!/bin/bash
# S2 — 03 — Vault init
#
# Clones the IkigAI repo to ~/IkigAI, sets up ~/ikigAI-me/ as the runtime vault
# (initially as a copy of docs/ikigAI-me from the repo, but git-tracked separately),
# initialises Chroma vector index and the graph index.

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/ijnebzor/IkigAI.git}"
REPO_DIR="${HOME}/IkigAI"
VAULT_DIR="${HOME}/ikigAI-me"
INDEX_DIR="${HOME}/ikigai-state/index"

echo "═══════════════════════════════════════════════════════════"
echo "  IkigAI — Vault init"
echo "═══════════════════════════════════════════════════════════"

# ─── 1. Clone repo ────────────────────────────────────────────────
echo ""
if [ ! -d "${REPO_DIR}" ]; then
  echo "→ Cloning ${REPO_URL} to ${REPO_DIR}"
  git clone "${REPO_URL}" "${REPO_DIR}"
else
  echo "→ Repo already at ${REPO_DIR} — pulling latest"
  cd "${REPO_DIR}"
  git pull --ff-only
fi

# ─── 2. Set up vault dir ─────────────────────────────────────────
echo ""
if [ ! -d "${VAULT_DIR}" ]; then
  echo "→ Initialising vault at ${VAULT_DIR}"
  cp -r "${REPO_DIR}/docs/ikigAI-me/" "${VAULT_DIR}"

  # Init as separate git repo (so your me/ stays private)
  cd "${VAULT_DIR}"
  git init -q
  git add .
  git config user.email "vault@ikigAI.local"
  git config user.name "ikigAI vault"
  git commit -q -m "Initial vault from core/ikigAI-me skeleton"

  # Create runtime dirs
  mkdir -p inbox/{web,voice,email,chat,tabs,ideas,unsorted}
  mkdir -p state
  touch state/feedback.jsonl
  touch state/fetch.log
  touch log.md

  echo "   ✓ Vault structure created"
else
  echo "→ Vault already exists at ${VAULT_DIR} — skipping init"
fi

# ─── 3. Vector index (Chroma) ─────────────────────────────────────
echo ""
echo "→ Setting up Chroma vector index"
mkdir -p "${INDEX_DIR}/chroma"

# Install Python deps if not present
if [ ! -d "${HOME}/ikigai-state/venv" ]; then
  python3 -m venv "${HOME}/ikigai-state/venv"
fi

source "${HOME}/ikigai-state/venv/bin/activate"

pip install --quiet --upgrade pip
pip install --quiet \
  chromadb \
  ollama \
  networkx \
  watchdog \
  pyyaml \
  python-frontmatter \
  google-auth \
  google-auth-oauthlib \
  google-auth-httplib2 \
  google-api-python-client \
  beautifulsoup4 \
  requests \
  rich \
  schedule \
  mcp

# Smoke test
python3 - << 'PYEOF'
import chromadb
client = chromadb.PersistentClient(path="${INDEX_DIR}/chroma".replace("${INDEX_DIR}", "/home/$(whoami)/ikigai-state/index"))
print("Chroma client initialised:", client)
PYEOF

echo "   ✓ Chroma initialised"

# ─── 4. Graph index ───────────────────────────────────────────────
echo ""
echo "→ Initialising NetworkX graph"
python3 - << 'PYEOF'
import os, json, networkx as nx
graph = nx.DiGraph()
out = os.path.expanduser("~/ikigai-state/index/graph.json")
data = {"nodes": [], "links": [], "schema": "v0.3"}
with open(out, "w") as f:
    json.dump(data, f, indent=2)
print("Graph initialised at", out)
PYEOF

echo "   ✓ Graph initialised"

# ─── 5. Generate initial config ───────────────────────────────────
echo ""
CONFIG_FILE="${VAULT_DIR}/config.yml"
if [ ! -f "${CONFIG_FILE}" ]; then
  echo "→ Writing default config.yml"
  cat > "${CONFIG_FILE}" << 'EOF'
schema_version: v0.3

ollama:
  host: localhost:11434
  model: llama3.2
  embed_model: nomic-embed-text

claude:
  api_key_env: ANTHROPIC_API_KEY
  model: claude-sonnet-4-20250514
  use_for: [retrieve_gear_2_polish, retrieve_gear_3, debaiser, phase_an_idea]

voice:
  retrieve_gear_1: helpful
  retrieve_gear_2: prepaired
  retrieve_gear_3: helpful
  morning_brief: ijneb-dev
  weekly_brief: prepaired

brief:
  morning: enabled
  morning_time: "07:30"
  weekly: enabled
  weekly_time: "Sunday 19:00"
  on_demand: enabled

capture:
  enabled: [chrome_phone, voice_memo, gmail_label, chat_paste]
  primary: voice_memo
  inbox_dir: ~/ikigAI-me/inbox

daemons:
  the_watcher:
    enabled: true
    interval_seconds: 30
  the_scout:
    enabled: true
    schedule: "0 2 * * *"   # 02:00 daily
  the_keeper:
    enabled: true
    schedule: "0 3 * * *"   # 03:00 daily
  the_herald:
    enabled: true
    schedule: "30 7 * * *"  # 07:30 daily
  the_debaiser:
    enabled: true
    auto_trigger_threshold:
      reinforcements: 5
      contradictions: 0
  the_gatekeeper:
    enabled: false   # enable after Gmail OAuth in step 09
    label: "IkigAI/Inbox"
    interval_seconds: 60
  the_scribe:
    enabled: false   # enable after Calendar OAuth in step 09
    sync_window_days: 14

retrieval:
  default_gear: 2
  decay_after_days: 90
  evergreen_threshold:
    reinforcements: 5
    confidence: 0.8
    no_decay_days: 60

debaiser:
  panel_size: 5
  min_corpus_pages: 3   # don't run on sparse topics
EOF
  echo "   ✓ config.yml written"
else
  echo "→ config.yml already exists — leaving alone"
fi

# ─── 6. Verify ────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Vault summary"
echo "═══════════════════════════════════════════════════════════"
echo "Repo:   ${REPO_DIR}"
echo "Vault:  ${VAULT_DIR}"
echo "Index:  ${INDEX_DIR}"
echo ""
ls "${VAULT_DIR}"
echo ""
echo "Inbox surfaces:"
ls "${VAULT_DIR}/inbox/"
echo ""
echo "✓ Vault initialised."
echo ""
echo "Next: review and edit ${VAULT_DIR}/CLAUDE.md, ikigai.md, lexicon.md"
echo "Then: ./04-docker-compose.yml (build the daemon stack)"
