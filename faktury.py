from connect import get_cursor, dataframe_from_query


def get_noty_by_zlecenia_id(zlecenia_id_list):
    cursor = get_cursor()

    faktury_query = f"""
    SELECT 
         [ID_FAKTURY]
        ,[NUMER_FAKTURY]
        ,[ZLECENIE_ID]
        ,[NOTA], [NOTA_UZNANIOWA]
    FROM [SPEED].[dbo].[FAKTURY]
    WHERE 
        NOTA = 1 AND 
        ZLECENIE_ID IN {zlecenia_id_list}
    """

    faktury_df = dataframe_from_query(cursor, faktury_query)

    return faktury_df


def get_faktury_by_zlecenia_id(zlecenia_id_list):
    cursor = get_cursor()

    faktury_query = f"""
    SELECT 
         [ID_FAKTURY]
        ,[NUMER_FAKTURY]
        ,[ZLECENIE_ID]
        ,[NOTA], [NOTA_UZNANIOWA]
      FROM [SPEED].[dbo].[FAKTURY] 
    WHERE ZLECENIE_ID IN {zlecenia_id_list}
    """

    faktury_df = dataframe_from_query(cursor, faktury_query)

    return faktury_df


def get_pozycje_by_faktury_id(faktury_id_list):

    cursor = get_cursor()
    pozycje_query = f"""
    SELECT [FAKTURY_ID]
          ,[ZLECENIE_ID]
          ,[WALUTOWA_NETTO_PLN]
    FROM [SPEED].[dbo].[FAKTURY_POZYCJE]
    WHERE FAKTURY_ID IN {faktury_id_list}
    """

    pozycje_df = dataframe_from_query(cursor, pozycje_query)

    return pozycje_df


def get_pozycje_by_zlecenia_id(zlecenia_id_list):

    cursor = get_cursor()
    pozycje_query = f"""
    SELECT [FAKTURY_ID]
          ,[ZLECENIE_ID]
          ,[WALUTOWA_NETTO_PLN]
    FROM [SPEED].[dbo].[FAKTURY_POZYCJE]
    WHERE ZLECENIE_ID IN {zlecenia_id_list}
    """

    pozycje_df = dataframe_from_query(cursor, pozycje_query)

    return pozycje_df
