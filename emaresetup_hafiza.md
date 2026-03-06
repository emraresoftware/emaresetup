# EMARE HUB — TAM HAFIZA DOSYASI

> 🔗 **Ortak Hafıza:** [`EMARE_ORTAK_HAFIZA.md`](/Users/emre/Desktop/Emare/EMARE_ORTAK_HAFIZA.md) — Tüm Emare ekosistemi, sunucu bilgileri, standartlar ve proje envanteri için bak.


> **Oluşturma tarihi:** 3 Mart 2026  
> **Versiyon:** 0.8.2  
> **Platform:** macOS Intel i7 MacBook Pro  
> **Geliştirici:** Emre  
> **Proje dizini:** `/Users/emre/Desktop/macoskurulumu`  
> **Python ortamı:** `.venv` (Python 3.11.14, uv ile kuruldu)

---

## 1. BU DOSYA NE İÇİN?

Bu dosya, projeyi herhangi bir AI ajana, yeni bir oturuma ya da farklı bir cihaza taşıdığında **sıfırdan anlayabilmesi için** hazırlanmıştır. Projenin ne olduğunu, şu an hangi aşamada olduğunu, hangi komutların ne işe yaradığını ve bir sonraki adımların ne olduğunu tamamen içerir.

---

## 2. PROJE NE?

**Emare Hub**, AI destekli bir **yazılım fabrikası** platformudur. Doğal dil komutlarıyla yazılım modülleri üretir, test eder, versiyonlar ve dağıtır.

### Temel Felsefe
```
Kullanıcı isteği
  → Multi-AI mimari çizer (Gemini / OpenAI / Azure failover)
  → Kod scaffold üretilir  
  → Otomatik test çalıştırılır
  → SQLite registry'e kaydedilir
  → iCloud üzerinden cihazlar arası senkronize olur
  → 1000+ cihaz filoya dağıtılır
```

### Tek cümle özet
> "Terminal komutları veya web arayüzüyle modül üretip yöneten, AI destekli, modüler bir yazılım fabrikası."

---

## 3. TEKNİK MİMARİ

```
┌──────────────────────────────────────────────────────────┐
│                   main.py (CLI — 558 satır)               │
│         13 Komut + İnteraktif Menü + Subcommand          │
├─────────┬──────────┬───────────┬────────────┬────────────┤
│         │          │           │            │            │
▼         ▼          ▼           ▼            ▼            │
smart_    factory_   provider_   fleet_       test_        │
factory   worker.py  router.py   manager.py   generator.py │
.py                                                        │
│                                                          │
▼                                                          │
emare_core.py → data/emare_hub.db (SQLite)                 │
             → data/registry.json (iCloud symlink, legacy)  │
                                                           │
api/server.py (FastAPI port 8000)                          │
web/src/App.jsx (React 19 + Vite 6, port 3001)             │
└──────────────────────────────────────────────────────────┘
```

### Katmanlar

| Katman | Dosya | Satır | Ne Yapar |
|--------|-------|-------|----------|
| CLI | `main.py` | 558 | 13 komut, interaktif menü, routing |
| Akıllı Fabrika | `smart_factory.py` | 167 | Doğal dil → çoklu modül planı + üretim |
| AI Motor | `factory_worker.py` | 170 | Multi-AI scaffold + versiyon + arşiv + auto-test |
| AI Router | `provider_router.py` | 210 | Gemini/OpenAI/Azure failover, retry/backoff |
| Filo | `fleet_manager.py` | 132 | Device heartbeat, deploy simülasyonu, özet |
| Test Üretici | `test_generator.py` | 141 | AI test kodu üretimi + pytest runner |
| Şablonlar | `templates/__init__.py` | 250 | 5 modül tipi şablonu |
| Çekirdek | `emare_core.py` | 53 | Registry CRUD + SQLite loglama |
| Veri Katmanı | `data/database.py` + `data/repository.py` | 264 | SQLAlchemy modeli + repository CRUD |
| REST API | `api/server.py` + `api/routes/fleet.py` | 373 | FastAPI CRUD, health, stats, fleet |
| Web | `web/src/App.jsx` + `web/src/styles.css` | 677 | React 19, 4 sayfa (Dashboard/Modules/Health/Fleet) |
| Otonom Köprü | `autonomy_bridge.py` | 41 | OpenHands Docker entegrasyonu |
| CI/CD | `.github/workflows/emare-hub.yml` | — | pytest + ruff lint + health check |
| Shell Scriptler | `scripts/*.sh` | 440 | Kurulum, sağlık, bootstrap (7 script) |

**Toplam kod:** ~3,756 satır (2,639 Python + 440 Shell + 677 React/CSS/JS)

