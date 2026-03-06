from __future__ import annotations

from datetime import datetime
from pathlib import Path

from data.repository import (
    get_last_activity,
    list_modules,
    record_log,
    remove_module,
    upsert_module,
)


class EmareHub:
    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path(__file__).resolve().parent
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _load_registry(self) -> dict:
        modules = list_modules()
        return {
            "modules": modules,
            "updated_at": get_last_activity(),
        }

    def register_module(
        self,
        name: str,
        module_type: str,
        description: str | None = None,
        version: str | None = None,
    ) -> None:
        upsert_module(
            name=name,
            module_type=module_type,
            description=description,
            version=version,
        )

    def remove_module(self, name: str) -> bool:
        return remove_module(name)

    def list_modules(self) -> list[dict]:
        return list_modules()

    def log_and_print(self, message: str, level: str = "info") -> None:
        record_log(level=level, message=message, timestamp=datetime.utcnow().isoformat())
        print(f"[{level.upper()}] {message}")


hub = EmareHub()
