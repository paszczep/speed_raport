from django.contrib import admin
from .models import ZleceniaRaport, SpedytorzyPremie, SpedytorzyOsoby, ZleceniaHistoria


@admin.register(SpedytorzyPremie)
class PremieAdmin(admin.ModelAdmin):
    # ['id', 'add_date', 'id_zlecenia', 'id_spedytor', 'spedytor', 'kwota_premii', 'nr_zlecenia']
    list_display = ['add_date', 'zlecenie', 'spedytor', 'kwota_premii']
    list_display_links = ['add_date', 'zlecenie', 'spedytor']
    list_filter = ('spedytor', )
    ordering = list_display
    search_fields = ('spedytor__osoba', 'zlecenie__nr_zlecenia')
    # raw_id_fields = ('zlecenie',)
    list_per_page = 10
    change_list_template = 'premie_changelist.html'


@admin.register(SpedytorzyOsoby)
class OsobyAdmin(admin.ModelAdmin):
    list_display = ['osoba', 'premia_procent']
    list_display_links = ['osoba']
    list_filter = ('osoba',)
    ordering = ('osoba', 'premia_procent')
    search_fields = ('osoba',)
    list_per_page = 50
    change_list_template = 'osoby_changelist.html'


# @admin.register(ZleceniaRaport)
class ZleceniaAdmin(admin.ModelAdmin):
    list_display = ['field_timestamp', 'nr_zlecenia', 'spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    list_filter = ('field_timestamp', 'spedytor', 'opiekun', 'opis', 'za_data')
    ordering = ('field_timestamp', 'nr_zlecenia',)
    search_fields = (
        'nr_zlecenia', 'spedytor', 'opiekun', )
    list_per_page = 5


class ZleceniaRaportAdmin(ZleceniaAdmin):
    readonly_fields = (
        'id',
        'field_timestamp',
        'nr_zlecenia'
    )
    list_display_links = ['nr_zlecenia']
    change_list_template = "zlecenia_changelist.html"


class ZleceniaHistoriaAdmin(ZleceniaAdmin):
    _fields = ['field_timestamp', 'nr_zlecenia', 'spedytor', 'opiekun', 'za_miejsce', 'za_data', 'wy_data', 'wy_miejsce', 'wy_miasto', 'wy_kraj', 'wy_kod', 'za_miasto', 'za_kraj', 'za_kod', 'trasa', 'opis', 'informacje', 'data_wystawienia_koszt', 'data_platnosci_koszt', 'data_wystawienia_przych', 'data_platnosci_przych', 'netto_pln_przych', 'netto_pln_koszt', 'noty_netto_pln', 'saldo_netto']
    readonly_fields = _fields + ['id']
    list_display = ['created'] + _fields

    class Meta:
        verbose_name = 'Zlecenie historia'
        verbose_name_plural = 'Zlecenia historia'


admin.site.register(ZleceniaRaport, ZleceniaRaportAdmin)
admin.site.register(ZleceniaHistoria, ZleceniaHistoriaAdmin)
