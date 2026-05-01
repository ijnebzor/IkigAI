#!/bin/bash
# S2 — 01 — Provision the NUC
#
# Run on the NUC as your normal user (not root).
# Idempotent — safe to re-run.
#
# Sets up: Docker, Tailscale, Python 3.11+, Git, system updates, NUC user in docker group.
#
# Usage:
#   chmod +x 01-nuc-provision.sh
#   ./01-nuc-provision.sh
#
# Or via Claude Code:
#   claude "Run docs/s2/01-nuc-provision.sh and walk me through each step. Stop on any failure."

set -euo pipefail

NUC_USER="${USER}"
echo "═══════════════════════════════════════════════════════════"
echo "  IkigAI — NUC provisioning"
echo "  User: ${NUC_USER}"
echo "  Host: $(hostname)"
echo "═══════════════════════════════════════════════════════════"

# ─── 1. System update ─────────────────────────────────────────────
echo ""
echo "→ Updating apt"
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

echo "→ Installing baseline packages"
sudo apt-get install -y -qq \
  curl \
  wget \
  git \
  build-essential \
  ca-certificates \
  gnupg \
  lsb-release \
  software-properties-common \
  jq \
  htop \
  unzip \
  zip \
  python3-pip \
  python3-venv \
  python3-dev

# ─── 2. Python 3.11+ ──────────────────────────────────────────────
echo ""
echo "→ Verifying Python 3.11+"
PY_VERSION=$(python3 --version | awk '{print $2}')
echo "   Found: ${PY_VERSION}"
PY_MAJOR=$(echo "${PY_VERSION}" | cut -d. -f1)
PY_MINOR=$(echo "${PY_VERSION}" | cut -d. -f2)
if [ "${PY_MAJOR}" -lt 3 ] || ([ "${PY_MAJOR}" -eq 3 ] && [ "${PY_MINOR}" -lt 11 ]); then
  echo "   Python <3.11 detected. Adding deadsnakes PPA and installing 3.11"
  sudo add-apt-repository -y ppa:deadsnakes/ppa
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3.11 python3.11-venv python3.11-dev
fi

# ─── 3. Docker + compose plugin ───────────────────────────────────
echo ""
echo "→ Installing Docker"
if ! command -v docker >/dev/null 2>&1; then
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -qq
  sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
  echo "   Already installed: $(docker --version)"
fi

echo "→ Adding ${NUC_USER} to docker group"
sudo usermod -aG docker "${NUC_USER}"
echo "   You'll need to log out + back in (or 'newgrp docker') for this to take effect"

echo "→ Enabling Docker on boot"
sudo systemctl enable --now docker

# ─── 4. Tailscale ─────────────────────────────────────────────────
echo ""
echo "→ Installing Tailscale"
if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sudo sh
else
  echo "   Already installed: $(tailscale version | head -1)"
fi

echo ""
echo "→ Tailscale up"
echo "   You'll be prompted to authenticate via the URL Tailscale prints."
echo "   If you have an auth key, run instead: sudo tailscale up --authkey=YOUR_KEY"
read -p "   Run 'sudo tailscale up' now? [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
  sudo tailscale up || true
fi

# ─── 5. IkigAI directory layout ───────────────────────────────────
echo ""
echo "→ Creating ~/ikigai-state/ for runtime state"
mkdir -p ~/ikigai-state/{logs,index,secrets,phase0}
chmod 700 ~/ikigai-state/secrets

# ─── 6. whisper.cpp ───────────────────────────────────────────────
echo ""
echo "→ Installing whisper.cpp for voice memo transcription"
if [ ! -d ~/whisper.cpp ]; then
  cd ~
  git clone https://github.com/ggerganov/whisper.cpp.git
  cd whisper.cpp
  make -j$(nproc)
  bash ./models/download-ggml-model.sh small.en
  echo "   small.en model downloaded"
else
  echo "   whisper.cpp already present at ~/whisper.cpp"
fi

# ─── 7. Verify ────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Provisioning summary"
echo "═══════════════════════════════════════════════════════════"
docker --version || echo "DOCKER MISSING"
docker compose version || echo "COMPOSE PLUGIN MISSING"
python3 --version
git --version
tailscale status | head -3 || echo "TAILSCALE NOT UP"
echo "Vault state dir: $(ls -la ~/ikigai-state/)"

echo ""
echo "✓ Provisioning complete."
echo ""
echo "Next steps:"
echo "  1. Log out and back in (or run 'newgrp docker') so docker group membership takes effect"
echo "  2. Run ./02-ollama-setup.sh"
echo ""
echo "If Tailscale isn't up yet, run: sudo tailscale up --auth-key=<your-key>"
