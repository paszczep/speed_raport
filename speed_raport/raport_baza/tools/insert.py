# from connect import get_output_connection
from join import get_raport_df
from connect import get_output_engine
import pandas as pd

# conn = get_output_connection()


def insert_into_database():
    raport_df = get_raport_df().astype(str)
    # print('1', len(raport_df))

    schema_name = 'public'
    table_name = 'zlecenia_raport'
    engine = get_output_engine()
    existing_df = pd.read_sql_query('select * from "zlecenia_raport"', con=engine).astype(str)
    raport_df = pd.concat([existing_df, raport_df])
    # print(list(zlec_df.columns))
    duplicates_cols = [el for el in raport_df.columns if el not in ['_TIMESTAMP', 'id']]
    # print('after removing', duplicates_cols)
    # print('2', len(raport_df))
    raport_df.drop_duplicates(subset=duplicates_cols, keep=False, ignore_index=True, inplace=True)
    # print('3', len(raport_df))
    existing_ids_list = existing_df['id'].to_list()
    raport_df = raport_df.loc[~(raport_df['id'].isin(existing_ids_list))]
    # print('4', len(raport_df))
    raport_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)


if __name__ == '__main__':
    insert_into_database()
