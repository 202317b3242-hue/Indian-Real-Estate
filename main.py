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
st.markdown("Interactive buyer-focused real estate analysis (no file upload required)")

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
        [50008, "HITEC City", "Apartment", 2120, 5456, 3, 11566720, 2.90, 10],
        [50014, "Kondapur", "Villa", 2760, 8487, 3, 23424120, 3.40, 10],
        [50020, "Madhapur", "Villa", 2359, 7604, 2, 17937836, 4.70, 10],
        [50027, "Gachibowli", "Villa", 2295, 6193, 3, 14212935, 2.47, 10],
        [50032, "Manikonda", "Apartment", 802, 4725, 1, 3789450, 4.78, 10],
        [50037, "LB Nagar", "Apartment", 2927, 5315, 3, 15557005, 4.33, 10],
        [50041, "Banjara Hills", "Villa", 2791, 7620, 4, 21267420, 2.35, 6.6],
        [50055, "Madhapur", "Villa", 2334, 7670, 3, 17901780, 4.44, 10],
        [50064, "Banjara Hills", "Independent House", 3120, 7827, 1, 24420240, 4.46, 9.6],
        [50070, "Madhapur", "Apartment", 2387, 9942, 1, 23731554, 2.37, 10],
        [50085, "Jubilee Hills", "Apartment", 1754, 8841, 1, 15507114, 6.48, 10],
        [50093, "Jubilee Hills", "Villa", 2043, 8631, 1, 17633133, 4.08, 10],
        [50100, "Gachibowli", "Villa", 2800, 5471, 4, 15318800, 6.44, 10],
    ]

    columns = [
        "Property ID",
        "Locality",
        "Property Type",
        "Built-up Area (sqft)",
        "Price per Sqft",
        "Bedrooms (BHK)",
        "Estimated Sale Price",
        "Rental Yield (%)",
        "Buyer Attraction Score",
    ]

    return pd.DataFrame(data, columns=columns)

df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Filters")

locality = st.sidebar.multiselect(
    "Locality",
    sorted(df["Locality"].unique()),
    default=df["Locality"].unique()
)

ptype = st.sidebar.multiselect(
    "Property Type",
    df["Property Type"].unique(),
    default=df["Property Type"].unique()
)

bhk = st.sidebar.multiselect(
    "Bedrooms (BHK)",
    sorted(df["Bedrooms (BHK)"].unique()),
    default=df["Bedrooms (BHK)"].unique()
)

budget = st.sidebar.slider(
    "Budget (₹)",
    int(df["Estimated Sale Price"].min()),
    int(df["Estimated Sale Price"].max()),
    (
        int(df["Estimated Sale Price"].min()),
        int(df["Estimated Sale Price"].max())
    )
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------
filtered_df = df[
    (df["Locality"].isin(locality)) &
