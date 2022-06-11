from tools.connect import get_raport_baza_engine
import pandas as pd
from datetime import datetime

engine = get_raport_baza_engine()


def get_zlecenia(existing_ids_list):
    existing_ids_str = str(existing_ids_list).replace('[', '(').replace(']', ')')
    # print('PATRZ', existing_ids_str)
    zlecenia_query = \
        f"""SELECT id, "SPEDYTOR", "OPIEKUN", "SALDO_NETTO"
        FROM "zlecenia_raport" 
        WHERE id NOT IN {existing_ids_str}"""

    zlecenia_df = pd.read_sql_query(zlecenia_query, con=engine)
    print('zlecenia dataframe', zlecenia_df)
    # [['id', 'SPEDYTOR', 'OPIEKUN', 'SALDO_NETTO']]
    return zlecenia_df


def get_osoby_procenty(engine):
    osoby_query = 'SELECT * FROM "spedytorzy_osoby";'
    osoby_procenty = pd.read_sql_query(osoby_query, con=engine)
    return osoby_procenty


def zlecenia_to_premie(created, zlecenia, osoby_procenty):
    premie = pd.DataFrame()
    for index, zlecenie in zlecenia.iterrows():
        zlec_id = zlecenie['id']
        osoby_zlec = set([el for el in [zlecenie['SPEDYTOR'], zlecenie['OPIEKUN']] if el not in ['', None]])
        for osoba_zlec in osoby_zlec:
            osoba_osoba = osoby_procenty.loc[osoby_procenty['osoba'] == osoba_zlec]
            osoba_id = int(osoba_osoba['id'])
            procent = int(osoba_osoba['premia_procent']) / 100
            premia = (float(zlecenie['SALDO_NETTO']) * procent) / len(osoby_zlec)
            premia = f"{premia:.2f}"
            row_dict = {'add_date': created, 'zlecenie_id': zlec_id, 'spedytor_id': osoba_id, 'kwota_premii': premia}
            premie = premie.append(row_dict, ignore_index=True)
    return premie


def zlecenie_to_premie(created, zlecenie, osoby_procenty):
    premie = pd.DataFrame()
    print('ZLECENIE', '\n', zlecenie)
    zlec_id = zlecenie['id']
    osoby_zlec = {zlecenie['SPEDYTOR'], zlecenie['OPIEKUN']}
    print('osoby_zlec', osoby_zlec)
    osoby_zlec = set([el for el in osoby_zlec if el not in ['', None]])
    for osoba_zlec in osoby_zlec:
        osoba_osoba = osoby_procenty.loc[osoby_procenty['osoba'] == osoba_zlec]
        osoba_id = int(osoba_osoba['id'])
        procent = int(osoba_osoba['premia_procent']) / 100
        premia = (float(zlecenie['SALDO_NETTO']) * procent) / len(osoby_zlec)
        premia = f"{premia:.2f}"
        row_dict = {'add_date': created, 'zlecenie_id': zlec_id, 'spedytor_id': osoba_id, 'kwota_premii': premia}
        premie = premie.append(row_dict, ignore_index=True)
    return premie


def update_premie(new_zlec):
    # print('NEW ZLEC', new_zlec)
    osoby_procenty = get_osoby_procenty(engine)

    created = datetime.now()

    zlecenie = pd.DataFrame(new_zlec, index=[0])
    print(zlecenie)
    premie = zlecenia_to_premie(created, zlecenie, osoby_procenty)

    schema_name = 'public'
    table_name = 'spedytorzy_premie'
    premie.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)


def create_premie():
    existing_premie_query = """SELECT zlecenie_id FROM "spedytorzy_premie";"""
    existing__premie_zlec_ids = pd.read_sql_query(existing_premie_query, con=engine)
    existing_zlec_ids_list = existing__premie_zlec_ids['zlecenie_id'].to_list()

    zlecenia_df = get_zlecenia(existing_zlec_ids_list)

    osoby_procenty = get_osoby_procenty(engine)

    created = datetime.now()

    premie = zlecenia_to_premie(created=created, zlecenia=zlecenia_df, osoby_procenty=osoby_procenty)

    schema_name = 'public'
    table_name = 'spedytorzy_premie'
    premie.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)
