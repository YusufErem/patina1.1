# 🏨 Patina Cappadocia - Admin Rehberi

Dinamik oda yönetim sisteminin nasıl kullanılacağına dair adım adım rehber.

## 📋 Admin Panel'e Erişim

```bash
# URL
http://yourdomain.com/admin

# Varsayılan admin hesabı oluşturma
python manage.py createsuperuser
```

## 🏠 Oda Kategorilerini Yönetme

### Yeni Oda Eklemek

1. **Admin paneline gir** → "Oda Türleri" → "Oda Türü Ekle"
2. **Temel Bilgiler** bölümü:
   - Oda Adı (TR) - örnek: "Superior Oda"
   - Room Name (EN) - örnek: "Superior Room"
   - Zimmer Name (DE), Nom (FR), Nombre (ES), Название (RU), الاسم (AR)
   - Aktif checkbox'ını işaretle
   - Sıralama numarası (ana sayfada kaçıncı sırada gösterilecek)

3. **Açıklama** bölümü (isteğe bağlı):
   - Her dile ait detaylı açıklama yaz
   - Örnek: "Kapadokya manzaralı, özel teraslı lüks odalarımız"

### Oda Resimleri Eklemek

Oda Türü detay sayfasında **Oda Resimleri** bölümü:

1. **[+ Resim Ekle]** butonuna tıkla
2. **Resim** - Bilgisayardan dosya seç
3. **Resim Başlığı** - Örnek: "Superior Oda - Ana Görünüm"
4. **Alt Text (SEO)** - Örnek: "Superior oda tasarımı ve iç dekorasyonu"
5. **Ana Sayfa Thumbnail** - İlk resim için ✓ işaretle (ana sayfa'da görünecek)
6. **Sıralama** - Resimlerin sırası (1, 2, 3...)
7. **Kaydet** - Düğmesine tıkla

### Oda Özelliklerini Eklemek

Aynı sayfada **Oda Özellikleri** bölümü:

1. **[+ Özellik Ekle]** butonuna tıkla
2. **İkon Seç** - Açılır menüden:
   - fa-bed (Yatak)
   - fa-bath (Banyo)
   - fa-tv (TV)
   - fa-wifi (Wi-Fi)
   - fa-water (Jacuzzi)
   - fa-door-open (Teras)
   - Vs. (15+ seçenek)

3. **Metinleri Doldur** - Her dil için:
   - Özellik (TR): "King Size Yatak"
   - Feature (EN): "King Size Bed"
   - Merkmal (DE), Caractéristique (FR), vb.

4. **Sıralama** - Özelliklerin gösterim sırası
5. **Kaydet**

## 🖼️ Resim Yönetimi (Doğrudan)

Admin → "Oda Resimleri" sayfasında:

- **Resim Listele** - Tüm resimleri gör
- **Sıra Değiştir** - Sütun başlıklarında sürükle-bırak
- **Ana Sayfa Thumbnail Seç** - Yıldız simgesine tıkla
- **Sil** - Satırın sonundaki seçenekler menüsünde

## 🎨 Özellik Yönetimi (Doğrudan)

Admin → "Oda Özellikleri" sayfasında:

- **Özellik Listele** - Tüm özellikleri gör
- **İkon Seç** - Bir özelliğin ikonunu değiştir
- **Metinleri Düzenle** - 7 dil desteğiyle

## 📱 Çok Dilli Yönetim

Sistem 7 dili destekliyor:

| Dil | Kod | Siteyi Görüntülemek |
|-----|-----|-----|
| Türkçe | TR | /tr/ |
| English | EN | /en/ |
| Deutsch | DE | /de/ |
| Français | FR | /fr/ |
| Español | ES | /es/ |
| Русский | RU | /ru/ |
| العربية | AR | /ar/ |

**Önemli:** Admin panelinde tüm dillerin metinlerini doldurmalısın. Kullanıcılar sitede dil seçince bu metinler gösterilir.

## 🚀 Yararlı İpuçları

### ✅ En İyi Uygulamalar

1. **Resim Boyutu** - 1920x1440px veya daha büyük (yüksek kalite için)
2. **Alt Text** - SEO için açıklayıcı olmalı (örnek: "Jakuzili banyo ayrıntısı")
3. **Sıralama** - 1, 2, 3... şeklinde sırasal sayılar kullan
4. **Dil Desteği** - Her odanın tüm 7 dili doldur
5. **Thumbnail** - İlk resim her zaman en güzel olanı seç

### ❌ Dikkat Edilmesi Gerekenler

- **Boş Alan Bırakma** - Tüm dil alanlarını doldur
- **Yanlış Resim Türü** - Sadece JPG/PNG/WebP kullan
- **Çok Fazla Resim** - Bir odaya 20+ resim ekleme (yavaşlama riski)
- **Türkçe Dışında Metin** - TR alanında İngilizce yazma

## 📊 Veri İstatistikleri

Mevcut içerik:
- **7 Oda Türü** (Superior, King Suite, Queen, Executive, Presidential, Honeymoon, Turkish Hamam)
- **53 Resim** (7 oda x ortalama 7-8 resim)
- **28 Özellik** (7 oda x 4 özellik)
- **7 Dil Desteği** (Tüm metinler çevrilmiş)

## 🔧 Teknik Bilgiler

### Database Modelleri

```
RoomCategory (Oda Türü)
├── name_tr, name_en, name_de, name_fr, name_es, name_ru, name_ar
├── description_tr ... description_ar
├── display_order (sıralama)
└── is_active (aktif/pasif)

RoomImage (Resim) → RoomCategory
├── image (dosya)
├── title, alt_text
├── is_featured (ana sayfa mı?)
├── display_order (sıralama)
└── uploaded_at (yükleme tarihi)

RoomFeature (Özellik) → RoomCategory
├── icon (fa-bed, fa-bath, vb.)
├── text_tr ... text_ar (7 dil)
└── display_order (sıralama)
```

### URL Yapısı

```
Ana Sayfa:        /
Odalar Sayfası:   /rooms/
Çok Dilli:        /en/rooms/, /de/rooms/, vb.
Admin Paneli:     /admin/
```

## 📞 Destek

Sorun yaşarsan:

1. **Resim yüklenmiyor?**
   - Dosya formatı JPG/PNG/WebP olmalı
   - Dosya boyutu 5MB'den küçük olmalı

2. **Metinler görülmüyor?**
   - Tüm 7 dile aynı metni doldur
   - Sayfa cache'i temizle (Ctrl+Shift+R)

3. **Sıralama değişmiyor?**
   - Display Order numaralarını kontrol et
   - Sayfayı yenile (F5)

---

**Oluşturulma Tarihi:** 2024
**Son Güncelleme:** November 2024
**Sistem:** Django + PostgreSQL/SQLite
