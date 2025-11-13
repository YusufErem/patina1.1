from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from mainapp.models import GoogleReview
import os
import requests
import re
import time
from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser

class Command(BaseCommand):
    help = 'Fetch Google reviews from RapidAPI Google Reviews Scraper and cache them in database'

    def parse_relative_date(self, date_str):
        """Parse relative date strings like '2 months ago', 'a week ago', etc."""
        if not date_str or not isinstance(date_str, str):
            return None
        
        date_str = date_str.lower().strip()
        now = timezone.now()
        
        # Pattern: "X [unit] ago" or "a [unit] ago"
        patterns = [
            (r'(\d+)\s*years?\s*ago', lambda m: now - timedelta(days=int(m.group(1)) * 365)),
            (r'a\s*year\s*ago', lambda m: now - timedelta(days=365)),
            (r'(\d+)\s*months?\s*ago', lambda m: now - timedelta(days=int(m.group(1)) * 30)),
            (r'a\s*month\s*ago', lambda m: now - timedelta(days=30)),
            (r'(\d+)\s*weeks?\s*ago', lambda m: now - timedelta(weeks=int(m.group(1)))),
            (r'a\s*week\s*ago', lambda m: now - timedelta(weeks=1)),
            (r'(\d+)\s*days?\s*ago', lambda m: now - timedelta(days=int(m.group(1)))),
            (r'a\s*day\s*ago', lambda m: now - timedelta(days=1)),
            (r'(\d+)\s*hours?\s*ago', lambda m: now - timedelta(hours=int(m.group(1)))),
            (r'an?\s*hour\s*ago', lambda m: now - timedelta(hours=1)),
            (r'(\d+)\s*minutes?\s*ago', lambda m: now - timedelta(minutes=int(m.group(1)))),
            (r'a\s*minute\s*ago', lambda m: now - timedelta(minutes=1)),
        ]
        
        for pattern, func in patterns:
            match = re.search(pattern, date_str)
            if match:
                return func(match)
        
        return None

    def parse_rating(self, rating):
        """Parse rating from various formats like '5', 'Rated 5 out of 5', etc."""
        if not rating:
            return 5
        
        # If it's already a number
        if isinstance(rating, (int, float)):
            return int(rating)
        
        # If it's a string, try to extract number
        if isinstance(rating, str):
            # Remove common prefixes/suffixes
            rating = rating.replace('Rated', '').replace('out of 5', '').replace(',', '').strip()
            # Extract first number
            match = re.search(r'\d+', rating)
            if match:
                return int(match.group())
        
        return 5

    def add_arguments(self, parser):
        parser.add_argument(
            '--business-id',
            type=str,
            default='0x152a6971a1e01c23:0x1b7c9235015f1949',
            help='Google Business ID (default: Patina Cappadocia)'
        )
        parser.add_argument(
            '--rapidapi-key',
            type=str,
            default=None,
            help='RapidAPI Key (or set RAPIDAPI_KEY env variable)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=200,
            help='Maximum number of reviews to fetch (default: 200)'
        )

    def handle(self, *args, **options):
        business_id = options['business_id']
        limit = options['limit']
        # RapidAPI key'i environment variable'dan veya settings'den al
        rapidapi_key = options['rapidapi_key'] or os.environ.get('RAPIDAPI_KEY') or getattr(settings, 'RAPIDAPI_KEY', None)

        if not rapidapi_key:
            self.stdout.write(
                self.style.ERROR(
                    '❌ RapidAPI key bulunamadı!\n'
                    'Lütfen RAPIDAPI_KEY environment variable\'ını ayarla\n'
                    'veya --rapidapi-key parametresi ile geç\n'
                    'Örnek: export RAPIDAPI_KEY="your-rapidapi-key"'
                )
            )
            return

        self.stdout.write(self.style.SUCCESS(f'🔄 Google Reviews çekiliyor... (Business ID: {business_id})'))

        verbosity = options.get('verbosity', 1)
        headers = {
            'x-rapidapi-key': rapidapi_key,
            'x-rapidapi-host': 'local-business-data.p.rapidapi.com'
        }

        try:
            # Tek seferde tüm yorumları çek
            self.stdout.write('📡 Yorumlar çekiliyor (tek seferde)...')
            url = 'https://local-business-data.p.rapidapi.com/business-reviews-v2'
            params = {
                'business_id': business_id,
                'limit': str(limit),
                'translate_reviews': 'false',
                'sort_by': 'most_relevant',
                'region': 'tr',
                'language': 'tr'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if verbosity >= 2:
                self.stdout.write(f'📋 API Response keys: {list(data.keys()) if isinstance(data, dict) else "List"}')
            
            # Hata kontrolü
            if isinstance(data, dict):
                if 'status' in data and data.get('status') != 'OK':
                    error_msg = data.get('error', 'Bilinmeyen hata')
                    self.stdout.write(self.style.ERROR(f'❌ API Hatası: {error_msg}'))
                    return
                
                # Reviews'ı al
                if 'data' in data and isinstance(data['data'], dict):
                    reviews = data['data'].get('reviews', [])
                else:
                    reviews = []
            else:
                reviews = []

            if not reviews:
                self.stdout.write(self.style.WARNING('⚠️ Hiç yorum bulunamadı'))
                if verbosity >= 1:
                    self.stdout.write(f'📋 Response içeriği: {data}')
                return

            self.stdout.write(self.style.SUCCESS(f'✓ {len(reviews)} yorum bulundu'))

            # Veritabanına kaydet
            created_count = 0
            updated_count = 0

            for review in reviews:
                try:
                    # Review objesinin formatını kontrol et
                    if not isinstance(review, dict):
                        self.stdout.write(self.style.WARNING(f'  ⚠️ Geçersiz review formatı: {type(review)}'))
                        continue
                    
                    # Yeni API formatına göre field'ları al
                    review_id = review.get('review_id', '')
                    author_name = review.get('author_name', 'Anonymous')
                    author_url = review.get('author_link', review.get('author_reviews_link', ''))
                    profile_photo_url = review.get('author_photo_url', '')
                    rating = review.get('rating', 5)
                    if not isinstance(rating, int):
                        rating = self.parse_rating(rating)
                    text = review.get('review_text', '') or ''  # Boş string olarak garanti et
                    language = review.get('review_language', 'tr') or 'tr'  # None kontrolü
                    if not language or language == 'None':
                        language = 'tr'
                    review_photos = review.get('review_photos', [])
                    if not isinstance(review_photos, list):
                        review_photos = []
                    
                    # Tarih alanını bul (yeni API formatı)
                    published_at = None
                    # Önce review_datetime_utc string formatını dene
                    if 'review_datetime_utc' in review:
                        try:
                            published_at = dateutil_parser.parse(review['review_datetime_utc'])
                            if timezone.is_naive(published_at):
                                published_at = timezone.make_aware(published_at)
                        except Exception as e:
                            if verbosity >= 2:
                                self.stdout.write(self.style.WARNING(f'  ⚠️ Tarih parse edilemedi: {e}'))
                    # Eğer datetime_utc yoksa timestamp kullan
                    elif 'review_timestamp' in review:
                        try:
                            timestamp = review['review_timestamp']
                            if isinstance(timestamp, (int, float)):
                                published_at = timezone.make_aware(datetime.fromtimestamp(int(timestamp)))
                        except Exception as e:
                            if verbosity >= 2:
                                self.stdout.write(self.style.WARNING(f'  ⚠️ Timestamp parse edilemedi: {e}'))
                    
                    # Tarih yoksa şu anki zamanı kullan
                    if not published_at:
                        published_at = timezone.now()
                    
                    # Google'dan gelen review ID'si (unique identifier olarak kullan)
                    # review_id varsa onu kullan, yoksa business_id + author_name + timestamp kombinasyonu
                    if review_id:
                        google_id = f"{business_id}_{review_id}"
                    else:
                        google_id = f"{business_id}_{author_name}_{published_at.timestamp()}"

                    review_obj, created = GoogleReview.objects.update_or_create(
                        google_id=google_id,
                        defaults={
                            'author_name': author_name,
                            'author_url': author_url,
                            'profile_photo_url': profile_photo_url,
                            'rating': rating,
                            'text': text,
                            'published_at': published_at,
                            'language': language,
                            'review_photos': review_photos,
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            f'  ✓ Yeni yorum eklendi: {author_name} ({rating}⭐)'
                        )
                    else:
                        updated_count += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️ Yorum işlenirken hata: {str(e)}')
                    )
                    continue

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Senkronizasyon tamamlandı!\n'
                    f'  Yeni yorumlar: {created_count}\n'
                    f'  Güncellenen yorumlar: {updated_count}\n'
                    f'  Toplam yorumlar: {GoogleReview.objects.count()}'
                )
            )

        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'❌ API isteği başarısız: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Beklenmeyen hata: {str(e)}')
            )
