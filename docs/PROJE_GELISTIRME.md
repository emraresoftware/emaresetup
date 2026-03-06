# 🏭 Emare Hub — Proje Geliştirme Dökümanı

> **Son Güncelleme:** 1 Mart 2026  
> **Versiyon:** 0.8.2 (Git + Alembic + API Key Auth)  
> **Platform:** macOS Intel i7 MacBook Pro  
> **Geliştirici:** Emre  
> **Toplam Kod:** ~3,756 satır (2,639 Python + 440 Shell + 677 React/CSS/JS)

---

## 📑 İçindekiler

1. [Proje Özeti](#-proje-özeti)
2. [Mevcut Mimari](#-mevcut-mimari)
3. [Dosya Haritası](#-dosya-haritası)
4. [Modül Sistemi](#-modül-sistemi)
5. [Kurulu Araçlar](#-kurulu-araçlar)
6. [CLI Kullanım Kılavuzu](#-cli-kullanım-kılavuzu)
7. [API & Web Dashboard](#-api--web-dashboard)
8. [Script Referansı](#-script-referansı)
9. [Tamamlanan Fazlar](#-tamamlanan-fazlar)
10. [Bilinen Sınırlamalar](#-bilinen-sınırlamalar)
11. [Yeni Öneriler — Faz 9+](#-yeni-öneriler--faz-9)

---

## 🎯 Proje Özeti

**Emare Hub**, AI destekli bir **yazılım fabrikası** platformudur. Tek bir komutla:

- **Çoklu AI** ile modül iskeleti üretir (Gemini + OpenAI + Azure failover)
- Doğal dil ile **çoklu modül** oluşturur ("Müşteri analizi yap" → 3 modül)
- Modülleri **otomatik test** eder ve **versiyonlar**
- **FastAPI REST** backend + **React web** dashboard sunar
- **Filo yönetimi** ile 1000+ cihaza modül dağıtır
- **iCloud** üzerinden cihazlar arası senkronize eder
- **CI/CD** pipeline ile otomatik test + lint + deploy

### Temel Felsefe
```
Kullanıcı isteği → Multi-AI mimari çizer → Scaffold üretilir → Otomatik test
→ Registry'e kaydolur → iCloud ile senkronize olur → Filoya dağıtılır
```

---

## 🏗 Mevcut Mimari

```
┌──────────────────────────────────────────────────────────────────────┐
│                         main.py (CLI — 558 satır)                    │
│              İnteraktif Menü + 13 Komut + Subcommand Desteği         │
├────────┬────────────┬──────────────┬──────────────┬─────────────────┤
│        │            │              │              │                 │
▼        ▼            ▼              ▼              ▼                 │
smart_   factory_     provider_      fleet_         test_             │
factory  worker.py    router.py      manager.py     generator.py      │
.py      │            │              │              │                 │
│        │ Scaffold   │ Gemini       │ Device       │ AI Test          │
│ NL→    │ + Version  │ OpenAI       │ Heartbeat    │ Generation       │
│ Multi  │ + Archive  │ Azure        │ Deploy       │ pytest Run       │
│ Module │ + AutoTest │ Failover     │ Fleet Stats  │                  │
│        │            │              │              │                  │
▼        ▼            ▼              ▼              ▼                  │
┌────────────────────────────────────────────┐    ┌──────────────────┐│
│              emare_core.py                  │    │ api/server.py   ││
│         Registry + SQLite Loglama           │    │ FastAPI Backend ││
└─────────────┬──────────────────────────────┘    │ + fleet routes   ││
        │                                    └────────┬────────┘│
        ▼                                              │         │
       data/emare_hub.db (SQLite)                            ▼         │
       data/registry.json (legacy/iCloud)               web/App.jsx     │
                  React Dashboard  │
┌─────────────────────────────────────────────────────────────────────┘
│ templates/__init__.py (5 modül tipi şablonu)
│ autonomy_bridge.py (OpenHands Docker köprüsü)
│ data/database.py + data/repository.py (SQLite data layer)
│ .github/workflows/emare-hub.yml (CI/CD)
└─────────────────────────────────────────────────────────────────────
```

### Katmanlar

| Katman | Dosya | Satır | Sorumluluk |
|--------|-------|-------|------------|
| **CLI Arayüz** | `main.py` | 558 | 13 komut, menü, subcommand routing |
| **Akıllı Fabrika** | `smart_factory.py` | 167 | Doğal dil → çoklu modül üretimi, pattern öğrenme |
| **AI Motor** | `factory_worker.py` | 170 | Multi-provider scaffold, versiyon, arşiv, auto-test |
| **AI Router** | `provider_router.py` | 210 | Gemini/OpenAI/Azure failover, retry/backoff |
| **Filo Yönetimi** | `fleet_manager.py` | 132 | Device heartbeat, deploy, fleet summary |
| **Test Üretici** | `test_generator.py` | 141 | AI/fallback test üretimi, pytest çalıştırıcı |
| **Şablonlar** | `templates/__init__.py` | 250 | 5 modül tipi template (analytics, api, worker, cli, standard) |
| **Çekirdek** | `emare_core.py` | 53 | Registry CRUD, SQLite loglama |
| **Veri Katmanı** | `data/database.py` + `data/repository.py` | 264 | SQLite veri modeli + repository CRUD |
| **REST API** | `api/server.py` + routes | 373 | FastAPI CRUD, health, stats, fleet endpoints |
| **Web Dashboard** | `web/src/` | 677 | React 19 + Vite 6, 4 sayfa (Dashboard, Modules, Health, Fleet) |
| **Otonom Köprü** | `autonomy_bridge.py` | 41 | OpenHands Docker entegrasyonu |
| **CI/CD** | `.github/workflows/` | — | pytest, ruff lint, health check pipeline |
| **Otomasyon** | `scripts/*.sh` | 440 | Kurulum, health check, bootstrap (7 script) |

**Toplam Kod:** ~3,756 satır (2,639 Python + 440 Shell + 677 React/CSS/JS)

---

## 📁 Dosya Haritası

```
macoskurulumu/
├── main.py                          # Ana CLI (13 komut, 558 satır)
├── emare_core.py                    # Hub çekirdeği (registry + log)
├── factory_worker.py                # Multi-AI scaffold üretici + versiyonlama
├── provider_router.py               # Gemini/OpenAI/Azure failover router
├── smart_factory.py                 # Doğal dil → çoklu modül fabrikası
├── fleet_manager.py                 # Filo cihaz yönetimi + deploy
├── test_generator.py                # AI test üretici + pytest runner
├── autonomy_bridge.py               # OpenHands otonom köprü
├── models.yaml                      # AI sağlayıcı yapılandırması
├── requirements.txt                 # Python bağımlılıkları (13 paket)
├── alembic.ini                      # Alembic migration ayarlari
├── alembic/                         # Migration dosyalari
├── .env                             # API anahtarları (git'e eklenmez)
├── .env.example                     # .env şablonu
├── .gitignore                       # Python/Node/env ignore kuralları
│
├── templates/
│   └── __init__.py                  # 5 modül tipi şablonu (250 satır)
│
├── api/                             # FastAPI REST Backend
│   ├── __init__.py
│   ├── server.py                    # CRUD, health, stats endpoints
│   └── routes/
│       ├── __init__.py
│       └── fleet.py                 # Filo API endpoints
│
├── web/                             # React Web Dashboard
│   ├── package.json                 # React 19 + Vite 6
│   ├── vite.config.js               # Port 3001, API proxy → 8000
│   ├── index.html
│   └── src/
│       ├── main.jsx                 # React giriş noktası
│       ├── App.jsx                  # 4 sayfa (Dashboard/Modules/Health/Fleet)
│       └── styles.css               # Dark theme CSS
│
├── modules/                         # Üretilen modüller
│   ├── cagri_analiz_pro/
│   │   ├── main.py                  # Modül kodu
│   │   └── manifest.json            # Modül meta verisi
│   └── cagri_duygu_analizi/
│       ├── main.py
│       └── manifest.json
│
├── data/
│   ├── __init__.py
│   ├── database.py                  # SQLAlchemy modelleri
│   ├── repository.py                # Repository CRUD katmanı
│   ├── emare_hub.db                 # SQLite veritabani (yeni)
│   ├── registry.json → iCloud       # Legacy registry (opsiyonel)
│   ├── registry.local.backup.json   # Yerel yedek
│   ├── hub_logs.jsonl               # Legacy log (opsiyonel)
│   └── fleet.json                   # Legacy fleet (opsiyonel)
│
├── scripts/
│   ├── one_click_setup.sh           # Tek komut kurulum
│   ├── install_macos_prereqs.sh     # Homebrew + araç kurulumu
│   ├── bootstrap_imac.sh            # Python/venv/deps kurulum
│   ├── bootstrap_and_openhands.sh   # Bootstrap + OpenHands
│   ├── setup_registry_sync.sh       # iCloud symlink kurulumu
│   ├── start_openhands_worker.sh    # OpenHands Docker başlatma
│   ├── fleet_health_check.sh        # Filo sağlık raporu
│   └── migrate_json_to_sqlite.py    # JSON → SQLite veri göçü
│
├── .github/
│   └── workflows/
│       └── emare-hub.yml            # CI/CD (pytest + ruff + health)
│
├── docs/
│   ├── PROJE_GELISTIRME.md          # ← Bu dosya
│   ├── ARCHITECTURE.md              # Teknik mimari
│   ├── FILO_YONETIMI.md             # 1000+ cihaz filo yönetimi
│   ├── SESSION-CONTEXT.md           # Oturum bağlamı
│   ├── CLOUD_CODE_PROMPTS.md        # AI prompt kütüphanesi
│   ├── CHAT_HISTORY.md              # Geliştirme sohbet geçmişi
│   ├── 02_Sistem_Hazirligi.md       # Sistem hazırlığı kılavuzu
│   ├── 03_Proje_Kurulumu_ve_Gizli_Dosyalar.md
│   ├── 04_VSCode_ve_Model_Yonetimi.md
│   └── 05_Test_ve_Senkronizasyon.md
│
├── .venv/                           # Python 3.11 sanal ortam (uv)
├── .vscode/settings.json            # VS Code yapılandırması
├── MAC_KURULUM.md                   # Kurulum indeks sayfası
└── README.md                        # Proje genel açıklama
```

---

## 🧩 Modül Sistemi

### Modül Yapısı
Her modül kendi dizininde yaşar:
```
modules/<modul_adi>/
├── main.py           # Çalıştırılabilir modül kodu
└── manifest.json     # Meta veri
```

### manifest.json Formatı
```json
{
  "name": "cagri_analiz_pro",
  "type": "analytics_module",
  "description": "Excel'den gelen çağrı kayıtlarını analiz edip öfke tespiti yapan asenkron servis.",
  "emare_hub_compatible": true
}
```

### Desteklenen Modül Tipleri

| # | Tip | Açıklama |
|---|-----|----------|
| 1 | `analytics_module` | Veri analizi modülü |
| 2 | `api_service` | REST API servisi |
| 3 | `worker_agent` | Arka plan işçisi / agent |
| 4 | `cli_tool` | Komut satırı aracı |
| 5 | `standard_module` | Genel amaçlı modül |

### Registry (SQLite: data/emare_hub.db)
SQLite ana veri kaynagi, registry.json ise legacy/iCloud amacli opsiyonel snapshot.

Ornek kayit (konsept):
```json
{
  "modules": [
    {
      "name": "cagri_duygu_analizi",
      "type": "analytics_module",
      "registered_at": "2026-03-01T01:35:31"
    },
    {
      "name": "cagri_analiz_pro",
      "type": "analytics_module",
      "registered_at": "2026-03-01T05:46:37"
    }
  ],
  "updated_at": "2026-03-01T05:46:37"
}
```

---

## 🛠 Kurulu Araçlar

| Araç | Versiyon | Kurulum Yöntemi |
|------|----------|-----------------|
| Python | 3.11.14 (.venv) | uv |
| Node.js | 25.6.1 | Homebrew |
| pnpm | 10.30.3 | Homebrew |
| Homebrew | 5.0.15 | Resmi script |
| Docker | 29.2.1 | Homebrew Cask |
| uv | 0.10.7 | curl installer |
| git | 2.50.1 | Apple Git |
| gh (GitHub CLI) | 2.87.3 | Homebrew |
| jq | — | Homebrew |
| wget, tree, htop | — | Homebrew |

### Python Bağımlılıkları (requirements.txt)
```
pyyaml          # YAML yapılandırma okuma
python-dotenv   # .env dosyası yükleme
google-genai    # Gemini AI SDK (yeni nesil)
openai          # OpenAI + Azure OpenAI SDK
pydantic        # Veri modelleri / doğrulama
requests        # HTTP istekleri
rich            # Zengin terminal çıktıları (tablo, panel, renk)
pytest          # Otomatik test framework
fastapi         # REST API backend
uvicorn         # ASGI sunucu
httpx           # Async HTTP istemci
sqlalchemy      # ORM + SQLite baglantisi
alembic         # DB migration araci
```

---

## 💻 CLI Kullanım Kılavuzu

### Doğrudan Komutlar (Non-interactive)
```bash
# Modül Yönetimi
python main.py create      # Yeni modül oluştur (AI destekli)
python main.py list        # Kayıtlı modülleri listele (rich tablo)
python main.py info        # Modül detayını göster
python main.py run         # Modül çalıştır
python main.py delete      # Modül sil (onaylı)
python main.py upgrade     # Modülü yeni versiyona yükselt (AI)
python main.py test        # Modül testlerini çalıştır (pytest)
python main.py export      # Modülleri ZIP olarak dışa aktar

# Akıllı Fabrika
python main.py smart       # Doğal dil → çoklu modül üretimi

# Filo & Altyapı
python main.py fleet       # Filo cihaz yönetimi
python main.py health      # Sistem sağlık kontrolü (12 nokta)
python main.py stats       # Proje istatistikleri (rich tablo)
python main.py api         # FastAPI sunucusunu başlat (port 8000)
```

### İnteraktif Menü
```bash
python main.py           # Menüyü aç

╔══════════════════════════════════════════╗
║         🏭 EMARE HUB FABRİKA            ║
║      Yazılım Üretim Komut Merkezi       ║
╚══════════════════════════════════════════╝

── Modül İşlemleri ──
  1) 🆕  Yeni modül oluştur        7) 🧪  Modül test et
  2) 📦  Modül listele              8) ⬆️   Modül yükselt
  3) ▶️   Modül çalıştır             9) 🗑️   Modül sil
  4) 🔍  Modül detayı              10) 📤  Modülleri export et

── Akıllı Fabrika ──
  5) 🧠  Akıllı modül üret (NL)   11) 🌐  Filo yönetimi

── Sistem ──
  6) 🩺  Sağlık kontrolü          12) 📊  İstatistikler
 13) 🚀  API sunucusu başlat
  q) 🚪  Çıkış
```

### Akıllı Fabrika Kullanımı
```
$ python main.py smart
🧠 Ne yapmak istiyorsunuz? Doğal dille anlatın:
> Müşteri şikayetlerini analiz edip otomatik yanıt üreten bir servis yap

📋 Planlanan modüller:
  1. sikayet_analiz (analytics_module)
  2. otomatik_yanit (api_service)
  3. entegrasyon_api (worker_agent)

🏗️ Modül 1/3: sikayet_analiz üretiliyor...
✅ sikayet_analiz oluşturuldu (v1.0.0)
🏗️ Modül 2/3: otomatik_yanit üretiliyor...
✅ otomatik_yanit oluşturuldu (v1.0.0)
🏗️ Modül 3/3: entegrasyon_api üretiliyor...
✅ entegrasyon_api oluşturuldu (v1.0.0)
🎉 Tüm modüller başarıyla üretildi!
```

---

## 🌐 API & Web Dashboard

### FastAPI Backend (port 8000)
```bash
python main.py api       # Sunucuyu başlat
# veya doğrudan:
uvicorn api.server:app --reload --port 8000
```

API Key (opsiyonel):
```
export EMARE_API_KEY="secret"
curl -H "X-API-Key: secret" http://localhost:8000/api/stats
```

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/` | API bilgisi + versiyon |
| GET | `/api/modules` | Tüm modülleri listele |
| POST | `/api/modules` | Yeni modül oluştur (AI) |
| DELETE | `/api/modules/{name}` | Modül sil |
| GET | `/api/health` | Sağlık kontrolü (4 nokta) |
| GET | `/api/stats` | Proje istatistikleri |
| GET | `/api/fleet/devices` | Filo cihaz listesi |
| POST | `/api/fleet/heartbeat` | Cihaz kalp atışı |
| GET | `/api/fleet/summary` | Filo özeti |
| POST | `/api/fleet/deploy/{mod}` | Modül dağıtımı |

Swagger UI: `http://localhost:8000/docs`

### React Web Dashboard (port 3001)
```bash
cd web && pnpm dev       # Geliştirme sunucusu
```

4 sayfa:
- **Dashboard** — Proje istatistikleri + modül kartları
- **Modules** — Modül oluşturma / silme tablosu
- **Health** — Canlı sağlık durumu kontrolleri
- **Fleet** — Filo cihaz listesi + kendini kayıt

Dark theme, Vite hot-reload, API proxy → localhost:8000

---

## 📜 Script Referansı

| Script | Açıklama | Kullanım |
|--------|----------|----------|
| `one_click_setup.sh` | Tek komut tam kurulum | `./scripts/one_click_setup.sh` |
| `install_macos_prereqs.sh` | Eksik araçları yükle (device-aware) | `./scripts/install_macos_prereqs.sh` |
| `bootstrap_imac.sh` | Python + venv + deps + sync | `./scripts/bootstrap_imac.sh` |
| `fleet_health_check.sh` | 12 nokta sağlık raporu | `./scripts/fleet_health_check.sh` |
| `setup_registry_sync.sh` | iCloud symlink kur | `./scripts/setup_registry_sync.sh` |
| `start_openhands_worker.sh` | OpenHands Docker başlat | `./scripts/start_openhands_worker.sh` |

### Device-Aware Kurulum
`install_macos_prereqs.sh` her aracı tek tek kontrol eder:
```
✅ git zaten kurulu — atlanıyor
✅ jq zaten kurulu — atlanıyor
⬇️  node kuruluyor...
⬇️  pnpm kuruluyor...
```

### Sağlık Kontrolü Çıktısı
```
PASS: 12  |  WARN: 0  |  FAIL: 0
✅ Filo sağlık kontrolü başarılı
```

---

## ✅ Tamamlanan Fazlar

### Faz 1 — Temel Altyapı
- [x] Proje iskelet yapısı (main.py, emare_core.py)
- [x] models.yaml yapılandırma dosyası
- [x] .env / .env.example güvenli anahtar yönetimi
- [x] 5 sayfalık dokümantasyon sistemi
- [x] README.md

### Faz 2 — AI Beyin
- [x] Gemini entegrasyonu (google-genai SDK)
- [x] factory_worker.py ile AI kod üretimi
- [x] Fallback şablon sistemi (API hatalarında graceful degrade)
- [x] Modül scaffold üretimi (main.py + manifest.json)
- [x] Merkezi registry (data/registry.json)
- [x] JSONL loglama (data/hub_logs.jsonl)

### Faz 2.5 — DevOps & Otomasyon
- [x] Python 3.11 kurulumu (uv ile user-space)
- [x] Homebrew + tam geliştirici araç seti
- [x] Docker Desktop kurulumu
- [x] iCloud registry senkronizasyonu
- [x] Device-aware installer (eksik olanı kur, var olanı atla)
- [x] Filo sağlık kontrolü (12 kontrol noktası)
- [x] Tek komut kurulum (one_click_setup.sh)
- [x] OpenHands otonom köprü

### Faz 3 — CLI Fabrika
- [x] İnteraktif menü sistemi (döngüsel)
- [x] Subcommand desteği (list, create, info, run, health)
- [x] 5 modül tipi desteği
- [x] Modül detay görüntüleme (manifest + kod preview)
- [x] Modül çalıştırma (subprocess)
- [x] Hata yakalama ve kullanıcı dostu mesajlar

### Faz 4 — Modül Yaşam Döngüsü ✨
- [x] **test_generator.py** — AI destekli otomatik test üretimi
- [x] Fallback test şablonu (AI bağlantısız çalışır)
- [x] `python main.py test` komutu — pytest ile modül testi
- [x] Modül versiyonlama (semantic versioning: major.minor.patch)
- [x] `python main.py upgrade` — AI ile yeni versiyon üretimi
- [x] Eski versiyonları `modules/<ad>/archive/` altında arşivleme
- [x] `python main.py delete` — Modül silme (onaylı)
- [x] `python main.py export` — Modülleri ZIP olarak dışa aktarma
- [x] `python main.py stats` — Rich tablo ile proje istatistikleri

### Faz 5 — Çoklu AI Sağlayıcı ✨
- [x] **provider_router.py** — Multi-AI router engine
- [x] Google Gemini 2.0 Flash entegrasyonu
- [x] OpenAI GPT-4o-mini desteği (API key gerekli)
- [x] Azure OpenAI desteği (API key gerekli)
- [x] Otomatik failover: biri başarısız → diğerine geç
- [x] AI kod kalite skoru (0-100, ikinci AI değerlendirir)
- [x] factory_worker.py ProviderRouter'a migrate edildi

### Faz 6 — Web Dashboard ✨
- [x] **api/server.py** — FastAPI REST backend (CORS, Pydantic modeller)
- [x] Modül CRUD endpoints (GET/POST/DELETE)
- [x] Health + Stats endpoints
- [x] **api/routes/fleet.py** — Filo API endpoints
- [x] **web/App.jsx** — React 19 dashboard (290 satır)
- [x] 4 sayfa: Dashboard, Modules, Health, Fleet
- [x] Dark theme CSS, responsive tasarım
- [x] Vite 6 hot-reload + API proxy yapılandırması
- [x] Swagger UI otomatik API dokümantasyonu

### Faz 7 — Filo Orkestrasyonu ✨
- [x] **fleet_manager.py** — Device fleet management engine
- [x] Cihaz heartbeat işleme + durum takibi
- [x] Filo özet raporu (toplam cihaz, online/offline, modül sayısı)
- [x] Modül dağıtım simülasyonu (deploy)
- [x] `python main.py fleet` CLI komutu
- [x] REST API: /api/fleet/* endpoints
- [x] Web dashboard Fleet sayfası + cihaz kaydı

### Faz 8 — Akıllı Fabrika + CI/CD ✨
- [x] **smart_factory.py** — Doğal dil → çoklu modül üretimi
- [x] AI ile istek analizi + modül planlama
- [x] Pattern öğrenme (data/learned_patterns.json)
- [x] Başarılı üretimlerden öneri sistemi
- [x] **templates/__init__.py** — 5 modül tipi şablonu
- [x] `.github/workflows/emare-hub.yml` — CI/CD pipeline
- [x] pytest + ruff lint + health check otomasyonu
- [x] `.gitignore` — Kapsamlı ignore kuralları

### Faz 9 — Foundation (SQLite + Git + Alembic) ✨
- [x] SQLite veri modeli (data/database.py)
- [x] Repository katmani (data/repository.py)
- [x] EmareHub + FleetManager SQLite adaptasyonu
- [x] JSON → SQLite gecis scripti (scripts/migrate_json_to_sqlite.py)
- [x] Git init + pre-commit hook (ruff + pytest)
- [x] Alembic init + ilk migration (alembic/versions)

### Faz 9.1 — Security (API Key) ✨
- [x] API Key korumasi (X-API-Key / Bearer)
- [x] EMARE_API_KEY env degiskeni ile kosullu auth

### Hızlı İyileştirmeler ✨
- [x] `rich` kütüphanesi ile renkli terminal (tablo, panel)
- [x] Modül silme komutu + onay mekanizması
- [x] ZIP export özelliği
- [x] İstatistik komutu (rich tablo)
- [x] 5 modül tipi template sistemi

---

## ⚠️ Bilinen Sınırlamalar

### Çözülenler ✅

| # | Konu | Çözüm |
|---|------|-------|
| ~~1~~ | ~~Tek AI Sağlayıcı~~ | ✅ provider_router.py — Gemini/OpenAI/Azure failover |
| ~~2~~ | ~~Modül Testi Yok~~ | ✅ test_generator.py — AI test üretimi + pytest |
| ~~3~~ | ~~Versiyon Yönetimi Yok~~ | ✅ Semantic versioning + arşivleme |
| ~~4~~ | ~~Modül Silme Yok~~ | ✅ `python main.py delete` komutu |

### Mevcut Sınırlamalar

| # | Konu | Detay | Öncelik |
|---|------|-------|---------|
| 1 | Gemini Free Tier Kota | Ücretsiz plan günlük istek limiti düşük, 429 hatası olabilir | Orta |
| 2 | OpenAI/Azure Key Eksik | .env'de boş — eklenince multi-AI aktif olur | Düşük |
| 3 | Async Runtime Yok | Üretilen async kodlar henüz bir runner'a sahip değil | Orta |
| 4 | Web Dashboard Build | React dev server çalışır, production build henüz yapılmadı | Düşük |
| 5 | Filo Gerçek Deploy | Deploy simülasyon — gerçek SSH/SCP transfer yok henüz | Orta |
| 6 | PostgreSQL Yok | Prod icin Postgres gecisi planlanacak | Orta |
| 7 | JWT/Rol Bazli Auth Yok | API key var, tam auth + roller eksik | Yüksek |
| 8 | Vault Yok | .env sifreleme ve secret rotation henuz yok | Orta |

---

## 🚀 Yeni Öneriler — Faz 9+

### 🔵 Faz 9 — Güvenlik & Kimlik Doğrulama (Öncelik: YÜKSEK)

#### 9.1 JWT Auth Sistemi
```python
# api/auth.py
from fastapi_jwt_auth import AuthJWT

@app.post("/api/login")
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    # Kullanıcı doğrulama → JWT token
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}

@app.get("/api/modules")
@require_auth  # Sadece giriş yapmış kullanıcılar
def list_modules(...):
```
- FastAPI JWT authentication
- Rol bazlı yetkilendirme (admin / developer / viewer)
- API key sistemi (harici entegrasyonlar için)
- Rate limiting per-user

#### 9.2 Kod Güvenlik Taraması
```
python main.py security <modul>

🔒 Güvenlik Raporu: siparis_takip
├── ✅ SQL Injection: Temiz
├── ✅ XSS: Temiz
├── ⚠️ Hardcoded Secret: .env'den oku (satır 42)
├── ✅ Dependency Audit: 0 kritik
└── Skor: 92/100
```
- `bandit` ile statik analiz
- AI destekli güvenlik açığı tespiti
- Bağımlılık güvenlik denetimi (pip-audit)
- Secret detection (gizli anahtar taraması)

#### 9.3 Şifreli Konfigürasyon
- `.env` dosyasını şifreli vault'a taşı (SOPS veya age)
- Ortam bazlı konfigürasyon (dev/staging/prod)
- Secret rotation desteği

---

### 🟢 Faz 10 — Plugin Ekosistemi & Marketplace (Öncelik: YÜKSEK)

#### 10.1 Plugin Hook Sistemi
```python
# plugins/my_plugin.py
from emare_hub import plugin

@plugin.hook("before_module_create")
def validate_naming(module_name: str) -> bool:
    """Modül adı kurallarını kontrol et."""
    return module_name.startswith("emre_")

@plugin.hook("after_module_create")
def send_notification(module_info: dict):
    """Slack'e bildirim gönder."""
    slack.post(f"Yeni modül: {module_info['name']}")
```
- Lifecycle hook'ları (before/after create, test, deploy, delete)
- Plugin keşfi (plugins/ dizini otomatik taranır)
- Plugin yapılandırması (plugin.yaml)
- Üçüncü parti plugin yükleme (pip install emare-plugin-xxx)

#### 10.2 Modül Marketplace
```
python main.py marketplace

📦 Emare Hub Marketplace
┌────────────────────┬─────────────┬──────────┬───────┐
│ Modül              │ Geliştirici │ İndirme  │ Puan  │
├────────────────────┼─────────────┼──────────┼───────┤
│ email_sender       │ emre        │ 1,240    │ ⭐4.8  │
│ pdf_generator      │ ali         │ 890      │ ⭐4.5  │
│ csv_parser         │ community   │ 2,100    │ ⭐4.9  │
└────────────────────┴─────────────┴──────────┴───────┘

> install email_sender
✅ email_sender v2.1.0 yüklendi!
```
- Topluluk modül paylaşımı
- Versiyon uyumluluğu kontrolü
- Otomatik bağımlılık çözümleme
- Puanlama ve inceleme sistemi

#### 10.3 Modül Bağımlılık Grafiği
```
python main.py deps siparis_takip

📊 Bağımlılık Grafiği:
siparis_takip
├── veritabani_baglanti (v1.2.0)
│   └── connection_pool (v1.0.0)
├── email_bildirim (v2.0.0)
└── log_manager (v1.1.0)
```
- Modüller arası import analizi
- Döngüsel bağımlılık tespiti
- Bağımlılık sağlık raporu

---

### 🟡 Faz 11 — AI Agent Swarm (Öncelik: ORTA)

#### 11.1 Uzmanlaşmış Agent Takımı
```python
# agents/architect.py — Mimari tasarım uzmanı
# agents/frontend.py  — UI/UX kod üretimi
# agents/backend.py   — API + veritabanı uzmanı
# agents/tester.py    — Test + QA uzmanı
# agents/reviewer.py  — Kod inceleme uzmanı

class AgentSwarm:
    def build_project(self, description: str):
        plan = self.architect.design(description)
        backend_code = self.backend.implement(plan.api_spec)
        frontend_code = self.frontend.implement(plan.ui_spec)
        tests = self.tester.generate(backend_code, frontend_code)
        review = self.reviewer.evaluate(all_code)
        return ProjectResult(code=all_code, tests=tests, review=review)
```
- Her agent kendi AI sağlayıcısını kullanabilir
- Agent'lar arası mesajlaşma (konuşma zinciri)
- Paralel kod üretimi (backend + frontend aynı anda)
- Consensus mekanizması (2+ agent onayı)

#### 11.2 Agent Memory & Context
```python
# Her agent uzun süreli hafızaya sahip
agent.memory.save("pricing_module", {
    "patterns": ["rate_limiter", "cache_layer"],
    "quality_score": 95,
    "user_feedback": "harika çalışıyor"
})

# Gelecek üretimlerde bu bilgiyi kullan
agent.memory.recall("pricing")  # → İlgili pattern'ler
```
- ChromaDB / Pinecone ile vektör hafıza
- Proje bazlı context window
- Kullanıcı feedback öğrenme döngüsü

#### 11.3 Otonom Sprint Planlama
```
python main.py sprint "E-ticaret MVP'si 2 haftada"

📋 Sprint Planı (AI tarafından):
┌──────────┬──────────────────────────────┬──────────┐
│ Hafta    │ Görev                        │ Agent    │
├──────────┼──────────────────────────────┼──────────┤
│ H1-G1    │ Veritabanı şeması tasarla    │ Backend  │
│ H1-G2    │ Kullanıcı API endpoints      │ Backend  │
│ H1-G3    │ Login/register UI            │ Frontend │
│ H1-G4    │ Unit testler                 │ Tester   │
│ H2-G1    │ Ürün kataloğu               │ Backend  │
│ H2-G2    │ Sepet + ödeme               │ Full     │
│ H2-G3    │ Entegrasyon testleri         │ Tester   │
│ H2-G4    │ Kod inceleme + refactor      │ Reviewer │
└──────────┴──────────────────────────────┴──────────┘
```

---

### 🟠 Faz 12 — Veritabanı & Veri Yönetimi (Öncelik: ORTA)

#### 12.1 SQLite → PostgreSQL Geçişi
```python
# data/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Geliştirme: SQLite
engine = create_engine("sqlite:///data/emare_hub.db")

# Üretim: PostgreSQL
engine = create_engine("postgresql://user:pass@host/emare_hub")

class ModuleRecord(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    version = Column(String, default="1.0.0")
    code_hash = Column(String)
    quality_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    dependencies = Column(JSON)
```
- SQLAlchemy ORM ile veritabanı soyutlama
- Alembic ile migration yönetimi
- JSON dosyalardan otomatik göç scripti

#### 12.2 Redis Cache Katmanı
```python
# Pahalı AI çağrılarını cache'le
@cache(ttl=3600)
def generate_module(description: str) -> str:
    # Aynı açıklama 1 saat içinde tekrar gelirse → cache'den döndür
    return provider_router.generate(prompt)
```
- AI yanıtlarını cache'le (maliyet tasarrufu)
- Modül meta verisi hızlı erişim
- Fleet heartbeat geçici depolama

#### 12.3 Veri Analitik Dashboard
```
python main.py analytics

📊 Kullanım Analitikleri (Son 30 gün)
┌────────────────────┬──────────┐
│ Metrik             │ Değer    │
├────────────────────┼──────────┤
│ Toplam AI çağrısı  │ 847      │
│ Başarılı üretim    │ 812 (96%)│
│ Ortalama kalite    │ 78.5/100 │
│ En çok kullanılan  │ Gemini   │
│ Toplam maliyet     │ $2.34    │
│ Provider failover  │ 12 kez   │
│ En popüler tip     │ api_svc  │
└────────────────────┴──────────┘
```

---

### 🔴 Faz 13 — Multi-Proje & Workspace (Öncelik: İLERİ)

#### 13.1 Proje (Workspace) Yönetimi
```
python main.py workspace new "e-ticaret-mvp"
python main.py workspace switch "e-ticaret-mvp"
python main.py workspace list

📁 Projeler
┌────────────────────┬────────┬──────────┬──────────────┐
│ Proje              │ Modül  │ Durum    │ Son Aktivite │
├────────────────────┼────────┼──────────┼──────────────┤
│ e-ticaret-mvp      │ 8      │ Aktif    │ 5 dk önce    │
│ crm-sistemi        │ 12     │ Durdur.  │ 2 gün önce   │
│ chatbot-v2         │ 5      │ Aktif    │ 1 saat önce  │
└────────────────────┴────────┴──────────┴──────────────┘
```
- Her proje izole registry + konfigürasyon
- Proje bazlı AI prompt şablonları
- Cross-project modül paylaşımı (shared library)

#### 13.2 Multi-File Proje Üretimi
```
python main.py generate-project "FastAPI + React e-ticaret"

🏗️ Proje İskeleti Üretiliyor...
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry
│   │   ├── models.py         # SQLAlchemy modeller
│   │   ├── routes/
│   │   │   ├── auth.py       # Kimlik doğrulama
│   │   │   ├── products.py   # Ürün CRUD
│   │   │   └── orders.py     # Sipariş yönetimi
│   │   └── config.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── services/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md

✅ 24 dosya oluşturuldu!
```
- Tek modülden tam proje iskeletlerine geçiş
- Docker Compose otomatik üretimi
- README + API docs otomatik oluşturma

#### 13.3 Proje Şablonları (Boilerplate)
```
python main.py template list

📋 Hazır Proje Şablonları
1) FastAPI + PostgreSQL + Docker
2) React + Vite + TypeScript
3) CLI Tool (Click + Rich)
4) Discord Bot (discord.py)
5) ML Pipeline (scikit-learn + MLflow)
6) Microservices (FastAPI + RabbitMQ + Redis)
```

---

### 🟣 Faz 14 — MLOps & Veri Bilimi (Öncelik: VİZYON)

#### 14.1 ML Model Serving Modülleri
```python
# ML modülü otomatik üretimi
python main.py create --type ml_model --description "Müşteri churn tahmini"

# Üretilen yapı:
modules/musteri_churn/
├── main.py              # Model eğitimi + tahmin
├── model/
│   ├── train.py         # Eğitim pipeline
│   ├── predict.py       # Inference endpoint
│   └── evaluate.py      # Metrik raporlama
├── data/
│   └── sample.csv       # Örnek veri
├── requirements.txt     # scikit-learn, pandas, mlflow
├── Dockerfile           # Model serving container
└── manifest.json
```
- AI ile ML kodu (train + predict + evaluate) üretimi
- MLflow entegrasyonu (experiment tracking)
- Model versiyonlama (model registry)

#### 14.2 Veri Pipeline Modülleri
```
python main.py create --type data_pipeline --description "CSV'den PostgreSQL'e ETL"

# Üretilen pipeline:
Extract (CSV/API) → Transform (pandas) → Load (PostgreSQL)
+ Zamanlama (APScheduler / cron)
+ Hata yönetimi + retry
+ Veri doğrulama (Pydantic / Great Expectations)
```

#### 14.3 LLM Fine-Tuning Pipeline
```
python main.py llm-tune --model gemini --dataset data/custom.jsonl

📊 Fine-Tuning İlerleme
├── Veri doğrulama: 1,000 örnek ✅
├── Eğitim: ████████░░ 80%
├── Evaluation loss: 0.23
└── Tahmin hızı: 45 token/s
```
- Özel domain verileriyle model ince ayar
- LoRA / QLoRA ile düşük kaynak eğitimi
- Hub'ın kendi modüllerinden eğitim verisi çıkarma

---

### ⚫ Faz 15 — Dağıtık Mimari & Ölçeklendirme (Öncelik: VİZYON)

#### 15.1 Mesaj Kuyruğu Entegrasyonu
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Producer  │────→│ RabbitMQ │────→│ Consumer │
│ (API)     │     │ / Redis  │     │ (Worker) │
└──────────┘     │ Queue    │     └──────────┘
                  └──────────┘
```
- Modül üretim isteklerini kuyruğa at
- Birden fazla worker paralel üretim
- İşlem durumu takibi (job tracker)

#### 15.2 Kubernetes Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: emare-hub-api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: emare-hub:latest
          ports:
            - containerPort: 8000
---
# Helm chart ile tek komut kurulum
helm install emare-hub ./charts/emare-hub
```
- Docker multi-stage build
- Helm chart ile Kubernetes deploy
- Horizontal Pod Autoscaler (yük bazlı ölçekleme)
- Health probe'ları (liveness + readiness)

#### 15.3 Edge Computing
```
# Filo cihazlarında yerel AI inference
python main.py edge-deploy --model gemini-nano --device macbook-005

# Cihaz üzerinde çalışan lightweight AI
# → İnternet bağlantısı gerekmez
# → Düşük gecikme süresi
# → Gizli veri cihazda kalır
```

---

## 📊 Yeni Öneri Öncelik Matrisi

```
                         ETKİ
              Düşük      Orta       Yüksek
         ┌───────────┬───────────┬───────────┐
  Kolay  │ Git Init  │ Redis     │ JWT Auth  │
  ZORLUK │           │ Cache     │  (9.1)    │
         │           │ (12.2)    │           │
         ├───────────┼───────────┼───────────┤
    Orta   │ Proje     │ Postgres  │ Plugin    │
      │ Template  │  (12.1)   │ System    │
         │ (13.3)    │           │ (10.1)    │
         ├───────────┼───────────┼───────────┤
  Zor    │ Edge AI   │ K8s       │ Agent     │
         │ (15.3)    │ Deploy    │ Swarm     │
         │           │ (15.2)    │ (11.1)    │
         └───────────┴───────────┴───────────┘

🟢 Hemen başla: 9.1 (JWT Auth) + 12.1 (Postgres plan)
🟡 Sonraki sprint: 10.1 (Plugin) + 9.2 (Security Scan)
🟠 Planlanan: 11.x (Agent Swarm) + 13.x (Multi-Project)
🔴 Vizyon: 14.x (MLOps) + 15.x (Dağıtık Mimari)
```

---

## 🏃 Hemen Yapılabilecek Hızlı İyileştirmeler

1. **OpenAI API key ekle** — Multi-AI failover'ı aktifleştir (~2 dk)
2. **JSON → SQLite migrate** — `python scripts/migrate_json_to_sqlite.py` (~2 dk)
3. **`python main.py test`** — Mevcut modüllerin testlerini çalıştır (~5 dk)
4. **Web dashboard prod build** — `cd web && pnpm build` (~5 dk)
5. **Dockerfile oluştur** — Hub'ı container'da çalıştır (~20 dk)
6. **Makefile** — Sık kullanılan komutları kısayol yap (~15 dk)
7. **JWT Auth** — API key yerine rol bazli auth (~45 dk)
8. **TypeScript geçişi** — React JSX → TSX (tip güvenliği) (~45 dk)

---

## 📈 Proje Büyüme Tablosu

| Faz | Tarih | Python | Shell | Web | Toplam | Yeni Özellik |
|-----|-------|--------|-------|-----|--------|-------------|
| 1.0 | Feb 2026 | 120 | 0 | 0 | 120 | Temel iskelet |
| 2.0 | Feb 2026 | 230 | 0 | 0 | 230 | AI beyin (Gemini) |
| 2.5 | Mar 2026 | 230 | 421 | 0 | 651 | DevOps otomasyon |
| 3.0 | Mar 2026 | 467 | 421 | 0 | 888 | CLI fabrika (5 komut) |
| **8.0** | **Mar 2026** | **2,084** | **440** | **677** | **3,201** | **Full-stack (13 komut)** |
| **8.1** | **Mar 2026** | **2,403** | **440** | **677** | **3,520** | **SQLite veri katmani** |
| **8.2** | **Mar 2026** | **2,639** | **440** | **677** | **3,756** | **Git + Alembic + API key** |
| 9.0 | ? | ~2,600 | ~500 | ~900 | ~4,000 | Auth + Security |
| 10.0 | ? | ~3,200 | ~550 | ~1,200 | ~4,950 | Plugin ekosistemi |

---

*Bu döküman proje geliştikçe güncellenecektir. Son güncelleme: Mart 2026 — v0.8.2*
