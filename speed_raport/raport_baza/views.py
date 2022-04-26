from raport_baza.models import ZleceniaRaport
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


# Create your views here.

def index1(request):
    return render(request, "index.html")


def index(request):
    obj = ZleceniaRaport.objects.all()
    context = {'obj': obj}
    return render(request, "index.html", context)


class RaportView(ListView):
    model = ZleceniaRaport
    template_name = 'raport.html'