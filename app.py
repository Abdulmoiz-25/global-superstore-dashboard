import streamlit as st
import pandas as pd
import plotly.express as px
import os
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Global Superstore Dashboard", layout="wide")
st.title("🌟 Global Superstore Interactive Dashboard")

# -------------------------------
# 1️⃣ Default Dataset in Repo
# -------------------------------
default_path = "Global_Superstore2.csv"

if os.path.exists(default_path):
    try:
        df = pd.read_csv(default_path, encoding='latin1')
        st.info(f"Using default dataset: {default_path}")
    except Exception as e:
        st.error(f"Error loading default dataset: {e}")
        st.stop()
else:
    st.warning("Default dataset not found! Please upload a CSV or Excel file.")
    st.stop()

# -------------------------------
# 2️⃣ Dataset Upload Option
# -------------------------------
uploaded_file = st.file_uploader("Or upload your own dataset (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"Loaded dataset: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error loading uploaded dataset: {e}")
        st.stop()

# -------------------------------
# 3️⃣ Data Cleaning
# -------------------------------
if 'Postal Code' in df.columns:
    df['Postal Code'] = df['Postal Code'].fillna(0)

for col in ['Order Date', 'Ship Date']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

df = df.drop_duplicates()

# -------------------------------
# 4️⃣ Sidebar Filters
# -------------------------------
st.sidebar.header("Filter Options")
regions = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())
sub_categories = st.sidebar.multiselect("Select Sub-Category", options=df['Sub-Category'].unique(), default=df['Sub-Category'].unique())

# Initialize session
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

# Reset Filter button in sidebar
if st.sidebar.button("🔄 Reset State Filter"):
    st.session_state.selected_state = None
    st.experimental_rerun()

filtered_df = df[(df['Region'].isin(regions)) &
                 (df['Category'].isin(categories)) &
                 (df['Sub-Category'].isin(sub_categories))]

# -------------------------------
# 5️⃣ KPIs
# -------------------------------
st.subheader("Key Performance Indicators (KPIs)")
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🛒 Total Orders", total_orders)
col4.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

# -------------------------------
# 6️⃣ Top 5 Customers by Sales
# -------------------------------
st.subheader("Top 5 Customers by Sales")
top_customers = filtered_df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
fig_customers = px.bar(top_customers, x='Customer Name', y='Sales', title='Top 5 Customers by Sales', text='Sales')
st.plotly_chart(fig_customers, use_container_width=True)

# -------------------------------
# 7️⃣ Top 5 Products by Sales
# -------------------------------
st.subheader("Top 5 Products by Sales")
top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
fig_products = px.bar(top_products, x='Product Name', y='Sales', title='Top 5 Products by Sales', text='Sales')
st.plotly_chart(fig_products, use_container_width=True)

# -------------------------------
# 8️⃣ Sales Trend Over Time
# -------------------------------
st.subheader("Sales Trend Over Time")
if 'Order Date' in filtered_df.columns:
    sales_time = filtered_df.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum().reset_index()
    fig_sales_time = px.line(sales_time, x='Order Date', y='Sales', title='Monthly Sales Trend', markers=True)
    st.plotly_chart(fig_sales_time, use_container_width=True)

# -------------------------------
# 9️⃣ Sales by Region
# -------------------------------
st.subheader("Sales by Region")
sales_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig_region = px.bar(sales_region, x='Region', y='Sales', title='Sales by Region', color='Region', text='Sales')
st.plotly_chart(fig_region, use_container_width=True)

# -------------------------------
# 🔟 Profit by Category
# -------------------------------
st.subheader("Profit by Category")
profit_category = filtered_df.groupby('Category')['Profit'].sum().reset_index()
fig_category = px.bar(profit_category, x='Category', y='Profit', title='Profit by Category', color='Category', text='Profit')
st.plotly_chart(fig_category, use_container_width=True)

# -------------------------------
# 11️⃣ Discount vs Profit Scatterplot
# -------------------------------
st.subheader("Discount vs Profit")
if 'Discount' in filtered_df.columns and 'Profit' in filtered_df.columns:
    fig_discount = px.scatter(filtered_df, x='Discount', y='Profit', color='Category',
                              title='Discount vs Profit', hover_data=['Product Name'])
    st.plotly_chart(fig_discount, use_container_width=True)

