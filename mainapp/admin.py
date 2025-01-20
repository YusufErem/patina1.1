from django.contrib import admin

# Register your models here.
from .models import Room, Reservation

admin.site.register(Room, list_display=['room_number', 'room_type', 'capacity'])
admin.site.register(Reservation)
