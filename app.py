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

# ==========================
# Sales by State Map (Final Single Map)
# ==========================
st.subheader("Sales by State (US)")

if 'State' in filtered_df.columns:
    # Aggregate sales by state
    sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()

    # Map state names to abbreviations
    state_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
        "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
        "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
        "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }
    sales_state['State Abbrev'] = sales_state['State'].map(state_abbrev)

    # Choropleth map
    fig_map = px.choropleth(
        sales_state,
        locations="State Abbrev",
        locationmode="USA-states",
        color="Sales",
        scope="usa",
        color_continuous_scale="Blues",
        labels={"Sales": "Sales ($)"}
    )

    # Add state abbreviation labels on map
    for _, row in sales_state.iterrows():
        abbrev = row['State Abbrev']
        if pd.notnull(abbrev):
            fig_map.add_scattergeo(
                locationmode="USA-states",
                locations=[abbrev],
                locationmode2="USA-states",
                text=[abbrev],
                mode="text",
                showlegend=False,
                textfont=dict(size=9, color="white", family="Arial Black")
            )

    # Styling for black background
    fig_map.update_geos(
        fitbounds="locations",
        showcountries=False,
        showcoastlines=False,
        showland=True,
        landcolor="black",      # Dark land
        lakecolor="black",      # Dark lakes
        showlakes=True,
        projection_type="albers usa"
    )
    fig_map.update_traces(marker_line_width=1.2, marker_line_color="white")
    fig_map.update_layout(
        title="Sales by State (US)",
        margin={"r":0,"t":30,"l":0,"b":0},
        height=500,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("⚠️ No 'State' column found in dataset. Map cannot be generated.")

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







