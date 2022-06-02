# from connect import get_output_connection
from tools.join import get_raport_df
from tools.connect import get_raport_baza_engine
import pandas as pd

# conn = get_output_connection()


def insert_into_database(month, year):
    speed_df = get_raport_df(month, year)
    # print('1', len(raport_df))

    engine = get_raport_baza_engine()
    raport_df = pd.read_sql_query('select * from "zlecenia_raport"', con=engine)
    new_raport_df = pd.concat([raport_df, speed_df])
    # raport_df
    new_raport_df.drop_duplicates(subset=['NR_ZLECENIA'], keep=False, ignore_index=True, inplace=True)
    # archive_df = pd.read_sql_query('select * from "zlecenia_raport_historia"', con=engine).astype(str)
    # print('speed', len(speed_df), speed_df.columns,
    #       'raport', len(raport_df), raport_df.columns,
    #       'speed', len(archive_df), archive_df.columns, sep='\n')
    # new_raport_df = pd.concat([raport_df, speed_df, archive_df])
    #
    # duplicates_cols = [el for el in speed_df.columns if el not in ['_TIMESTAMP', '_id']]
    # new_raport_df.drop_duplicates(subset=duplicates_cols, keep=False, ignore_index=True, inplace=True)

    # existing_ids_list = raport_df['_id'].to_list()
    # new_raport_df = new_raport_df.loc[~(new_raport_df['_id'].isin(existing_ids_list))]
    schema_name = 'public'
    table_name = 'zlecenia_raport'
    new_raport_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)


if __name__ == '__main__':
    insert_into_database(month=1, year=2022)
