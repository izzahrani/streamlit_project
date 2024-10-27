import streamlit as st
from helper_functions.utility import check_password

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

st.title('Welcome to your HDB Resale Assistant!')
st.subheader('You may use the "QnA Resale Chatbot" or "Resale Analyst" to help guide you in your HDB Resale flat purchase!')

