from raport_baza.models import ZleceniaRaport
from django.shortcuts import render
from tools.insert import insert_into_database
from datetime import datetime
from django import template

# Create your views here.


def index1(request):
    return render(request, "index.html")


def index(request):
    obj = ZleceniaRaport.objects.all()
    context = {'obj': obj}
    return render(request, "index.html", context)


def _insert_into_db_view(month, year):
    insert_into_database(month, year)


def years_list(request):
    years_list = _list_of_years = list(range(2011, datetime.now().year))
    return render(request, template_name="zlecenia_changelist.html", context={'years_list': years_list})


def years_list1(request):

    months_dict = {1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec', 8: 'Sierpień', 9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'}

    years_list = list(range(2011, datetime.now().year))

    context = {'years_list': years_list,
               'months_dict': months_dict}

    return render(
        request=request,
        template_name="import_rows.html",
        context=context)

