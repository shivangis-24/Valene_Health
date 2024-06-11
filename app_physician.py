import streamlit as st
import pandas as pd
import json

# This will act as a mock database
diagnosis_data = []

# Define a function to handle incoming diagnosis data
def handle_incoming_data():
    data = st.experimental_get_query_params().get("data")
    if data:
        diagnosis_data.append(json.loads(data[0]))

# Initialize the dashboard
st.set_page_config(page_title="Physician Dashboard", page_icon="🩺")

# Handle incoming data
handle_incoming_data()

# Display the diagnosis data
st.title("Physician Dashboard")

if diagnosis_data:
    df = pd.DataFrame(diagnosis_data)
    st.dataframe(df)
else:
    st.write("No diagnosis data available.")
