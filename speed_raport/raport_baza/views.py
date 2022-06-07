from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from tools.insert import insert_into_database
from tools.insert_osoby import update_osoby
from tools.premie import create_premie
from raport_baza.models import SpedytorzyPremie
from datetime import datetime
from django import template

# Create your views here.


def drop_parallel_premie(zlecenie_id='99bf2ada-2b97-42f4-8e4c-d0d85585e6db'):
    print('click!')
    objects = SpedytorzyPremie.objects.get(zlecenie_id=zlecenie_id)
    print(objects)
    HttpResponseRedirect('/admin/raport_baza/spedytorzypremie/')


def upadate_osoby(request):
    update_osoby()
    return HttpResponseRedirect('/admin/raport_baza/spedytorzyosoby/')


def calculate_premie(request):
    create_premie()
    return HttpResponseRedirect('/admin/raport_baza/zleceniaraport/')


def index_redundant(request):
    return render(request, "index.html")


def index():
    return redirect('/admin/')


def select_month_and_year_view(request):

    months_dict = {1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec',
                   8: 'Sierpień', 9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'}
    year_now = datetime.now().year
    month_now = datetime.now().month
    years_list = reversed(list(range(2019, (year_now + 1))))

    context = {'years_list': years_list,
               'months_dict': months_dict,
               'month_now': month_now}

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
    return HttpResponseRedirect('/admin/raport_baza/zleceniaraport/')
