from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# This file remains minimal - URL configuration is in patina_cappadocia/urls.py
# Include all URL patterns from the main Django app

urlpatterns = [
    path('', include('patina_cappadocia.urls')),
]

# Serve media files in development mode
# In production, Whitenoise handles both static and media files via WHITENOISE_MEDIA_ROOTS
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 