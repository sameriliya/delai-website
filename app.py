import streamlit as st
import datetime
from model import pred
from flightaware import get_processed_flight_details, get_airport_details_dict

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

if st.button('Search for flight!'):
        with st.spinner("Locating your flight details..."):
            X_new = get_processed_flight_details(flight_number, d)
            origin = get_airport_details_dict(X_new['Origin'][0])
            dest = get_airport_details_dict(X_new['Dest'][0])

            f'''
            ## Your flight:
            ### **{origin['name']}** to **{dest['name']}**
            ### Scheduled Dep Time: {X_new['CRSDepTime'][0]}
            ### Scheduled Arr Time: {X_new['CRSArrTime'][0]}
            '''


if st.button('Predict my delay!'):
        with st.spinner("Working hard to get your prediction..."):
            prediction = pred(flight_number=flight_number, date=d)
            st.balloons()

            f'''
            # Our prediction:
            ## {round(prediction*100, 2)}% chance of flight delay of 30 mins or more!
            '''
