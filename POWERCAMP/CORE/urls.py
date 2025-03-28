from django.contrib import admin
from django.urls import URLResolver, path


urlpatterns: list[URLResolver] = [
    path('admin/', admin.site.urls),
]
