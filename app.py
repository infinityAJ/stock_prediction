import streamlit as st
from config import *
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas_datareader as web
from model import Model
from tensorflow import keras
import sqlite3 as sql
import time

st.sidebar.title(PROJECT_NAME)
choice = st.sidebar.radio("Project Menu", MENU)
chart_data = pd.DataFrame(np.random.randn(50, 3), columns=['a', 'b', 'c'])

def home():
    st.title('Stock Smart')
    st.subheader('Featuring future stock price prediction')
    st.write("""The project Stock Smart uses stock price prediction model to
    predict future stock prices of a give company.""")
    st.write("""this model uses a Recurrent Neural Network to predict next step
    of a time-series data which in our case is history of a company's stock
    prices.""")

def stck():
    company = st.selectbox('Select a company', tuple(stks.keys()))
    stk_tik = stks[company]
    if stk_tik:
        stk_data = web.DataReader(stk_tik, 'yahoo', start, end)
        stk_data[company] = 0
        stk_data.to_csv('stk_data.csv', index=True)
        st.success("company recorded successfully.")

def data():
    stk_data = pd.read_csv('stk_data.csv')
    st.title(f"{stk_data.columns[-1]} stock's raw data")
    stk_data = stk_data.drop(stk_data.columns[-1], axis=1)
    st.write(stk_data)

def grph():
    df = pd.read_csv('stk_data.csv')
    st.title(f"{df.columns[-1]} stock price's graph")
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],open=df['Open'],
                high=df['High'],low=df['Low'],close=df['Close'])])
    st.plotly_chart(fig)

def predict():
    stk_data = pd.read_csv('stk_data.csv')
    stk_tik = {'stk': stks[stk_data.columns[-1]]}
    
    st.title(f'Make future predictions for {stk_data.columns[-1]}')
    st.header('creating and training the neural network')
    bar = st.progress(0)
    time.sleep(1)
    
    nn = Model()
    st.write('Training the Neural Network')
    
    conn = sql.connect('stock_smart.db')
    cur = conn.cursor()
    cur.execute('select path from models where tik=:stk', stk_tik)
    path = cur.fetchall()[0][0]
    
    bar.progress(50)
    seq = keras.models.load_model(path)
    nn.predict(seq)
    df = pd.DataFrame()
    
    fig = nn.plotting()
    st.plotly_chart(fig)
    bar.progress(70)

    res = nn.results()
    st.success(f"""prediced price for tomorrow is {res['prediction']}$ with an
        accuracy of {res['r2']}%.""")
    bar.progress(100)

def hist():
    conn = sql.connect('stock_smart.db')
    cur = conn.cursor()
    cur.execute('select * from history')
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['date', 'ticker', 'prediction', 'accuracy'])
    df.date = [x.split()[0] for x in df.date]
    df.accuracy = [str(x)+'%' for x in df.accuracy]
    st.table(df)

def about():
    pass

if choice == MENU[0]:
    home()
if choice == MENU[1]:
    stck()
if choice == MENU[2]:
    data()
if choice == MENU[3]:
    grph()
if choice == MENU[4]:
    predict()
if choice == MENU[5]:
    hist()
if choice == MENU[6]:
    about()
