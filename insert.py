from connect import get_output_connection
from join import get_raport_df
from connect import get_output_engine

conn = get_output_connection()

raport_df = get_raport_df()

schema_name = 'public'

table_name = 'zlecenia_raport'
# print('len df', len(raport_df))
engine = get_output_engine()
raport_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='replace', index=False)

# data_columns_list = []
# for col in raport_df.columns:
#     if 'TIME' in col:
#         col_str = ' '.join([col, 'timestamp without time zone'])
#     elif 'DATE' in col:
#         col_str = ' '.join([col, 'date'])
#     elif 'NETTO' in col:
#         col_str = ' '.join([col, 'numeric(12,2)'])
#     else:
#         col_str = ' '.join([col, 'character varying'])
#     data_columns_list.append(col_str)
#
# columns_str = ', '.join(data_columns_list)

# create_table_query = f"""
#     CREATE TABLE IF NOT EXISTS
#     {schema_name}.{table_name} ({columns_str})
#     """
# print(create_table_query)
# cursor = conn.cursor()
# cursor.execute(create_table_query)
# conn.commit()


# select_table_query = f"""SELECT * FROM {table_name}"""
# cursor.execute(select_table_query)
