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
    st.header('Stock Smart')
    st.subheader('Featuring future stock price prediction')
    st.write("""The project Stock Smart uses price prediction model to
    predict future stock prices of a given company.""")
    st.write('The Neural network we are using to predict prices'+
             ' maybe represented like this-')
    st.image('img.png')
    st.write('However, our neural network uses two hidden layer instead of one.')

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
    
    bar = st.progress(0)
    msg = st.empty()
    msg.text('Reading databases...')
    time.sleep(1)
    nn = Model()
    conn = sql.connect('stock_smart.db')
    cur = conn.cursor()
    cur.execute('select path from models where tik=:stk', stk_tik)
    path = cur.fetchall()[0][0]
    msg.text('Loading Neural Network...')
    
    bar.progress(50)
    seq = keras.models.load_model(path)
    nn.predict(seq)
    msg.text('Plotting calculations...')
    fig = nn.plotting()
    st.plotly_chart(fig)
    
    bar.progress(70)
    res = nn.results()
    price = res['prediction']
    price = round(float(price), 2)
    st.success(f"""Prediced price for tomorrow is {price}$ with an
        accuracy of {res['r2']}%.""")
    msg.text('Done...')
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
