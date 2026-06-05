import streamlit as st
import requests

st.title("🤖 AI Interview Platform")
st.subheader("Welcome, Team! This is our Python Frontend Skeleton.")

# A simple button to test connecting to your backend server
if st.button("Test Backend Connection"):
    try:
        response = requests.get("http://localhost:8000/")
        st.success(f"Backend says: {response.json()['message']}")
    except:
        st.error("Could not connect to the backend server. Is it running?")