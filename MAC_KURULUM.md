# 1) Emare Hub — MacBook Kurulum Dokümantasyonu

Bu doküman seti, Emare Hub geliştirme istasyonunu temiz bir Mac üzerinde ayağa kaldırmak için 5 sayfaya bölünmüştür.

## Sayfa Haritası

1. Bu sayfa: `MAC_KURULUM.md` (genel akış)
2. `docs/02_Sistem_Hazirligi.md`
3. `docs/03_Proje_Kurulumu_ve_Gizli_Dosyalar.md`
4. `docs/04_VSCode_ve_Model_Yonetimi.md`
5. `docs/05_Test_ve_Senkronizasyon.md`

## Hızlı Başlangıç

Sırasıyla şu adımları uygula:

- Sistem araçlarını kur (Homebrew, Python, Git)
- Projeyi aç, `.venv` oluştur, bağımlılıkları yükle
- `.env` ve gerekiyorsa `data/registry.json` dosyalarını yerleştir
- VS Code yorumlayıcısını `./.venv/bin/python` olarak seç
- `./.venv/bin/python main.py` ile doğrulama yap

## Kapsam

Bu 5 sayfa birlikte aşağıdakileri kapsar:

- Kurulum komutları
- Güvenli gizli bilgi yönetimi
- VS Code ve model seçimi
- Çoklu model yapılandırma yaklaşımı
- Test, sorun giderme ve iMac ↔ MacBook senkronizasyon disiplini
