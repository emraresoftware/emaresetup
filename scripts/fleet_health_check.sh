#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  echo "PASS | $1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  echo "FAIL | $1"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  echo "WARN | $1"
}

check_cmd() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    pass "$name kurulu"
  else
    fail "$name eksik"
  fi
}

echo "🔎 Emare Hub Filo Sağlık Kontrolü"
echo "📍 Proje: $PROJECT_ROOT"

printf "\n== Sistem Araçları ==\n"
check_cmd git
check_cmd jq
check_cmd uv
check_cmd node
check_cmd pnpm
check_cmd gh

if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    pass "docker çalışıyor"
  else
    warn "docker kurulu ama daemon çalışmıyor"
  fi
else
  fail "docker eksik"
fi

printf "\n== Python Ortamı ==\n"
if [[ -x ".venv/bin/python" ]]; then
  PY_VER="$(./.venv/bin/python --version 2>/dev/null || true)"
  if [[ "$PY_VER" == Python\ 3.11* || "$PY_VER" == Python\ 3.12* || "$PY_VER" == Python\ 3.13* ]]; then
    pass ".venv python sürümü uygun: $PY_VER"
  else
    warn ".venv python sürümü beklenenden farklı: ${PY_VER:-bilinmiyor}"
  fi
else
  fail ".venv python bulunamadı"
fi

if [[ -f "requirements.txt" && -x ".venv/bin/python" ]]; then
  if ./.venv/bin/python -c "import dotenv, yaml, requests, pydantic" >/dev/null 2>&1; then
    pass "kritik Python bağımlılıkları import ediliyor"
  else
    fail "kritik Python bağımlılıkları eksik"
  fi
fi

printf "\n== Sync ve İçerik ==\n"
REG_PATH="data/registry.json"
EXPECTED_TARGET="$HOME/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json"

if [[ -L "$REG_PATH" ]]; then
  RESOLVED="$(python3 - <<'PY'
from pathlib import Path
print(Path("data/registry.json").resolve())
PY
)"
  if [[ "$RESOLVED" == "$EXPECTED_TARGET" ]]; then
    pass "registry symlink hedefi doğru"
  else
    warn "registry symlink farklı hedefe bağlı: $RESOLVED"
  fi
else
  fail "data/registry.json symlink değil"
fi

if [[ -f "docs/ARCHITECTURE.md" ]]; then
  pass "docs/ARCHITECTURE.md mevcut"
else
  fail "docs/ARCHITECTURE.md eksik"
fi

if [[ -f "docs/FILO_YONETIMI.md" ]]; then
  pass "docs/FILO_YONETIMI.md mevcut"
else
  fail "docs/FILO_YONETIMI.md eksik"
fi

printf "\n== Özet ==\n"
echo "PASS: $PASS_COUNT"
echo "WARN: $WARN_COUNT"
echo "FAIL: $FAIL_COUNT"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  printf "\n❌ Filo sağlık kontrolü başarısız\n"
  echo "Düzeltme için çalıştır: ./scripts/one_click_setup.sh"
  exit 1
fi

printf "\n✅ Filo sağlık kontrolü başarılı\n"
