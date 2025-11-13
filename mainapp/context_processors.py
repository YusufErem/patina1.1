from .models import GoogleReview
from django.db.models import Avg

def google_reviews_context(request):
    """Tüm template'lere Google yorum sayısını ve ortalama rating'i ekler"""
    total_count = GoogleReview.objects.count()
    avg_rating = GoogleReview.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)
    
    return {
        'total_reviews_count': total_count,
        'avg_rating': avg_rating,
    }

