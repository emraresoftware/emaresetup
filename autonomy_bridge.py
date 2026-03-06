from __future__ import annotations

from dataclasses import dataclass

import requests

from emare_core import hub


@dataclass
class AutonomyBridge:
    endpoint: str = "http://localhost:3000"

    def __post_init__(self) -> None:
        print("🤖 Otonom İşçi Köprüsü Hazır.")

    def healthcheck(self, timeout_seconds: int = 3) -> bool:
        try:
            response = requests.get(self.endpoint, timeout=timeout_seconds)
            return response.status_code < 500
        except requests.RequestException:
            return False

    def delegate_task(self, task_description: str) -> None:
        print(f"🚀 GÖREV DEVREDİLİYOR: {task_description}")
        if self.healthcheck():
            hub.log_and_print(
                f"Otonom görev başlatıldı: {task_description[:80]}...",
                "info",
            )
            print(f"🌐 OpenHands arayüzü: {self.endpoint}")
            return

        hub.log_and_print(
            "OpenHands endpoint erişilemedi. Önce worker konteynerini başlat.",
            "warning",
        )
        print("Çalıştır: ./scripts/start_openhands_worker.sh")


autonomy = AutonomyBridge()
