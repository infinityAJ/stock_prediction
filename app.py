import streamlit as st
from config import *
import pandas as pd
import numpy as np
import plotly.express as px
import pandas_datareader as web
from model import Model

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
    st.write('Reading the data and pre-processing it.')
    nn = Model()
    st.write('Creating Neural Network')
    nn.create()
    st.write('Training the neural network using the data')
    nn.predict()
    nn.write('Calculating the results')
    res = nn.results()
    st.write(res['r2'])
    st.write(res['prediction'])


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
