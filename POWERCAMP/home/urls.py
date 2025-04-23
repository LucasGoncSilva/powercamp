from typing import Final

from django.urls import URLPattern, path

from home.views import event_form, landpage


app_name: Final[str] = 'home'

urlpatterns: list[URLPattern] = [
    path('', landpage, name='landpage'),
    path('participar', event_form, name='event-form'),
]
