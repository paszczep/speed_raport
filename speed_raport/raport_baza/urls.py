from django.urls import path
from . import views

urlpatterns = [
    # path('raport_baza/zleceniaraport/', years_list1),
    path('', views.index),
    path('update/', views.select_month_and_year_view, name='select_date'),
    path('update/do_insert/', views.insert_into_db_view, name='insert_view')
]
