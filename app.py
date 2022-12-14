import streamlit as st
import datetime
from model import pred
from flightaware import get_processed_flight_details, get_airport_details_dict

import pandas as pd
import numpy as np


st.set_page_config(
            page_title="Delai", # => Quick reference - Streamlit
            page_icon=":airplane:",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


st.markdown('''
# :airplane: DelAI :airplane:
''')

st.markdown('''
Please enter your flight details... :
''')

col1, col2 = st.columns(2)

with col1:
    flight_number = st.text_input('Flight Number... e.g DAL383')


with col2:
    d = st.date_input(
    "Flight date",
    datetime.date.today())


if st.button('Search for flight!'):
    with st.spinner("Locating your flight details..."):
        X_new = get_processed_flight_details(flight_number, d)
        if type(X_new) != pd.DataFrame:
            st.markdown(f"Couldn't find a flight with those details, please try again!")
        else:
            with st.expander("See your flight details"):
                origin = get_airport_details_dict(X_new['Origin'][0])
                dest = get_airport_details_dict(X_new['Dest'][0])
                dep_time = datetime.datetime.strptime(str(X_new['CRSDepTime'][0]).zfill(4),'%H%M').strftime('%H:%M')
                arr_time = datetime.datetime.strptime(str(X_new['CRSArrTime'][0]).zfill(4),'%H%M').strftime('%H:%M')
                st.markdown(f'''
                        ## Your flight:
                        ### {origin['name']} to {dest['name']}
                        ### 🛫 Sched. Dep Time: {dep_time}
                        ### 🛬 Sched. Arr Time: {arr_time}
                            ''')
if st.button('Predict my delay!'):
    # with st.spinner("Working hard to get your prediction..."):
    prediction = round(pred(flight_number=flight_number, date=d)*100,2)
    st.success("Successfully predicted your chance of delay!")
    st.balloons()

    st.markdown(f'''
    # Our prediction:
    ## {round(prediction)}% chance of delay in your arrival of 30 mins or more!
    ''')
    with st.expander('Disclaimer'):
        if prediction <= 15:
            st.markdown("It's looking good! Your flight is probably going to be on time :relaxed: but it's always best to check with your airline!")
        else:
            st.markdown("Don't be silly and have an extra beer at the airport. Check the departure board")
# df = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(df)
