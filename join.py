import pandas as pd
from zlecenia import run_get_zlecenia
from faktury import get_pozycje_by_zlecenia_id, get_faktury_by_zlecenia_id

zlec_df = run_get_zlecenia()

relevant_zlec_ids = str(set(zlec_df.ID_ZLECENIA.to_list()))
relevant_zlec_ids = relevant_zlec_ids.replace('{', '(').replace('}', ')')

faktury_df = get_faktury_by_zlecenia_id(relevant_zlec_ids)
pozycje_df = get_pozycje_by_zlecenia_id(relevant_zlec_ids)

faktury_cols = ['ID_FAKTURY', 'NUMER_FAKTURY', 'ZLECENIE_ID']
# index_cols = ['ZLECENIE_ID', 'NUMER_FAKTURY']

koszt_ids = faktury_df.loc[faktury_df.NUMER_FAKTURY.isin(set(zlec_df.FAKTURA_K.to_list()))][faktury_cols]
koszt_ids['INDEX'] = koszt_ids['NUMER_FAKTURY'] + ' ' + koszt_ids['ZLECENIE_ID'].astype(str)
koszt_ids.drop(['NUMER_FAKTURY', 'ZLECENIE_ID'], axis=1, inplace=True)
koszt_ids.columns = koszt_ids.columns.values + '_KOSZT'
zlec_df['INDEX_KOSZT'] = zlec_df['FAKTURA_K'] + ' ' + zlec_df['ID_ZLECENIA'].astype(str)
zlec_df = pd.merge(zlec_df, koszt_ids, how='left', on='INDEX_KOSZT')

przych_ids = faktury_df.loc[faktury_df.NUMER_FAKTURY.isin(set(zlec_df.FAKTURA.to_list()))][faktury_cols]
przych_ids['INDEX'] = przych_ids['NUMER_FAKTURY'] + ' ' + przych_ids['ZLECENIE_ID'].astype(str)
przych_ids.drop(['NUMER_FAKTURY', 'ZLECENIE_ID'], axis=1, inplace=True)
przych_ids.columns = przych_ids.columns.values + '_PRZYCH'
zlec_df['INDEX_PRZYCH'] = zlec_df['FAKTURA'] + ' ' + zlec_df['ID_ZLECENIA'].astype(str)
zlec_df = pd.merge(zlec_df, przych_ids, how='left', on='INDEX_PRZYCH')

noty_cols = ['ZLECENIE_ID', 'ID_FAKTURY', 'NOTA_UZNANIOWA']
noty_ids = faktury_df.loc[faktury_df.NOTA == 1][noty_cols]
noty_ids.rename(columns={'ID_FAKTURY': 'ID_FAKTURY_NOTA'}, inplace=True)
zlec_df = pd.merge(zlec_df, noty_ids, how='left', left_on='ID_ZLECENIA', right_on='ZLECENIE_ID')

# print(
#     'zlec', zlec_df[['ID_ZLECENIA', 'ID_FAKTURY_KOSZT', 'ID_FAKTURY_PRZYCH']],
#     'koszt', koszt_ids,
#     'przychód', przych_ids,
#     'NOTY', noty_ids,
#     # 'raport', raport_df,
#     sep='\n')

# print(zlec_df.loc[zlec_df.ID_FAKTURY_PRZYCH != '', ['FAKTURA_ZB_ID', 'ID_FAKTURY_PRZYCH']].sample(10))
zlec_df.fillna('', inplace=True)
print(zlec_df.loc[zlec_df.ID_FAKTURY_NOTA != '', ['ZLECENIE_ID', 'ID_FAKTURY_NOTA']])
# faktury_df.set_index('NUMER_FAKTURY', drop=True, inplace=True)
# faktury_cols = ['NUMER_FAKTURY', 'ID_FAKTURY']


#
# noty_cols = ['ID_FAKTURY', 'NOTA', 'NOTA_UZNANIOWA']
# noty_ids = faktury_df.loc[faktury_df.NOTA == 1][noty_cols]

# przych_df.set_index('NUMER_FAKTURY', drop=True, inplace=True)
# raport_df = zlec_df.join(przych_df, on='FAKTURA', how='left', rsuffix='_PRZYCH')
# raport_df = raport_df.join(faktury_df, on='FAKTURA_K', how='left', rsuffix='_KOSZT')
#
# raport_df = pd.merge(zlec_df, faktury_df[['ID_FAKTURY', 'NUMER_FAKTURY']], left_on='FAKTURA', right_on='NUMER_FAKTURY')
# raport_df = pd.merge(raport_df, faktury_df, left_on='FAKTURA_K', right_on='NUMER_FAKTURY')

# raport_df = pd.merge(zlec_df, przych_ids, how='left', left_on='FAKTURA', right_on='NUMER_FAKTURY')


