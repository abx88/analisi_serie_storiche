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


uploaded_file = st.file_uploader("Selezionare un file .csv/.txt")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter = delimitatore)

inizio_serie=str(df.index.min())
inizio_serieY=int(df.index.min().year)
inizio_serieM=int(df.index.min().month)
inizio_serieD=int(df.index.min().day)
fine_serie=str(df.index.max())
fine_serieY=int(df.index.max().year)
fine_serieM=int(df.index.max().month)
fine_serieD=int(df.index.max().day)


st.sidebar.text("INIZIO SERIE "+inizio_serie)
st.sidebar.text("FINE SERIE "+fine_serie)

start = st.sidebar.date_input(
         "data inizio",
         dt.date(inizio_serieY, inizio_serieM, inizio_serieD))


stop = st.sidebar.date_input(
     "data fine",
     dt.date(fine_serieY, fine_serieM, fine_serieD))

for n in len(df):
        serie[n] = st.sidebar.selectbox('data f-{n}', (df.columns.tolist())) 

''''
serie1 = st.sidebar.selectbox('data 1 grafico 1', (df.columns.tolist())) 
serie2 = st.sidebar.selectbox('data 2 grafico 1', (df.columns.tolist())) 
serie3 = st.sidebar.selectbox('data 1 grafico 2', (df.columns.tolist())) 
serie4 = st.sidebar.selectbox('data 2 grafico 2', (df.columns.tolist())) 
serie5 = st.sidebar.selectbox('data 1 grafico 3', (df.columns.tolist())) 
serie6 = st.sidebar.selectbox('data 2 grafico 3', (df.columns.tolist())) 
''''

st.title('analisi serie storiche')



fig = make_subplots(rows=3, cols=1, 
                     specs=[[{"secondary_y": True}],
                           [{"secondary_y": True}],
                           [{"secondary_y": True}]])
fig.add_trace(go.Scatter(
    mode = "lines",
    y = df[start:stop][serie1],
    x = df[start:stop].index,
    name= serie1,
    connectgaps=True), row=1, col=1,secondary_y=False,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = df[start:stop][serie2],
    x = df[start:stop].index,
    name= serie2,
    connectgaps=True), row=1, col=1,secondary_y=True,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = df[start:stop][serie3],
    x = df[start:stop].index,
    name= serie3,
    connectgaps=True,
    yaxis="y1"), row=2, col=1,secondary_y=False,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = df[start:stop][serie4],
    x = df[start:stop].index,
    name = serie4,
    connectgaps=True,
    yaxis="y2"), row=2, col=1, secondary_y=True,)
fig.add_trace(go.Scatter(
    mode = "lines",
    y = df[start:stop][serie5],
    x = df[start:stop].index,
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

