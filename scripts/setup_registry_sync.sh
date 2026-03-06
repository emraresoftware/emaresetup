#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$PROJECT_ROOT/data"
LOCAL_REGISTRY="$DATA_DIR/registry.json"
BACKUP_REGISTRY="$DATA_DIR/registry.local.backup.json"
ICLOUD_REGISTRY="$HOME/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json"

mkdir -p "$(dirname "$ICLOUD_REGISTRY")"
mkdir -p "$DATA_DIR"

if [[ ! -f "$ICLOUD_REGISTRY" ]]; then
  if [[ -f "$LOCAL_REGISTRY" && ! -L "$LOCAL_REGISTRY" ]]; then
    cp "$LOCAL_REGISTRY" "$ICLOUD_REGISTRY"
  else
    printf '{\n  "modules": [],\n  "updated_at": null\n}\n' > "$ICLOUD_REGISTRY"
  fi
fi

if [[ -L "$LOCAL_REGISTRY" ]]; then
  rm "$LOCAL_REGISTRY"
elif [[ -f "$LOCAL_REGISTRY" ]]; then
  mv "$LOCAL_REGISTRY" "$BACKUP_REGISTRY"
fi

ln -s "$ICLOUD_REGISTRY" "$LOCAL_REGISTRY"

echo "✅ registry.json iCloud ile senkronize edildi"
echo "🔗 $LOCAL_REGISTRY -> $ICLOUD_REGISTRY"
