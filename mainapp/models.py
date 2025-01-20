# models.py
from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('royal', 'Royal Oda'),
        ('exclusive', 'Exclusive Oda'),
        ('luxury', 'Luxury Oda'),
        ('executive', 'Executive Oda'),
        ('superior', 'Superior Oda'),
    ]
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.room_number}"

class Reservation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    adults = models.IntegerField()
    children = models.IntegerField()

    def __str__(self):
        return f"Rezervasyon: {self.guest_name} - {self.room}"