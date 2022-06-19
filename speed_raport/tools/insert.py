# from connect import get_output_connection
from tools.join import get_raport_df
from tools.connect import get_raport_baza_engine, SCHEMA_NAME
import pandas as pd

# conn = get_output_connection()


def insert_into_database(month, year):
    
    speed_df = get_raport_df(month, year)
    engine = get_raport_baza_engine()
    raport_df = pd.read_sql_query('select * from "zlecenia_raport"', con=engine)
    new_raport_df = pd.concat([raport_df, speed_df])

    new_raport_df.drop_duplicates(subset=['NR_ZLECENIA'], keep=False, ignore_index=True, inplace=True)

    schema_name = SCHEMA_NAME
    table_name = 'zlecenia_raport'
    new_raport_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)
