import pandas as pd
import pymssql
# import psycopg2
from sqlalchemy import create_engine

SCHEMA_NAME = 'public'

OUT_DB = {
    'host': '10.100.200.3',
    'port': '5432',
    'database': "postgres",
    'user': "postgres",
    'password': ""
}


def dataframe_from_query(given_cursor, given_query):
    given_cursor.execute(given_query)
    return_data = given_cursor.fetchall()
    dfr_columns = [item[0] for item in given_cursor.description]
    return_dataframe = pd.DataFrame(data=return_data, columns=dfr_columns)

    return return_dataframe


def get_input_cursor():
    conn = pymssql.connect(
        server='10.100.200.3',
        port='1433',
        user='pawel',
        password='20Al3Mot@VP@weL22#',
        database='SPEED',
        charset='CP1250'
    )
    cursor = conn.cursor()

    return cursor


def get_raport_baza_engine():
    engine_str = f"postgresql://{OUT_DB['user']}:{OUT_DB['password']}@{OUT_DB['host']}:{OUT_DB['port']}/{OUT_DB['database']}"
    engine = create_engine(engine_str, encoding='ISO-8859-2')
    return engine
