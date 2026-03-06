"""Emare Hub — Akıllı Fabrika (Faz 8)

Doğal dil ile çoklu modül üretimi, pattern öğrenme,
modül bağımlılık grafiği.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from provider_router import ProviderRouter, router as default_router


class SmartFactory:
    """Doğal dil komutlarından çoklu modül üretir."""

    def __init__(self, router: ProviderRouter | None = None) -> None:
        self.router = router or default_router
        self.templates_dir = Path(__file__).resolve().parent / "templates"
        self.patterns_path = Path(__file__).resolve().parent / "data" / "learned_patterns.json"

    def analyze_request(self, natural_language: str) -> list[dict]:
        """Doğal dil isteğini analiz edip modül planı çıkar."""
        prompt = f"""Sen bir yazılım mimarısın. Aşağıdaki isteği analiz et ve
gerekli modüllerin listesini JSON dizisi olarak ver.

Her modül için:
- name: snake_case modül adı
- type: analytics_module | api_service | worker_agent | cli_tool | standard_module
- description: Kısa görev açıklaması
- dependencies: Bağımlı olduğu diğer modül adları (varsa)

İstek: {natural_language}

SADECE JSON dizisi yaz, başka hiçbir şey yazma. Örnek format:
[{{"name":"x","type":"y","description":"z","dependencies":[]}}]

JSON:"""

        result = self.router.generate(prompt)
        if not result.success:
            # Fallback: tek modül olarak yorumla
            safe_name = re.sub(r'[^a-z0-9_]', '_', natural_language.lower()[:30])
            return [{
                "name": safe_name,
                "type": "standard_module",
                "description": natural_language,
                "dependencies": [],
            }]

        try:
            text = result.text.strip()
            # JSON bloğunu çıkar
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
                text = text.strip()

            modules = json.loads(text)
            if isinstance(modules, dict):
                modules = [modules]
            return modules
        except (json.JSONDecodeError, IndexError):
            safe_name = re.sub(r'[^a-z0-9_]', '_', natural_language.lower()[:30])
            return [{
                "name": safe_name,
                "type": "standard_module",
                "description": natural_language,
                "dependencies": [],
            }]

    def build_from_request(self, natural_language: str) -> list[dict]:
        """Doğal dil isteğinden modülleri üret."""
        from factory_worker import worker

        print(f"🧠 İstek analiz ediliyor: \"{natural_language[:60]}...\"")
        plan = self.analyze_request(natural_language)
        print(f"📐 Plan: {len(plan)} modül üretilecek\n")

        results = []
        for i, mod in enumerate(plan, 1):
            name = mod.get("name", f"module_{i}")
            mtype = mod.get("type", "standard_module")
            desc = mod.get("description", "")
            deps = mod.get("dependencies", [])

            print(f"  [{i}/{len(plan)}] {name} ({mtype})")

            try:
                worker.create_module_scaffold(name, mtype, desc)
                # Bağımlılıkları manifest'e ekle
                manifest_path = Path("modules") / name / "manifest.json"
                if manifest_path.exists():
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                    manifest["dependencies"] = deps
                    manifest["generated_from"] = natural_language[:100]
                    manifest["generated_at"] = datetime.utcnow().isoformat()
                    manifest_path.write_text(
                        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
                    )

                results.append({"name": name, "status": "created"})
                self._learn_pattern(name, mtype, desc)
            except Exception as exc:
                results.append({"name": name, "status": "failed", "error": str(exc)})
                print(f"    ❌ Hata: {exc}")

        print(f"\n✅ {sum(1 for r in results if r['status'] == 'created')}/{len(results)} modül üretildi.")
        return results

    def _learn_pattern(self, name: str, module_type: str, description: str) -> None:
        """Başarılı üretim kalıplarını kaydet."""
        self.patterns_path.parent.mkdir(parents=True, exist_ok=True)

        patterns = []
        if self.patterns_path.exists():
            try:
                patterns = json.loads(self.patterns_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                patterns = []

        patterns.append({
            "name": name,
            "type": module_type,
            "description": description,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Son 100 pattern'i tut
        patterns = patterns[-100:]
        self.patterns_path.write_text(
            json.dumps(patterns, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def get_learned_patterns(self) -> list[dict]:
        """Öğrenilmiş pattern'leri getir."""
        if not self.patterns_path.exists():
            return []
        try:
            return json.loads(self.patterns_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

    def suggest_from_patterns(self) -> list[str]:
        """Öğrenilmiş kalıplardan modül önerileri üret."""
        patterns = self.get_learned_patterns()
        if not patterns:
            return ["Henüz öğrenilmiş kalıp yok."]

        type_counts: dict[str, int] = {}
        for p in patterns:
            t = p.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

        suggestions = []
        most_common = max(type_counts, key=type_counts.get)
        suggestions.append(f"En sık ürettiğiniz tip: {most_common} ({type_counts[most_common]} kez)")
        suggestions.append(f"Toplam {len(patterns)} başarılı üretim kaydedildi.")

        return suggestions


smart_factory = SmartFactory()
