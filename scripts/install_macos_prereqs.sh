#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] $*"
  else
    eval "$*"
  fi
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

ensure_formula() {
  local formula="$1"
  local cmd_name="$2"

  if has_cmd "$cmd_name"; then
    echo "✅ $formula zaten kurulu"
    return
  fi

  echo "⬇️ $formula kuruluyor"
  run_cmd "brew install $formula"
}

ensure_cask() {
  local cask="$1"
  local check_cmd_name="$2"

  if has_cmd "$check_cmd_name"; then
    echo "✅ $cask zaten kurulu"
    return
  fi

  echo "⬇️ $cask kuruluyor"
  run_cmd "brew install --cask $cask"
}

echo "🍏 Emare Hub macOS prerequisite kurulumu başlıyor"

if ! has_cmd xcode-select; then
  echo "❌ xcode-select komutu bulunamadı. Command Line Tools gerekli."
  exit 1
fi

if ! xcode-select -p >/dev/null 2>&1; then
  echo "🧰 Apple Command Line Tools kuruluyor"
  run_cmd "xcode-select --install"
  echo "⚠️ Kurulum penceresi açıldıysa tamamla ve scripti tekrar çalıştır."
  exit 0
fi

if ! has_cmd brew; then
  echo "🍺 Homebrew kuruluyor"
  run_cmd '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
fi

if [[ "$DRY_RUN" -eq 0 ]]; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
fi

if ! has_cmd brew; then
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY-RUN] brew henüz kurulmuş sayılıyor, kurulum adımları simüle edilecek"
  else
    echo "❌ brew bulunamadı. PATH ayarlarını kontrol et."
    exit 1
  fi
fi

echo "📦 Cihaz envanteri kontrol ediliyor ve eksikler kuruluyor"
run_cmd "brew update"

ensure_formula "git" "git"
ensure_formula "jq" "jq"
ensure_formula "node" "node"
ensure_formula "pnpm" "pnpm"
ensure_formula "gh" "gh"
ensure_formula "wget" "wget"
ensure_formula "tree" "tree"
ensure_formula "htop" "htop"

ensure_cask "docker" "docker"
ensure_cask "visual-studio-code" "code"

echo "☁️ uv kurulumu kontrol ediliyor"
if ! has_cmd uv; then
  echo "⬇️ uv kuruluyor"
  run_cmd "curl -LsSf https://astral.sh/uv/install.sh | sh"
else
  echo "✅ uv zaten kurulu"
fi

echo "✅ Prerequisite kurulum adımları tamamlandı"
echo "✅ Kurulan temel geliştirici araçları: git, jq, node, pnpm, gh, wget, tree, htop"
echo "👉 Docker Desktop'u en az bir kez aç ve lisans/onboarding adımlarını tamamla"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "ℹ️ Dry-run tamamlandı, hiçbir kurulum uygulanmadı"
fi
