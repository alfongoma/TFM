from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np

def yahoo(stock):
    name_df = "df_" + stock.lower()
    path_csv = "data/" + stock + "/yahoo"
    
    files = [f for f in listdir(path_csv) if isfile(join(path_csv, f))]
    
    df_yahoo = pd.DataFrame()
    appended_data = []
    for file in files:
        if 'csv' in file:
            df = pd.read_csv(path_csv + "/" + file ,decimal=","
                             ,header=0,
                             names=['Date','Open','Max','Min','Close','Adj Close','Vol'])
            appended_data.append(df)

    df_yahoo = pd.concat(appended_data)
    
    # Convertimos el string en Date
    df_yahoo['Date'] = pd.to_datetime(df_yahoo['Date'],format="%Y-%m-%d")
    df_yahoo['Close'] = df_yahoo['Close'].astype(float)
    df_yahoo['Open'] = df_yahoo['Open'].astype(float)
    df_yahoo['Max'] = df_yahoo['Max'].astype(float)
    df_yahoo['Min'] = df_yahoo['Min'].astype(float)
    df_yahoo['Adj Close'] = df_yahoo['Adj Close'].astype(float)
    
    df_yahoo = df_yahoo.sort_values(by=['Date'],ascending=True)
    
    # En la data de yahoo no viene % Var, lo calculamos y se lo añadimos al dataframe
    for i in range(1, len(df_yahoo)):
        df_yahoo.loc[i, '% var'] = ((df_yahoo.loc[i, 'Close']*100) / df_yahoo.loc[i-1, 'Close'])-100
    
    return df_yahoo

def investing(stock):

    name_df = "df_" + stock.lower()
    path_csv = "data/" + stock
    files = [f for f in listdir(path_csv) if isfile(join(path_csv, f))]
    
    df_invest = pd.DataFrame()
    appended_data = []
    for file in files:
        if 'csv' in file:
            df = pd.read_csv(path_csv + "/" + file ,decimal=",",
                                              header=0,names=['Date', 'Close', 'Open','Max','Min','Vol','% var'])
            appended_data.append(df)
    
    df_invest = pd.concat(appended_data)
    # Convertimos el string en Date
    df_invest['Date'] = pd.to_datetime(df_invest['Date'],format="%d.%m.%Y")
    
    # Convertimos el string en float y cambiamos los - por Nan
    df_invest['Vol'] = df_invest['Vol'].str.replace(',','.')
    df_invest['Vol'] = df_invest['Vol'].replace('-', np.nan, regex=True)
   
    # % Var los convertimos en float
    df_invest['% var'] = df_invest['% var'].str.replace('%','').str.replace('.','').str.replace(',','.').astype(float)
    
    # Ordenamos el df por fecha ascendente
    df_invest = df_invest.sort_values(by=['Date'],ascending=True)
    
    return df_invest
