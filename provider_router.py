"""Emare Hub — AI Provider Router (Faz 5)

Birden fazla AI sağlayıcıyı (Gemini, OpenAI, Azure) tek bir
arayüzden kullanır. Rate limit'te otomatik fallback yapar.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ProviderResult:
    provider: str
    model: str
    text: str
    success: bool
    error: Optional[str] = None
    quality_score: Optional[int] = None


@dataclass
class AIProvider:
    name: str
    model: str
    api_key_env: str
    endpoint_env: Optional[str] = None

    @property
    def api_key(self) -> Optional[str]:
        return os.getenv(self.api_key_env)

    @property
    def available(self) -> bool:
        return bool(self.api_key)


class ProviderRouter:
    """Birden fazla AI sağlayıcıyı yöneten router."""

    def __init__(self) -> None:
        self.providers: list[AIProvider] = [
            AIProvider("google", os.getenv("GEMINI_MODEL", "gemini-2.0-flash"), "GOOGLE_API_KEY"),
            AIProvider("openai", os.getenv("OPENAI_MODEL", "gpt-4o-mini"), "OPENAI_API_KEY"),
            AIProvider(
                "azure",
                os.getenv("AZURE_MODEL", "gpt-4o"),
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
            ),
        ]

    @property
    def available_providers(self) -> list[AIProvider]:
        return [p for p in self.providers if p.available]

    def generate(self, prompt: str, preferred: Optional[str] = None) -> ProviderResult:
        """Prompt'u uygun sağlayıcıya gönder. Hata → sonraki sağlayıcıya geç."""
        order = list(self.providers)
        if preferred:
            pref = [p for p in order if p.name == preferred]
            rest = [p for p in order if p.name != preferred]
            order = pref + rest

        for provider in order:
            if not provider.available:
                continue
            result = self._call_with_retry(provider, prompt)
            if result.success:
                return result
            print(f"  ⚠️ {provider.name} başarısız: {result.error}")

        return ProviderResult(
            provider="none",
            model="fallback",
            text="",
            success=False,
            error="Hiçbir AI sağlayıcı kullanılamıyor.",
        )

    def _call_provider(self, provider: AIProvider, prompt: str) -> ProviderResult:
        try:
            if provider.name == "google":
                return self._call_google(provider, prompt)
            elif provider.name == "openai":
                return self._call_openai(provider, prompt)
            elif provider.name == "azure":
                return self._call_azure(provider, prompt)
            else:
                return ProviderResult(provider.name, provider.model, "", False, "Bilinmeyen sağlayıcı")
        except Exception as exc:
            return ProviderResult(
                provider.name, provider.model, "", False,
                f"{exc.__class__.__name__}: {str(exc)[:150]}"
            )

    def _is_retryable_error(self, error: Optional[str]) -> bool:
        if not error:
            return False
        lowered = error.lower()
        return any(
            token in lowered
            for token in (
                "429",
                "rate limit",
                "resource_exhausted",
                "temporarily",
                "timeout",
                "unavailable",
            )
        )

    def _call_with_retry(
        self,
        provider: AIProvider,
        prompt: str,
        max_retries: int = 2,
        base_delay: float = 1.0,
    ) -> ProviderResult:
        attempt = 0
        while True:
            result = self._call_provider(provider, prompt)
            if result.success:
                return result

            if attempt >= max_retries or not self._is_retryable_error(result.error):
                return result

            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            attempt += 1

    def _call_google(self, provider: AIProvider, prompt: str) -> ProviderResult:
        from google import genai
        client = genai.Client(api_key=provider.api_key)
        response = client.models.generate_content(model=provider.model, contents=prompt)
        text = getattr(response, "text", "") or ""
        return ProviderResult(provider.name, provider.model, text.strip(), bool(text.strip()))

    def _call_openai(self, provider: AIProvider, prompt: str) -> ProviderResult:
        from openai import OpenAI
        client = OpenAI(api_key=provider.api_key)
        response = client.chat.completions.create(
            model=provider.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        text = response.choices[0].message.content or ""
        return ProviderResult(provider.name, provider.model, text.strip(), bool(text.strip()))

    def _call_azure(self, provider: AIProvider, prompt: str) -> ProviderResult:
        from openai import AzureOpenAI
        endpoint = os.getenv(provider.endpoint_env or "")
        if not endpoint:
            return ProviderResult(provider.name, provider.model, "", False, "Azure endpoint eksik")
        client = AzureOpenAI(
            api_key=provider.api_key,
            azure_endpoint=endpoint,
            api_version="2024-06-01",
        )
        response = client.chat.completions.create(
            model=provider.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        text = response.choices[0].message.content or ""
        return ProviderResult(provider.name, provider.model, text.strip(), bool(text.strip()))


# ─── AI Kalite Değerlendirme ──────────────────────────────────

def score_code_quality(code: str, router: ProviderRouter) -> int:
    """Üretilen kodun kalitesini 0-100 arası puanla."""
    if not code.strip():
        return 0

    scoring_prompt = f"""Aşağıdaki Python kodunu 0-100 arasında puanla.
Sadece tek bir sayı yaz, başka hiçbir şey yazma.

Kriterlerin:
- Söz dizimi doğruluğu (25 puan)
- Async/await kullanımı (25 puan)
- Hata yönetimi try/except (25 puan)
- Pydantic model kullanımı (25 puan)

KOD:
```python
{code[:2000]}
```

PUAN:"""

    result = router.generate(scoring_prompt)
    if not result.success:
        return -1  # Puanlama yapılamadı

    try:
        score = int("".join(c for c in result.text if c.isdigit())[:3])
        return min(100, max(0, score))
    except (ValueError, IndexError):
        return -1


router = ProviderRouter()
