from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

# ... existing imports and urlpatterns ...

urlpatterns += [
    path('sitemap.xml', cache_page(86400)(TemplateView.as_view(
        template_name='sitemap.xml',
        content_type='application/xml'
    )), name='sitemap'),
] 