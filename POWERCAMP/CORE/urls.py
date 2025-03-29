from django.contrib import admin
from django.urls import URLResolver, include, path


urlpatterns: list[URLResolver] = [
    # Admin
    path('admin/', admin.site.urls),
    # App
    path('', include('home.urls')),
    path('hall/', include('hall.urls')),
    path('equipes', include('teams.urls')),
]
