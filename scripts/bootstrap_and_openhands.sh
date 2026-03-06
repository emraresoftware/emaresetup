#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🚀 Bootstrap + OpenHands akışı başlıyor"

./scripts/bootstrap_imac.sh

if ! command -v docker >/dev/null 2>&1; then
  echo "❌ Docker bulunamadı. Docker Desktop kur ve tekrar dene."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "❌ Docker çalışmıyor. Docker Desktop'u aç ve tekrar dene."
  exit 1
fi

if [[ -z "${GOOGLE_API_KEY:-}" && -z "${LLM_API_KEY:-}" ]]; then
  echo "❌ GOOGLE_API_KEY veya LLM_API_KEY tanımlı değil."
  echo "Örnek: export GOOGLE_API_KEY='...'
"
  exit 1
fi

./scripts/start_openhands_worker.sh
