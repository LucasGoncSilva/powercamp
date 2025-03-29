from typing import Final

from django.urls import URLPattern, path

from hall.views import index


app_name: Final[str] = 'hall'

urlpatterns: list[URLPattern] = [path('', index, name='index')]
