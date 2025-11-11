from django.core.management.base import BaseCommand
from django.utils import timezone
from mainapp.models import GoogleReview
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Load sample Google reviews for testing (without API key)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📝 Örnek Google yorumları yükleniyor...'))

        # Örnek yorumlar
        sample_reviews = [
            {
                'author_name': 'Mehmet Kaplan',
                'rating': 5,
                'text': 'Harika bir konaklama deneyimi! Odalar çok temiz ve güzel dekorasyonu var. Personel çok yardımcı ve dostça. Cappadocia\'nın mağara oteli arasında en iyisi bence. Kesinlikle tavsiye ederim!',
                'days_ago': 5
            },
            {
                'author_name': 'Sarah Johnson',
                'rating': 5,
                'text': 'Amazing cave hotel! The views from the terrace are incredible. The room is spacious and luxurious. The staff is very attentive and helpful. We had breakfast on the terrace and it was perfect. Highly recommended!',
                'days_ago': 15
            },
            {
                'author_name': 'Emma Schmidt',
                'rating': 5,
                'text': 'Ein wunderbar gelegenes Höhlenhotel mit fantastischer Aussicht. Die Zimmer sind geschmackvoll eingerichtet und sehr komfortabel. Das Personal ist freundlich und zuvorkommend. Wir haben unsere Zeit hier sehr genossen!',
                'days_ago': 25
            },
            {
                'author_name': 'Sophie Laurent',
                'rating': 5,
                'text': 'Un séjour merveilleux dans ce magnifique hôtel troglodyte! Les chambres sont spacieuses et bien équipées. La vue sur les cheminées de fées est spectaculaire. Le service est excellent et le personnel très attentionné.',
                'days_ago': 30
            },
            {
                'author_name': 'Juan Garcia',
                'rating': 4,
                'text': 'Excelente hotel cueva con una ubicación fantástica en Cappadocia. Las habitaciones son muy bonitas y cómodas. El personal es amable y servicial. La única pequeña pega es que el wifi podría ser más fuerte.',
                'days_ago': 40
            },
            {
                'author_name': 'Yuki Tanaka',
                'rating': 5,
                'text': 'Patina Cappadociaは素晴らしいホテルです。洞窟の部屋は快適で素敵に装飾されています。スタッフは非常に親切で親切です。Cappadociaの最高の経験をしました。',
                'days_ago': 45
            },
            {
                'author_name': 'Natasha Petrov',
                'rating': 5,
                'text': 'Отличный пещерный отель с потрясающим видом! Номера просторные и современные. Персонал очень внимательный и гостеприимный. Рекомендую всем, кто хочет посетить Каппадокию!',
                'days_ago': 50
            },
            {
                'author_name': 'فاطمة علي',
                'rating': 5,
                'text': 'فندق رائع جداً! الغرف جميلة جداً وواسعة ومريحة. الموظفون لطيفون جداً وخدمتهم ممتازة. المنظر من الشرفة رائع جداً. سأعود مرة أخرى بالتأكيد!',
                'days_ago': 60
            },
            {
                'author_name': 'Cem Yıldırım',
                'rating': 5,
                'text': 'Cappadocia\'da yaşadığımız en güzel deneyimlerden biri. Otelin tasarımı, konumu ve hizmet kalitesi enfes. Jacuzzi\'li odalar çok rahat. Kahvaltı berbat değildi! Tekrar geleceğiz!',
                'days_ago': 70
            },
            {
                'author_name': 'Maria Santos',
                'rating': 4,
                'text': 'Lovely cave hotel with beautiful decorations. The rooms are clean and comfortable. The view is amazing. The only thing is that the Wi-Fi can be a bit slow sometimes, but overall a great experience.',
                'days_ago': 80
            },
        ]

        created_count = 0
        for review in sample_reviews:
            try:
                published_at = timezone.now() - timedelta(days=review['days_ago'])

                review_obj, created = GoogleReview.objects.update_or_create(
                    google_id=f"sample_{review['author_name'].replace(' ', '_')}",
                    defaults={
                        'author_name': review['author_name'],
                        'rating': review['rating'],
                        'text': review['text'],
                        'published_at': published_at,
                        'language': 'tr',
                        'author_url': 'https://www.google.com',
                        'profile_photo_url': '',
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        f'  ✓ {review["author_name"]} ({review["rating"]}⭐)'
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️ Hata: {review["author_name"]} - {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ {created_count} örnek yorum yüklendi!\n'
                f'  Toplam yorumlar: {GoogleReview.objects.count()}'
            )
        )
