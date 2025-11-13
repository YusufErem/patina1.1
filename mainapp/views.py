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
    slider_images = list(HomePageImage.objects.filter(section='slider', is_active=True).order_by('display_order'))
    about_images = list(HomePageImage.objects.filter(section='about', is_active=True).order_by('display_order'))

    # Hakkımızda bölüm içeriği
    about_sections = list(AboutSection.objects.filter(is_active=True).order_by('display_order'))

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

def reviews(request):
    """Yorumlar sayfası - Tüm yorumları göster (pagination ile)"""
    from django.db.models import Avg, Count
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    # Tüm yorumları al
    all_reviews = GoogleReview.objects.all().order_by('-published_at')
    
    # Ortalama rating hesapla
    avg_rating = GoogleReview.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)
    
    # Rating dağılımı
    rating_distribution = GoogleReview.objects.values('rating').annotate(
        count=Count('id')
    ).order_by('-rating')
    
    # Toplam yorum sayısı
    total_count = all_reviews.count()
    
    # Pagination - Her sayfada 12 yorum göster
    paginator = Paginator(all_reviews, 12)
    page = request.GET.get('page', 1)
    
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    
    context = {
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_count': total_count,
        'rating_distribution': rating_distribution,
    }
    return render(request, 'reviews.html', context)

def ping(request):
    return HttpResponse("pong")

