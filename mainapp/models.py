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