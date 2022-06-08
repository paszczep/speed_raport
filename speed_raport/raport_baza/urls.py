from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('update/', views.select_month_and_year_view, name='select_date'),
    path('update/do_insert/', views.insert_into_db_view, name='insert_view'),
    path('update/premie/', views.calculate_premie, name='calculate_premie'),
    path('update/osoby', views.upadate_osoby, name='update_osoby')
]
