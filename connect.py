import pandas as pd
import pymssql


def dataframe_from_query(given_cursor, given_query):
    given_cursor.execute(given_query)
    return_data = given_cursor.fetchall()
    dfr_columns = [item[0] for item in given_cursor.description]
    return_dataframe = pd.DataFrame(data=return_data, columns=dfr_columns)

    return return_dataframe


def get_cursor():
    conn = pymssql.connect(
        server='10.100.200.3',
        port='1433',
        user='pawel',
        password='20Al3Mot@VP@weL22#',
        database='SPEED',
        charset='ISO-8859-2')
    cursor = conn.cursor()

    return cursor
