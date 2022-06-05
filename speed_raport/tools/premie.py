from tools.connect import get_raport_baza_engine
import pandas as pd

engine = get_raport_baza_engine()


def get_zlecenia():
    zlecenia_query = 'SELECT * FROM "zlecenia_raport"'

    zlecenia_df = pd.read_sql_query(zlecenia_query, con=engine)
    return zlecenia_df[['id', 'SPEDYTOR', 'OPIEKUN', 'SALDO_NETTO']]


def create_premie():
    osoby_query = 'SELECT * FROM "spedytorzy_osoby"'
    osoby_procenty = pd.read_sql_query(osoby_query, con=engine)
    print(osoby_procenty[['id', 'osoba', 'premia_procent']])

    zlecenia_df = get_zlecenia()
    premie = pd.DataFrame(columns=['zlecenie', 'spedytor' 'kwota_premii'])
    for zlec in zlecenia_df.to_dict(orient="records"):
        zlec_id = zlec['id']
        osoba = zlec['SPEDYTOR']
        # print('osoba', osoba)
        procent = int(osoby_procenty.loc[osoby_procenty['osoba'] == osoba, 'premia_procent'])
        print('spedytor_procent', procent)
        saldo = zlec['SALDO_NETTO']
        premia = zlec['SALDO_NETTO'] * procent/100
        print(zlec_id, osoba, procent, saldo, premia)
