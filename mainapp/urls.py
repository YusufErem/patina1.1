from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(_('iletisim/'), views.contact, name='contact'),
    path(_('hakkimizda/'), views.about, name='about'),
    path(_('odalar/'), views.rooms, name='rooms'),
]