from connect import get_output_cursor
from join import get_raport_df
# import psycopg2

cursor = get_output_cursor()

raport_df = get_raport_df().reset_index(drop=True)

data_columns_list = []
print(raport_df.columns)
for col in raport_df.columns:
    if 'TIME' in col:
        col_str = ' '.join([col, 'TIMESTAMP'])
    elif 'DATE' in col:
        col_str = ' '.join([col, 'DATE'])
    elif 'NETTO' in col:
        col_str = ' '.join([col, 'DATE'])
    else:
        col_str = ' '.join([col, 'VARCHAR(250)'])

    data_columns_list.append(col_str)

columns_str = ', '.join(data_columns_list)

create_table_query = f"""CREATE TABLE IF NOT EXISTS zlecenia ({columns_str})"""
print(create_table_query)
cursor.execute(create_table_query)
