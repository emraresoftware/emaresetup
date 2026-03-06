#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🚀 Emare Hub iMac bootstrap başlıyor"

if ! command -v uv >/dev/null 2>&1; then
  echo "ℹ️ uv bulunamadı, kuruluyor..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  echo "❌ uv kurulamadı. PATH ayarını kontrol et: $HOME/.local/bin"
  exit 1
fi

echo "🧠 Python 3.11 hazırlanıyor"
uv python install 3.11

if [[ ! -d ".venv" ]]; then
  echo "📦 .venv oluşturuluyor"
  uv venv --python 3.11 .venv
else
  echo "📦 .venv zaten mevcut, yeniden kullanılıyor"
fi

echo "📚 Bağımlılıklar kuruluyor"
uv pip install --python .venv/bin/python -r requirements.txt

if [[ ! -f ".env" && -f ".env.example" ]]; then
  cp .env.example .env
  echo "🔐 .env dosyası .env.example üzerinden oluşturuldu"
fi

echo "🔗 iCloud registry senkronu ayarlanıyor"
./scripts/setup_registry_sync.sh

echo "🧪 Çalıştırma kontrolü"
./.venv/bin/python --version
./.venv/bin/python main.py || true

echo "🐳 Docker/OpenHands kontrolü"
if ! command -v docker >/dev/null 2>&1; then
  echo "⚠️ Docker bulunamadı. OpenHands için Docker Desktop kurmalısın."
else
  if docker info >/dev/null 2>&1; then
    echo "✅ Docker çalışıyor"
    echo "▶ OpenHands başlatmak için: ./scripts/start_openhands_worker.sh"
  else
    echo "⚠️ Docker kurulu ama çalışmıyor. Docker Desktop'u aç."
  fi
fi

echo "✅ Bootstrap tamamlandı"
echo "👉 VS Code interpreter: ./.venv/bin/python"
