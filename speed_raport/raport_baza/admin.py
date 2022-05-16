from django.contrib import admin
from .models import ZleceniaRaport
from django.shortcuts import render
from datetime import datetime
# Register your models here.

#


# @admin.register(ZleceniaRaport)
class ZleceniaAdmin(admin.ModelAdmin):
    list_display = ['id', 'field_timestamp', 'nr_zlecenia', 'spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    list_display_links = ['nr_zlecenia']
    list_editable = ['spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    list_filter = ('spedytor', 'opiekun', 'opis', 'za_data')
    ordering = ('field_timestamp', 'nr_zlecenia',)
    search_fields = ('id', 'nr_zlecenia', 'spedytor', 'opiekun', )
    list_per_page = 10
    change_list_template = "zlecenia_changelist.html"


admin.site.register(ZleceniaRaport, ZleceniaAdmin)

# year_dropdown = []
# for y in range(2011, (datetime.now().year + 5)):
#     year_dropdown.append((y, y))


