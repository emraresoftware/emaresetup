from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import func

from data.database import Device, Log, Module, get_session, init_db

init_db()


def _to_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str) and value:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def _module_to_dict(module: Module) -> dict:
    return {
        "name": module.name,
        "type": module.type,
        "description": module.description,
        "version": module.version,
        "registered_at": module.registered_at.isoformat() if module.registered_at else None,
        "updated_at": module.updated_at.isoformat() if module.updated_at else None,
    }


def _device_to_dict(device: Device) -> dict:
    modules = []
    if device.modules_json:
        try:
            modules = json.loads(device.modules_json)
        except json.JSONDecodeError:
            modules = []

    return {
        "device_id": device.device_id,
        "hostname": device.hostname,
        "platform": device.platform,
        "status": device.status,
        "health_pass": device.health_pass,
        "health_warn": device.health_warn,
        "health_fail": device.health_fail,
        "modules": modules,
        "python_version": device.python_version,
        "last_heartbeat": device.last_heartbeat.isoformat() if device.last_heartbeat else None,
        "first_seen": device.first_seen.isoformat() if device.first_seen else None,
    }


def upsert_module(
    name: str,
    module_type: str,
    description: Optional[str] = None,
    version: Optional[str] = None,
    registered_at: Optional[Any] = None,
    updated_at: Optional[Any] = None,
) -> dict:
    now = datetime.utcnow()
    reg_dt = _to_datetime(registered_at) or now
    upd_dt = _to_datetime(updated_at) or now

    with get_session() as session:
        module = session.query(Module).filter_by(name=name).one_or_none()
        if module:
            module.type = module_type
            if description is not None:
                module.description = description
            if version is not None:
                module.version = version
            module.updated_at = upd_dt
        else:
            module = Module(
                name=name,
                type=module_type,
                description=description,
                version=version,
                registered_at=reg_dt,
                updated_at=upd_dt,
            )
            session.add(module)
        session.flush()
        return _module_to_dict(module)


def list_modules() -> list[dict]:
    with get_session() as session:
        modules = session.query(Module).order_by(Module.name.asc()).all()
        return [_module_to_dict(m) for m in modules]


def get_module(name: str) -> Optional[dict]:
    with get_session() as session:
        module = session.query(Module).filter_by(name=name).one_or_none()
        return _module_to_dict(module) if module else None


def remove_module(name: str) -> bool:
    with get_session() as session:
        module = session.query(Module).filter_by(name=name).one_or_none()
        if not module:
            return False
        session.delete(module)
        session.flush()
        return True


def record_log(level: str, message: str, timestamp: Optional[Any] = None) -> None:
    ts = _to_datetime(timestamp) or datetime.utcnow()
    with get_session() as session:
        session.add(Log(timestamp=ts, level=level, message=message))
        session.flush()


def get_last_activity() -> Optional[str]:
    with get_session() as session:
        mod_ts = session.query(func.max(Module.updated_at)).scalar()
        log_ts = session.query(func.max(Log.timestamp)).scalar()

    candidates = [ts for ts in (mod_ts, log_ts) if ts]
    if not candidates:
        return None
    return max(candidates).isoformat()


def upsert_device(record: dict) -> dict:
    now = datetime.utcnow()
    modules_json = json.dumps(record.get("modules", []))
    last_heartbeat = _to_datetime(record.get("last_heartbeat")) or now
    first_seen = _to_datetime(record.get("first_seen")) or now

    with get_session() as session:
        device = session.query(Device).filter_by(device_id=record["device_id"]).one_or_none()
        if device:
            device.hostname = record.get("hostname", device.hostname)
            device.platform = record.get("platform", device.platform)
            device.status = record.get("status", device.status)
            device.health_pass = record.get("health_pass", device.health_pass)
            device.health_warn = record.get("health_warn", device.health_warn)
            device.health_fail = record.get("health_fail", device.health_fail)
            device.modules_json = modules_json
            device.python_version = record.get("python_version", device.python_version)
            device.last_heartbeat = last_heartbeat
            if device.first_seen is None:
                device.first_seen = first_seen
        else:
            device = Device(
                device_id=record["device_id"],
                hostname=record.get("hostname", "unknown"),
                platform=record.get("platform", "unknown"),
                status=record.get("status", "unknown"),
                health_pass=record.get("health_pass", 0),
                health_warn=record.get("health_warn", 0),
                health_fail=record.get("health_fail", 0),
                modules_json=modules_json,
                python_version=record.get("python_version"),
                last_heartbeat=last_heartbeat,
                first_seen=first_seen,
            )
            session.add(device)
        session.flush()
        return _device_to_dict(device)


def list_devices() -> list[dict]:
    with get_session() as session:
        devices = session.query(Device).order_by(Device.device_id.asc()).all()
        return [_device_to_dict(d) for d in devices]


def get_device(device_id: str) -> Optional[dict]:
    with get_session() as session:
        device = session.query(Device).filter_by(device_id=device_id).one_or_none()
        return _device_to_dict(device) if device else None


def remove_device(device_id: str) -> bool:
    with get_session() as session:
        device = session.query(Device).filter_by(device_id=device_id).one_or_none()
        if not device:
            return False
        session.delete(device)
        session.flush()
        return True
