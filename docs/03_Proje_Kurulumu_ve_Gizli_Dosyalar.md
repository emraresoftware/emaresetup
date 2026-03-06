# 3) Proje Kurulumu ve Gizli Dosyalar

## Proje klasörüne geçiş ve sanal ortam

```bash
cd ~/Desktop/EmareHub
uv venv --python 3.11 .venv
source .venv/bin/activate
```

## Bağımlılık kurulumu

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

Alternatif (ilk kurulum):

```bash
pip install fastapi uvicorn google-genai python-dotenv pyyaml
```

## Gizli dosyalar

`.env` dosyası:

```text
GOOGLE_API_KEY=...
OPENAI_API_KEY=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
ENVIRONMENT=development
```

Opsiyonel veri taşıma:

- iMac'teki `data/` klasörünü bu cihaza kopyalayabilirsin.
- Özellikle `data/registry.json` iki cihazda eşit kalmalı.
