import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patina_cappadocia.settings')

django_application = get_wsgi_application()

# Wrap the Django application with WhiteNoise for static and media file serving
application = WhiteNoise(
    django_application,
    root=settings.STATIC_ROOT,
    mimetypes=getattr(settings, 'WHITENOISE_MIMETYPES', {}),
)

# Add media roots to WhiteNoise for serving user-uploaded files
if hasattr(settings, 'WHITENOISE_MEDIA_ROOTS'):
    for media_root in settings.WHITENOISE_MEDIA_ROOTS:
        application.add_files(media_root, prefix='media/')