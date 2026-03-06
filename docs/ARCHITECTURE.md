# ARCHITECTURE — Emare Hub v0.3

## 1) Çekirdek Katman

### `emare_core.py`

- `EmareHub` sınıfı registry dosyasını yönetir.
- Registry yolu: `data/registry.json`
- Ana görev: modül kayıtlarını kalıcı şekilde tutmak.

### Registry Şeması

```json
{
  "modules": [
    {
      "name": "modul_adi",
      "type": "analytics_module",
      "registered_at": "ISO8601"
    }
  ],
  "updated_at": "ISO8601"
}
```

## 2) Üretim Katmanı

### `factory_worker.py`

- Gemini istemcisi `google-genai` ile başlatılır.
- `create_module_scaffold(...)` çağrısı:
  - `modules/<module_name>/main.py` üretir
  - `modules/<module_name>/manifest.json` üretir
  - `hub.register_module(...)` ile merkezi kayda işler

## 3) Başlatma Katmanı

### `main.py`

- Önce iCloud registry senkronunu kontrol eder.
- Sonra worker çağırarak modül üretimini tetikler.

## 4) Senkronizasyon Katmanı

### `scripts/setup_registry_sync.sh`

- iCloud ortak dosya yolu:
  `~/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json`
- Projedeki `data/registry.json` dosyasını symlink olarak bu dosyaya bağlar.
- Yerel dosyayı gerektiğinde `data/registry.local.backup.json` olarak yedekler.

## 5) Tasarım İlkeleri

1. Basitlik: Minimal ama genişletilebilir çekirdek.
2. İzlenebilirlik: Her modül kayıt altına alınır.
3. Taşınabilirlik: iMac/MacBook arasında ortak registry kullanımı.
4. Dayanıklılık: API anahtarı yokken fallback ile sistem ayakta kalır.

## 6) Otonom İşçi Katmanı (OpenHands)

### Dosyalar

- `autonomy_bridge.py`: Python çekirdeğinden otonom işçiye görev devri
- `scripts/start_openhands_worker.sh`: Docker ile OpenHands konteyner başlatma

### Başlatma Akışı

```bash
export GOOGLE_API_KEY="<senin_anahtarin>"
./scripts/start_openhands_worker.sh
```

Arayüz:

`http://localhost:3000`

### Bridge Kullanımı

```python
from autonomy_bridge import autonomy

autonomy.delegate_task(
  "docs/ARCHITECTURE.md kurallarına uygun musteri_yonetimi modülü üret"
)
```

Not: endpoint erişilemezse bridge otomatik uyarı verir ve gerekli komutu gösterir.

## 7) Filo Ölçekleme (1000+ Cihaz)

Binlerce cihazda merkezi yönetim ve içerik standardizasyon modeli için:

- [Filo Yönetimi Dokümanı](FILO_YONETIMI.md)

Bu model; tek kaynak repo, tek komut bootstrap, merkezi sürüm kontrolü ve drift azaltma prensipleriyle çalışır.
