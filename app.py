import streamlit as st
import datetime
from model import pred
from PIL import Image

import pydeck as pdk
import pandas as pd
import numpy as np


st.set_page_config(
            page_title="Delai", # => Quick reference - Streamlit
            page_icon=":airplane:",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded_img = base64.b64encode(img_bytes).decode()
#     return encoded_img


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

view_state = pdk.ViewState(latitude=32,
                           longitude=35,
                           zoom=7,
                           pitch=0)

d1 = {'lon': [35, 35.1], 'lat': [32.5, 32.6], 'name':['meA', 'meB'], 'prec':[100,300], 'temp':[10,30], 'elevationValue':[100,300]}
df_map1 = pd.DataFrame(data=d1)

tooltip = {
    "html":
        "<b>Name:</b> {name} <br/>"
        "<b>Rain:</b> {prec} mm<br/>",
    "style": {
        "backgroundColor": "steelblue",
        "color": "black",
    }
}

slayer = pdk.Layer(
    type='ScatterplotLayer',
    data=df_map1,
    get_position=["lon", "lat"],
    get_color=["255-temp*3", "31+temp*2", "31+temp*3"],
    get_line_color=[0, 0, 0],
    get_radius=1750,
    pickable=True,
    onClick=True,
    filled=True,
    line_width_min_pixels=10,
    opacity=2,
)

layert1 = pdk.Layer(
    type="TextLayer",
    data=df_map1,
    pickable=False,
    get_position=["lon", "lat"],
    get_text="name",
    get_size=3000,
    sizeUnits='meters',
    get_color=[0, 0, 0],
    get_angle=0,
    # Note that string constants in pydeck are explicitly passed as strings
    # This distinguishes them from columns in a data set
    getTextAnchor= '"middle"',
    get_alignment_baseline='"bottom"'
)

pp = pdk.Deck(
    initial_view_state=view_state,
    map_provider='mapbox',
    map_style=pdk.map_styles.SATELLITE,
    layers=[
        slayer,
        layert1,
    ],
    tooltip=tooltip
)

deckchart = st.pydeck_chart(pp)
