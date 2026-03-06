from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from emare_core import hub
from provider_router import router as ai_router
from templates import get_template


class EmareWorker:
    def __init__(self) -> None:
        load_dotenv()
        self.router = ai_router
        self._last_provider: str | None = None

        if not self.router.available_providers:
            print("⚠️ UYARI: Hiçbir AI sağlayıcı yapılandırılmamış. Şablon modu aktif.")

    def _generate_ai_code(self, module_name: str, module_type: str, description: str) -> str:
        if not self.router.available_providers:
            return get_template(module_type, module_name)

        prompt = f"""
Sen Emare Hub yazılım fabrikasının baş mimarısın.
'{module_name}' adında, '{module_type}' tipinde bir modül yazmanı istiyorum.
Görev: {description}

KURALLAR:
1. Daima async/await yapısını kullan.
2. Pydantic modelleri ve kapsamlı hata yönetimi (try-except) kullan.
3. run() adında bir ana fonksiyon olmalı (async).
4. if __name__ == "__main__" bloğu ile çalıştırılabilir olmalı.
5. Sadece çalışabilir Python kodu ver, açıklama yapma.
"""

        result = self.router.generate(prompt)
        self._last_provider = result.provider

        if result.success:
            code = result.text.replace("```python", "").replace("```", "").strip()
            if code:
                return code

        print(f"  ⚠️ AI üretemedi, tip-bazlı şablon kullanılıyor.")
        return get_template(module_type, module_name)

    def create_module_scaffold(
        self,
        module_name: str,
        module_type: str = "standard_module",
        description: str = "Genel görev",
        auto_test: bool = True,
        version: str = "1.0.0",
    ) -> None:
        module_path = Path("./modules") / module_name
        is_upgrade = module_path.exists()

        if is_upgrade:
            # Versiyonlama: eski kodu arşivle
            self._archive_version(module_name)

        module_path.mkdir(parents=True, exist_ok=True)

        providers_str = ", ".join(p.name for p in self.router.available_providers) or "yok"
        print(f"🧠 AI '{module_name}' için mimariyi çiziyor... (sağlayıcılar: {providers_str})")
        real_code = self._generate_ai_code(module_name, module_type, description)

        with (module_path / "main.py").open("w", encoding="utf-8") as file:
            file.write(real_code)

        # Versiyon bilgili manifest
        manifest = {
            "name": module_name,
            "type": module_type,
            "description": description,
            "version": version,
            "emare_hub_compatible": True,
            "created_at": datetime.utcnow().isoformat(),
            "provider": self._last_provider,
            "changelog": [
                {
                    "version": version,
                    "date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "changes": "İlk üretim" if not is_upgrade else "Yeniden üretim",
                }
            ],
        }

        # Mevcut manifest varsa changelog'u koru
        existing_manifest_path = module_path / "manifest.json"
        if is_upgrade and existing_manifest_path.exists():
            try:
                old = json.loads(existing_manifest_path.read_text(encoding="utf-8"))
                old_changelog = old.get("changelog", [])
                old_version = old.get("version", "0.0.0")
                manifest["changelog"] = old_changelog + [{
                    "version": version,
                    "date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "changes": f"{old_version} → {version} yükseltme",
                }]
            except (json.JSONDecodeError, KeyError):
                pass

        with (module_path / "manifest.json").open("w", encoding="utf-8") as file:
            json.dump(manifest, file, ensure_ascii=False, indent=2)

        hub.register_module(
            module_name,
            module_type,
            description=description,
            version=version,
        )
        print(f"✅ FABRİKA: '{module_name}' v{version} üretildi. (via {self._last_provider or 'template'})")

        # Otomatik test üretimi
        if auto_test:
            try:
                from test_generator import create_test_file
                test_path = create_test_file(module_name)
                print(f"🧪 Test dosyası üretildi: {test_path}")
            except Exception as exc:
                print(f"  ⚠️ Test üretilemedi: {exc}")

    def _archive_version(self, module_name: str) -> None:
        """Mevcut versiyonu arşivle."""
        module_path = Path("./modules") / module_name
        manifest_path = module_path / "manifest.json"

        if not manifest_path.exists():
            return

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            old_version = manifest.get("version", "unknown")
        except (json.JSONDecodeError, KeyError):
            old_version = "unknown"

        archive_dir = module_path / "archive" / f"v{old_version}"
        archive_dir.mkdir(parents=True, exist_ok=True)

        for f in ("main.py", "manifest.json"):
            src = module_path / f
            if src.exists():
                import shutil
                shutil.copy2(src, archive_dir / f)

        print(f"  📦 v{old_version} arşivlendi → {archive_dir}")

    def upgrade_module(self, module_name: str) -> None:
        """Modülü yeni versiyona yükselt."""
        manifest_path = Path("./modules") / module_name / "manifest.json"
        if not manifest_path.exists():
            print(f"❌ Modül bulunamadı: {module_name}")
            return

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        old_version = manifest.get("version", "1.0.0")
        parts = old_version.split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        new_version = ".".join(parts)

        self.create_module_scaffold(
            module_name=module_name,
            module_type=manifest.get("type", "standard_module"),
            description=manifest.get("description", ""),
            version=new_version,
        )


worker = EmareWorker()
