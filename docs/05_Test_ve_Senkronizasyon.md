# 5) Test ve Senkronizasyon

## Uygulamayı çalıştırma

```bash
./.venv/bin/python main.py
```

İlk çalıştırmada uygulama, `data/registry.json` için iCloud symlink kontrolü yapar.
Eğer link eksik/hatalıysa şu komutu önerir:

```bash
./scripts/setup_registry_sync.sh
```

Beklenen başlangıç:

- iCloud registry linki doğruysa: `🔗 iCloud registry senkronu aktif.`
- `GOOGLE_API_KEY` yoksa AI pasif uyarısı görünür.
- `cagri_analiz_pro` modülü için üretim tetiklenir.
- `modules/cagri_analiz_pro/` altında dosyalar güncellenir.

## Git disiplini

- MacBook'ta iş bitince: `git push`
- iMac'e geçince: `git pull`

## Veri senkronizasyonu (opsiyonel)

- Bu proje için otomatik kurulum komutu:

```bash
./scripts/setup_registry_sync.sh
```

- Script, `data/registry.json` dosyasını iCloud altındaki ortak dosyaya bağlar:
	`~/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json`
- Aynı komutu iMac'te de çalıştırdığında her iki cihaz tek kayıt dosyasını paylaşır.

## Sorun giderme

- `ModuleNotFoundError`: `uv pip install --python .venv/bin/python -r requirements.txt`
- Eksik env hatası: `.env.example` → `.env` kopyala ve doldur
- Link kontrolü: `ls -l data/registry.json`
