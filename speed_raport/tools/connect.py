import pandas as pd
import pymssql
# import psycopg2
from sqlalchemy import create_engine


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
        # charset='ISO-8859-2',
        charset='CP1250'
    )
    cursor = conn.cursor()

    return cursor


# def get_output_connection():
#     connection = psycopg2.connect(
#         host='10.100.200.3',
#         port='5432',
#         database="postgres",
#         user="postgres",
#         password='DbMot!v@SerWBaza22#')
#
#     # cursor = connection.cursor()
#     # cursor.execute("SELECT version();")
#     # print(cursor.fetchone()[0])
#
#     return connection

OUT_DB = {
    'host': '10.100.200.3',
    'port': '5432',
    'database': "postgres",
    'user': "postgres",
    # 'password': "DbMot!v@SerWBaza22#",
    'password': "S4FVVyqlkPexcBryOx7Q5hVMuDY70eQl"
}


# def get_output_engine2():
#     create_str = 'postgresql://postgres:DbMot!v@SerWBaza22#@10.100.200.3:5432/postgres'
#     engine = create_engine(create_str, encoding='ISO-8859-2')
#     return engine


def get_output_engine():
    # create_str = 'postgresql://postgres:DbMot!v@SerWBaza22#@10.100.200.3:5432/postgres'
    engine_str = f"postgresql://{OUT_DB['user']}:{OUT_DB['password']}@{OUT_DB['host']}:{OUT_DB['port']}/{OUT_DB['database']}"
    print(engine_str)
    engine = create_engine(engine_str, encoding='ISO-8859-2')
    return engine
