from django.urls import path
from . import views

urlpatterns = [
    # path('raport_baza/zleceniaraport/', years_list1),
    path('update/', views.years_list1)
]