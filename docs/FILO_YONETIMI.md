# Filo Yönetimi — Binlerce Cihazda Standart Emare Hub

Bu doküman, Emare Hub altyapısının binlerce macOS cihazda merkezi olarak yönetilmesi ve aynı içerik standardının korunması için operasyon modelini tanımlar.

## 1) Hedef

- Tüm cihazlarda aynı klasör yapısı, aynı script sürümü, aynı temel araç seti.
- Tek komutla kurulum ve güncelleme.
- Merkezi envanter, sürüm takibi ve drift (sapma) tespiti.

## 2) Dağıtım Modeli

### Merkez Kaynak (Single Source of Truth)

- Bu repo birincil kaynak kabul edilir.
- Cihazlar düzenli aralıklarla aynı branch/tag sürümüne çekilir.
- Öneri: sürüm etiketleri (`v0.3.x`) ile kontrollü dağıtım.

### Bootstrap Akışı

Her cihazda minimum adım:

```bash
./scripts/one_click_setup.sh
```

Bu komut:
- sistem bağımlılıklarını kurar,
- proje ortamını hazırlar,
- iCloud registry senkronunu bağlar,
- uygun koşulda OpenHands başlatır.

## 3) İçerik Eşitleme Stratejisi

## Kod ve Script Eşitleme

- Dağıtım kuralı: `git pull --ff-only`
- Merge yerine kontrollü release tag ile güncelleme.
- Kritik scriptler:
  - `scripts/one_click_setup.sh`
  - `scripts/install_macos_prereqs.sh`
  - `scripts/bootstrap_imac.sh`

## Veri Eşitleme

- `data/registry.json` iCloud ortak dosyaya symlink olmalı.
- Kurulum komutu:

```bash
./scripts/setup_registry_sync.sh
```

## 4) Cihaz Yönetimi Prensipleri

- Cihaz kimliği: her cihaz hostname + kullanıcı ile envantere girilir.
- Ortam standardı: Python 3.11 + `.venv` zorunlu.
- Değişiklik denetimi: docs + script güncellemesi birlikte yapılır.
- Geri dönüş: sürüm etiketi bazlı rollback prosedürü uygulanır.

## 5) Operasyon Kontrol Listesi (Toplu)

Yeni cihaz onboarding:
1. Repo klonla
2. `./scripts/one_click_setup.sh` çalıştır
3. `./.venv/bin/python main.py` doğrula
4. `data/registry.json` symlink doğrula

Periyodik uyum kontrolü:
1. `git fetch --tags`
2. hedef sürüme geçiş
3. one-click script ile refresh
4. sağlık kontrolü raporu al

Sağlık raporu komutu:

```bash
./scripts/fleet_health_check.sh
```

## 6) Önerilen Kurumsal Genişleme

- MDM ile komut dağıtımı (Jamf / Kandji / Intune)
- Merkezi log toplama (ör. ELK, Cloud Logging)
- CI ile release doğrulama + imzalı script dağıtımı
- Zorunlu güvenlik baseline (disk encryption, endpoint hardening)

## 7) Başarı Ölçütleri

- Kurulum başarı oranı: %99+
- Drift oranı: %2 altı
- Ortalama cihaz hazırlama süresi: < 15 dk
- Rollback süresi: < 10 dk
