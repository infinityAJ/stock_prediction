import streamlit as st
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import plotly.express as px
import os

st.sidebar.header('Stock Smart')
st.sidebar.write('made by Anant Jain')

choice = st.sidebar.selectbox("Project Menu", ["home","about","contacts"])

"""home = st.sidebar.button("home")
abt = st.sidebar.button("about")
cnt = st.sidebar.button("contacts")

home = True
"""
if choice == "home":
    st.title('Home')
if choice == "contacts":
    st.text_input("kimi no nawa?")
if choice == "about":
    st.title("yamete kudasai")
