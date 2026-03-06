"""Modül şablonları — Hazır template'ler.

Gemini API kullanılamadığında bu şablonlar kullanılır.
"""

TEMPLATES = {
    "analytics_module": '''"""Emare Hub Analytics Module — {name}"""
from __future__ import annotations

import asyncio
from pydantic import BaseModel


class AnalyticsInput(BaseModel):
    data_source: str
    query: str = ""
    limit: int = 100


class AnalyticsResult(BaseModel):
    module: str = "{name}"
    total_records: int = 0
    results: list[dict] = []
    status: str = "pending"


async def analyze(input_data: AnalyticsInput) -> AnalyticsResult:
    """Ana analiz fonksiyonu."""
    try:
        # TODO: Gerçek analiz mantığı
        return AnalyticsResult(
            total_records=0,
            results=[{{"source": input_data.data_source, "query": input_data.query}}],
            status="completed",
        )
    except Exception as exc:
        return AnalyticsResult(status=f"error: {{exc}}")


async def run(payload: str = "") -> dict:
    input_data = AnalyticsInput(data_source=payload or "default")
    result = await analyze(input_data)
    return result.model_dump()


if __name__ == "__main__":
    print(asyncio.run(run("test_source")))
''',

    "api_service": '''"""Emare Hub API Service — {name}"""
from __future__ import annotations

import asyncio
from pydantic import BaseModel


class ServiceRequest(BaseModel):
    action: str
    payload: dict = {{}}


class ServiceResponse(BaseModel):
    module: str = "{name}"
    success: bool = True
    data: dict = {{}}
    message: str = ""


async def handle_request(req: ServiceRequest) -> ServiceResponse:
    """İstek işleyici."""
    try:
        if req.action == "ping":
            return ServiceResponse(data={{"pong": True}}, message="OK")

        # TODO: Gerçek API mantığı
        return ServiceResponse(
            data={{"action": req.action, "received": req.payload}},
            message=f"İstek işlendi: {{req.action}}",
        )
    except Exception as exc:
        return ServiceResponse(success=False, message=f"Hata: {{exc}}")


async def run(payload: str = "") -> dict:
    req = ServiceRequest(action=payload or "ping")
    result = await handle_request(req)
    return result.model_dump()


if __name__ == "__main__":
    print(asyncio.run(run("ping")))
''',

    "worker_agent": '''"""Emare Hub Worker Agent — {name}"""
from __future__ import annotations

import asyncio
import time
from pydantic import BaseModel


class Task(BaseModel):
    task_id: str = "default"
    action: str = "process"
    data: dict = {{}}


class TaskResult(BaseModel):
    module: str = "{name}"
    task_id: str
    status: str = "pending"
    duration_ms: float = 0
    output: dict = {{}}


async def process_task(task: Task) -> TaskResult:
    """Görevi işle."""
    start = time.time()
    try:
        # TODO: Gerçek iş mantığı
        await asyncio.sleep(0.1)  # Simülasyon

        duration = (time.time() - start) * 1000
        return TaskResult(
            task_id=task.task_id,
            status="completed",
            duration_ms=round(duration, 2),
            output={{"action": task.action, "processed": True}},
        )
    except Exception as exc:
        duration = (time.time() - start) * 1000
        return TaskResult(
            task_id=task.task_id,
            status=f"error: {{exc}}",
            duration_ms=round(duration, 2),
        )


async def run(payload: str = "") -> dict:
    task = Task(action=payload or "process")
    result = await process_task(task)
    return result.model_dump()


if __name__ == "__main__":
    print(asyncio.run(run("test_task")))
''',

    "cli_tool": '''"""Emare Hub CLI Tool — {name}"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pydantic import BaseModel


class CLIArgs(BaseModel):
    command: str = "help"
    args: list[str] = []
    verbose: bool = False


class CLIResult(BaseModel):
    module: str = "{name}"
    command: str
    success: bool = True
    output: str = ""


async def execute(cli_args: CLIArgs) -> CLIResult:
    """CLI komutunu çalıştır."""
    try:
        if cli_args.command == "help":
            return CLIResult(
                command="help",
                output="{name} CLI — Kullanılabilir komutlar: help, version, run",
            )
        elif cli_args.command == "version":
            return CLIResult(command="version", output="{name} v1.0.0")
        else:
            # TODO: Gerçek komut mantığı
            return CLIResult(
                command=cli_args.command,
                output=f"Komut çalıştırıldı: {{cli_args.command}}",
            )
    except Exception as exc:
        return CLIResult(command=cli_args.command, success=False, output=f"Hata: {{exc}}")


async def run(payload: str = "") -> dict:
    args = CLIArgs(command=payload or "help")
    result = await execute(args)
    return result.model_dump()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="{name}")
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("-v", "--verbose", action="store_true")
    parsed = parser.parse_args()

    result = asyncio.run(run(parsed.command))
    print(result)
''',

    "standard_module": '''"""Emare Hub Standard Module — {name}"""
from __future__ import annotations

import asyncio
from pydantic import BaseModel


class TaskInput(BaseModel):
    payload: str = ""
    options: dict = {{}}


class TaskOutput(BaseModel):
    module: str = "{name}"
    status: str = "pending"
    result: dict = {{}}


async def run(task: TaskInput | None = None) -> dict:
    """Ana modül fonksiyonu."""
    if task is None:
        task = TaskInput()

    try:
        # TODO: Modül mantığı
        output = TaskOutput(
            status="completed",
            result={{"payload": task.payload, "processed": True}},
        )
        return output.model_dump()
    except Exception as exc:
        return TaskOutput(status=f"error: {{exc}}").model_dump()


if __name__ == "__main__":
    print(asyncio.run(run(TaskInput(payload="test"))))
''',
}


def get_template(module_type: str, module_name: str) -> str:
    """Modül tipine göre şablon kodu döndür."""
    template = TEMPLATES.get(module_type, TEMPLATES["standard_module"])
    return template.format(name=module_name)
