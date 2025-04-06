from os import getenv

from django.conf import settings
from django.conf.urls.static import static
from django.urls import URLPattern, URLResolver, include, path

from CORE.admin import adm


urlpatterns: list[URLResolver | URLPattern] = [
    # Admin
    path('admin/', adm.urls),
    # App
    path('', include('home.urls')),
    path('hall/', include('hall.urls')),
    path('equipes', include('teams.urls')),
]

if getenv('DJANGO_SETTINGS_MODULE') == 'CORE.settings.dev':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
