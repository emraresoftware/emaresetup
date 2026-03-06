# Emare Hub

Emare Hub, modül bazlı çalışan ve AI destekli kod üretimi yapan bir yazılım fabrikasıdır.

## Hızlı Başlangıç

Tam tek komut kurulum:

```bash
./scripts/one_click_setup.sh
```

Bu komut sırasıyla:
- macOS prerequisite yazılımlarını kurar
- geliştirici araçlarını kurar (git, node, pnpm, gh, jq, wget, tree, htop)
- Python/.venv/proje bağımlılıklarını hazırlar
- iCloud registry senkronunu bağlar
- Docker + API key hazırsa OpenHands'i başlatır
- kurulum sonunda otomatik sağlık raporu üretir (`fleet_health_check`)

Sadece prerequisite kurulum:

```bash
./scripts/install_macos_prereqs.sh
```

Ön izleme (kurmadan görmek):

```bash
./scripts/install_macos_prereqs.sh --dry-run
```

Filo uyumluluk raporu:

```bash
./scripts/fleet_health_check.sh
```

Mevcut proje bootstrap akışı:

```bash
./scripts/bootstrap_imac.sh
```

Manuel akış:

```bash
./scripts/setup_registry_sync.sh
./.venv/bin/python main.py
```

## Otonom İşçi (OpenHands)

Tek komut (bootstrap + OpenHands):

```bash
export GOOGLE_API_KEY="<senin_anahtarin>"
./scripts/bootstrap_and_openhands.sh
```

Sadece OpenHands başlatma:

```bash
export GOOGLE_API_KEY="<senin_anahtarin>"
./scripts/start_openhands_worker.sh
```

Ardından tarayıcıdan `http://localhost:3000` adresini aç.

Python köprüsü ile görev devri:

```python
from autonomy_bridge import autonomy

autonomy.delegate_task("mimariye uygun yeni modül üret")
```

## Dokümantasyon

- [Kurulum Ana Sayfa](MAC_KURULUM.md)
- [Session Context](docs/SESSION-CONTEXT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Filo Yönetimi (Binlerce Cihaz)](docs/FILO_YONETIMI.md)
- [Cloud Code Prompt Şablonları](docs/CLOUD_CODE_PROMPTS.md)
- [Chat History](docs/CHAT_HISTORY.md)