# -------------------------------
# 13️⃣ Sales by State Map (Interactive Drill-down)
# -------------------------------
st.subheader("Sales by State Map")

# ✅ Static mapping: State → Abbreviation
state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

# ✅ Hardcoded state centers (lat, lon)
state_centers = {
    "AL": (32.806671, -86.791130), "AK": (61.370716, -152.404419),
    "AZ": (33.729759, -111.431221), "AR": (34.969704, -92.373123),
    "CA": (36.116203, -119.681564), "CO": (39.059811, -105.311104),
    "CT": (41.597782, -72.755371), "DE": (39.318523, -75.507141),
    "FL": (27.766279, -81.686783), "GA": (33.040619, -83.643074),
    "HI": (21.094318, -157.498337), "ID": (44.240459, -114.478828),
    "IL": (40.349457, -88.986137), "IN": (39.849426, -86.258278),
    "IA": (42.011539, -93.210526), "KS": (38.526600, -96.726486),
    "KY": (37.668140, -84.670067), "LA": (31.169546, -91.867805),
    "ME": (44.693947, -69.381927), "MD": (39.063946, -76.802101),
    "MA": (42.230171, -71.530106), "MI": (43.326618, -84.536095),
    "MN": (45.694454, -93.900192), "MS": (32.741646, -89.678696),
    "MO": (38.456085, -92.288368), "MT": (46.921925, -110.454353),
    "NE": (41.125370, -98.268082), "NV": (38.313515, -117.055374),
    "NH": (43.452492, -71.563896), "NJ": (40.298904, -74.521011),
    "NM": (34.840515, -106.248482), "NY": (42.165726, -74.948051),
    "NC": (35.630066, -79.806419), "ND": (47.528912, -99.784012),
    "OH": (40.388783, -82.764915), "OK": (35.565342, -96.928917),
    "OR": (44.572021, -122.070938), "PA": (40.590752, -77.209755),
    "RI": (41.680893, -71.511780), "SC": (33.856892, -80.945007),
    "SD": (44.299782, -99.438828), "TN": (35.747845, -86.692345),
    "TX": (31.054487, -97.563461), "UT": (40.150032, -111.862434),
    "VT": (44.045876, -72.710686), "VA": (37.769337, -78.169968),
    "WA": (47.400902, -121.490494), "WV": (38.491226, -80.954456),
    "WI": (44.268543, -89.616508), "WY": (42.755966, -107.302490),
    "DC": (38.9072, -77.0369)
}

if 'State' in df.columns:  
    sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
    sales_state['State Abbrev'] = sales_state['State'].map(state_abbrev)
    sales_state = sales_state.dropna(subset=['State Abbrev'])

    # ✅ Base choropleth (only one colored map)
    fig_map = px.choropleth(
        sales_state,
        locations='State Abbrev',
        locationmode='USA-states',
        color='Sales',
        color_continuous_scale='Blues',
        scope='usa',
        hover_name='State',
        hover_data={'Sales': ':.2f'},
        title='Sales by State'
    )

    # ✅ Add labels inside state boundaries
    for i, row in sales_state.iterrows():
        abbrev = row['State Abbrev']
        if abbrev in state_centers:
            lat, lon = state_centers[abbrev]
            fig_map.add_scattergeo(
                lon=[lon], lat=[lat],
                text=abbrev,
                mode='text',
                textfont=dict(size=10, color="black"),
                showlegend=False,
                hoverinfo="skip"
            )

    # Render interactive map & capture clicks
    selected_points = plotly_events(fig_map, click_event=True, hover_event=False, key="state_map")

    if selected_points:
        st.session_state.selected_state = selected_points[0]["text"]

    if st.session_state.selected_state:
        st.success(f"🔎 Dashboard filtered for: {st.session_state.selected_state}")
        filtered_df = filtered_df[filtered_df['State'] == st.session_state.selected_state]

else:
    st.info("State data not available for map visualization.")



# -------------------------------
# 14️⃣ Download Filtered Dataset
# -------------------------------
st.subheader("Download Filtered Dataset")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name='filtered_global_superstore.csv',
    mime='text/csv'
)




