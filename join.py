import pandas as pd
from zlecenia import run_get_zlecenia
from faktury import get_pozycje_by_zlecenia_id, get_faktury_by_zlecenia_id

# bardzo niedobrze ID_ZLECENIA = 7938


def _index(series):
    series = pd.to_numeric(series, errors='coerce').astype('Int64').astype(str).str.replace('<NA>', '')
    return series


def _calc(series):
    series.fillna(0, inplace=True)
    series = pd.to_numeric(series)
    return series


zlec_df = run_get_zlecenia()
print('1', len(zlec_df))
zlec_df.fillna('', inplace=True)
relevant_zlec_ids = str(set(zlec_df.ID_ZLECENIA.to_list()))
relevant_zlec_ids = relevant_zlec_ids.replace('{', '(').replace('}', ')')
faktury_df = get_faktury_by_zlecenia_id(relevant_zlec_ids)
pozycje_df = get_pozycje_by_zlecenia_id(relevant_zlec_ids)

pozycje_df['INDEX_POZYCJE'] = _index(pozycje_df['FAKTURY_ID']) + _index(pozycje_df['ZLECENIE_ID'])
pozycje_df.drop(['FAKTURY_ID', 'ZLECENIE_ID'], axis=1, inplace=True)
print('POZYCJE SAMPLE', pozycje_df.sample(30), sep='\n')
print('pozycje cols', pozycje_df.columns)
faktury_cols = ['ID_FAKTURY', 'NUMER_FAKTURY', 'ZLECENIE_ID']
# index_cols = ['ZLECENIE_ID', 'NUMER_FAKTURY']

koszt_ids = faktury_df.loc[faktury_df.NUMER_FAKTURY.isin(set(zlec_df.FAKTURA_K.to_list()))][faktury_cols]
koszt_ids['INDEX'] = koszt_ids['NUMER_FAKTURY'] + _index(koszt_ids['ZLECENIE_ID'])
koszt_ids.drop(['NUMER_FAKTURY', 'ZLECENIE_ID'], axis=1, inplace=True)
koszt_ids.columns = koszt_ids.columns.values + '_KOSZT'

print('koszt_ids cols', koszt_ids.columns)
zlec_df['INDEX_KOSZT'] = zlec_df['FAKTURA_K'] + _index(zlec_df['ID_ZLECENIA'])
zlec_df = pd.merge(zlec_df, koszt_ids, how='left', on='INDEX_KOSZT').drop(columns='INDEX_KOSZT')
print('2', len(zlec_df))

print('1 zlec_df cols', zlec_df.columns)

przych_ids = faktury_df.loc[faktury_df.NUMER_FAKTURY.isin(set(zlec_df.FAKTURA.to_list()))][faktury_cols]
przych_ids['INDEX'] = przych_ids['NUMER_FAKTURY'] + _index(przych_ids['ZLECENIE_ID'])
przych_ids.drop(['NUMER_FAKTURY', 'ZLECENIE_ID'], axis=1, inplace=True)
przych_ids.columns = przych_ids.columns.values + '_PRZYCH'
print('przych_ids cols', przych_ids.columns)
zlec_df['INDEX_PRZYCH'] = zlec_df['FAKTURA'] + _index(zlec_df['ID_ZLECENIA'])
zlec_df = pd.merge(zlec_df, przych_ids, how='left', on='INDEX_PRZYCH').drop(columns='INDEX_PRZYCH')

print('3', len(zlec_df))
print('2 zlec_df cols', zlec_df.columns)
noty_cols = ['ZLECENIE_ID', 'ID_FAKTURY', 'NOTA_UZNANIOWA']
noty_ids = faktury_df.loc[faktury_df.NOTA == 1][noty_cols]
noty_ids['INDEX_NOTY'] = _index(noty_ids['ID_FAKTURY']) + _index(noty_ids['ZLECENIE_ID'])
noty_df = pd.merge(noty_ids, pozycje_df, how='left', left_on='INDEX_NOTY', right_on='INDEX_POZYCJE').drop(columns=['INDEX_POZYCJE', 'INDEX_NOTY'])
noty_df['WALUTOWA_NETTO_PLN'].loc[noty_df.NOTA_UZNANIOWA == 1].apply(lambda x: x*(-1))
noty_df.rename(columns={'WALUTOWA_NETTO_PLN': 'NOTY_NETTO_PLN'}, inplace=True)
noty_df = noty_df.groupby(['ZLECENIE_ID'])['NOTY_NETTO_PLN'].sum()

