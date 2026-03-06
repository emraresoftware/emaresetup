"""Emare Hub — Otomatik Test Üretici (Faz 4.1)

Modüller için pytest test dosyaları üretir.
"""
from __future__ import annotations

import json
from pathlib import Path

from provider_router import ProviderRouter, router as default_router


def generate_tests_for_module(module_name: str, router: ProviderRouter | None = None) -> str:
    """Modülün main.py koduna bakarak pytest testleri üret."""
    router = router or default_router
    mod_path = Path("modules") / module_name / "main.py"

    if not mod_path.exists():
        return _fallback_test(module_name)

    code = mod_path.read_text(encoding="utf-8")

    prompt = f"""Aşağıdaki Python modülü için pytest testleri yaz.

KURALLAR:
1. pytest ve pytest-asyncio kullan
2. En az 3 test fonksiyonu yaz
3. Her test fonksiyonu 'test_' ile başlamalı
4. Edge case'leri de test et
5. Sadece test kodu yaz, açıklama yapma

MODÜL KODU:
```python
{code[:3000]}
```

TESTLER:"""

    result = router.generate(prompt)
    if result.success and result.text.strip():
        text = result.text.strip()
        text = text.replace("```python", "").replace("```", "").strip()
        if "import pytest" in text or "def test_" in text:
            return text

    return _fallback_test(module_name)


def _fallback_test(module_name: str) -> str:
    """AI oluşturamadığında varsayılan test şablonu."""
    return f'''"""Otomatik üretilmiş testler — {module_name}"""
import pytest
import asyncio
import importlib
import sys
from pathlib import Path

# Modülü import et
MODULE_PATH = Path(__file__).resolve().parent.parent / "main.py"


def _load_module():
    """Modülü dinamik olarak yükle."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("{module_name}", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Test{module_name.title().replace("_", "")}:
    """Test sınıfı: {module_name}"""

    def test_module_loads(self):
        """Modül sorunsuz import ediliyor mu."""
        mod = _load_module()
        assert mod is not None

    def test_run_function_exists(self):
        """run() fonksiyonu var mı."""
        mod = _load_module()
        assert hasattr(mod, "run"), "run() fonksiyonu bulunamadı"

    def test_run_returns_dict(self):
        """run() dict döndürüyor mu."""
        mod = _load_module()
        if asyncio.iscoroutinefunction(mod.run):
            result = asyncio.run(mod.run())
        else:
            result = mod.run()
        assert isinstance(result, dict), f"Beklenen dict, gelen {{type(result)}}"

    def test_run_has_status(self):
        """run() sonucu status içeriyor mu."""
        mod = _load_module()
        if asyncio.iscoroutinefunction(mod.run):
            result = asyncio.run(mod.run())
        else:
            result = mod.run()
        # status veya module anahtarı olmalı
        assert any(k in result for k in ("status", "module")), \\
            f"Sonuçta status/module anahtarı yok: {{result.keys()}}"
'''


def create_test_file(module_name: str) -> Path:
    """Modül için test dosyası oluştur."""
    tests_dir = Path("modules") / module_name / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    # __init__.py
    init_path = tests_dir / "__init__.py"
    if not init_path.exists():
        init_path.write_text("", encoding="utf-8")

    test_code = generate_tests_for_module(module_name)
    test_path = tests_dir / "test_main.py"
    test_path.write_text(test_code, encoding="utf-8")

    return test_path


def run_module_tests(module_name: str) -> dict:
    """Modülün testlerini çalıştır."""
    import subprocess, sys
    test_dir = Path("modules") / module_name / "tests"

    if not test_dir.exists():
        return {"module": module_name, "status": "no_tests", "output": "Test dizini yok"}

    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"],
        capture_output=True, text=True, timeout=30,
    )

    return {
        "module": module_name,
        "status": "passed" if result.returncode == 0 else "failed",
        "returncode": result.returncode,
        "output": result.stdout + result.stderr,
    }
