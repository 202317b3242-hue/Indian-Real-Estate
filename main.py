import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Hyderabad Real Estate Dashboard",
    layout="wide"
)

st.title("🏙 Hyderabad Real Estate Buyer Dashboard")
st.markdown("Buyer-focused real estate insights (data embedded in code)")

# --------------------------------------------------
# EMBEDDED DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    data = [
        [50001, "Banjara Hills", "Apartment", 1283, 7461, 3, 9572463, 4.77, 10],
        [50002, "Kondapur", "Independent House", 1263, 9473, 3, 11964399, 5.58, 10],
        [50003, "Nizampet", "Apartment", 2598, 8933, 3, 23207934, 4.17, 10],
        [50004, "Jubilee Hills", "Apartment", 2231, 8277, 4, 18465987, 2.53, 7.5],
        [50005, "Kukatpally", "Independent House", 2095, 7369, 2, 15438055, 2.56, 10],
