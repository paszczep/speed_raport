from django.contrib import admin
from .models import ZleceniaRaport
# Register your models here.

# admin.site.register(ZleceniaRaport)


@admin.register(ZleceniaRaport)
class ZleceniaAdmin(admin.ModelAdmin):
    list_display = ('field_timestamp', 'nr_zlecenia', 'spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto')
    ordering = ('field_timestamp', 'nr_zlecenia',)
    search_fields = ('nr_zlecenia', 'spedytor', 'opiekun',)