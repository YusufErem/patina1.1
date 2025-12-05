"""
URL configuration for patina_cappadocia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.middleware.csrf import get_token
from django.utils import translation
from django.http import HttpResponse, FileResponse
from django.views.decorators.cache import cache_page
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.static import serve
import os

@cache_page(60 * 15)  # Cache for 15 minutes
def sitemap_view(request):
    response = render(request, 'sitemap.xml', {
        'request': request,
    })
    response['Content-Type'] = 'application/xml; charset=utf-8'
    return response

def custom_404(request, exception=None):
    # Ensure CSRF token is generated
    get_token(request)
    
    # Get current language
    current_language = translation.get_language()
    
    return render(request, '404.html', {
        'LANGUAGE_CODE': current_language,
    }, status=404)

def custom_500(request, exception=None):
    # Ensure CSRF token is generated
    get_token(request)
    
    # Get current language
    current_language = translation.get_language()
    
    return render(request, '404.html', {
        'LANGUAGE_CODE': current_language,
    }, status=500)

# Favicon view - serve patina_logo.png
def favicon_view(request):
    from django.contrib.staticfiles import finders
    from django.http import HttpResponse
    
    # Force serve patina_logo.png as favicon
    logo_path = finders.find('img/patina_logo.png')
    if logo_path:
        with open(logo_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            # Cache for 1 year
            response['Cache-Control'] = 'public, max-age=31536000'
            return response
            
    # Last resort: return 404
    from django.http import HttpResponseNotFound
    return HttpResponseNotFound()

# Temel URL desenleri
# Admin paneli kapalı (güvenlik için)
urlpatterns = [
    # Admin paneli devre dışı - güvenlik için
    # path('patina-secret-admin-2024/', admin.site.urls),  # Admin kapalı
    path('favicon.ico', favicon_view, name='favicon'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap_view, name='sitemap'),
]

# Static ve media dosyaları için development modunda
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Çoklu dil desteği için URL desenleri
urlpatterns += i18n_patterns(
    path('', include('mainapp.urls')),
    prefix_default_language=True,
)

# Error handlers
handler404 = 'patina_cappadocia.urls.custom_404'
handler500 = 'patina_cappadocia.urls.custom_500'
