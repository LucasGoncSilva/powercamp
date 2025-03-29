from typing import Final

from django.urls import URLPattern, path

from teams.views import index


app_name: Final[str] = 'teams'

urlpatterns: list[URLPattern] = [path('', index, name='index')]
