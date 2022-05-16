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


def years_list(request):
    years_list = _list_of_years = list(range(2011, datetime.now().year))
    return render(request, template_name="zlecenia_changelist.html", context={'years_list': years_list})


def select_month_and_year_view(request):

    months_dict = {1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec', 8: 'Sierpień', 9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'}

    years_list = list(range(2011, datetime.now().year))

    context = {'years_list': years_list,
               'months_dict': months_dict}

    return render(
        request=request,
        template_name="import_rows.html",
        context=context)


def get_year(request):
    answer = request.GET['year_dropdown']
    return answer


def get_month(request):
    answer = request.GET['month_dropdown']
    return answer


def insert_into_db_view(request):

    month = request.GET['month_dropdown']
    year = request.GET['year_dropdown']
    insert_into_database(month, year)
