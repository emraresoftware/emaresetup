from __future__ import annotations

import json
import sys
from pathlib import Path

from data.repository import record_log, upsert_device, upsert_module

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
DATA_DIR = PROJECT_ROOT / "data"


def migrate_registry() -> int:
    registry_path = DATA_DIR / "registry.json"
    if not registry_path.exists():
        print("registry.json bulunamadi, atlandi.")
        return 0

    data = json.loads(registry_path.read_text(encoding="utf-8"))
    modules = data.get("modules", [])
    updated_at = data.get("updated_at")

    count = 0
    for mod in modules:
        upsert_module(
            name=mod.get("name", ""),
            module_type=mod.get("type", "standard_module"),
            registered_at=mod.get("registered_at"),
            updated_at=mod.get("registered_at") or updated_at,
        )
        count += 1

    print(f"registry.json -> SQLite: {count} modul tasindi.")
    return count


def migrate_fleet() -> int:
    fleet_path = DATA_DIR / "fleet.json"
    if not fleet_path.exists():
        print("fleet.json bulunamadi, atlandi.")
        return 0

    data = json.loads(fleet_path.read_text(encoding="utf-8"))
    devices = data.get("devices", [])

    count = 0
    for device in devices:
        upsert_device(device)
        count += 1

    print(f"fleet.json -> SQLite: {count} cihaz tasindi.")
    return count


def migrate_logs() -> int:
    logs_path = DATA_DIR / "hub_logs.jsonl"
    if not logs_path.exists():
        print("hub_logs.jsonl bulunamadi, atlandi.")
        return 0

    count = 0
    with logs_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            record_log(
                level=entry.get("level", "info"),
                message=entry.get("message", ""),
                timestamp=entry.get("timestamp"),
            )
            count += 1

    print(f"hub_logs.jsonl -> SQLite: {count} log tasindi.")
    return count


def main() -> None:
    total = 0
    total += migrate_registry()
    total += migrate_fleet()
    total += migrate_logs()
    print(f"Toplam kayit: {total}")


if __name__ == "__main__":
    main()
