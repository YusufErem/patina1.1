# models.py
from django.db import models

class RoomCategory(models.Model):
    """Oda Türü (Superior, King Suite, vb.)"""
    name_tr = models.CharField(max_length=100, verbose_name="Oda Adı (TR)")
    name_en = models.CharField(max_length=100, verbose_name="Room Name (EN)")
    name_de = models.CharField(max_length=100, verbose_name="Zimmer Name (DE)")
    name_fr = models.CharField(max_length=100, verbose_name="Nom de la Chambre (FR)")
    name_es = models.CharField(max_length=100, verbose_name="Nombre de la Habitación (ES)")
    name_ru = models.CharField(max_length=100, verbose_name="Название номера (RU)")
    name_ar = models.CharField(max_length=100, verbose_name="اسم الغرفة (AR)")

    description_tr = models.TextField(verbose_name="Açıklama (TR)")
    description_en = models.TextField(verbose_name="Description (EN)")
    description_de = models.TextField(verbose_name="Beschreibung (DE)")
    description_fr = models.TextField(verbose_name="Description (FR)")
    description_es = models.TextField(verbose_name="Descripción (ES)")
    description_ru = models.TextField(verbose_name="Описание (RU)")
    description_ar = models.TextField(verbose_name="الوصف (AR)")

    display_order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Oda Türü"
        verbose_name_plural = "Oda Türleri"

    def __str__(self):
        return self.name_tr

    @property
    def featured_image(self):
        """Ana sayfa için gösterilecek resim"""
        return self.images.filter(is_featured=True).first() or self.images.first()


class RoomImage(models.Model):
    """Oda Resimleri"""
    room_category = models.ForeignKey(
        RoomCategory,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Oda Türü"
    )
    image = models.ImageField(
        upload_to='rooms/',
        verbose_name="Resim"
    )
    title = models.CharField(max_length=200, verbose_name="Resim Başlığı")
    alt_text = models.CharField(
        max_length=200,
        verbose_name="Alt Text (SEO)",
        help_text="Resim gösterilemediğinde gösterilecek text"
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Ana Sayfa Thumbnail",
        help_text="Ana sayfa'da bu resmi göster"
    )
    display_order = models.IntegerField(default=0, verbose_name="Sıralama")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Oda Resimi"
        verbose_name_plural = "Oda Resimleri"

    def __str__(self):
        return f"{self.room_category.name_tr} - {self.title}"


class RoomFeature(models.Model):
    """Oda Özellikleri (dinamik)"""
    ICON_CHOICES = [
        ('fa-bed', 'Yatak'),
        ('fa-bath', 'Banyo'),
        ('fa-tv', 'Televizyon'),
        ('fa-wifi', 'Wi-Fi'),
        ('fa-mug-hot', 'Mini Bar'),
        ('fa-snowflake', 'Klima'),
        ('fa-couch', 'Oturma Alanı'),
        ('fa-door-open', 'Teras'),
        ('fa-water', 'Jacuzzi'),
        ('fa-fan', 'Soğutma'),
        ('fa-hair-dryer', 'Saç Kurutma Makinesi'),
        ('fa-key', 'Kasa'),
        ('fa-phone', 'Telefon'),
        ('fa-utensils', 'Mini Mutfak'),
        ('fa-briefcase', 'Çalışma Alanı'),
    ]

    room_category = models.ForeignKey(
        RoomCategory,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name="Oda Türü"
    )
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        verbose_name="İkon"
    )
    text_tr = models.CharField(max_length=200, verbose_name="Özellik (TR)")
    text_en = models.CharField(max_length=200, verbose_name="Feature (EN)")
    text_de = models.CharField(max_length=200, verbose_name="Merkmal (DE)")
    text_fr = models.CharField(max_length=200, verbose_name="Caractéristique (FR)")
    text_es = models.CharField(max_length=200, verbose_name="Característica (ES)")
    text_ru = models.CharField(max_length=200, verbose_name="Особенность (RU)")
    text_ar = models.CharField(max_length=200, verbose_name="الميزة (AR)")

    display_order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        ordering = ['display_order']
        verbose_name = "Oda Özelliği"
        verbose_name_plural = "Oda Özellikleri"

    def __str__(self):
        return f"{self.room_category.name_tr} - {self.text_tr}"

    def get_text(self, language='tr'):
        """Dile göre özellik metni al"""
        field_name = f'text_{language}'
        return getattr(self, field_name, self.text_tr)


class Room(models.Model):
    """Eski model - compatibility için tutuyoruz"""
    ROOM_TYPES = [
        ('royal', 'Royal Oda'),
        ('exclusive', 'Exclusive Oda'),
        ('luxury', 'Luxury Oda'),
        ('executive', 'Executive Oda'),
        ('superior', 'Superior Oda'),
        ('turkish_hamam_cave', 'Türk Hamamlı Mağara Oda'),
    ]
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.room_number}"


