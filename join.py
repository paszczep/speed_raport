from cursor import get_cursor, dataframe_from_query
from zlecenia import get_zlec_df, zlecenia_query

cursor = get_cursor()

zlec_df = dataframe_from_query(cursor, zlecenia_query)
zlec_df = get_zlec_df(zlec_df)
print(zlec_df)
# status_str = str(set(zlec_df['STATUS'].to_list())).replace('{', '(').replace('}', ')')
#
# status_query = f"""
#   SELECT KOD, OPIS
#   FROM [SPEED].[dbo].[STATUS]
#   WHERE KOD IN {status_str}
#   AND TYP = 'FT'
# """
#
# status_df = dataframe_from_query(cursor, status_query).set_index('KOD')
# zlec_df = zlec_df.join(status_df, on='STATUS')

relevant_zlec_ids = str(set(zlec_df.ID_ZLECENIA.to_list()))
relevant_zlec_ids = relevant_zlec_ids.replace('{', '(').replace('}', ')')

faktury_query = f"""
  SELECT * FROM FAKTURY WHERE ZLECENIE_ID IN {relevant_zlec_ids}"""

all_faktury_df = dataframe_from_query(cursor, faktury_query)

numery_faktur_list = [el for el in zlec_df.FAKTURA.to_list() if el not in ['', None]]
numery_faktur_str = str(set(numery_faktur_list)).replace('{', '(').replace('}', ')')

numery_faktur_query = f"""
  SELECT * FROM FAKTURY WHERE NUMER_FAKTURY IN {numery_faktur_str}"""

faktury_przych_df = dataframe_from_query(cursor, numery_faktur_query)

faktury_cols = ['NETTO_PLN', 'NUMER_FAKTURY', 'ID_FAKTURY', 'ZLECENIE_ID']

faktury_df = all_faktury_df[faktury_cols].loc[all_faktury_df.NOTA == 0]

missing_faktury = [el for el in faktury_przych_df.NUMER_FAKTURY.to_list() if el not in faktury_df.NUMER_FAKTURY.to_list()]

unique_ids = zlec_df.ID_ZLECENIA.to_list()

numery_faktur_przych_list = [el for el in zlec_df.FAKTURA.to_list() if el != '']

przych_faktury_df = all_faktury_df.loc[all_faktury_df.NUMER_FAKTURY.isin(numery_faktur_przych_list)].set_index('NUMER_FAKTURY')

numery_faktur_koszt_list = [el for el in zlec_df['FAKTURA_K'].to_list() if el != '']

koszt_faktury_df = all_faktury_df.loc[all_faktury_df.NUMER_FAKTURY.isin(numery_faktur_koszt_list)].set_index('NUMER_FAKTURY')

saldo_cols = ['KWOTA_K', 'WALUTA_K', 'FAKTURA', 'FAKTURA_ZB_ID', 'FAKTURA_K', 'FAKTURA_K_ZB', 'KWOTA_P', 'WALUTA_P']

zlec_df[saldo_cols].loc[zlec_df['FAKTURA_K'] != ''].join(koszt_faktury_df['NETTO_PLN'], how='left', on='FAKTURA_K')

print(zlec_df)
