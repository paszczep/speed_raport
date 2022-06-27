import pandas as pd
from tools.connect import get_input_cursor, OUT_DB, get_raport_baza_engine, dataframe_from_query, SCHEMA_NAME


def update_osoby():
    spedytorzy_query = """
       SELECT [SPEDYTOR], [OPIEKUN] FROM [SPEED].[dbo].[ZLECENIA]
    """

    cursor_speed = get_input_cursor()
    spedytorzy_df = dataframe_from_query(cursor_speed, spedytorzy_query)
    spedytorzy = spedytorzy_df.SPEDYTOR.append(spedytorzy_df.OPIEKUN)

    engine = get_raport_baza_engine()
    existing_df = pd.read_sql_query('select * from "spedytorzy_osoby"', con=engine)
    existing_list = existing_df.osoba.to_list()
    spedytorzy_list = [sped for sped in spedytorzy.unique() if sped not in existing_list + [None, '', '-']]
    unique_sped_df = pd.DataFrame(data=spedytorzy_list, columns=['osoba'])
    unique_sped_df['premia_procent'] = 10

    schema_name = SCHEMA_NAME
    table_name = 'spedytorzy_osoby'
    unique_sped_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)
