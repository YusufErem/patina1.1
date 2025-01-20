# mainapp/forms.py
from django import forms
from .models import Reservation

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'start_date', 'end_date', 'guest_name', 'adults', 'children']