class Reservation(models.Model):
    """Eski model - compatibility için tutuyoruz"""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    adults = models.IntegerField()
    children = models.IntegerField()

    def __str__(self):
        return f"Rezervasyon: {self.guest_name} - {self.room}"


class GoogleReview(models.Model):
    """Google Places'den çekilen müşteri yorumları"""
    google_id = models.CharField(max_length=500, unique=True, verbose_name="Google Review ID")
    author_name = models.CharField(max_length=200, verbose_name="Yazar Adı")
    author_url = models.URLField(max_length=500, verbose_name="Yazar URL", blank=True)
    profile_photo_url = models.URLField(max_length=500, verbose_name="Profil Fotoğrafı", blank=True)
    rating = models.IntegerField(verbose_name="Puan (1-5)")
    text = models.TextField(verbose_name="Yorum")
    published_at = models.DateTimeField(verbose_name="Yayın Tarihi")
    language = models.CharField(max_length=10, default='tr', verbose_name="Dil")
    review_photos = models.JSONField(default=list, blank=True, verbose_name="Yorum Fotoğrafları", help_text="Yorumla birlikte paylaşılan fotoğraflar")

    # Sistema ait alanlar
    synced_at = models.DateTimeField(auto_now=True, verbose_name="Senkronize Tarihi")
    is_featured = models.BooleanField(default=False, verbose_name="Ana sayfada göster")
    display_order = models.IntegerField(default=0, verbose_name="Sıralama")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Google Yorum"
        verbose_name_plural = "Google Yorumlar"

    def __str__(self):
        return f"{self.author_name} - {self.rating}⭐"

    @property
    def star_display(self):
        """Yıldız gösterimi"""
        return "⭐" * self.rating


class HomePageImage(models.Model):
    """Ana sayfa için dinamik resimler (hero, about, experiences, vb.)"""
    SECTION_CHOICES = [
        ('slider', 'Ana Sayfa Slider (Hero)'),
        ('about', 'Hakkımızda Bölümü'),
        ('experiences', 'Deneyimler Bölümü'),
        ('activities', 'Aktiviteler Bölümü'),
    ]

    section = models.CharField(max_length=50, choices=SECTION_CHOICES, verbose_name="Bölüm")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    image = models.ImageField(upload_to='homepage/', verbose_name="Resim")
    caption = models.CharField(max_length=500, blank=True, verbose_name="Alt Yazı")

    display_order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['section', 'display_order']
        verbose_name = "Ana Sayfa Resimi"
        verbose_name_plural = "Ana Sayfa Resimleri"

    def __str__(self):
        return f"{self.get_section_display()} - {self.title}"


class AboutSection(models.Model):
    """Hakkımızda sayfası içeriği (dinamik)"""
    title_tr = models.CharField(max_length=200, verbose_name="Başlık (TR)")
    title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=200, verbose_name="Überschrift (DE)")
    title_fr = models.CharField(max_length=200, verbose_name="Titre (FR)")
    title_es = models.CharField(max_length=200, verbose_name="Título (ES)")
    title_ru = models.CharField(max_length=200, verbose_name="Заголовок (RU)")
    title_ar = models.CharField(max_length=200, verbose_name="العنوان (AR)")

    content_tr = models.TextField(verbose_name="İçerik (TR)")
    content_en = models.TextField(verbose_name="Content (EN)")
    content_de = models.TextField(verbose_name="Inhalt (DE)")
    content_fr = models.TextField(verbose_name="Contenu (FR)")
    content_es = models.TextField(verbose_name="Contenido (ES)")
    content_ru = models.TextField(verbose_name="Содержание (RU)")
    content_ar = models.TextField(verbose_name="المحتوى (AR)")

    image = models.ImageField(upload_to='about/', verbose_name="Resim")
    image_position = models.CharField(
        max_length=10,
        choices=[('left', 'Sol'), ('right', 'Sağ')],
        default='left',
        verbose_name="Resim Pozisyonu"
    )

    display_order = models.IntegerField(default=0, verbose_name="Sıralama")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Hakkımızda Bölümü"
        verbose_name_plural = "Hakkımızda Bölümleri"

    def __str__(self):
        return self.title_tr

    def get_title(self, language='tr'):
        """Dile göre başlık"""
        field_name = f'title_{language}'
        return getattr(self, field_name, self.title_tr)

    def get_content(self, language='tr'):
        """Dile göre içerik"""
        field_name = f'content_{language}'
        return getattr(self, field_name, self.content_tr)