import streamlit as st
st.title("About Us")

st.subheader("Project Scope")
st.text("The project will covering the domain area of buying a HDB flat in the resale market.")

st.subheader("Objectives")
st.text("This app aims to allow users to make informed purchase decision when making a HDB resale process and keep up with the current trends.")

st.subheader("Data Sources")
st.text("QnA Resale Chatbot used the URL: https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/overview")
st.text("Resale Analyst used the dataset from HDB i.e. Median Resale Prices for Registered Applications by Town and Flat Type: https://data.gov.sg/datasets/d_b51323a474ba789fb4cc3db58a3116d4/view")

st.subheader("Features")
st.text("1. Q&A Chatbot about HDB Resale Processes")
st.text("2. Analyse the resale prices for the past year by Area and HDB Type")