print('4', len(zlec_df))
print('3 zlec_df cols', zlec_df.columns)
print(
    'zlec', zlec_df[['ID_ZLECENIA', 'ID_FAKTURY_KOSZT', 'ID_FAKTURY_PRZYCH']],
    'koszt', koszt_ids,
    'przychód', przych_ids,
    'NOTY', noty_df,
    # 'raport', raport_df,
    sep='\n')

# print(zlec_df.loc[zlec_df.ID_FAKTURY_PRZYCH != '', ['FAKTURA_ZB_ID', 'ID_FAKTURY_PRZYCH']].sample(10))
zlec_df.fillna('', inplace=True)
# print(zlec_df.loc[zlec_df.ID_FAKTURY_NOTA != '', ['ZLECENIE_ID', 'ID_FAKTURY_NOTA']])
print(zlec_df[['ID_FAKTURY_PRZYCH', 'FAKTURA_ZB_ID', 'ID_FAKTURY_KOSZT', 'FAKTURA_K_ZB_ID']].sample(30))

zlec_df['POZYCJE_INDEX_KOSZT'] = _index(zlec_df['ID_FAKTURY_KOSZT']) + \
                                 _index(zlec_df['FAKTURA_K_ZB_ID']) + \
                                 _index(zlec_df['ID_ZLECENIA'])

zlec_df['POZYCJE_INDEX_PRZYCH'] = _index(zlec_df['ID_FAKTURY_PRZYCH']) + \
                                  _index(zlec_df['FAKTURA_ZB_ID']) + \
                                  _index(zlec_df['ID_ZLECENIA'])
zlec_df.drop(columns=['ID_FAKTURY_PRZYCH', 'FAKTURA_ZB_ID', 'ID_FAKTURY_KOSZT', 'FAKTURA_K_ZB_ID'], inplace=True)
print('POZYCJE INDEX:', zlec_df[['POZYCJE_INDEX_PRZYCH', 'POZYCJE_INDEX_KOSZT']].sample(30), sep='\n')

print('pozycje cols', pozycje_df.columns)

zlec_df = pd.merge(zlec_df, pozycje_df, how='left', left_on='POZYCJE_INDEX_PRZYCH', right_on='INDEX_POZYCJE').drop(columns=['POZYCJE_INDEX_PRZYCH', 'INDEX_POZYCJE'])
#
zlec_df.rename(columns={'WALUTOWA_NETTO_PLN': 'NETTO_PLN_PRZYCH'}, inplace=True)
#
print('4 zlec_df cols', zlec_df.columns)
dorsz_cols = [col for col in zlec_df.columns if 'INDEX' in col]
print(zlec_df[dorsz_cols])
zlec_df = pd.merge(zlec_df, pozycje_df, how='left', left_on='POZYCJE_INDEX_KOSZT', right_on='INDEX_POZYCJE')
zlec_df.rename(columns={'WALUTOWA_NETTO_PLN': 'NETTO_PLN_KOSZT'}, inplace=True)
print('5 zlec_df cols', zlec_df.columns)

zlec_df = zlec_df.join(noty_df, on='ID_ZLECENIA', how='left')

netto_cols = [col for col in zlec_df.columns if 'NETTO' in col]

print(zlec_df[netto_cols +['OPIS']].sample(30))

zlec_df['SALDO_NETTO'] = _calc(zlec_df['NETTO_PLN_PRZYCH']) - _calc(zlec_df['NETTO_PLN_KOSZT']) - _calc(zlec_df['NOTY_NETTO_PLN'])

print(zlec_df[netto_cols + ['SALDO_NETTO']].sample(30))
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
