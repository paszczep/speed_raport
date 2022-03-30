zlecenia_query = """ SELECT [ID_ZLECENIA], [NR_ZLECENIA], [SPEDYTOR], [OPIEKUN], [ZA_MIEJSCE], [ZA_MIASTO], [ZA_KRAJ], 
[ZA_KOD], [TRASA], [ZA_DATA], [ZA_DATA_RZ], [WY_DATA], [WY_DATA_RZ], [WY_DATA_RZ_K], [WY_MIEJSCE], [WY_MIASTO], 
[WY_KRAJ], [WY_KOD], [KWOTA_K], [WALUTA_K], [FAKTURA], [FAKTURA_ZB_ID], [FAKTURA_ZB], [NR_ZLECENIA_K], [KWOTA_P], 
[WALUTA_P], [WALUTA_FV_P], [FAKTURA_K], [FAKTURA_K_ZB], [FAKTURA_K_ZB_ID], [LOKALIZACJA], [STATUS]
FROM [SPEED].[dbo].[ZLECENIA] 
WHERE LOKALIZACJA = 'KAT_MS' AND MONTH([ZA_DATA]) = 1 AND YEAR([ZA_DATA]) = 2022 AND [ZAFAKTUROWANE] = 1
"""


def get_zlec_df(zlec_df):

    zlec_df.FAKTURA_K_ZB_ID = zlec_df.FAKTURA_K_ZB_ID.astype(str).replace('nan', '0')
    zlec_df.FAKTURA_K_ZB_ID = zlec_df.FAKTURA_K_ZB_ID.astype(float).astype(int)
    zlec_df.FAKTURA_K_ZB_ID = zlec_df.FAKTURA_K_ZB_ID.astype(str).replace('0', '')
    zlec_df.fillna('', inplace=True)
    zlec_df.FAKTURA_ZB_ID = zlec_df.FAKTURA_ZB_ID.astype(str).replace('0', '')

    cols = []
    for col in zlec_df.columns:
        if isinstance(zlec_df[col].iloc[1], str):
            try:
                zlec_df[col] = zlec_df[col].str.replace('Ľ', 'Ą')
                cols.append(col)
            except ValueError as excc:
                print(col, excc)
                pass
    print(cols)
    zlec_cols = ['ID_ZLECENIA', 'KWOTA_K', 'WALUTA_K', 'FAKTURA', 'FAKTURA_ZB_ID', 'FAKTURA_ZB', 'NR_ZLECENIA_K',
                 'KWOTA_P', 'WALUTA_P', 'FAKTURA_K', 'FAKTURA_K_ZB', 'FAKTURA_K_ZB_ID']

    return zlec_df[zlec_cols]
