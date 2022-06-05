import pymssql
import pandas as pd
from sqlalchemy import create_engine
from tools.connect import get_input_cursor, OUT_DB, get_raport_baza_engine


def dataframe_from_query(given_cursor, given_query):
    given_cursor.execute(given_query)
    return_data = given_cursor.fetchall()
    dfr_columns = [item[0] for item in given_cursor.description]
    return_dataframe = pd.DataFrame(data=return_data, columns=dfr_columns)

    return return_dataframe


def get_output_engine():
    engine_str = f"postgresql://{OUT_DB['user']}:{OUT_DB['password']}@{OUT_DB['host']}:{OUT_DB['port']}/{OUT_DB['database']}"
    engine = create_engine(engine_str,
                           encoding='ISO-8859-2',
                           # encoding='UTF-8'
                          )
    return engine


# conn_speed = pymssql.connect(
#     server='10.100.200.3',
#     port='1433',
#     user='pawel',
#     password='20Al3Mot@VP@weL22#',
#     database='SPEED',
#     charset='CP1250')
# cursor_speed = conn_speed.cursor()

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
    OUT_DB = {
        'host': '10.100.200.3',
        'port': '5432',
        'database': "postgres",
        'user': "postgres",
        # 'password': "DbMot!v@SerWBaza22#",
        'password': "S4FVVyqlkPexcBryOx7Q5hVMuDY70eQl"}

    schema_name = 'public'
    table_name = 'spedytorzy_osoby'
    engine = get_raport_baza_engine()
    unique_sped_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)
