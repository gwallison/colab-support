# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 20:21:24 2022

@author: Gary

Used to make
"""
import pandas as pd


def summarize_api_set(lst,df):
    upk = df[df.api10.isin(lst)].UploadKey.unique().tolist()
    print(f'Number of disclosures within range: {len(upk)} ')
    #print(df.columns)
    df['year'] = df.date.dt.year
    t = df[df.UploadKey.isin(upk)]
    mg = pd.merge(t.groupby('bgCAS',as_index=False)['calcMass'].sum(),
                  t.groupby('bgCAS',as_index=False)['epa_pref_name'].first(),
                  on='bgCAS',how='inner')
    mg1 = pd.merge(t.groupby('bgCAS',as_index=False)['year'].min().rename({'year':'min'},axis=1),
                  t.groupby('bgCAS',as_index=False)['year'].max().rename({'year':'max'},axis=1),
                  on='bgCAS',how='inner')
    
    return pd.merge(mg,mg1,on='bgCAS',how='inner')