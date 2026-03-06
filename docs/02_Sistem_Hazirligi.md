# 2) Sistem Hazırlığı

Bu sayfa, temiz Mac kurulumunda temel araçları hazırlar.

## Homebrew + Temel Paketler

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python git
```

## Python 3.11 (önerilen, root gerektirmez)

Tek komutla kurulum (önerilen):

```bash
./scripts/one_click_setup.sh
```

Sadece sistem yazılımlarını kurmak için:

```bash
./scripts/install_macos_prereqs.sh
```

Bu scriptin kurduğu başlıca araçlar:

- Homebrew
- Docker Desktop
- Visual Studio Code
- git, jq, node, pnpm, gh, wget, tree, htop
- uv (yoksa)

Kurulum adımlarını önce görmek için:

```bash
./scripts/install_macos_prereqs.sh --dry-run
```

Sadece proje bootstrap için:

```bash
./scripts/bootstrap_imac.sh
```

Kurulum + OpenHands başlatma (Docker yüklüyse):

```bash
export GOOGLE_API_KEY="<senin_anahtarin>"
./scripts/bootstrap_and_openhands.sh
```

Adım adım manuel kurulum:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.11
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

VS Code yorumlayıcı yolu:

`./.venv/bin/python`

## Doğrulama

```bash
python3 --version
git --version
brew --version
```

## Notlar

- Intel i7 MacBook için ek bir optimizasyon gerekmiyor.
- Python proje izolasyonu için bir sonraki sayfada `.venv` kullanılacak.
