"""Emare Hub — Filo Orkestrasyonu (Faz 7)

Birden fazla cihazı merkezi olarak yönetir.
Her cihaz heartbeat gönderir, merkez durumu takip eder.
"""
from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from data.repository import (
    get_device as repo_get_device,
    list_devices as repo_list_devices,
    remove_device as repo_remove_device,
    upsert_device as repo_upsert_device,
)


class DeviceHeartbeat(BaseModel):
    device_id: str
    hostname: str
    platform: str  # darwin, linux
    health_pass: int = 0
    health_warn: int = 0
    health_fail: int = 0
    modules: list[str] = []
    python_version: Optional[str] = None
    last_sync: Optional[str] = None


class DeviceRecord(BaseModel):
    device_id: str
    hostname: str
    platform: str
    status: str = "unknown"  # healthy, degraded, offline
    health_pass: int = 0
    health_warn: int = 0
    health_fail: int = 0
    modules: list[str] = []
    python_version: Optional[str] = None
    last_heartbeat: Optional[str] = None
    first_seen: Optional[str] = None


class FleetManager:
    """Cihaz filosunu yöneten merkezi sınıf."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or Path(__file__).resolve().parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def process_heartbeat(self, hb: DeviceHeartbeat) -> DeviceRecord:
        """Cihazdan gelen heartbeat'i işle ve kaydet."""
        now = datetime.utcnow().isoformat()

        existing = repo_get_device(hb.device_id)

        if hb.health_fail == 0:
            status = "healthy"
        elif hb.health_fail <= 2:
            status = "degraded"
        else:
            status = "unhealthy"

        record_data = {
            "device_id": hb.device_id,
            "hostname": hb.hostname,
            "platform": hb.platform,
            "status": status,
            "health_pass": hb.health_pass,
            "health_warn": hb.health_warn,
            "health_fail": hb.health_fail,
            "modules": hb.modules,
            "python_version": hb.python_version,
            "last_heartbeat": now,
            "first_seen": existing.get("first_seen", now) if existing else now,
        }
        stored = repo_upsert_device(record_data)
        return DeviceRecord(**stored)

    def get_device(self, device_id: str) -> Optional[DeviceRecord]:
        device = repo_get_device(device_id)
        return DeviceRecord(**device) if device else None

    def list_devices(self) -> list[DeviceRecord]:
        return [DeviceRecord(**d) for d in repo_list_devices()]

    def remove_device(self, device_id: str) -> bool:
        return repo_remove_device(device_id)

    def get_fleet_summary(self) -> dict:
        devices = self.list_devices()
        healthy = sum(1 for d in devices if d.status == "healthy")
        degraded = sum(1 for d in devices if d.status == "degraded")
        unhealthy = sum(1 for d in devices if d.status in ("unhealthy", "offline"))

        all_modules = set()
        for d in devices:
            all_modules.update(d.modules)

        return {
            "total_devices": len(devices),
            "healthy": healthy,
            "degraded": degraded,
            "unhealthy": unhealthy,
            "unique_modules": len(all_modules),
            "module_list": sorted(all_modules),
        }

    def deploy_module(self, module_name: str, target_devices: list[str] | None = None) -> list[dict]:
        """Modülü hedef cihazlara dağıt (simülasyon)."""
        devices = self.list_devices()
        if target_devices:
            devices = [d for d in devices if d.device_id in target_devices]

        results = []
        for device in devices:
            results.append({
                "device_id": device.device_id,
                "module": module_name,
                "status": "queued",
                "message": f"'{module_name}' dağıtım kuyruğuna eklendi.",
            })

        return results


fleet_manager = FleetManager()
