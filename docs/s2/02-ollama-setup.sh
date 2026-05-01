#!/bin/bash
# S2 — 02 — Ollama setup
#
# Installs Ollama, pulls llama3.2, configures it to bind to all interfaces (so
# Docker containers + Tailscale clients can reach it), and verifies inference.
#
# Run on the NUC. Idempotent.

set -euo pipefail

echo "═══════════════════════════════════════════════════════════"
echo "  IkigAI — Ollama setup"
echo "═══════════════════════════════════════════════════════════"

# ─── 1. Install Ollama ────────────────────────────────────────────
echo ""
echo "→ Installing Ollama"
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "   Already installed: $(ollama --version | head -1)"
fi

# ─── 2. Configure Ollama to bind to 0.0.0.0 ───────────────────────
echo ""
echo "→ Configuring Ollama systemd service"
SERVICE_FILE="/etc/systemd/system/ollama.service.d/override.conf"
sudo mkdir -p "$(dirname ${SERVICE_FILE})"
sudo tee "${SERVICE_FILE}" > /dev/null << 'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"
EOF

sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl enable ollama
sleep 3

# ─── 3. Pull models ───────────────────────────────────────────────
echo ""
echo "→ Pulling llama3.2 (this may take 5-10 minutes)"
ollama pull llama3.2

echo ""
echo "→ Pulling nomic-embed-text (for vector embeddings)"
ollama pull nomic-embed-text

# ─── 4. Verify ────────────────────────────────────────────────────
echo ""
echo "→ Verifying Ollama is reachable"
sleep 2
if curl -sf http://localhost:11434/api/tags >/dev/null; then
  echo "   ✓ Ollama responding on localhost:11434"
else
  echo "   ✗ Ollama not responding. Check: sudo journalctl -u ollama -f"
  exit 1
fi

echo ""
echo "→ Smoke test: simple prompt"
RESPONSE=$(curl -sf http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Say exactly: ikigai brain online",
    "stream": false
  }' | jq -r '.response')

echo "   llama3.2 said: ${RESPONSE}"

# ─── 5. Test embeddings ───────────────────────────────────────────
echo ""
echo "→ Testing embeddings model"
EMBED_DIM=$(curl -sf http://localhost:11434/api/embeddings \
  -d '{
    "model": "nomic-embed-text",
    "prompt": "test"
  }' | jq -r '.embedding | length')
echo "   Embedding dimensions: ${EMBED_DIM} (expected 768)"

if [ "${EMBED_DIM}" -ne 768 ]; then
  echo "   ⚠ Unexpected embedding dimension. Continuing but flag this."
fi

# ─── 6. Reachability from Tailscale ───────────────────────────────
echo ""
echo "→ Tailscale-local reachability check"
TS_IP=$(tailscale ip -4 2>/dev/null || echo "")
if [ -n "${TS_IP}" ]; then
  if curl -sf "http://${TS_IP}:11434/api/tags" >/dev/null; then
    echo "   ✓ Reachable on tailnet at ${TS_IP}:11434"
  else
    echo "   ⚠ Not reachable on tailnet — check firewall (ufw allow 11434 from 100.64.0.0/10)"
  fi
else
  echo "   ⚠ Tailscale not up; skipping tailnet reachability check"
fi

echo ""
echo "✓ Ollama setup complete."
echo ""
echo "Models available:"
ollama list
echo ""
echo "Next: ./03-vault-init.sh"
