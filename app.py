import streamlit as st
from config import *
import pandas as pd
import numpy as np
import plotly.express as px
import pandas_datareader as web
from model import Model
from tensorflow import keras
import sqlite3 as sql

st.sidebar.title(PROJECT_NAME)
choice = st.sidebar.radio("Project Menu", MENU_OPTIONS)
chart_data = pd.DataFrame(np.random.randn(50, 3), columns=['a', 'b', 'c'])

def home():
    st.title('Stock Smart')
    st.subheader('Featuring future stock price prediction')
    st.write("""The project Stock Smart uses stock price prediction model to
    predict future stock prices of a give company.""")
    st.write("""this model uses a Recurrent Neural Network to predict next step
    of a time-series data which in our case is history of a company's stock
    prices.""")
    st.header('there is a change.')

def stck():
    company = st.selectbox(
        'Select a company',
        tuple(stks.keys()))
    stk_tik = stks[company]
    if stk_tik:
        stk_data = web.DataReader(stk_tik, 'yahoo', start, end)
        stk_data[company] = 0
        stk_data.to_csv('stk_data.csv',index=True)
        st.success("stock ticker recorded, you may go to 'view data' page now")

def data():
    stk_data = pd.read_csv('stk_data.csv')
    st.title(f"{stk_data.columns[-1]} stock's raw data")
    st.header('')
    stk_data = stk_data.drop(stk_data.columns[-1], axis=1)
    st.write(stk_data)

def grph():
    stk_data = pd.read_csv('stk_data.csv')
    st.title(f"{stk_data.columns[-1]} stock price's graph")
    st.header('')
    fig = px.line(data_frame=stk_data, x='Date', y='Close',
                  labels={'Close':'Price in $'})
    st.plotly_chart(fig)

def predict():
    stk_data = pd.read_csv('stk_data.csv')
    stk_tik = {'stk': stks[stk_data.columns[-1]]}
    st.title(f'Make future predictions for {stk_data.columns[-1]}')
    st.write('Creating a Neural Network')
    nn = Model()
    st.write('Training the Neural Network')
    try:
        conn = sql.connect('stock_smart.db')
        cur = conn.cursor()
        cur.execute('select path from models where tik=:stk', stk_tik)
        path = cur.fetchall()[0][1]
        seq = keras.models.load_model(path)
    except:
        seq = nn.create()
        seq.save('stock_smart')
    st.success('Please head to the results page to see your results')

def rslt():
    seq = keras.models.load_model('stock_smart')
    nn = Model()
    nn.predict(seq)
    res = nn.results()
    st.write(res['r2'])
    st.write(res['prediction'])

def about():
    pass

if choice == 'home':
    home()
if choice == 'choose stock':
    stck()
if choice == 'view data':
    data()
if choice == 'visualize data':
    grph()
if choice == 'make predictions':
    predict()
if choice == 'visualize results':
    rslt()
if choice == 'about':
    about()
