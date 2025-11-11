from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from mainapp.models import RoomCategory, RoomImage, RoomFeature
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Import existing room images from static folder to database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting room import...'))

        # Mevcut resimleri bir dizine organize et
        static_path = Path('static/img/rooms')

        # Oda kategorileri ve resimleri tanımla
        rooms_data = {
            'Superior Oda': {
                'name_en': 'Superior Room',
                'name_de': 'Superior Zimmer',
                'name_fr': 'Chambre Supérieure',
                'name_es': 'Habitación Superior',
                'name_ru': 'Люкс Superior',
                'name_ar': 'غرفة سوبيريور',
                'description_tr': 'Kapadokya manzaralı, özel teraslı lüks odalarımız',
                'description_en': 'Luxury rooms with Cappadocia views and private terrace',
                'description_de': 'Luxuszimmer mit Blick auf Kappadokien und privater Terrasse',
                'description_fr': 'Chambres luxueuses avec vue Cappadoce et terrasse privée',
                'description_es': 'Habitaciones de lujo con vistas a Capadocia y terraza privada',
                'description_ru': 'Люксовые номера с видом на Каппадокию и частной террасой',
                'description_ar': 'غرف فاخرة مع إطلالات على كابادوكيا وشرفة خاصة',
                'images': ['superior1.jpg', 'superior1.jpeg', 'superior2.jpeg', 'superior3.jpeg', 'superior4.jpeg', 'superior5.jpeg', 'superior6.jpeg', 'superior7.jpeg', 'superior8.jpeg', 'superior9.jpeg', 'superior10.jpeg'],
                'features': [
                    {'icon': 'fa-bed', 'text_tr': 'King Size Yatak', 'text_en': 'King Size Bed'},
                    {'icon': 'fa-bath', 'text_tr': 'Özel Tasarım Banyo', 'text_en': 'Designer Bathroom'},
                    {'icon': 'fa-tv', 'text_tr': 'Smart TV', 'text_en': 'Smart TV'},
                    {'icon': 'fa-wifi', 'text_tr': 'Ücretsiz Wi-Fi', 'text_en': 'Free Wi-Fi'},
                    {'icon': 'fa-mug-hot', 'text_tr': 'Mini Bar', 'text_en': 'Mini Bar'},
                    {'icon': 'fa-snowflake', 'text_tr': 'Klima', 'text_en': 'Air Conditioning'},
                ]
            },
            'King Suite': {
                'name_en': 'King Suite',
                'name_de': 'König Suite',
                'name_fr': 'Suite King',
                'name_es': 'Suite King',
                'name_ru': 'King Suite',
                'name_ar': 'King Suite',
                'description_tr': 'Tarihi atmosferde lüks deneyim ile geniş yaşam alanı',
                'description_en': 'Luxury experience in historic atmosphere with spacious living area',
                'description_de': 'Luxuserlebnis in historischer Atmosphäre mit großzügigem Wohnbereich',
                'description_fr': 'Expérience luxueuse dans une atmosphère historique avec grand espace de vie',
                'description_es': 'Experiencia de lujo en atmósfera histórica con amplia sala de estar',
                'description_ru': 'Люксовый опыт в исторической атмосфере с просторной гостиной',
                'description_ar': 'تجربة فاخرة في أجواء تاريخية مع مساحة معيشة واسعة',
                'images': ['kingsuite1.jpeg', 'kingsuite2.jpeg', 'kingsuite3.jpeg', 'kingsuite4.jpeg', 'kingsuite5.jpeg', 'kingsuite6.jpeg', 'kingsuite7.jpeg', 'kingsuite8.jpeg', 'kingsuite9.jpeg'],
                'features': [
                    {'icon': 'fa-bed', 'text_tr': 'King Size Yatak', 'text_en': 'King Size Bed'},
                    {'icon': 'fa-couch', 'text_tr': 'Oturma Alanı', 'text_en': 'Living Area'},
                    {'icon': 'fa-door-open', 'text_tr': 'Özel Teras', 'text_en': 'Private Terrace'},
                    {'icon': 'fa-water', 'text_tr': 'Jakuzili Banyo', 'text_en': 'Jacuzzi Bathroom'},
                    {'icon': 'fa-tv', 'text_tr': 'Smart TV', 'text_en': 'Smart TV'},
                    {'icon': 'fa-wifi', 'text_tr': 'Ücretsiz Wi-Fi', 'text_en': 'Free Wi-Fi'},
                ]
            },
            'Queen Oda': {
                'name_en': 'Queen Room',
                'name_de': 'Königin Zimmer',
                'name_fr': 'Chambre Queen',
                'name_es': 'Habitación Queen',
                'name_ru': 'Queen номер',
                'name_ar': 'غرفة Queen',
                'description_tr': 'Şık tasarımlı, konforlu odalarımız',
                'description_en': 'Elegantly designed and comfortable rooms',
                'description_de': 'Elegant gestaltete und komfortable Zimmer',
                'description_fr': 'Chambres élégamment conçues et confortables',
                'description_es': 'Habitaciones elegantemente diseñadas y cómodas',
                'description_ru': 'Элегантно оформленные и удобные номера',
                'description_ar': 'غرف مصممة بأناقة ومريحة',
                'images': ['queen1.jpeg', 'queen2.jpeg', 'queen3.jpeg', 'queen4.jpeg', 'queen5.jpeg', 'queen6.jpeg', 'queen7.jpeg', 'queen8.jpeg'],
                'features': [
                    {'icon': 'fa-bed', 'text_tr': 'Queen Size Yatak', 'text_en': 'Queen Size Bed'},
                    {'icon': 'fa-bath', 'text_tr': 'Şık Banyo', 'text_en': 'Stylish Bathroom'},
                    {'icon': 'fa-tv', 'text_tr': 'Flat Screen TV', 'text_en': 'Flat Screen TV'},
                    {'icon': 'fa-wifi', 'text_tr': 'Ücretsiz Wi-Fi', 'text_en': 'Free Wi-Fi'},
                ]
            },
            'Executive Oda': {
                'name_en': 'Executive Room',
                'name_de': 'Executive Zimmer',
                'name_fr': 'Chambre Executive',
                'name_es': 'Habitación Executive',
                'name_ru': 'Executive номер',
                'name_ar': 'غرفة Executive',
                'description_tr': 'İş seyahatleri için ideal, konforlu odalarımız',
                'description_en': 'Ideal for business travelers, comfortable rooms',
                'description_de': 'Ideal für Geschäftsreisende, komfortable Zimmer',
                'description_fr': 'Idéal pour les voyages d\'affaires, chambres confortables',
                'description_es': 'Ideal para viajeros de negocios, habitaciones cómodas',
                'description_ru': 'Идеально для деловых путешественников, удобные номера',
                'description_ar': 'مثالي لرجال الأعمال والغرف المريحة',
                'images': ['executive1.jpeg', 'executive2.jpeg', 'executive3.jpeg', 'executive4.jpeg', 'executive5.jpeg', 'executive6.jpeg'],
                'features': [
                    {'icon': 'fa-bed', 'text_tr': 'Queen Size Yatak', 'text_en': 'Queen Size Bed'},
                    {'icon': 'fa-briefcase', 'text_tr': 'Çalışma Alanı', 'text_en': 'Work Desk'},
                    {'icon': 'fa-tv', 'text_tr': 'Smart TV', 'text_en': 'Smart TV'},
                    {'icon': 'fa-wifi', 'text_tr': 'Hızlı Wi-Fi', 'text_en': 'High-Speed Wi-Fi'},
                ]
            },
            'Presidential Suite': {
                'name_en': 'Presidential Suite',
                'name_de': 'Präsidenten Suite',
                'name_fr': 'Suite Présidentielle',
                'name_es': 'Suite Presidencial',
                'name_ru': 'Президентский люкс',
                'name_ar': 'جناح رئاسي',
                'description_tr': 'En lüks ve geniş suit odamız',
                'description_en': 'Our most luxurious and spacious suite room',
                'description_de': 'Unser luxuriöstes und geräumigstes Suite-Zimmer',
                'description_fr': 'Notre suite la plus luxueuse et spacieuse',
                'description_es': 'Nuestra suite más lujosa y espaciosa',
                'description_ru': 'Наш самый роскошный и просторный номер люкс',
                'description_ar': 'أكثر أجنحتنا فخامة واتساعاً',
                'images': ['presidentialsuite1.jpeg', 'presidentialsuite2.jpeg', 'presidentialsuite3.jpeg'],
                'features': [
                    {'icon': 'fa-bed', 'text_tr': 'Çift King Size Yatak', 'text_en': 'Double King Size Beds'},
                    {'icon': 'fa-couch', 'text_tr': 'Geniş Oturma Alanı', 'text_en': 'Large Living Area'},
                    {'icon': 'fa-door-open', 'text_tr': 'Panoramik Teras', 'text_en': 'Panoramic Terrace'},
                    {'icon': 'fa-water', 'text_tr': 'Lüks Banyo', 'text_en': 'Luxury Bathroom'},
                ]
            },
            'Cave Honeymoon': {
                'name_en': 'Cave Honeymoon Suite',
                'name_de': 'Höhlen Flitterwochensuite',
                'name_fr': 'Suite Lune de Miel Grotte',
                'name_es': 'Suite Luna de Miel Cueva',
                'name_ru': 'Пещерный люкс медового месяца',
                'name_ar': 'جناح شهر العسل الكهفي',
                'description_tr': 'Balayı çiftleri için özel tasarlanmış suit odamız',
                'description_en': 'Specially designed suite room for honeymoon couples',
                'description_de': 'Speziell gestaltetes Zimmer für Flitterwochen-Paare',
                'description_fr': 'Suite spécialement conçue pour les couples en lune de miel',
                'description_es': 'Suite especialmente diseñada para parejas en luna de miel',
                'description_ru': 'Люкс специально разработан для молодоженов',
                'description_ar': 'جناح مصمم خصيصاً لأزواج شهر العسل',
                'images': ['CurveHoneymoon1.jpeg', 'CurveHoneymoon2.jpeg', 'CurveHoneymoon3.jpeg', 'CurveHoneymoon4.jpeg', 'CurveHoneymoon5.jpeg', 'CurveHoneymoon6.jpeg'],
                'features': [
                    {'icon': 'fa-bed', 'text_tr': 'King Size Yatak', 'text_en': 'King Size Bed'},
                    {'icon': 'fa-water', 'text_tr': 'Romantik Jacuzzi', 'text_en': 'Romantic Jacuzzi'},
                    {'icon': 'fa-door-open', 'text_tr': 'Teras', 'text_en': 'Terrace'},
                    {'icon': 'fa-fan', 'text_tr': 'Klima', 'text_en': 'Air Conditioning'},
                ]
            },
            'Türk Hamamlı Mağara Oda': {
                'name_en': 'Turkish Bath Cave Room',
                'name_de': 'Türkisches Bad Höhlenzimmer',
                'name_fr': 'Chambre Grotte Bain Turc',
                'name_es': 'Habitación Cueva Baño Turco',
                'name_ru': 'Пещерный номер с турецкой баней',
                'name_ar': 'غرفة كهفية بحمام تركي',
                'description_tr': 'Geleneksel Türk hamam deneyimi ile lüks konaklama',
                'description_en': 'Luxury accommodation with traditional Turkish bath experience',
                'description_de': 'Luxusunterkunft mit traditionellem türkischen Badet-Erlebnis',
                'description_fr': 'Hébergement de luxe avec expérience de bain turc traditionnel',
                'description_es': 'Alojamiento de lujo con experiencia de baño turco tradicional',
                'description_ru': 'Люксовое проживание с традиционным опытом турецкой бани',
                'description_ar': 'إقامة فاخرة مع تجربة الحمام التركي التقليدي',
                'images': ['turkishhamam1.jpeg', 'turkishhamam2.jpeg', 'turkishhamam3.jpeg', 'turkishhamam4.jpeg', 'turkishhamam5.jpeg', 'turkishhamam6.jpeg'],
                'features': [
                    {'icon': 'fa-bath', 'text_tr': 'Türk Hamamı', 'text_en': 'Turkish Bath'},
                    {'icon': 'fa-bed', 'text_tr': 'King Size Yatak', 'text_en': 'King Size Bed'},
                    {'icon': 'fa-water', 'text_tr': 'Masaj Duşu', 'text_en': 'Massage Shower'},
                    {'icon': 'fa-snowflake', 'text_tr': 'Klima', 'text_en': 'Air Conditioning'},
                ]
            },
        }

        display_order = 1
        for room_name, room_info in rooms_data.items():
            # Oda kategorisini oluştur
            room_category, created = RoomCategory.objects.get_or_create(
                name_tr=room_name,
                defaults={
                    'name_en': room_info['name_en'],
                    'name_de': room_info['name_de'],
                    'name_fr': room_info['name_fr'],
                    'name_es': room_info['name_es'],
                    'name_ru': room_info['name_ru'],
                    'name_ar': room_info['name_ar'],
                    'description_tr': room_info['description_tr'],
                    'description_en': room_info['description_en'],
                    'description_de': room_info['description_de'],
                    'description_fr': room_info['description_fr'],
                    'description_es': room_info['description_es'],
                    'description_ru': room_info['description_ru'],
                    'description_ar': room_info['description_ar'],
                    'display_order': display_order,
                    'is_active': True,
                }
            )
            display_order += 1

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Oda kategorisi oluşturuldu: {room_name}'))
            else:
                self.stdout.write(f'Oda zaten mevcut: {room_name}')

            # Resimleri ekle
            image_order = 1
            for image_file in room_info['images']:
                image_path = static_path / image_file

                if image_path.exists():
                    # Resim zaten database'de var mı kontrol et
                    if not room_category.images.filter(image__contains=image_file).exists():
                        try:
                            with open(image_path, 'rb') as f:
                                image_data = f.read()
                                room_image = RoomImage.objects.create(
                                    room_category=room_category,
                                    image=ContentFile(image_data, name=image_file),
                                    title=f'{room_name} - Resim {image_order}',
                                    alt_text=f'{room_name} odası resmi',
                                    is_featured=(image_order == 1),
                                    display_order=image_order
                                )
                                self.stdout.write(f'  └─ Resim eklendi: {image_file}')
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  └─ Hata: {image_file} - {str(e)}'))
                    image_order += 1

            # Özellikleri ekle
            feature_order = 1
            for feature in room_info['features']:
                feature_obj, feature_created = RoomFeature.objects.get_or_create(
                    room_category=room_category,
                    text_tr=feature['text_tr'],
                    defaults={
                        'icon': feature['icon'],
                        'text_en': feature['text_en'],
                        'text_de': feature['text_en'],  # Default olarak İngilizce kullan
                        'text_fr': feature['text_en'],
                        'text_es': feature['text_en'],
                        'text_ru': feature['text_en'],
                        'text_ar': feature['text_en'],
                        'display_order': feature_order
                    }
                )
                if feature_created:
                    self.stdout.write(f'  └─ Özellik eklendi: {feature["text_tr"]}')
                feature_order += 1

            self.stdout.write(self.style.SUCCESS(''))

        self.stdout.write(self.style.SUCCESS('✓ Import tamamlandı!'))