---

## 4. DOSYA HARİTASI (TAM)

```
/Users/emre/Desktop/macoskurulumu/
│
├── main.py                          ← Ana CLI (13 komut, 558 satır)
├── emare_core.py                    ← Hub çekirdeği (registry + SQLite log)
├── factory_worker.py                ← Multi-AI scaffold üretici + versiyonlama
├── provider_router.py               ← Gemini/OpenAI/Azure failover router
├── smart_factory.py                 ← Doğal dil → çoklu modül fabrikası
├── fleet_manager.py                 ← Filo cihaz yönetimi + deploy
├── test_generator.py                ← AI test üretici + pytest runner
├── autonomy_bridge.py               ← OpenHands Docker köprüsü
├── models.yaml                      ← AI sağlayıcı yapılandırması
├── requirements.txt                 ← 13 Python bağımlılığı
├── alembic.ini                      ← DB migration config
├── MAC_KURULUM.md                   ← Kurulum indeks
├── README.md                        ← Genel açıklama
├── emaresetup_hafiza.md             ← ← ← BU DOSYA
│
├── templates/
│   └── __init__.py                  ← 5 modül tipi şablonu (250 satır)
│
├── api/
│   ├── server.py                    ← FastAPI CRUD + health + stats (port 8000)
│   └── routes/
│       └── fleet.py                 ← Filo API endpoints
│
├── web/
│   ├── package.json                 ← React 19 + Vite 6
│   ├── vite.config.js               ← Port 3001, API proxy → 8000
│   └── src/
│       ├── App.jsx                  ← 4 sayfa (Dashboard/Modules/Health/Fleet)
│       └── styles.css               ← Dark theme CSS
│
├── modules/                         ← Üretilen modüller burada yaşar
│   ├── cagri_analiz_pro/
│   │   ├── main.py
│   │   └── manifest.json
│   └── cagri_duygu_analizi/
│       ├── main.py
│       └── manifest.json
│
├── data/
│   ├── database.py                  ← SQLAlchemy modelleri
│   ├── repository.py                ← Repository CRUD katmanı
│   ├── emare_hub.db                 ← ANA VERİTABANI (SQLite)
│   ├── registry.json → iCloud       ← Legacy registry (opsiyonel, symlink)
│   ├── registry.local.backup.json   ← Yerel yedek
│   └── fleet.json                   ← Legacy fleet (opsiyonel)
│
├── scripts/
│   ├── one_click_setup.sh           ← Tek komut tam kurulum
│   ├── install_macos_prereqs.sh     ← Homebrew + araç kurulumu (device-aware)
│   ├── bootstrap_imac.sh            ← Python/venv/deps kurulum
│   ├── bootstrap_and_openhands.sh   ← Bootstrap + OpenHands başlat
│   ├── setup_registry_sync.sh       ← iCloud symlink kur
│   ├── start_openhands_worker.sh    ← OpenHands Docker başlat
│   ├── fleet_health_check.sh        ← Filo sağlık raporu (12 kontrol noktası)
│   └── migrate_json_to_sqlite.py    ← JSON → SQLite veri göçü
│
├── alembic/
│   └── versions/
│       └── 50fc1580a882_init.py     ← İlk migration
│
├── docs/
│   ├── PROJE_GELISTIRME.md          ← Kapsamlı geliştirme dokümanı (1017 satır)
│   ├── ARCHITECTURE.md              ← Teknik mimari
│   ├── FILO_YONETIMI.md             ← 1000+ cihaz filo yönetimi
│   ├── SESSION-CONTEXT.md           ← Oturum bağlamı (kısa özet)
│   ├── CLOUD_CODE_PROMPTS.md        ← AI prompt kütüphanesi
│   ├── CHAT_HISTORY.md              ← Geliştirme sohbet geçmişi
│   └── ...                          ← Diğer kurulum kılavuzları
│
└── .venv/                           ← Python 3.11.14 sanal ortam (uv ile)
```

---

## 5. KURULU ARAÇLAR VE BAĞIMLILIKLAR

### Sistem Araçları

| Araç | Versiyon | Nasıl Kuruldu |
|------|----------|---------------|
| Python | 3.11.14 | uv (`.venv`) |
| Node.js | 25.6.1 | Homebrew |
| pnpm | 10.30.3 | Homebrew |
| Homebrew | 5.0.15 | Resmi script |
| Docker | 29.2.1 | Homebrew Cask |
| uv | 0.10.7 | curl installer |
| git | 2.50.1 | Apple Git |
| gh (GitHub CLI) | 2.87.3 | Homebrew |
| jq, wget, tree, htop | — | Homebrew |

