import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import requests


# Page Config
st.set_page_config(layout='wide', page_title='AirBnb Stays Map', page_icon=':house:')

# Function for lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_url = "https://assets4.lottiefiles.com/datafiles/AtGF4p7zA8LpP2R/data.json"
lottie = load_lottieurl(lottie_url)


# Load Data once
DATA_URL = "http://data.insideairbnb.com/italy/lazio/rome/2022-09-11/visualisations/listings.csv"
@st.experimental_singleton
def load_data():
    data = pd.read_csv(DATA_URL)
    # Data cleaning
    cols = ['name',
            'host_name',
            'neighbourhood',
            'latitude',
            'longitude',
            'room_type',
            'price',
            'minimum_nights',
            'number_of_reviews',
            'availability_365']
    data = data[list(cols)]
    data.price = data['price'].astype('float')
    data.drop(data[data.price > 307.5].index, axis=0, inplace=True)
    data.drop(data[data.price <= 0].index, axis=0, inplace=True)
    data.drop(data[data.minimum_nights > 6].index, axis=0, inplace=True)

    return data


# Function for city/host map
def map(data, viz_selected):
    if viz_selected == 'pl':
        fig = px.scatter_mapbox(
            filterdata(data, price_selected_start, price_selected_end, rtype_selected),
            lat="latitude",
            lon="longitude",
            hover_name="name",
            hover_data=["price", "room_type", "neighbourhood"],
            color="price",
            color_continuous_scale="Jet",
            zoom=8,
            center={"lat": 41.9100, "lon": 12.5500},
            height=500,
            mapbox_style="open-street-map",
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit")
    else:
        st.write(
            "Under development"
        )


# Filter Data for a specific price and room type
@st.experimental_memo
def filterdata(data, price_selected_start, price_selected_end, rtype_selected):
    datafiltered = data[(data["price"] >= price_selected_start) &
                        (data["price"] >= price_selected_start) &
                        (data["room_type"].isin(rtype_selected))]
    return datafiltered

# Function to dashboard
def average(data):
    return round(data["price"].mean())

def counts(data):
    return data["name"].count()

def counts_type(data):
    return data["name"].count()

# App Layout
data = load_data()

# sidebar
with st.sidebar:
    st.sidebar.header("AirBnb Clone Stays Map")
    #st.sidebar.write(st_lottie(lottie))
    st.sidebar.subheader("Preferences")
    price_selected_start, price_selected_end = st.sidebar.select_slider("Select price per night",
                                                                        range(0, 400),
                                                                        (100, 150))
    rtype = data['room_type'].unique().tolist()
    rtype_selected = st.sidebar.multiselect("Select room type", rtype, rtype)
    viz_selected = st.sidebar.radio("Select map style", ('pl', 'fo'), 0,
                                    help='Library used to plot map: pl = Plotly | fo = Folium')


# main
row0_1, row0_2 = st.columns((8,1))

with row0_1:
    st.header("Vacation Homes & Condo Rentals MAP")

with row0_2:
    st.sidebar.write(st_lottie(lottie))


row1_1, row1_2, row1_3, row1_4 = st.columns(4)

with row1_1:
    st.caption("City")
    st.subheader("ROME")

with row1_2:
    st.caption("Average Price")
    st.subheader(f"${average(data)} USD")

with row1_3:
    st.caption("Homes Available")
    st.subheader(f"{counts(data)}")

with row1_4:
    st.caption(f"Total by Preferences")
    st.subheader(f"{counts_type(filterdata(data, price_selected_start, price_selected_end, rtype_selected))}")

with st.empty():
    map(filterdata(data, price_selected_start, price_selected_end, rtype_selected), viz_selected)

st.info('Data Source: [Inside Airbnb](http://insideairbnb.com/)', icon='☁️')
st.info('Developed by Pierre Bomfim', icon='💻')