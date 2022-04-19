import pandas as pd
from datetime import datetime
from zlecenia import run_get_zlecenia
from faktury import get_pozycje_by_zlecenia_id, get_faktury_by_zlecenia_id

DATETIME_FORMAT = '%Y-%m-%d_%H%M'


def _index(series):
    series = pd.to_numeric(series, errors='coerce').astype('Int64').astype(str).str.replace('<NA>', '')
    return series


def _calc(series):
    series.fillna(0, inplace=True)
    series = pd.to_numeric(series)
    return series


def get_raport_df():
    zlec_df = run_get_zlecenia()
    # print(zlec_df)
    zlec_df.fillna('', inplace=True)
    relevant_zlec_ids = str(set(zlec_df.ID_ZLECENIA.to_list()))
    relevant_zlec_ids = relevant_zlec_ids.replace('{', '(').replace('}', ')')
    faktury_df = get_faktury_by_zlecenia_id(relevant_zlec_ids)
    pozycje_df = get_pozycje_by_zlecenia_id(relevant_zlec_ids)
    print(faktury_df.columns)
    pozycje_df['INDEX_POZYCJE'] = _index(pozycje_df['FAKTURY_ID']) + _index(pozycje_df['ZLECENIE_ID'])
    pozycje_df.drop(['FAKTURY_ID', 'ZLECENIE_ID'], axis=1, inplace=True)
    faktury_cols = ['ID_FAKTURY', 'NUMER_FAKTURY', 'ZLECENIE_ID', 'DATA_WYSTAWIENIA', 'DATA_PLATNOSCI']

    koszt_ids = faktury_df.loc[faktury_df.NUMER_FAKTURY.isin(set(zlec_df.FAKTURA_K.to_list()))][faktury_cols]
    koszt_ids['INDEX'] = koszt_ids['NUMER_FAKTURY'] + _index(koszt_ids['ZLECENIE_ID'])
    koszt_ids.drop(['NUMER_FAKTURY', 'ZLECENIE_ID'], axis=1, inplace=True)
    koszt_ids.columns = koszt_ids.columns.values + '_KOSZT'

    zlec_df['INDEX_KOSZT'] = zlec_df['FAKTURA_K'] + _index(zlec_df['ID_ZLECENIA'])
    zlec_df = pd.merge(zlec_df, koszt_ids, how='left', on='INDEX_KOSZT').drop(columns='INDEX_KOSZT')

    przych_ids = faktury_df.loc[faktury_df.NUMER_FAKTURY.isin(set(zlec_df.FAKTURA.to_list()))][faktury_cols]
    przych_ids['INDEX'] = przych_ids['NUMER_FAKTURY'] + _index(przych_ids['ZLECENIE_ID'])
    przych_ids.drop(['NUMER_FAKTURY', 'ZLECENIE_ID'], axis=1, inplace=True)
    przych_ids.columns = przych_ids.columns.values + '_PRZYCH'

    zlec_df['INDEX_PRZYCH'] = zlec_df['FAKTURA'] + _index(zlec_df['ID_ZLECENIA'])
    zlec_df = pd.merge(zlec_df, przych_ids, how='left', on='INDEX_PRZYCH').drop(columns='INDEX_PRZYCH')

    noty_cols = ['ZLECENIE_ID', 'ID_FAKTURY', 'NOTA_UZNANIOWA']
    noty_ids = faktury_df.loc[faktury_df.NOTA == 1][noty_cols]
    noty_ids['INDEX_NOTY'] = _index(noty_ids['ID_FAKTURY']) + _index(noty_ids['ZLECENIE_ID'])
    noty_df = pd.merge(noty_ids, pozycje_df, how='left', left_on='INDEX_NOTY', right_on='INDEX_POZYCJE').drop(
        columns=['INDEX_POZYCJE', 'INDEX_NOTY'])
    noty_df['WALUTOWA_NETTO_PLN'].loc[noty_df.NOTA_UZNANIOWA == 1].apply(lambda x: x * (-1))
    noty_df.rename(columns={'WALUTOWA_NETTO_PLN': 'NOTY_NETTO_PLN'}, inplace=True)
    noty_df = noty_df.groupby(['ZLECENIE_ID'])['NOTY_NETTO_PLN'].sum()

    #

    zlec_df.fillna('', inplace=True)

    zlec_df['POZYCJE_INDEX_KOSZT'] = _index(zlec_df['ID_FAKTURY_KOSZT']) + \
                                     _index(zlec_df['FAKTURA_K_ZB_ID']) + \
                                     _index(zlec_df['ID_ZLECENIA'])

    zlec_df['POZYCJE_INDEX_PRZYCH'] = _index(zlec_df['ID_FAKTURY_PRZYCH']) + \
                                      _index(zlec_df['FAKTURA_ZB_ID']) + \
                                      _index(zlec_df['ID_ZLECENIA'])

    zlec_df.drop(columns=['ID_FAKTURY_PRZYCH', 'FAKTURA_ZB_ID', 'ID_FAKTURY_KOSZT', 'FAKTURA_K_ZB_ID'], inplace=True)

    # PRZYCHÓD
    index_przych = zlec_df.POZYCJE_INDEX_PRZYCH.tolist()
    przych_df = pozycje_df.loc[pozycje_df.INDEX_POZYCJE.isin(index_przych)].groupby(['INDEX_POZYCJE'])[
        'WALUTOWA_NETTO_PLN'].sum()
    zlec_df = pd.merge(zlec_df, przych_df, how='left', left_on='POZYCJE_INDEX_PRZYCH', right_on='INDEX_POZYCJE')
    zlec_df = zlec_df.drop(columns=['POZYCJE_INDEX_PRZYCH'])
    zlec_df.rename(columns={'WALUTOWA_NETTO_PLN': 'NETTO_PLN_PRZYCH'}, inplace=True)

    # KOSZT
    index_koszt = zlec_df.POZYCJE_INDEX_KOSZT.tolist()
    koszt_df = pozycje_df.loc[pozycje_df.INDEX_POZYCJE.isin(index_koszt)].groupby(['INDEX_POZYCJE'])[
        'WALUTOWA_NETTO_PLN'].sum()
    zlec_df = pd.merge(zlec_df, koszt_df, how='left', left_on='POZYCJE_INDEX_KOSZT', right_on='INDEX_POZYCJE')
    zlec_df = zlec_df.drop(columns=['POZYCJE_INDEX_KOSZT'])
    zlec_df.rename(columns={'WALUTOWA_NETTO_PLN': 'NETTO_PLN_KOSZT'}, inplace=True)

    zlec_df = zlec_df.join(noty_df, on='ID_ZLECENIA', how='left')

    zlec_df['SALDO_NETTO'] = _calc(zlec_df['NETTO_PLN_PRZYCH']) - _calc(zlec_df['NETTO_PLN_KOSZT']) - _calc(
        zlec_df['NOTY_NETTO_PLN'])

    netto_cols = ['NETTO_PLN_PRZYCH', 'NETTO_PLN_KOSZT', 'NOTY_NETTO_PLN', 'SALDO_NETTO']
    for col in netto_cols:
        zlec_df[col] = zlec_df[col].apply(lambda x: "{:.2f}".format(x))

    datetime_cols = [col for col in zlec_df.columns if '_DATA_' in col]
    for col in datetime_cols:
        zlec_df[col] = pd.to_datetime(zlec_df[col]).dt.date

    # for row in zlec_df.iteritems():
    #     print(row['ZA_DATA'], row['ZA_DATA_RZ'])

    # zlec_df.loc[zlec_df['ZA_DATA_RZ'] != '', 'ZA_DATA'] = zlec_df.loc[zlec_df['ZA_DATA_RZ'] != '', 'ZA_DATA_RZ']
    # zlec_df.loc[zlec_df['WY_DATA_RZ'] != '', 'WY_DATA'] = zlec_df.loc[zlec_df['WY_DATA_RZ'] != '', 'WY_DATA_RZ']

    zlec_df[['ZA_DATA']].update(zlec_df[['ZA_DATA_RZ']])
    zlec_df[['WY_DATA']].update(zlec_df[['WY_DATA_RZ']])
    zlec_df['_TIMESTAMP'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    zlec_df['INFORMACJE'] = ''
    print(zlec_df.columns)
    relevant_zlec_cols = ['_TIMESTAMP', 'NR_ZLECENIA',
                          'SPEDYTOR', 'OPIEKUN', 'ZA_MIEJSCE',
                          'ZA_DATA', 'WY_DATA',
                          'WY_MIEJSCE', 'WY_MIASTO', 'WY_KRAJ', 'WY_KOD',
                          'ZA_MIASTO', 'ZA_KRAJ', 'ZA_KOD', 'TRASA',
                          'OPIS', 'INFORMACJE',
                          'DATA_WYSTAWIENIA_KOSZT', 'DATA_PLATNOSCI_KOSZT',
                          'DATA_WYSTAWIENIA_PRZYCH', 'DATA_PLATNOSCI_PRZYCH',
                          'NETTO_PLN_PRZYCH', 'NETTO_PLN_KOSZT', 'NOTY_NETTO_PLN', 'SALDO_NETTO']

    # zlec_df.to_excel('output.xlsx', columns=relevant_zlec_cols)
    # zlec_df.to_csv('output.csv', encoding='UTF-8', columns=relevant_zlec_cols)

    return zlec_df[relevant_zlec_cols]


# if __name__ == '__main__':
#
#     raport_dataframe = get_raport_df()
#
#     print(raport_dataframe[['ZA_DATA', 'WY_DATA']])
