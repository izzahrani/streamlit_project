import pandas as pd
import numpy as np
import streamlit as st

try:
    _ = st.session_state.keep_graphics
except AttributeError:
    st.session_state.keep_graphics = False

DATE_COLUMN = 'quarter'
DATA = "./data/MedianResalePricesforRegisteredApplicationsbyTownandFlatType.csv"

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data = data[(data['price']!='na') & (data['price']!='-')]
    data['price'] = data['price'].astype('int')
    data['year'] = data['quarter'].dt.year
    return data

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

df = pd.read_csv(DATA)
df = df[(df['price']!='na') & (df['price']!='-')]
df[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
df['price'] = df['price'].astype('float')
df['year'] = df[DATE_COLUMN].dt.year


with st.form("Input Parameters"):
    town = st.selectbox(
        "Which town would you like to analyse?",
        ("Ang Mo Kio", "Bedok", "Bishan", "Bukit Batok", "Bukit Merah", "Bukit Panjang", "Bukit Timah", "Central", "Choa Chu Kang", "Clementi", "Geylang", "Hougang", "Jurong East", "Jurong West", "Kallang/Whampoa", "Marine Parade", "Pasir Ris", "Punggol", "Queenstown", "Sembawang", "Sengkang", "Serangoon", "Tampines", "Toa Payoh", "Woodlands", "Yishun", "CENTRAL AREA"),
    )
    st.write("You selected:", town)

    flat_type = st.selectbox(
        "Which flat type would you like to analyse?",
        ("1-room", "2-room", "3-room", "4-room", "5-room", "Executive")
    )
    st.write("You selected:", flat_type)

    year = st.selectbox(
        "Which year would you like to analyse?",
        ("2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024")
    )
    st.write("You selected:", year)

    submitted = st.form_submit_button("Submit")


# Running the Crew
if submitted or st.session_state.keep_graphics: 
    #result = crew.kickoff(inputs={"topic": f"What is the average median resale price for {town}, {flat_type} flat in {year}?"})
    #st.markdown(result)
    st.session_state.keep_graphics = True