import streamlit as st
import datetime
from model import pred
from flightaware import get_raw_flight_details, get_airport_details_dict, process_flight_details
import pandas as pd
import numpy as np
import pydeck as pdk
from PIL import Image

st.set_page_config(
            page_title="Delai", # => Quick reference - Streamlit
            page_icon=":airplane:",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

col1, col2, col3 = st.columns(3)
with col2:
    st.markdown('# :airplane: DelAI :airplane:')
    st.caption('Predicting delays since 2022...')

st.markdown('''
**Please enter your flight details** :
''')

col1, col2 = st.columns(2)

with col1:
    flight_number = st.text_input('✈️ Flight Number...  e.g DAL383')

with col2:
    d = st.date_input(
    "📅  Flight date",
    datetime.date.today())

def load_image(airline_code):
    image = Image.open(f'airline_images/{airline_code}.png')
    return image

with st.container():
    if st.button('Search for flight!'):
        with st.spinner("Locating your flight details..."):
            response = get_raw_flight_details(flight_number, d)
            print(response)
            X_new = process_flight_details(response=response)
            if type(X_new) != pd.DataFrame:
                st.markdown(f"Couldn't find a flight with those details, please try again!")
            else:
                # Get variables to display to user
                flight = response.json()['flights'][0]
                origin = get_airport_details_dict(X_new['Origin'][0])
                dest = get_airport_details_dict(X_new['Dest'][0])
                dep_time = datetime.datetime.strptime(str(X_new['CRSDepTime'][0]).zfill(4),'%H%M').strftime('%H:%M')
                arr_time = datetime.datetime.strptime(str(X_new['CRSArrTime'][0]).zfill(4),'%H%M').strftime('%H:%M')
                s = flight['filed_ete']
                flight_time = '{:2}h {:02}m'.format(s // 3600, s % 3600 // 60)
                dist = flight['route_distance']

                # Display variables to user
                col1,col2 = st.columns(2)
                col1.markdown((f'''## Your flight:'''))
                col2.image(load_image(flight_number[:3]))
                st.markdown(f'''
                        ##### From: {origin['name']}, {origin['location']}
                        ##### To:   {dest['name']}, {dest['location']}''')
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🛫 Sched. Dep. Time", dep_time, 'Local Time', delta_color='off')
                col2.metric("🛬 Sched. Arr. Time", arr_time, 'Local Time', delta_color='off')
                col3.metric("🕓 Air Time", flight_time, delta='Planned', delta_color ='off')
                col4.metric("📍 Distance",dist,'Miles', delta_color='off')

                zoom = (6300 - dist)/1200

                pydeck_df = pd.DataFrame()
                pydeck_df['from'] = origin
                pydeck_df['to'] = dest

                init_lon = int((pydeck_df['from']['coord'][0]+pydeck_df['to']['coord'][0])/2)
                init_lat = int((pydeck_df['from']['coord'][1]+pydeck_df['to']['coord'][1])/2)

                st.pydeck_chart(pdk.Deck(map_style=None,
                                initial_view_state=pdk.ViewState(latitude=init_lat,
                                               longitude=init_lon,
                                               zoom = zoom,
                                               bearing=0,
                                               pitch=45),
                                layers=[

                    # Define a layer to display on a map
                                pdk.Layer(
                                    "GreatCircleLayer",
                                    pydeck_df,
                                    pickable=True,
                                    get_stroke_width=40,
                                    get_source_position=pydeck_df['from']['coord'],
                                    get_target_position=pydeck_df['to']['coord'],
                                    get_source_color=[255, 65, 0],
                                    get_target_color=[0, 128, 200],
                                    auto_highlight=True,
                                    widthScale = 6,
                                )
                                ]
                )
                )

with st.container():
    if st.button('Predict my delay!'):
        with st.spinner("Working hard to get your prediction..."):
            if flight_number == '':
                st.error("Please enter a flight number and search for your flight again!")
            else:
                try:
                    prediction = round(pred(flight_number=flight_number, date=d)*100,2)
                    st.success("Successfully predicted your chance of delay at your destination!")

                    st.markdown(f'''
                    # Our prediction:
                    ## {round(prediction)}% chance of delay to your arrival of 30 mins or more!
                    ''')
                    with st.expander('Disclaimer'):
                        if prediction < 20:
                            st.markdown("""
                                        It's looking good! Your flight is probably going to be on time 😃 but it's always best to check with your airline! 👀

                                        ### Have a great trip! 🫶
                                        """)
                        else:
                            st.markdown("""
                                        You may want to give yourself some extra time at your destination.
                                        Don't be silly and have an extra beer at the airport. Check the departure board! 👀

                                        ### Have a great trip! 🫶
                                        """)
                except:
                    st.error("Couldn't predict your flight delay for that flight number! Please try again or contact our __support team__")
