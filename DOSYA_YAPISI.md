# 📁 EmareSetup — Dosya Yapısı

> **Oluşturulma:** Otomatik  
> **Amaç:** Yapay zekalar kod yazmadan önce mevcut dosya yapısını incelemeli

---

## Proje Dosya Ağacı

```
/Users/emre/Desktop/Emare/emaresetup
├── .env
├── .env.example
├── .github
│   └── workflows
│       └── emare-hub.yml
├── .gitignore
├── .vscode
│   └── settings.json
├── DOSYA_YAPISI.md
├── EMARE_AI_COLLECTIVE.md
├── EMARE_ANAYASA.md
├── EMARE_ORTAK_CALISMA -> /Users/emre/Desktop/Emare/EMARE_ORTAK_CALISMA
├── EMARE_ORTAK_HAFIZA.md
├── MAC_KURULUM.md
├── README.md
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 50fc1580a882_init.py
├── alembic.ini
├── api
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── fleet.py
│   └── server.py
├── autonomy_bridge.py
├── data
│   ├── __init__.py
│   ├── database.py
│   ├── emare_hub.db
│   ├── emare_modules_20260301_091755.zip
│   ├── fleet.json
│   ├── registry.json -> /Users/emre/Library/Mobile Documents/com~apple~CloudDocs/EmareHubSync/registry.json
│   ├── registry.local.backup.json
│   └── repository.py
├── docs
│   ├── 02_Sistem_Hazirligi.md
│   ├── 03_Proje_Kurulumu_ve_Gizli_Dosyalar.md
│   ├── 04_VSCode_ve_Model_Yonetimi.md
│   ├── 05_Test_ve_Senkronizasyon.md
│   ├── ARCHITECTURE.md
│   ├── CHAT_HISTORY.md
│   ├── CLOUD_CODE_PROMPTS.md
│   ├── FILO_YONETIMI.md
│   ├── PROJE_GELISTIRME.md
│   └── SESSION-CONTEXT.md
├── emare_core.py
├── emaresetup_hafiza.md
├── factory_worker.py
├── fleet_manager.py
├── main.py
├── models.yaml
├── modules
│   ├── cagri_analiz_pro
│   │   ├── main.py
│   │   └── manifest.json
│   └── cagri_duygu_analizi
│       ├── main.py
│       └── manifest.json
├── provider_router.py
├── requirements.txt
├── scripts
│   ├── bootstrap_and_openhands.sh
│   ├── bootstrap_imac.sh
│   ├── fleet_health_check.sh
│   ├── install_macos_prereqs.sh
│   ├── migrate_json_to_sqlite.py
│   ├── one_click_setup.sh
│   ├── setup_registry_sync.sh
│   └── start_openhands_worker.sh
├── smart_factory.py
├── templates
│   └── __init__.py
├── test_generator.py
└── web
    ├── index.html
    ├── package.json
    ├── pnpm-lock.yaml
    ├── src
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── styles.css
    └── vite.config.js

18 directories, 69 files

```

---

## 📌 Kullanım Talimatları (AI İçin)

Bu dosya, kod üretmeden önce projenin mevcut yapısını kontrol etmek içindir:

1. **Yeni dosya oluşturmadan önce:** Bu ağaçta benzer bir dosya var mı kontrol et
2. **Yeni klasör oluşturmadan önce:** Mevcut klasör yapısına uygun mu kontrol et
3. **Import/require yapmadan önce:** Dosya yolu doğru mu kontrol et
4. **Kod kopyalamadan önce:** Aynı fonksiyon başka dosyada var mı kontrol et

**Örnek:**
- ❌ "Yeni bir auth.py oluşturalım" → ✅ Kontrol et, zaten `app/auth.py` var mı?
- ❌ "config/ klasörü oluşturalım" → ✅ Kontrol et, zaten `config/` var mı?
- ❌ `from utils import helper` → ✅ Kontrol et, `utils/helper.py` gerçekten var mı?

---

**Not:** Bu dosya otomatik oluşturulmuştur. Proje yapısı değiştikçe güncellenmelidir.

```bash
# Güncelleme komutu
python3 /Users/emre/Desktop/Emare/create_dosya_yapisi.py
```