### Python Bağımlılıkları (`requirements.txt`)

```
pyyaml          # YAML yapılandırma okuma
python-dotenv   # .env dosyası yükleme
google-genai    # Gemini AI SDK (yeni nesil)
openai          # OpenAI + Azure OpenAI SDK
pydantic        # Veri modelleri / doğrulama
requests        # HTTP istekleri
rich            # Zengin terminal çıktıları (tablo, panel, renk)
pytest          # Test framework
fastapi         # REST API backend
uvicorn         # ASGI sunucu
httpx           # Async HTTP istemci
sqlalchemy      # ORM + SQLite bağlantısı
alembic         # DB migration aracı
```

### AI Sağlayıcı Yapılandırması (`models.yaml`)

```
Varsayılan: Google (Gemini)
├── google  → gemini-1.5-pro     (env: GOOGLE_API_KEY)
├── openai  → gpt-4o-mini        (env: OPENAI_API_KEY)
└── azure   → gpt-4o             (env: AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT)
```

---

## 6. ORTAM DEĞİŞKENLERİ (`.env` dosyası)

```bash
# .env dosyasında bulunur, git'e eklenmez
GOOGLE_API_KEY=       # Gemini AI (ana AI sağlayıcı)
OPENAI_API_KEY=       # OpenAI GPT — boşsa failover çalışmaz
AZURE_OPENAI_API_KEY= # Azure OpenAI — opsiyonel
AZURE_OPENAI_ENDPOINT=
EMARE_API_KEY=        # FastAPI endpoint koruma (opsiyonel)
```

> **Not:** `GOOGLE_API_KEY` tanımlı değilse sistem fallback şablon koduyla çalışmaya devam eder. Hiçbir şey çökmez.

---

## 7. ÇALIŞMA KOMUTLARI

### Temel

```bash
# Virtual environment aktif et
source /Users/emre/Desktop/macoskurulumu/.venv/bin/activate

# İnteraktif menüyü aç
python main.py

# Direkt komutlar
python main.py create    # Yeni modül oluştur (AI destekli)
python main.py list      # Kayıtlı modülleri listele
python main.py info      # Modül detayını göster
python main.py run       # Modül çalıştır
python main.py delete    # Modül sil (onay ister)
python main.py upgrade   # Modülü yeni versiyona yükselt (AI)
python main.py test      # Modül testlerini çalıştır (pytest)
python main.py export    # Modülleri ZIP olarak dışa aktar
python main.py smart     # Doğal dil → çoklu modül üretimi
python main.py fleet     # Filo cihaz yönetimi
python main.py health    # Sistem sağlık kontrolü (12 nokta)
python main.py stats     # Proje istatistikleri
python main.py api       # FastAPI sunucuyu başlat (port 8000)
```

### API Sunucusu

```bash
python main.py api
# veya:
uvicorn api.server:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

### Web Dashboard

```bash
cd web
pnpm dev
# Tarayıcı: http://localhost:3001
```

### iCloud Senkron Kurulumu

```bash
./scripts/setup_registry_sync.sh
# data/registry.json → ~/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json
```

### Tek Komut Tam Kurulum (yeni makineye)

```bash
./scripts/one_click_setup.sh
```

### Sağlık Kontrolü

```bash
./scripts/fleet_health_check.sh
# Beklenen çıktı: PASS: 12  |  WARN: 0  |  FAIL: 0
```

### OpenHands Otonom İşçi

```bash
export GOOGLE_API_KEY="<anahtarin>"
./scripts/start_openhands_worker.sh
# Arayüz: http://localhost:3000
```

---

## 8. API ENDPOINTLERİ (FastAPI — port 8000)

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/` | API bilgisi + versiyon |
| GET | `/api/modules` | Tüm modülleri listele |
| POST | `/api/modules` | Yeni modül oluştur (AI) |
| DELETE | `/api/modules/{name}` | Modül sil |
| GET | `/api/health` | Sağlık kontrolü |
| GET | `/api/stats` | İstatistikler |
| GET | `/api/fleet/devices` | Filo cihaz listesi |
| POST | `/api/fleet/heartbeat` | Cihaz kalp atışı |
| GET | `/api/fleet/summary` | Filo özeti |
| POST | `/api/fleet/deploy/{mod}` | Modül dağıtımı |

API Key koruması:
```bash
curl -H "X-API-Key: secret" http://localhost:8000/api/stats
```

---

## 9. MODÜL SİSTEMİ

### Her Modülün Yapısı

