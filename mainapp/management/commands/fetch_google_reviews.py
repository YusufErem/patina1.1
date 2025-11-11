from django.core.management.base import BaseCommand
from django.utils import timezone
from mainapp.models import GoogleReview
import os
import requests
from datetime import datetime
from dateutil import parser as dateutil_parser

class Command(BaseCommand):
    help = 'Fetch Google reviews from Google Places API and cache them in database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--place-id',
            type=str,
            default='ChIJIxzgoXFpKhURSRlfATWSfBs',
            help='Google Place ID (default: Patina Cappadocia)'
        )
        parser.add_argument(
            '--api-key',
            type=str,
            default=None,
            help='Google Places API Key (or set GOOGLE_PLACES_API_KEY env variable)'
        )

    def handle(self, *args, **options):
        place_id = options['place_id']
        api_key = options['api_key'] or os.environ.get('GOOGLE_PLACES_API_KEY')

        if not api_key:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Google Places API key bulunamadı!\n'
                    'Lütfen GOOGLE_PLACES_API_KEY environment variable\'ını ayarla\n'
                    'veya --api-key parametresi ile geç'
                )
            )
            return

        self.stdout.write(self.style.SUCCESS(f'🔄 Google Reviews çekiliyor... (Place ID: {place_id})'))

        try:
            # Google Places API'den veri çek
            url = 'https://maps.googleapis.com/maps/api/place/details/json'
            params = {
                'place_id': place_id,
                'fields': 'reviews,rating,user_ratings_total',
                'key': api_key
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data['status'] != 'OK':
                self.stdout.write(
                    self.style.ERROR(f'❌ API Hatası: {data.get("error_message", "Bilinmeyen hata")}')
                )
                return

            place_data = data.get('result', {})
            reviews = place_data.get('reviews', [])

            if not reviews:
                self.stdout.write(self.style.WARNING('⚠️ Hiç yorum bulunamadı'))
                return

            self.stdout.write(self.style.SUCCESS(f'✓ {len(reviews)} yorum bulundu'))

            # Veritabanına kaydet
            created_count = 0
            updated_count = 0

            for review in reviews:
                try:
                    # Google'dan gelen review ID'si (unique identifier olarak kullan)
                    google_id = f"{place_id}_{review['time']}"

                    # Review tarihini parse et
                    published_at = timezone.make_aware(
                        datetime.fromtimestamp(int(review['time']))
                    )

                    review_obj, created = GoogleReview.objects.update_or_create(
                        google_id=google_id,
                        defaults={
                            'author_name': review.get('author_name', 'Anonymous'),
                            'author_url': review.get('author_url', ''),
                            'profile_photo_url': review.get('profile_photo_url', ''),
                            'rating': review.get('rating', 5),
                            'text': review.get('text', ''),
                            'published_at': published_at,
                            'language': review.get('language', 'tr'),
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            f'  ✓ Yeni yorum eklendi: {review.get("author_name", "Anonymous")} ({review.get("rating")}⭐)'
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
