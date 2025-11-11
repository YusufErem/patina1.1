from django.core.management.base import BaseCommand
from mainapp.models import HomePageImage, AboutSection
from django.core.files.base import ContentFile
from PIL import Image
import io


class Command(BaseCommand):
    help = 'Load sample homepage images and about sections for testing'

    def create_test_image(self, width=800, height=600, color='#FF6B6B', text='Test Image'):
        """Create a simple test image programmatically"""
        img = Image.new('RGB', (width, height), color)
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        return ContentFile(img_io.getvalue(), name=f'test_{width}x{height}.jpg')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📸 Örnek içerik yükleniyor...\n'))

        # Create sample HomePage images for slider
        slider_images = [
            {
                'section': 'slider',
                'title': 'Kapadokya Manzarası',
                'caption': 'Eşsiz balonlar ve peri bacaları',
                'display_order': 1,
                'is_active': True,
            },
            {
                'section': 'slider',
                'title': 'Gün Batımı',
                'caption': 'Kapadokya\'da unutulmaz güneş batımı',
                'display_order': 2,
                'is_active': True,
            },
            {
                'section': 'slider',
                'title': 'Otel Binası',
                'caption': 'Modern tasarım ve eski mimarinin birleşimi',
                'display_order': 3,
                'is_active': True,
            },
        ]

        slider_count = 0
        for slider in slider_images:
            try:
                img = HomePageImage.objects.get_or_create(
                    section=slider['section'],
                    title=slider['title'],
                    defaults={
                        'caption': slider['caption'],
                        'display_order': slider['display_order'],
                        'is_active': slider['is_active'],
                        'image': self.create_test_image(1920, 600, '#3498db', slider['title']),
                    }
                )
                if img[1]:
                    slider_count += 1
                    self.stdout.write(f"  ✓ Slider resmi eklendi: {slider['title']}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ⚠️ Hata: {slider['title']} - {str(e)}"))

        # Create sample About sections
        about_sections = [
            {
                'title_tr': 'Patina Cappadocia Hakkında',
                'title_en': 'About Patina Cappadocia',
                'title_de': 'Über Patina Kappadokien',
                'title_fr': 'À propos de Patina Cappadocia',
                'title_es': 'Acerca de Patina Capadocia',
                'title_ru': 'О Patina Cappadocia',
                'title_ar': 'حول Patina Cappadocia',
                'content_tr': 'Uçhisar\'ın büyüleyici manzaraları içerisinde yer alan Patina Kapadokya, geleneksel dokuyu ve modern lüksü mükemmel bir uyumla bir araya getiriyor. Taş işçiliğiyle inşa edilen mimarimiz, bölgenin zengin kültürel mirasını yansıtırken, sunduğumuz çağdaş imkanlar size konforlu bir konaklama deneyimi yaşatıyor.',
                'content_en': 'Located within the enchanting landscapes of Üchisar, Patina Cappadocia brings together traditional texture and modern luxury in perfect harmony. Our stone-carved architecture reflects the region\'s rich cultural heritage, while our contemporary facilities provide you with a comfortable stay experience.',
                'content_de': 'Im faszinierenden Panorama von Üchisar gelegen, vereint Patina Kappadokien traditionelle Struktur und modernen Luxus in perfekter Harmonie. Unsere aus Stein erbaute Architektur spiegelt das reiche Kulturerbe der Region wider, während unsere modernen Einrichtungen Ihnen ein komfortables Aufenthaltserleben bieten.',
                'content_fr': 'Situé dans les paysages enchanteurs d\'Üchisar, Patina Cappadocia allie la texture traditionnelle et le luxe moderne dans une harmonie parfaite. Notre architecture en pierre sculptée reflète le riche patrimoine culturel de la région, tandis que nos installations modernes vous offrent une expérience de séjour confortable.',
                'content_es': 'Ubicado en los paisajes cautivadores de Üchisar, Patina Capadocia reúne la textura tradicional y el lujo moderno en armonía perfecta. Nuestra arquitectura tallada en piedra refleja el rico patrimonio cultural de la región, mientras que nuestras instalaciones contemporáneas le proporcionan una experiencia de hospedaje cómoda.',
                'content_ru': 'Расположенный в очаровательных пейзажах Юхисара, Patina Cappadocia сочетает традиционную структуру и современный роскошь в идеальной гармонии. Наша высеченная из камня архитектура отражает богатое культурное наследие региона, а наши современные удобства обеспечивают вам комфортное проживание.',
                'content_ar': 'يقع Patina Cappadocia في المناظر الطبيعية الساحرة لأوتشيسار ، ويجمع بين النسيج التقليدي والفخامة الحديثة بتناغم مثالي. تعكس عمارتنا المنحوتة من الحجر التراث الثقافي الغني للمنطقة ، بينما توفر لنا المرافق المعاصرة تجربة إقامة مريحة.',
                'image_position': 'left',
                'display_order': 1,
                'is_active': True,
            },
            {
                'title_tr': 'Konfor ve Hizmet',
                'title_en': 'Comfort and Service',
                'title_de': 'Komfort und Service',
                'title_fr': 'Confort et Service',
                'title_es': 'Comodidad y Servicio',
                'title_ru': 'Комфорт и Сервис',
                'title_ar': 'الراحة والخدمة',
                'content_tr': 'Her odamız benzersiz tasarımı, lüks konforuyla ve modern teknolojisiyle misafirlerimize ihtişamlı bir deneyim sunmaktadır. Başarılı arkadaşlık ve aile değerleri önceleyen anlayışımız, tüm ziyaretçilerimiz için hatırlanacak anılar yaratır.',
                'content_en': 'Each of our rooms offers our guests a magnificent experience with its unique design, luxurious comfort and modern technology. Our understanding that values successful companionship and family values creates memorable moments for all our visitors.',
                'content_de': 'Jedes unserer Zimmer bietet unseren Gästen mit seinem einzigartigen Design, luxuriösem Komfort und moderner Technologie ein großartiges Erlebnis. Unser Verständnis, das erfolgreiche Kameradschaft und Familienwerte schätzt, schafft unvergessliche Momente für alle unsere Besucher.',
                'content_fr': 'Chacune de nos chambres offre à nos clients une expérience magnifique avec sa conception unique, son confort luxueux et sa technologie moderne. Notre compréhension qui valorise la camaraderie réussie et les valeurs familiales crée des moments mémorables pour tous nos visiteurs.',
                'content_es': 'Cada una de nuestras habitaciones ofrece a nuestros huéspedes una experiencia magnífica con su diseño único, comodidad lujosa y tecnología moderna. Nuestra comprensión que valora la camaradería exitosa y los valores familiares crea momentos memorables para todos nuestros visitantes.',
                'content_ru': 'Каждый из наших номеров предлагает нашим гостям великолепный опыт благодаря его уникальному дизайну, роскошному комфорту и современным технологиям. Наше понимание, которое ценит успешное товарищество и семейные ценности, создает незабываемые моменты для всех наших посетителей.',
                'content_ar': 'تقدم كل غرفة من غرفنا لضيوفنا تجربة رائعة مع تصميمها الفريد والراحة الفاخرة والتكنولوجيا الحديثة. يخلق فهمنا الذي يقدر الرفقة الناجحة والقيم العائلية لحظات لا تُنسى لجميع زوارنا.',
                'image_position': 'right',
                'display_order': 2,
                'is_active': True,
            },
        ]

        about_count = 0
        for section in about_sections:
            try:
                about, created = AboutSection.objects.get_or_create(
                    title_tr=section['title_tr'],
                    defaults={
                        'title_en': section['title_en'],
                        'title_de': section['title_de'],
                        'title_fr': section['title_fr'],
                        'title_es': section['title_es'],
                        'title_ru': section['title_ru'],
                        'title_ar': section['title_ar'],
                        'content_tr': section['content_tr'],
                        'content_en': section['content_en'],
                        'content_de': section['content_de'],
                        'content_fr': section['content_fr'],
                        'content_es': section['content_es'],
                        'content_ru': section['content_ru'],
                        'content_ar': section['content_ar'],
                        'image': self.create_test_image(600, 400, '#2ecc71', section['title_tr']),
                        'image_position': section['image_position'],
                        'display_order': section['display_order'],
                        'is_active': section['is_active'],
                    }
                )
                if created:
                    about_count += 1
                    self.stdout.write(f"  ✓ About bölümü eklendi: {section['title_tr']}")
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ⚠️ Hata: {section['title_tr']} - {str(e)}"))

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Örnek içerik yükleme tamamlandı!\n'
                f'  Slider resimleri: {slider_count}\n'
                f'  About bölümleri: {about_count}\n'
                f'  Toplam HomePage resimleri: {HomePageImage.objects.count()}\n'
                f'  Toplam About bölümleri: {AboutSection.objects.count()}'
            )
        )
