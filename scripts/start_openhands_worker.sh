#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v docker >/dev/null 2>&1; then
  echo "❌ Docker bulunamadı. Docker Desktop kur ve tekrar dene."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "❌ Docker çalışmıyor. Docker Desktop uygulamasını başlat."
  exit 1
fi

LLM_API_KEY="${LLM_API_KEY:-${GOOGLE_API_KEY:-}}"
LLM_MODEL="${LLM_MODEL:-gemini/gemini-1.5-pro}"

if [[ -z "$LLM_API_KEY" ]]; then
  echo "❌ LLM_API_KEY veya GOOGLE_API_KEY tanımlı değil."
  echo "Örnek: export GOOGLE_API_KEY='...'
"
  exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -qx 'emare-otonom-worker'; then
  echo "ℹ️ emare-otonom-worker konteyneri zaten var, yeniden oluşturuluyor."
  docker rm -f emare-otonom-worker >/dev/null 2>&1 || true
fi

docker run -it \
  --pull=always \
  -e SANDBOX_USER_ID="$(id -u)" \
  -e WORKSPACE_BASE="$PROJECT_ROOT" \
  -e LLM_API_KEY="$LLM_API_KEY" \
  -e LLM_MODEL="$LLM_MODEL" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$PROJECT_ROOT":/opt/workspace \
  -p 3000:3000 \
  --name emare-otonom-worker \
  ghcr.io/all-hands-ai/openhands:0.15
