from connect import get_input_cursor, dataframe_from_query

zlec_cols = ['ID_ZLECENIA', 'NR_ZLECENIA', 'SPEDYTOR', 'OPIEKUN', 'ZA_MIEJSCE', 'ZA_MIASTO', 'ZA_KRAJ', 'ZA_KOD', 'TRASA', 'ZA_DATA', 'ZA_DATA_RZ', 'WY_DATA', 'WY_DATA_RZ', 'WY_DATA_RZ_K', 'WY_MIEJSCE', 'WY_MIASTO', 'WY_KRAJ', 'WY_KOD', 'FAKTURA', 'FAKTURA_ZB_ID', 'FAKTURA_ZB', 'NR_ZLECENIA_K', 'FAKTURA_K', 'FAKTURA_K_ZB', 'FAKTURA_K_ZB_ID', 'LOKALIZACJA', 'STATUS']

zlecenia_query = """ SELECT 
[ID_ZLECENIA], [NR_ZLECENIA], [SPEDYTOR], [OPIEKUN], 
[ZA_MIEJSCE], [ZA_MIASTO], [ZA_KRAJ], [ZA_KOD], [TRASA], [ZA_DATA], [ZA_DATA_RZ], 
[WY_DATA], [WY_DATA_RZ], [WY_DATA_RZ_K], [WY_MIEJSCE], [WY_MIASTO], [WY_KRAJ], [WY_KOD], 
[FAKTURA], [FAKTURA_ZB_ID], [FAKTURA_ZB], 
[NR_ZLECENIA_K], [FAKTURA_K], [FAKTURA_K_ZB], [FAKTURA_K_ZB_ID], 
[LOKALIZACJA], [STATUS]
FROM [SPEED].[dbo].[ZLECENIA] 
WHERE LOKALIZACJA = 'KAT_MS' AND MONTH([ZA_DATA]) = 1 AND YEAR([ZA_DATA]) = 2022 AND [ZAFAKTUROWANE] = 1
"""


def clean_zlec_df(zlec_df):

    zlec_df.FAKTURA_K_ZB_ID = zlec_df.FAKTURA_K_ZB_ID.astype(str).replace('nan', '0')
    zlec_df.FAKTURA_K_ZB_ID = zlec_df.FAKTURA_K_ZB_ID.astype(float).astype(int)
    zlec_df.FAKTURA_K_ZB_ID = zlec_df.FAKTURA_K_ZB_ID.astype(str).replace('0', '')
    zlec_df.fillna('', inplace=True)
    zlec_df.FAKTURA_ZB_ID = zlec_df.FAKTURA_ZB_ID.astype(str).replace('0', '')

    # for col in zlec_df.columns:
    #     print(zlec_df[col].dtype)
    #     if isinstance(zlec_df[col].dtype, object) and 'NETTO' not in str(col):
    #         print(True)
    #         try:
    #             zlec_df[col] = zlec_df[col].str.replace('Ľ', 'Ą')
    #             zlec_df[col] = zlec_df[col].str.replace('', 'ś')
    #             zlec_df[col] = zlec_df[col].str.replace('', 'Ś')
    #             # zlec_df[col] = zlec_df[col].str.decode('ISO-8859-2', 'strict')
    #             # zlec_df[col] = zlec_df[col].str.encode('UTF-8', 'strict')
    #         except Exception as exception:
    #             print(col, exception)
    #             pass
    # print(zlec_df)
    return zlec_df


def run_get_zlecenia():
    cursor = get_input_cursor()

    zlec_df = dataframe_from_query(cursor, zlecenia_query)
    zlec_df = clean_zlec_df(zlec_df)
    # print(zlec_df)
    status_str = str(set(zlec_df['STATUS'].to_list())).replace('{', '(').replace('}', ')')

    status_query = f"""
      SELECT KOD, OPIS
      FROM [SPEED].[dbo].[STATUS]
      WHERE KOD IN {status_str}
      AND TYP = 'FT'
    """

    status_df = dataframe_from_query(cursor, status_query).set_index('KOD')
    zlec_df = zlec_df.join(status_df, on='STATUS')

    return zlec_df
