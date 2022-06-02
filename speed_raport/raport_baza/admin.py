from django.contrib import admin
from .models import ZleceniaRaport, SpedytorzyPremie, SpedytorzyOsoby, ZleceniaHistoria
# from django.shortcuts import render
# from datetime import datetime
# Register your models here.


@admin.register(SpedytorzyPremie)
class PremieAdmin(admin.ModelAdmin):
    # ['id', 'add_date', 'id_zlecenia', 'id_spedytor', 'spedytor', 'kwota_premii', 'nr_zlecenia']
    list_display = ['add_date', 'id_zlecenia', 'spedytor', 'kwota_premii']
    list_display_links = list_display
    list_filter = ('spedytor', )
    ordering = ('add_date', 'spedytor', 'kwota_premii',)
    search_fields = ('spedytor', 'id_zlecenia')
    raw_id_fields = ('id_zlecenia',)
    list_per_page = 10


@admin.register(SpedytorzyOsoby)
class OsobyAdmin(admin.ModelAdmin):
    list_display = ['spedytor']
    list_display_links = ['spedytor']
    list_filter = ('spedytor',)
    ordering = ('spedytor',)
    search_fields = ('spedytor',)
    list_per_page = 50


# @admin.register(ZleceniaRaport)
class ZleceniaAdmin(admin.ModelAdmin):
    list_display = ['field_timestamp', 'nr_zlecenia', 'spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    # list_editable = ['spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    list_filter = ('field_timestamp', 'spedytor', 'opiekun', 'opis', 'za_data')
    ordering = ('field_timestamp', 'nr_zlecenia',)
    search_fields = (
        # '_id',
        'nr_zlecenia', 'spedytor', 'opiekun', )
    list_per_page = 5
    # change_list_template = "zlecenia_changelist.html"


class ZleceniaRaportAdmin(ZleceniaAdmin):
    readonly_fields = (
        # '_id',
        'field_timestamp', )
    list_display_links = ['nr_zlecenia']
    change_list_template = "zlecenia_changelist.html"


class ZleceniaHistoriaAdmin(ZleceniaAdmin):

    readonly_fields = ['field_timestamp', 'nr_zlecenia', 'spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    list_display = ['created'] + readonly_fields

    class Meta:
        verbose_name = 'Zlecenie historia'
        verbose_name_plural = 'Zlecenia historia'


admin.site.register(ZleceniaRaport, ZleceniaRaportAdmin)
admin.site.register(ZleceniaHistoria, ZleceniaHistoriaAdmin)
