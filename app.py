import streamlit as st
from config import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web

st.sidebar.title(PROJECT_NAME)
choice = st.sidebar.radio("Project Menu", MENU_OPTIONS)
chart_data = pd.DataFrame(np.random.randn(50, 3), columns=['a', 'b', 'c'])


def home():
    pass


def stck():
    stk_tik = stks[st.selectbox(
        'enter Stock ticker value',
        tuple(stks.keys()))]
    if stk_tik:
        stk_data = web.DataReader(stk_tik, 'yahoo', start, end)
        stk_data.to_csv('stk_data.csv',index=True)
        st.success("stock ticker recorded, you may go to 'view data' page now")


def data():
    st.title("Stock's raw data")
    stk_data = pd.read_csv('stk_data.csv')
    st.table(stk_data)


def grph():
    st.title("Stock price's graph")
    stk_data = pd.read_csv('stk_data.csv')
    prices = stk_data['Close'].values
    st.line_chart(prices)


def predict():
    pass


def rslt():
    pass


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
