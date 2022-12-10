import streamlit as st
import datetime
from model import pred

import pandas as pd
import numpy as np


st.set_page_config(
            page_title="Delai", # => Quick reference - Streamlit
            page_icon=":airplane:",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


'''
# DelAI
'''

st.markdown('''
Give us your flight details
''')

col1, col2 = st.columns(2)

with col1:
    flight_number = st.text_input('Flight Number')

with col2:
    d = st.date_input(
    "Flight date",
    datetime.date.today())

if st.button('Predict my delay!'):
        with st.spinner("Working hard to get your prediction..."):
            prediction = pred(flight_number=flight_number, date=d)
            st.balloons()

            f'''
            # Our prediction:
            ## {round(prediction*100, 2)}% chance of flight delay of 30 mins or more!
            '''



df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)
