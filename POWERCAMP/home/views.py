from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landpage(r: HttpRequest) -> HttpResponse:
    return render(r, 'home/landpage.html')
