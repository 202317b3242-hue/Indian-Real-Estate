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
    default=list(df["Locality"].unique())
)

ptype = st.sidebar.multiselect(
    "Property Type",
    df["Property Type"].unique(),
    default=list(df["Property Type"].unique())
)

bhk = st.sidebar.multiselect(
    "Bedrooms (BHK)",
    sorted(df["Bedrooms (BHK)"].unique()),
    default=list(df["Bedrooms (BHK)"].unique())
)

budget = st.sidebar.slider(
    "Budget (INR)",
    int(df["Estimated Sale Price"].min()),
    int(df["Estimated Sale Price"].max()),
    (
        int(df["Estimated Sale Price"].min()),
        int(df["Estimated Sale Price"].max())
    )
)

# --------------------------------------------------
# ✅ FILTER DATA (ERROR FIXED HERE)
# --------------------------------------------------
filtered_df = df[
    (df["Locality"].isin(locality)) &
    (df["Property Type"].isin(ptype)) &
    (df["Bedrooms (BHK)"].isin(bhk)) &
    (df["Estimated Sale Price"].between(budget[0], budget[1]))
]

# Safety check
if filtered_df.empty:
    st.warning("No properties match the selected filters.")
    st.stop()

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
st.subheader("📊 Key Buyer Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Properties", len(filtered_df))
col2.metric("Avg Price / Sqft", f"₹ {int(filtered_df['Price per Sqft'].mean())}")
col3.metric("Avg Sale Price", f"₹ {int(filtered_df['Estimated Sale Price'].mean()):,}")
col4.metric("Avg Rental Yield", f"{filtered_df['Rental Yield (%)'].mean():.2f}%")

# --------------------------------------------------
# CHART 1: AVG PRICE BY LOCALITY
# --------------------------------------------------
st.subheader("📈 Average Sale Price by Locality")

avg_price = (
    filtered_df
    .groupby("Locality")["Estimated Sale Price"]
    .mean()
    .sort_values()
)

fig1, ax1 = plt.subplots()
avg_price.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Locality")
ax1.set_ylabel("Average Sale Price (INR)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# --------------------------------------------------
# CHART 2: AREA VS PRICE
# --------------------------------------------------
st.subheader("📐 Built-up Area vs Estimated Price")

fig2, ax2 = plt.subplots()
ax2.scatter(
    filtered_df["Built-up Area (sqft)"],
    filtered_df["Estimated Sale Price"]
)
ax2.set_xlabel("Built-up Area (sqft)")
ax2.set_ylabel("Estimated Sale Price (INR)")
st.pyplot(fig2)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
st.subheader("📋 Property Details")

st.dataframe(
    filtered_df.sort_values("Buyer Attraction Score", ascending=False),
    use_container_width=True
)
