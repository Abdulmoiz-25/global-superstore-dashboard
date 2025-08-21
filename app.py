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
# 13️⃣ Sales by State Map (Interactive Drill-down + Zoom + Reset)
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

# ✅ Tiny states needing smaller labels
tiny_states = {"RI", "DC", "DE", "VT", "NH", "NJ", "CT", "MA", "MD"}

# ✅ Approx lat/lon for zoom centers
state_coords = {
    "CA": (37.5, -119.5), "TX": (31.0, -99.9), "NY": (42.9, -75.5), "FL": (27.8, -81.7),
    "IL": (40.0, -89.2), "PA": (41.0, -77.7), "OH": (40.3, -82.8), "GA": (32.7, -83.5),
    "NC": (35.5, -79.0), "MI": (44.3, -85.6), "NJ": (40.0, -74.5), "VA": (37.7, -78.2),
    "WA": (47.4, -120.7), "AZ": (34.3, -111.7), "MA": (42.3, -71.8), "TN": (35.9, -86.4),
    "IN": (39.9, -86.3), "MO": (38.6, -92.6), "MD": (39.0, -76.7), "WI": (44.5, -89.5),
    "CO": (39.0, -105.5), "MN": (46.3, -94.3), "SC": (33.9, -80.9), "AL": (32.8, -86.8),
    "LA": (30.9, -92.0), "KY": (37.5, -85.3), "OR": (44.0, -120.5), "OK": (35.5, -97.5),
    "CT": (41.6, -72.7), "IA": (42.1, -93.6), "NV": (39.3, -116.6), "AR": (34.9, -92.4),
    "MS": (32.7, -89.7), "KS": (38.5, -98.3), "UT": (39.3, -111.7), "NE": (41.5, -99.8),
    "NM": (34.3, -106.0), "WV": (38.6, -80.6), "ID": (44.1, -114.7), "HI": (20.8, -156.3),
    "NH": (43.9, -71.6), "ME": (45.3, -69.2), "MT": (46.9, -110.4), "ND": (47.5, -100.5),
    "SD": (44.3, -100.3), "WY": (43.0, -107.5), "VT": (44.0, -72.7), "DC": (38.9, -77.0),
    "DE": (39.0, -75.5), "RI": (41.7, -71.5), "AK": (64.8, -152.0)
}

if 'State' in df.columns:  
    sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
    sales_state['State Abbrev'] = sales_state['State'].map(state_abbrev)
    sales_state = sales_state.dropna(subset=['State Abbrev'])

    # ✅ Reset button
    if st.button("🔄 Reset Map to USA"):
        st.session_state.selected_state = None

    # ✅ Base choropleth
    fig_map = px.choropleth(
        sales_state,
        locations='State Abbrev',
        locationmode='USA-states',
        color='Sales',
        color_continuous_scale=["#deebf7", "#9ecae1", "#3182bd"],  # fixed light → dark blue
        range_color=(sales_state['Sales'].min(), sales_state['Sales'].max()),
        scope='usa',
        hover_name='State',
        hover_data={'Sales': ':.2f'},
    )

    # ✅ Style layout
    fig_map.update_layout(
        geo=dict(
            scope="usa",
            showland=True,
            landcolor="lightgrey",
            lakecolor="white",
            bgcolor="white",
            showcountries=False,
            showsubunits=False
        ),
        margin=dict(l=0, r=0, t=30, b=40),
        height=650,
        coloraxis_colorbar=dict(
            title="<b>Sales ($)</b>",
            titlefont=dict(color="#3182bd", size=12),
            tickfont=dict(size=10),
            orientation="h",
            thickness=12,
            len=0.4,
            x=0.5,
            xanchor="center",
            y=-0.15,
            yanchor="top"
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    # ✅ Add state abbreviations + sales values
    for i, row in sales_state.iterrows():
        abbrev = row['State Abbrev']
        sales_val = f"${row['Sales']:,.0f}"
        font_size = 9 if abbrev in tiny_states else 10
        fig_map.add_scattergeo(
            locations=[abbrev],
            locationmode="USA-states",
            text=[f"{abbrev}<br>{sales_val}"],
            mode="text",
            showlegend=False,
            textfont=dict(color="black", size=font_size),
            hoverinfo="skip"
        )

    # ✅ Capture clicks
    selected_points = plotly_events(fig_map, click_event=True, hover_event=False, key="state_map")
    if selected_points:
        st.session_state.selected_state = selected_points[0]["text"].split("<br>")[0]

    # ✅ Apply zoom + filter
    if st.session_state.get("selected_state"):
        abbrev = st.session_state.selected_state
        st.success(f"🔎 Dashboard filtered for: {abbrev}")
        filtered_df = filtered_df[filtered_df['State'] == sales_state[sales_state['State Abbrev'] == abbrev]['State'].values[0]]

        # Zoom into state
        if abbrev in state_coords:
            lat, lon = state_coords[abbrev]
            fig_map.update_layout(
                geo=dict(
                    scope="usa",
                    center=dict(lat=lat, lon=lon),
                    projection_scale=7 if abbrev not in {"TX", "CA", "AK"} else 4,
                    showlakes=False,
                    showland=True
                )
            )

    st.plotly_chart(fig_map, use_container_width=True)

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









