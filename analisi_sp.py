#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import datetime as dt
from plotly.subplots import make_subplots

cci_df = pd.read_csv('C:\\Users\\Utente\\Documents\\Python\\analisi_serie_storiche\\cci.csv')
bci_df = pd.read_csv('C:\\Users\\Utente\\Documents\\Python\\analisi_serie_storiche\\bci.csv')
cli_df = pd.read_csv('C:\\Users\\Utente\\Documents\\Python\\analisi_serie_storiche\\cli.csv')
gdp_df = pd.read_csv('C:\\Users\\Utente\\Documents\\Python\\analisi_serie_storiche\\gdp.csv')
ir_df = pd.read_csv('C:\\Users\\Utente\\Documents\\Python\\analisi_serie_storiche\\STinterest_rate.csv')

cci_df['TIME'] = pd.to_datetime(cci_df.TIME)
cci_df.set_index('TIME', inplace = True)
cci_df.drop(['FREQUENCY','INDICATOR','SUBJECT','MEASURE', 'Flag Codes'], axis=1,inplace=True)
bci_df['TIME'] = pd.to_datetime(bci_df.TIME)
bci_df.set_index('TIME', inplace = True)
bci_df.drop(['FREQUENCY','INDICATOR','SUBJECT','MEASURE', 'Flag Codes'], axis=1,inplace=True)
cli_df['TIME'] = pd.to_datetime(cli_df.TIME)
cli_df.set_index('TIME', inplace = True)
cli_df.drop(['FREQUENCY','INDICATOR','SUBJECT','MEASURE', 'Flag Codes'], axis=1,inplace=True)
gdp_df['TIME'] = pd.to_datetime(gdp_df.TIME)
gdp_df.set_index('TIME', inplace = True)
gdp_df.drop(['FREQUENCY','INDICATOR','SUBJECT','MEASURE', 'Flag Codes'], axis=1,inplace=True)
ir_df['TIME'] = pd.to_datetime(ir_df.TIME)
ir_df.set_index('TIME', inplace = True)
ir_df.drop(['FREQUENCY','INDICATOR','SUBJECT','MEASURE', 'Flag Codes'], axis=1,inplace=True)
ir_df['Value_perc'] = ir_df['Value'].pct_change()*100


indicatori_df = pd.DataFrame(data=cci_df)
indicatori_df["CCI"]=indicatori_df.Value
indicatori_df.drop(['Value'],axis=1,inplace=True)
indicatori_df["BCI"] = bci_df.Value
indicatori_df["CLI"] = cli_df.Value
indicatori_df["GDP"] = gdp_df.Value
indicatori_df["InterestRate"] = ir_df.Value



sp_df = pd.read_excel('C:\\Users\\Utente\\Documents\\Python\\analisi_serie_storiche\\sp500.xlsx')

sp_df['Data'] = pd.to_datetime(sp_df.Data)
sp_df.set_index('Data', inplace=True)
sp_df['month'] = sp_df.index.day
sp_df['day'] = sp_df.index.month
sp_df['year'] = sp_df.index.year
sp_df['data_ok'] = sp_df['year'].astype(str) + '-' + sp_df['month'].astype(str)
sp_df['data_ok'] = pd.to_datetime(sp_df.data_ok)
sp_df = sp_df.sort_values('data_ok')
sp_df.set_index('data_ok', inplace=True)
sp_df['Value_perc'] = sp_df['Ultimo'].pct_change()*100
sp_df['stazionaria'] = sp_df['Ultimo'].diff().dropna()


inizio_serie=str(sp_df.index.min())
inizio_serieY=int(sp_df.index.min().year)
inizio_serieM=int(sp_df.index.min().month)
inizio_serieD=int(sp_df.index.min().day)
fine_serie=str(sp_df.index.max())
fine_serieY=int(sp_df.index.max().year)
fine_serieM=int(sp_df.index.max().month)
fine_serieD=int(sp_df.index.max().day)

st.sidebar.text("INIZIO SERIE "+inizio_serie)
st.sidebar.text("FINE SERIE "+fine_serie)

start = st.sidebar.date_input(
         "data inizio",
         dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


stop = st.sidebar.date_input(
     "data fine",
     dt.date(fine_serieY, fine_serieM, fine_serieD))


mm = st.sidebar.number_input("periodo media mobile", step=1)

sp_df['media_mobile']=sp_df['Ultimo'].rolling(window=mm).mean()
sp_df['differenze'] = sp_df['Ultimo']-sp_df['media_mobile']
sp_df['rollMax'] = sp_df['differenze'].rolling(window=mm).max()
sp_df['rollMin'] = sp_df['differenze'].rolling(window=mm).min()
sp_df['diffNorm'] = np.where(sp_df['differenze']<=0,(sp_df['differenze']/sp_df['rollMin'])*-1,
                             (sp_df['differenze']/sp_df['rollMax']))

serie1 = st.sidebar.selectbox('data 1 grafico 1', (sp_df.columns.tolist())) 
serie2 = st.sidebar.selectbox('data 2 grafico 1', (sp_df.columns.tolist())) 
serie3 = st.sidebar.selectbox('data 1 grafico 2', (sp_df.columns.tolist())) 
serie4 = st.sidebar.selectbox('data 2 grafico 2', (indicatori_df.columns.tolist())) 
serie5 = st.sidebar.selectbox('data 1 grafico 3', (sp_df.columns.tolist())) 
serie6 = st.sidebar.selectbox('data 2 grafico 3', (indicatori_df.columns.tolist())) 



st.title('analisi serie storiche')



fig = make_subplots(rows=3, cols=1, 
                     specs=[[{"secondary_y": True}],
                           [{"secondary_y": True}],
                           [{"secondary_y": True}]])
fig.add_trace(go.Scatter(
    mode = "lines",
    y = sp_df[start:stop][serie1],
    x = sp_df[start:stop].index,
    name= serie1,
    connectgaps=True), row=1, col=1,secondary_y=False,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = sp_df[start:stop][serie2],
    x = sp_df[start:stop].index,
    name= serie2,
    connectgaps=True), row=1, col=1,secondary_y=True,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = sp_df[start:stop][serie3],
    x = sp_df[start:stop].index,
    name= serie3,
    connectgaps=True,
    yaxis="y1"), row=2, col=1,secondary_y=False,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = indicatori_df[start:stop][serie4],
    x = indicatori_df[start:stop].index,
    name = serie4,
    connectgaps=True,
    yaxis="y2"), row=2, col=1, secondary_y=True,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = sp_df[start:stop][serie5],
    x = sp_df[start:stop].index,
    name=serie5,
    connectgaps=True,
    yaxis="y3"), row=3, col=1,secondary_y=False,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = indicatori_df[start:stop][serie6],
    x = indicatori_df[start:stop].index,
    name=serie6,
    connectgaps=True,
    yaxis="y4"), row=3, col=1,secondary_y=True,)
fig.update_layout(
    yaxis=dict(
        #overlaying='y',
        side='left'))


st.plotly_chart(fig,use_container_width=False )

# In[ ]:

