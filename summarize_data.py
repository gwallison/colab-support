# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 20:21:24 2022

@author: Gary

Used to make
"""
import pandas as pd
from IPython.display import display
# from IPython.display import Markdown as md
from google.colab import data_table
data_table.enable_dataframe_formatter()

def summarize_api_set(lst,df):
    upk = df[df.api10.isin(lst)].UploadKey.unique().tolist()
    print(f'Number of disclosures within range: {len(upk)} ')
    gb = df[df.UploadKey.isin(upk)].groupby('UploadKey',as_index=False)[['APINumber',
                                                                         'WellName',
                                                                         'date',
                                                                         'OperatorName',
                                                                         'TotalBaseWaterVolume',]].first()
    data_table.DataTable(gb, include_index=False, num_rows_per_page=25)

    # print(df.columns)
    df['year'] = df.date.dt.year
    t = df[df.UploadKey.isin(upk)]
    mg = pd.merge(t.groupby('bgCAS',as_index=False)['calcMass'].sum(),
                  t.groupby('bgCAS',as_index=False)['epa_pref_name'].first(),
                  on='bgCAS',how='inner')
    mg1 = pd.merge(t.groupby('bgCAS',as_index=False)['year'].min().rename({'year':'min_year'},axis=1),
                  t.groupby('bgCAS',as_index=False)['year'].max().rename({'year':'max_year'},axis=1),
                  on='bgCAS',how='inner')
    
    display(pd.merge(mg,mg1,on='bgCAS',how='inner'))