from django.contrib import admin
from .models import RoomCategory, RoomImage, RoomFeature, Room, Reservation


class RoomImageInline(admin.TabularInline):
    """Oda resimleri inline editor"""
    model = RoomImage
    extra = 1
    fields = ['image', 'title', 'alt_text', 'is_featured', 'display_order']
    ordering = ['display_order']


class RoomFeatureInline(admin.TabularInline):
    """Oda özellikleri inline editor"""
    model = RoomFeature
    extra = 1
    fields = ['icon', 'text_tr', 'text_en', 'display_order']
    ordering = ['display_order']


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_tr', 'is_active', 'display_order', 'image_count']
    list_editable = ['display_order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_tr', 'name_en', 'description_tr']

    inlines = [RoomImageInline, RoomFeatureInline]

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name_tr', 'name_en', 'name_de', 'name_fr', 'name_es', 'name_ru', 'name_ar')
        }),
        ('Açıklama', {
            'fields': ('description_tr', 'description_en', 'description_de', 'description_fr', 'description_es', 'description_ru', 'description_ar'),
            'classes': ('collapse',)
        }),
        ('Ayarlar', {
            'fields': ('is_active', 'display_order')
        }),
    )

    def image_count(self, obj):
        """Resim sayısını göster"""
        return obj.images.count()
    image_count.short_description = "Resim Sayısı"


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room_category', 'title', 'is_featured', 'display_order', 'uploaded_at']
    list_editable = ['display_order', 'is_featured']
    list_filter = ['room_category', 'is_featured', 'uploaded_at']
    search_fields = ['title', 'room_category__name_tr']
    readonly_fields = ['uploaded_at']

    fieldsets = (
        ('Resim Bilgisi', {
            'fields': ('room_category', 'image', 'title', 'alt_text')
        }),
        ('Ayarlar', {
            'fields': ('is_featured', 'display_order')
        }),
        ('Bilgi', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(RoomFeature)
class RoomFeatureAdmin(admin.ModelAdmin):
    list_display = ['room_category', 'icon', 'text_tr', 'display_order']
    list_editable = ['display_order']
    list_filter = ['room_category', 'icon']
    search_fields = ['text_tr', 'room_category__name_tr']

    fieldsets = (
        ('Oda', {
            'fields': ('room_category',)
        }),
        ('Özellik', {
            'fields': ('icon', 'text_tr', 'text_en', 'text_de', 'text_fr', 'text_es', 'text_ru', 'text_ar'),
        }),
        ('Ayarlar', {
            'fields': ('display_order',)
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'room_number', 'capacity']
    list_filter = ['room_type']
    search_fields = ['room_number']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['guest_name', 'room__room_number']
