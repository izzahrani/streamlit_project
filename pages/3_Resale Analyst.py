import pandas as pd
import numpy as np
import streamlit as st

  
DATE_COLUMN = 'quarter'
DATA = ".\data\MedianResalePricesforRegisteredApplicationsbyTownandFlatType.csv"

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

st.subheader('Average Median Resale Price per Year and Quarter')
# Some number in the range 2007 to 2024
year_to_filter = st.slider('year', 2007, 2024, 2007)
filtered_data = data[data[DATE_COLUMN].dt.year == year_to_filter]

average_median_resale_price_by_year = pd.DataFrame(data.groupby(['year','town','flat_type']).mean('price'))
st.write(average_median_resale_price_by_year)

