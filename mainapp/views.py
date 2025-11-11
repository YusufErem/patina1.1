from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomCategory, RoomImage, RoomFeature, GoogleReview, HomePageImage, AboutSection

# views.py
def index(request):
    """Ana sayfa - Dinamik odaları, resimleri ve yorumları göster"""
    rooms = RoomCategory.objects.filter(is_active=True).prefetch_related('images', 'features').order_by('display_order')

    # Google reviews (featured olanları göster, yoksa hepsi)
    reviews = GoogleReview.objects.filter(is_featured=True).order_by('display_order')[:5]
    if not reviews:
        reviews = GoogleReview.objects.all().order_by('-published_at')[:5]

    # Ana sayfa resimleri (bölüm bazında)
    slider_images = HomePageImage.objects.filter(section='slider', is_active=True).order_by('display_order')
    about_images = HomePageImage.objects.filter(section='about', is_active=True).order_by('display_order')

    # Hakkımızda bölüm içeriği
    about_sections = AboutSection.objects.filter(is_active=True).order_by('display_order')

    context = {
        'rooms': rooms,
        'reviews': reviews,
        'slider_images': slider_images,
        'about_images': about_images,
        'about_sections': about_sections,
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