```
modules/<modul_adi>/
├── main.py           # Çalıştırılabilir modül kodu
├── manifest.json     # Meta veri
└── archive/          # Eski versiyonlar (upgrade sonrası)
    └── v1.0.0_main.py
```

### manifest.json Formatı

```json
{
  "name": "cagri_analiz_pro",
  "type": "analytics_module",
  "description": "Excel'den gelen çağrı kayıtlarını analiz eden servis.",
  "version": "1.0.0",
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

### Mevcut Kayıtlı Modüller

```
cagri_duygu_analizi    → analytics_module  (2026-03-01)
cagri_analiz_pro       → analytics_module  (2026-03-01)
```

---

## 10. VERİTABANI YAPISI

### Ana Veritabanı: `data/emare_hub.db` (SQLite)

- SQLAlchemy ORM kullanılır (`data/database.py`)
- Repository katmanı CRUD sağlar (`data/repository.py`)
- Alembic ile migration yönetilir (`alembic/`)
- İlk migration tamamlandı: `alembic/versions/50fc1580a882_init.py`

### Legacy (Opsiyonel)

- `data/registry.json` — iCloud symlink, eski modül kaydı (snapshot olarak kullanılabilir)
- `data/fleet.json` — Eski filo verisi

### JSON → SQLite Göçü

```bash
python scripts/migrate_json_to_sqlite.py
```

---

## 11. TAMAMLANAN FAZLAR

| Faz | Konu | Durum |
|-----|------|-------|
| **Faz 1** | Temel altyapı, proje iskeleti, .env, docs | ✅ |
| **Faz 2** | Gemini AI entegrasyonu, factory_worker, fallback sistemi | ✅ |
| **Faz 2.5** | DevOps otomasyon, iCloud sync, sağlık kontrolü, one-click setup | ✅ |
| **Faz 3** | İnteraktif CLI menü, 5 modül tipi, modül çalıştırma | ✅ |
| **Faz 4** | Test üretici (AI), semantic versioning, upgrade, delete, export, stats | ✅ |
| **Faz 5** | Multi-AI router (Gemini/OpenAI/Azure), failover, kod kalite skoru | ✅ |
| **Faz 6** | FastAPI backend (10 endpoint), React 19 web dashboard (4 sayfa) | ✅ |
| **Faz 7** | Filo yönetimi (heartbeat, deploy, summary), fleet CLI + API | ✅ |
| **Faz 8** | Akıllı fabrika (doğal dil → çoklu modül), 5 tip şablon, CI/CD pipeline | ✅ |
| **Faz 9** | SQLite veri katmanı, Alembic migration, git init, pre-commit hook | ✅ |
| **Faz 9.1** | API Key koruması (X-API-Key / Bearer, EMARE_API_KEY env) | ✅ |

---

## 12. ŞU ANKİ DURUM (3 Mart 2026)

### Ne Çalışıyor ✅

- `python main.py` — Tüm 13 komut çalışıyor
- Gemini AI — API key varsa gerçek üretim, yoksa fallback şablon
- SQLite veritabanı — Aktif (emare_hub.db)
- iCloud senkron — `data/registry.json` → iCloud symlink
- FastAPI backend — Port 8000, Swagger UI aktif
- React web dashboard — Port 3001, hot-reload
- Filo yönetimi — Heartbeat + deploy simülasyonu
- Akıllı fabrika — Doğal dil → çoklu modül üretimi
- CI/CD pipeline — pytest + ruff lint + health check
- Alembic migration — İlk migration tamamlandı
- `rich` terminal çıktısı — Renkli tablo + paneller

### Bilinen Sınırlamalar ⚠️

| # | Sorun | Detay | Öncelik |
|---|-------|-------|---------|
| 1 | Gemini Free Tier Kota | Günlük limit düşük, 429 hatası olabilir | Orta |
| 2 | OpenAI/Azure key boş | `.env`'e eklenince multi-AI failover tam aktif olur | Düşük |
| 3 | Async runtime yok | Üretilen async kod çalıştırıcısı yok | Orta |
| 4 | React prod build yok | Dev server çalışıyor, `pnpm build` yapılmadı | Düşük |
| 5 | Filo deploy simülasyon | Gerçek SSH/SCP transferi yok | Orta |
| 6 | PostgreSQL yok | Prod için Postgres geçişi planlanacak | Orta |
| 7 | JWT/Rol auth yok | API key var, tam kimlik doğrulama + rol sistemi eksik | Yüksek |
| 8 | Vault/Secret rotation yok | `.env` şifreleme ve rotation henüz yok | Orta |

---

## 13. SONRAKİ ADIMLAR (Öncelik Sırası)

### Hemen Yapılabilir (~2–20 dk)

```bash
# 1. OpenAI API key ekle → multi-AI failover tam aktif
echo 'OPENAI_API_KEY=sk-...' >> .env

