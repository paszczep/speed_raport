from django.shortcuts import render
from speed_raport.raport_baza.models import ZleceniaRaport
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.
