from raport_baza.models import ZleceniaRaport
from django.shortcuts import render
from tools.insert import insert_into_database
from datetime import datetime
# Create your views here.


def index1(request):
    return render(request, "index.html")


def index(request):
    obj = ZleceniaRaport.objects.all()
    context = {'obj': obj}
    return render(request, "index.html", context)


def _insert_into_db_view():
    insert_into_database()


def years_list(request):
    years_list = _list_of_years = list(range(2011, (datetime.now().year + 5)))
    return render(request, 'zlecenia_changelist.html', {'years_list': years_list})
