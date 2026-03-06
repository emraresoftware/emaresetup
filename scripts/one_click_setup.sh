#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🚀 Emare Hub ONE-CLICK kurulum başlıyor"

./scripts/install_macos_prereqs.sh
./scripts/bootstrap_imac.sh

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  if [[ -n "${GOOGLE_API_KEY:-}" || -n "${LLM_API_KEY:-}" ]]; then
    echo "🤖 OpenHands otomatik başlatılıyor"
    ./scripts/start_openhands_worker.sh
  else
    echo "ℹ️ API key yok, OpenHands otomatik başlatılmadı."
    echo "   export GOOGLE_API_KEY='...'
   ./scripts/start_openhands_worker.sh"
  fi
else
  echo "ℹ️ Docker hazır değil; OpenHands atlandı."
  echo "   Docker Desktop'u açtıktan sonra: ./scripts/start_openhands_worker.sh"
fi

echo "🩺 Kurulum sonrası sağlık raporu alınıyor"
if ./scripts/fleet_health_check.sh; then
  echo "✅ Cihaz durumu uygun"
else
  echo "⚠️ Cihazda eksik bileşenler var, raporu inceleyip tekrar çalıştır"
fi

echo "✅ ONE-CLICK kurulum tamamlandı"
