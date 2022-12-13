# import streamlit as st
# import datetime
# from model import pred
# from PIL import Image
# #import plotly.graph_objects as go

# import pydeck as pdk
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


# Map: returns the origin & destination route

df_flight_paths = pd.read_csv('https://storage.cloud.google.com/combined_flights/combined_subset.csv')
df_flight_paths.head()

#fig = go.Figure()

# fig.add_trace(go.Scattergeo(
#     locationmode = 'USA-states',
#     lon = df_airports['long'],
#     lat = df_airports['lat'],
#     hoverinfo = 'text',
#     text = df_airports['airport'],
#     mode = 'markers',
#     marker = dict(
#         size = 2,
#         color = 'rgb(255, 0, 0)',
#         line = dict(
#             width = 3,
#             color = 'rgba(68, 68, 68, 0)'
#         )
#     )))

# flight_paths = []
# for i in range(len(df_flight_paths)):
#     fig.add_trace(
#         go.Scattergeo(
#             locationmode = 'USA-states',
#             lon = [df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i]],
#             lat = [df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i]],
#             mode = 'lines',
#             line = dict(width = 1,color = 'red'),
#             opacity = float(df_flight_paths['cnt'][i]) / float(df_flight_paths['cnt'].max()),
#         )
#     )

# fig.update_layout(
#     title_text = 'Feb. 2011 American Airline flight paths<br>(Hover for airport names)',
#     showlegend = False,
#     geo = dict(
#         scope = 'north america',
#         projection_type = 'azimuthal equal area',
#         showland = True,
#         landcolor = 'rgb(243, 243, 243)',
#         countrycolor = 'rgb(204, 204, 204)',
#     ),
# )

# fig.show()
