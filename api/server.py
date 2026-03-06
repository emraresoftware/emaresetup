"""Emare Hub — FastAPI Web Backend (Faz 6.1)

Tüm CLI komutlarını REST API olarak sunar.
Çalıştır: uvicorn api.server:app --reload --port 8000
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# ─── Proje kök dizini ─────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from emare_core import hub  # noqa: E402

load_dotenv()

API_KEY = os.getenv("EMARE_API_KEY")

app = FastAPI(
    title="Emare Hub API",
    description="🏭 Yazılım Fabrikası REST API",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ─── Auth Helper ──────────────────────────────────────────────

def _bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> None:
    if not API_KEY:
        return

    bearer = _bearer_token(authorization)
    if x_api_key == API_KEY or bearer == API_KEY:
        return

    raise HTTPException(status_code=401, detail="API anahtari gecersiz")


# Fleet routes
from api.routes.fleet import fleet_router  # noqa: E402
app.include_router(fleet_router, dependencies=[Depends(require_api_key)])


# ─── Modeller ─────────────────────────────────────────────────

class ModuleCreateRequest(BaseModel):
    name: str
    module_type: str = "standard_module"
    description: str = "Genel görev"


class ModuleResponse(BaseModel):
    name: str
    type: str
    registered_at: Optional[str] = None
    has_code: bool = False
    has_tests: bool = False
    version: Optional[str] = None


class HealthCheck(BaseModel):
    status: str
    pass_count: int
    warn_count: int
    fail_count: int
    checks: list[dict]


class GenerateResponse(BaseModel):
    name: str
    status: str
    message: str
    provider: Optional[str] = None


class StatsResponse(BaseModel):
    total_modules: int
    total_code_lines: int
    total_test_files: int
    providers_available: list[str]
    last_activity: Optional[str] = None


# ─── Endpoints ─────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"name": "Emare Hub API", "version": "0.4.0", "status": "running"}


@app.get("/api/modules", response_model=list[ModuleResponse], dependencies=[Depends(require_api_key)])
async def list_modules():
    """Tüm kayıtlı modülleri listele."""
    modules = hub.list_modules()
    result = []
    for mod in modules:
        name = mod.get("name", "")
        mod_path = PROJECT_ROOT / "modules" / name
        result.append(ModuleResponse(
            name=name,
            type=mod.get("type", "unknown"),
            registered_at=mod.get("registered_at"),
            has_code=(mod_path / "main.py").exists(),
            has_tests=(mod_path / "tests" / "test_main.py").exists(),
            version=_get_module_version(name),
        ))
    return result


@app.get("/api/modules/{name}", dependencies=[Depends(require_api_key)])
async def get_module(name: str):
    """Modül detayını getir."""
    mod_path = PROJECT_ROOT / "modules" / name
    manifest_path = mod_path / "manifest.json"

    if not manifest_path.exists():
        raise HTTPException(404, f"Modül bulunamadı: {name}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    code_path = mod_path / "main.py"
    code = code_path.read_text(encoding="utf-8") if code_path.exists() else ""

    return {
        "manifest": manifest,
        "code": code,
        "code_lines": len(code.splitlines()),
        "has_tests": (mod_path / "tests" / "test_main.py").exists(),
    }


@app.post("/api/modules", response_model=GenerateResponse, dependencies=[Depends(require_api_key)])
async def create_module(req: ModuleCreateRequest):
    """Yeni modül oluştur (AI ile)."""
    from factory_worker import worker

    try:
        worker.create_module_scaffold(
            module_name=req.name,
            module_type=req.module_type,
            description=req.description,
        )
        return GenerateResponse(
            name=req.name,
            status="created",
            message=f"'{req.name}' modülü üretildi.",
            provider=getattr(worker, "_last_provider", None),
        )
    except Exception as exc:
        raise HTTPException(500, f"Modül üretilemedi: {exc}")


@app.delete("/api/modules/{name}", dependencies=[Depends(require_api_key)])
async def delete_module(name: str):
    """Modülü sil."""
    import shutil
    mod_path = PROJECT_ROOT / "modules" / name
    if not mod_path.exists():
        raise HTTPException(404, f"Modül bulunamadı: {name}")

    shutil.rmtree(mod_path)

    # Registry'den kaldır
    removed = hub.remove_module(name)
    if not removed:
        raise HTTPException(404, f"Modül bulunamadı: {name}")

    return {"status": "deleted", "name": name}


@app.get("/api/health", response_model=HealthCheck, dependencies=[Depends(require_api_key)])
async def health_check():
    """Sistem sağlık kontrolü."""
    checks = []
    pass_count = warn_count = fail_count = 0

    health_items = [
        ("git", "git --version"),
        ("node", "node --version"),
        ("docker", "docker --version"),
        ("python_venv", f"{PROJECT_ROOT}/.venv/bin/python --version"),
    ]

    for name, cmd in health_items:
        try:
            result = subprocess.run(
                cmd.split(), capture_output=True, text=True, timeout=5
            )
            ok = result.returncode == 0
            checks.append({"name": name, "status": "PASS" if ok else "FAIL", "output": result.stdout.strip()})
            if ok:
                pass_count += 1
            else:
                fail_count += 1
        except Exception:
            checks.append({"name": name, "status": "FAIL", "output": "çalıştırılamadı"})
            fail_count += 1

    status = "healthy" if fail_count == 0 else "degraded" if fail_count < 3 else "unhealthy"
    return HealthCheck(
        status=status,
        pass_count=pass_count,
        warn_count=warn_count,
        fail_count=fail_count,
        checks=checks,
    )


@app.get("/api/stats", response_model=StatsResponse, dependencies=[Depends(require_api_key)])
async def get_stats():
    """Proje istatistikleri."""
    data = hub._load_registry()
    modules = data.get("modules", [])
    modules_dir = PROJECT_ROOT / "modules"

    total_lines = 0
    total_tests = 0
    for mod in modules:
        name = mod.get("name", "")
        code_path = modules_dir / name / "main.py"
        test_path = modules_dir / name / "tests" / "test_main.py"
        if code_path.exists():
            total_lines += len(code_path.read_text(encoding="utf-8").splitlines())
        if test_path.exists():
            total_tests += 1

    from provider_router import router
    available = [p.name for p in router.available_providers]

    return StatsResponse(
        total_modules=len(modules),
        total_code_lines=total_lines,
        total_test_files=total_tests,
        providers_available=available,
        last_activity=data.get("updated_at"),
    )


# ─── Helpers ───────────────────────────────────────────────────

def _get_module_version(name: str) -> Optional[str]:
    manifest_path = PROJECT_ROOT / "modules" / name / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        return manifest.get("version")
    return None
