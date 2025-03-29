from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(r: HttpRequest) -> HttpResponse:
    return render(r, 'home/index.html')
