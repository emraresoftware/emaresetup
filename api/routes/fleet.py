"""Emare Hub — Fleet & Advanced API Routes (Faz 7)"""
from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fleet_manager import fleet_manager, DeviceHeartbeat  # noqa: E402

fleet_router = APIRouter(prefix="/api/fleet", tags=["fleet"])


@fleet_router.get("/devices")
async def list_fleet_devices():
    """Tüm filo cihazlarını listele."""
    return fleet_manager.list_devices()


@fleet_router.get("/summary")
async def fleet_summary():
    """Filo özeti."""
    return fleet_manager.get_fleet_summary()


@fleet_router.post("/heartbeat")
async def receive_heartbeat(hb: DeviceHeartbeat):
    """Cihazdan heartbeat al."""
    record = fleet_manager.process_heartbeat(hb)
    return {"status": "ok", "device": record}


@fleet_router.get("/devices/{device_id}")
async def get_device(device_id: str):
    """Cihaz detayı."""
    device = fleet_manager.get_device(device_id)
    if not device:
        raise HTTPException(404, f"Cihaz bulunamadı: {device_id}")
    return device


@fleet_router.delete("/devices/{device_id}")
async def remove_device(device_id: str):
    """Cihazı filodan kaldır."""
    removed = fleet_manager.remove_device(device_id)
    if not removed:
        raise HTTPException(404, f"Cihaz bulunamadı: {device_id}")
    return {"status": "removed", "device_id": device_id}


@fleet_router.post("/deploy/{module_name}")
async def deploy_module(module_name: str, device_ids: list[str] | None = None):
    """Modülü cihazlara dağıt."""
    results = fleet_manager.deploy_module(module_name, device_ids)
    return {"module": module_name, "deployments": results}


@fleet_router.post("/register-self")
async def register_self():
    """Bu cihazı filoya kaydet (kendi heartbeat'ini gönder)."""
    from emare_core import hub

    modules = [m.get("name", "") for m in hub.list_modules()]

    hb = DeviceHeartbeat(
        device_id=f"{platform.node()}-{os.getlogin()}",
        hostname=platform.node(),
        platform=sys.platform,
        modules=modules,
        python_version=platform.python_version(),
    )

    # Run health check and parse
    try:
        result = subprocess.run(
            ["bash", str(PROJECT_ROOT / "scripts" / "fleet_health_check.sh")],
            capture_output=True, text=True, timeout=30,
        )
        for line in result.stdout.splitlines():
            if line.startswith("PASS:"):
                hb.health_pass = int(line.split(":")[1].strip())
            elif line.startswith("WARN:"):
                hb.health_warn = int(line.split(":")[1].strip())
            elif line.startswith("FAIL:"):
                hb.health_fail = int(line.split(":")[1].strip())
    except Exception:
        pass

    record = fleet_manager.process_heartbeat(hb)
    return {"status": "registered", "device": record}
