from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomCategory, RoomImage, RoomFeature

# views.py
def index(request):
    """Ana sayfa - Dinamik odaları göster"""
    rooms = RoomCategory.objects.filter(is_active=True).prefetch_related('images', 'features').order_by('display_order')
    context = {
        'rooms': rooms
    }
    return render(request, 'index.html', context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def rooms(request):
    """Odalar sayfası - Tüm odaları detaylı göster"""
    room_categories = RoomCategory.objects.filter(is_active=True).prefetch_related(
        'images',
        'features'
    ).order_by('display_order')
    context = {
        'rooms': room_categories
    }
    return render(request, 'rooms.html', context)

def blog(request):
    return render(request, 'blog.html')

def ping(request):
    return HttpResponse("pong")

