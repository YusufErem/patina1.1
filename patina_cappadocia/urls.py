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

# Temel URL desenleri
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
]

# Statik dosyalar için URL desenleri
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Çoklu dil desteği için URL desenleri
urlpatterns += i18n_patterns(
    path('', include('mainapp.urls')),
    prefix_default_language=True,
)

# Error handlers
handler404 = 'patina_cappadocia.urls.custom_404'
handler500 = 'patina_cappadocia.urls.custom_500'