# 2. JSON → SQLite migrate (henüz yapılmadıysa)
python scripts/migrate_json_to_sqlite.py

# 3. Mevcut modülleri test et
python main.py test

# 4. React production build
cd web && pnpm build
```

### Faz 9+ Yol Haritası

| Öncelik | Faz | Konu |
|---------|-----|------|
| 🔴 Yüksek | 9.1 | JWT Auth + Rol bazlı yetkilendirme (admin/dev/viewer) |
| 🔴 Yüksek | 9.2 | Kod güvenlik taraması (bandit + pip-audit) |
| 🟡 Orta | 10.1 | Plugin sistemi (lifecycle hook'ları) |
| 🟡 Orta | 12.1 | SQLite → PostgreSQL geçişi |
| 🟡 Orta | 12.2 | Redis cache (AI çağrı maliyeti azaltma) |
| 🟠 İleri | 11.1 | Agent Swarm (uzmanlaşmış AI agent takımı) |
| 🟠 İleri | 13.1 | Multi-proje workspace yönetimi |
| 🔵 Vizyon | 14.x | MLOps + ML model serving |
| 🔵 Vizyon | 15.x | Kubernetes + dağıtık mimari |

---

## 14. iCLOUD SENKRON YAPISI

iCloud senkronunda `data/registry.json` şu dizine symlink olur:

```
~/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json
```

Kurulum komutu:
```bash
./scripts/setup_registry_sync.sh
```

Bu sayede iMac ve MacBook arasında aynı registry kullanılır. SQLite (`data/emare_hub.db`) ise yerel kalır — gelecekte Postgres'e taşınacak.

---

## 15. CI/CD PIPELINE

`.github/workflows/emare-hub.yml` dosyası:

```
Push/PR tetiklemesi
├── pytest — tüm testler
├── ruff lint — Python kod kalitesi
└── fleet_health_check.sh — sistem sağlığı
```

---

## 16. AÇILIRKEN YAPILACAKLAR (YENİ OTURUM)

Projeyi taşıdıktan veya yeni bir oturumda açtıktan sonra:

```bash
# 1. Proje dizinine git
cd /Users/emre/Desktop/macoskurulumu

# 2. Ortamı aktif et
source .venv/bin/activate

# 3. Ortam kontrolü
python main.py health

# 4. İnteraktif menü
python main.py
```

Yeni makineye kurulum:
```bash
git clone <repo> /Users/emre/Desktop/macoskurulumu
cd /Users/emre/Desktop/macoskurulumu
./scripts/one_click_setup.sh
```

---

## 17. PROJE BÜYÜME GEÇMİŞİ

| Faz | Tarih | Python | Shell | Web | Toplam | Yeni Özellik |
|-----|-------|--------|-------|-----|--------|-------------|
| 1.0 | Şub 2026 | 120 | 0 | 0 | 120 | Temel iskelet |
| 2.0 | Şub 2026 | 230 | 0 | 0 | 230 | AI beyin (Gemini) |
| 2.5 | Mar 2026 | 230 | 421 | 0 | 651 | DevOps otomasyon |
| 3.0 | Mar 2026 | 467 | 421 | 0 | 888 | CLI fabrika |
| 8.0 | Mar 2026 | 2,084 | 440 | 677 | 3,201 | Full-stack (13 komut) |
| 8.1 | Mar 2026 | 2,403 | 440 | 677 | 3,520 | SQLite veri katmanı |
| **8.2** | **3 Mar 2026** | **2,639** | **440** | **677** | **3,756** | **Git + Alembic + API Key** |

---

## 18. HIZLI BAŞVURU KARTI

```
PROJE    : Emare Hub v0.8.2 — AI Yazılım Fabrikası
DİZİN    : /Users/emre/Desktop/macoskurulumu
PYTHON   : .venv/bin/python (3.11.14)
ANA DOSYA: main.py (13 komut)
VERİTABANI: data/emare_hub.db (SQLite)
AI       : Gemini 1.5 Pro (varsayılan) → OpenAI → Azure (failover)
API      : http://localhost:8000 (FastAPI)
WEB      : http://localhost:3001 (React)
OPENHANDS: http://localhost:3000 (Docker)
SAĞLIK   : ./scripts/fleet_health_check.sh
KURULUM  : ./scripts/one_click_setup.sh
```

---

*Bu dosya proje hafızasıdır. Taşıyabilir, AI ajana verebilir, yeni cihaza kopyalayabilirsin.*  
*Son güncelleme: 3 Mart 2026*
