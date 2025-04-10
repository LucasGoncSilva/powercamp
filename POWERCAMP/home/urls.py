from typing import Final

from django.urls import URLPattern, path

from home.views import landpage


app_name: Final[str] = 'home'

urlpatterns: list[URLPattern] = [path('', landpage, name='landpage')]
