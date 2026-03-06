# SESSION CONTEXT — Emare Hub

Bu dosya, Cloud Code/terminal AI ajanlarının projeyi hızlı ve doğru anlaması için hazırlanmıştır.

## Proje Kimliği

- Proje adı: Emare Hub
- Amaç: Modüler bir yazılım fabrikası kurmak ve AI destekli modül üretimi yapmak
- Çalışma ortamı: macOS (Intel), Python 3.11, `.venv`

## Mevcut Çekirdek Bileşenler

- `main.py`: Başlatma girişi, iCloud senkron kontrolü + ilk modül üretim çağrısı
- `factory_worker.py`: Gemini tabanlı (google-genai) modül scaffold üretimi
- `emare_core.py`: Kalıcı registry yönetimi (`data/registry.json`)
- `scripts/setup_registry_sync.sh`: iCloud tabanlı registry symlink kurulumu

## Çalıştırma Komutları

```bash
./scripts/setup_registry_sync.sh
./.venv/bin/python main.py
```

## Kritik Kural Seti

1. `data/registry.json` iCloud symlink olmalı.
2. Yeni modül üretiminde `manifest.json` mutlaka yazılmalı.
3. Kod değişiklikleri proje mimarisi ve dokümantasyonla tutarlı olmalı.
4. Çalıştırma komutları `.venv` yorumlayıcısıyla verilmelidir.

## Bilinen Durum

- `GOOGLE_API_KEY` tanımlı değilse AI üretimi fallback kod ile devam eder.
- API anahtarı tanımlandığında gerçek Gemini üretimi aktif olur.
