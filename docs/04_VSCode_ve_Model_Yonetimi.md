# 4) VS Code ve Model Yönetimi

## VS Code profil ve interpreter

1. VS Code profilini **Emare Hub** olarak seç.
2. `Cmd + Shift + P` → `Python: Select Interpreter`.
3. `./.venv/bin/python` yorumlayıcısını seç.

## Manage Models notu

`Manage Models` ekranında manuel model ekleyememe durumu normal olabilir. Bazı ortamlarda yalnızca hesapta açık modeller listelenir.

## Proje içinden model yönetimi (önerilen)

`models.yaml` ile model tanımı:

```yaml
default_provider: google
providers:
  google:
    model: gemini-1.5-pro
    api_key_env: GOOGLE_API_KEY
  openai:
    model: gpt-4o-mini
    api_key_env: OPENAI_API_KEY
  azure:
    model: gpt-4o
    api_key_env: AZURE_OPENAI_API_KEY
    endpoint_env: AZURE_OPENAI_ENDPOINT
```

## Hızlı kontrol

- API anahtarları `.env` içinde mi?
- Model adları sağlayıcı tarafında doğru mu?
- Ağ/VPN çağrıları engelliyor mu?
