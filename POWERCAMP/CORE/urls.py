from django.urls import URLResolver, include, path

from CORE.admin import adm


urlpatterns: list[URLResolver] = [
    # Admin
    path('admin/', adm.urls),
    # App
    path('', include('home.urls')),
    path('hall/', include('hall.urls')),
    path('equipes', include('teams.urls')),
]
