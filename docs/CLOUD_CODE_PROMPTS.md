# Cloud Code Prompt Şablonları

Bu şablonlar terminal tabanlı AI ajana doğrudan kopyala-yapıştır için hazırlanmıştır.

## 1) Oturum Başlatma (Bağlam Yükleme)

```text
Şu an Emare Hub projesindeyiz.
Önce şu dosyaları sırayla oku ve kısa bir özet çıkar:
1) docs/SESSION-CONTEXT.md
2) docs/ARCHITECTURE.md
3) docs/05_Test_ve_Senkronizasyon.md

Ardından bu formatta cevap ver:
- Mevcut durum
- Riskler
- Sonraki en doğru adım
```

## 2) Yeni Modül Üretimi

```text
factory_worker.py kullanarak yeni modül üret.
Parametreler:
- module_name: <modul_adi>
- module_type: <tip>
- description: <is_tanimi>

Kural:
- Çıktıda manifest.json zorunlu.
- Üretim sonrası modules/<modul_adi>/main.py ve manifest.json içeriğini doğrula.
- data/registry.json içine kayıt düşüldüğünü kontrol et.
```

## 3) Hata Analizi (Terminal Log Odaklı)

```text
Aşağıdaki terminal hatasını kök nedene göre analiz et.
Sonra sadece gerekli minimum dosya değişikliğini öner ve uygula.
Değişiklik sonrası aynı komutu yeniden çalıştırıp sonucu raporla.

Hata logu:
<paste_log_here>
```

## 4) Mimariye Uygun Refactor

```text
Bu refactor görevinde docs/ARCHITECTURE.md kurallarına sadık kal.
- Public davranışı bozma
- Gereksiz dosya/özellik ekleme
- Önce en küçük düzeltme
- Sonra test komutu çalıştır

Görev:
<paste_task_here>
```

## 5) iMac ↔ MacBook Senkron Kontrolü

```text
Aşağıdaki kontrolleri sırayla yap:
1) data/registry.json symlink mi?
2) Hedef iCloud dosyası doğru mu?
3) setup_registry_sync.sh idempotent çalışıyor mu?
4) main.py çalışınca registry okunuyor mu?

Her maddeyi PASS/FAIL olarak raporla.
```

## 6) Faz Başlatma Promptu (Genel)

```text
Faz <N> başlatılıyor.
Önce mevcut sistemin etkilenebilecek parçalarını çıkar.
Sonra 5 adımlık bir uygulama planı ver.
Ardından planı uygulayıp her adım sonunda kısa doğrulama yap.
Sonunda şu başlıklarda rapor ver:
- Değişen dosyalar
- Çalıştırılan komutlar
- Açık riskler
- Bir sonraki önerilen adım
```
