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
fig_customers = px.bar(
    top_customers, 
    x='Customer Name', 
    y='Sales', 
    text='Sales',
    color='Sales',
    color_continuous_scale="Tealgrn",
    title='Top 5 Customers by Sales'
)
fig_customers.update_traces(texttemplate='$%{text:,.0f}', textposition="outside")
fig_customers.update_layout(
    xaxis_title="Customer",
    yaxis_title="Sales ($)",
    uniformtext_minsize=10,
    uniformtext_mode='hide',
    showlegend=False,
    height=400
)
st.plotly_chart(fig_customers, use_container_width=True)


# -------------------------------
# 7️⃣ Top 5 Products by Sales
# -------------------------------
st.subheader("Top 5 Products by Sales")
top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
fig_products = px.bar(
    top_products, 
    x='Product Name', 
    y='Sales', 
    text='Sales',
    color='Sales',
    color_continuous_scale="Purples",
    title='Top 5 Products by Sales'
)
fig_products.update_traces(texttemplate='$%{text:,.0f}', textposition="outside")
fig_products.update_layout(
    xaxis_title="Product",
    yaxis_title="Sales ($)",
    xaxis_tickangle=-30,
    showlegend=False,
    height=400
)
st.plotly_chart(fig_products, use_container_width=True)


# -------------------------------
# 8️⃣ Sales Trend Over Time
# -------------------------------
st.subheader("Sales Trend Over Time")
if 'Order Date' in filtered_df.columns:
    sales_time = filtered_df.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum().reset_index()
    fig_sales_time = px.line(
        sales_time, 
        x='Order Date', 
        y='Sales', 
        title='📈 Monthly Sales Trend',
        markers=True
    )
    fig_sales_time.update_traces(line=dict(width=3, color="royalblue"), marker=dict(size=8))
    fig_sales_time.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        hovermode="x unified",
        height=450
    )
    st.plotly_chart(fig_sales_time, use_container_width=True)


# -------------------------------
# 9️⃣ Sales by Region
# -------------------------------
st.subheader("Sales by Region")
sales_region = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig_region = px.bar(
    sales_region, 
    x='Region', 
    y='Sales', 
    color='Region', 
    text='Sales',
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="Sales by Region"
)
fig_region.update_traces(texttemplate='$%{text:,.0f}', textposition="outside")
fig_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Sales ($)",
    showlegend=False,
    height=400
)
st.plotly_chart(fig_region, use_container_width=True)


# -------------------------------
# 🔟 Profit by Category
# -------------------------------
st.subheader("Profit by Category")
profit_category = filtered_df.groupby('Category')['Profit'].sum().reset_index()
fig_category = px.bar(
    profit_category, 
    x='Category', 
    y='Profit', 
    color='Category', 
    text='Profit',
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Profit by Category"
)
fig_category.update_traces(texttemplate='$%{text:,.0f}', textposition="outside")
fig_category.update_layout(
    xaxis_title="Category",
    yaxis_title="Profit ($)",
    showlegend=False,
    height=400
)
st.plotly_chart(fig_category, use_container_width=True)


# -------------------------------
# 11️⃣ Discount vs Profit (Box / Violin Toggle + Summary Stats)
# -------------------------------
st.subheader("Discount vs Profit Analysis")

if 'Discount' in filtered_df.columns and 'Profit' in filtered_df.columns:
    # Create discount bins (0–10%, 10–20%, etc.)
    filtered_df['Discount Bin'] = pd.cut(
        filtered_df['Discount'],
        bins=[0, 0.1, 0.2, 0.3, 0.4, 1.0],
        labels=['0-10%', '10-20%', '20-30%', '30-40%', '40%+']
    )

    # User choice: Boxplot or Violin
    plot_type = st.radio(
        "Choose plot type:",
        ["📦 Box Plot", "🎻 Violin Plot"],
        horizontal=True
    )

    if plot_type == "📦 Box Plot":
        fig_discount = px.box(
            filtered_df,
            x='Discount Bin',
            y='Profit',
            color='Category',
            title="Profit Distribution Across Discount Ranges (Box Plot)",
            points="all"
        )
    else:
        fig_discount = px.violin(
            filtered_df,
            x='Discount Bin',
            y='Profit',
            color='Category',
            box=True,
            points="all",
            title="Profit Distribution Across Discount Ranges (Violin Plot)"
        )

    fig_discount.update_layout(
        xaxis_title="Discount Range",
        yaxis_title="Profit",
        legend_title="Category",
        height=600
    )

    st.plotly_chart(fig_discount, use_container_width=True)

    # -------------------------------
    # 📊 Summary Statistics Table
    # -------------------------------
    st.subheader("Summary Statistics by Discount Range")

    summary_stats = filtered_df.groupby("Discount Bin")["Profit"].agg(
        Count="count",
        Mean="mean",
        Median="median",
        Std_Dev="std",
        Min="min",
        Max="max"
    ).reset_index()

    st.dataframe(summary_stats.style.format({
        "Mean": "{:.2f}",
        "Median": "{:.2f}",
        "Std_Dev": "{:.2f}",
        "Min": "{:.2f}",
        "Max": "{:.2f}"
    }))


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

    # State lat/lon centers (for labels)
    state_coords = {
        "CA": [37.3, -119.7], "TX": [31.0, -100.0], "NY": [42.9, -75.0],
        "FL": [27.8, -81.7], "IL": [40.0, -89.0], "PA": [41.0, -77.5],
        "OH": [40.3, -82.8], "GA": [32.6, -83.5], "NC": [35.5, -79.0],
        "MI": [44.3, -85.5], "NJ": [40.1, -74.7], "VA": [37.7, -78.0],
        "WA": [47.4, -120.7], "AZ": [34.0, -111.7], "MA": [42.3, -71.8],
        "TN": [35.7, -86.4], "IN": [39.9, -86.3], "MO": [38.6, -92.4],
        "WI": [44.5, -89.5], "MN": [46.3, -94.3], "CO": [39.1, -105.5],
        "SC": [33.8, -80.9], "AL": [32.6, -86.8], "KY": [37.5, -85.3],
        "OR": [44.0, -120.5], "OK": [35.6, -97.5], "CT": [41.6, -72.7],
        "IA": [42.1, -93.5], "KS": [38.5, -98.0], "NV": [39.3, -116.6],
        "AR": [34.9, -92.4], "MS": [32.7, -89.6], "UT": [39.3, -111.7],
        "NE": [41.5, -99.8], "NM": [34.5, -106.1], "WV": [38.6, -80.6],
        "ID": [44.1, -114.7], "ME": [45.3, -69.0], "NH": [43.7, -71.6],
        "MT": [46.9, -110.3], "RI": [41.7, -71.5], "DE": [39.0, -75.5],
        "SD": [44.4, -100.2], "ND": [47.5, -100.5], "VT": [44.0, -72.7],
        "WY": [43.1, -107.6], "AK": [64.8, -147.7], "HI": [20.8, -156.3],
        "MD": [39.0, -76.7]
    }

    # Define font sizes (smaller for tiny states like RI, DE, VT, NH, MA, CT, NJ, MD, DC)
    small_states = {"RI", "DE", "VT", "NH", "MA", "CT", "NJ", "MD"}
    font_sizes = {abbr: 7 if abbr in small_states else 11 for abbr in state_abbrev.values()}

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

    # Add state abbreviation labels
    for _, row in sales_state.iterrows():
        abbrev = row['State Abbrev']
        if pd.notnull(abbrev) and abbrev in state_coords:
            lat, lon = state_coords[abbrev]
            fig_map.add_scattergeo(
                lon=[lon],
                lat=[lat],
                text=[abbrev],
                mode="text",
                showlegend=False,
                textfont=dict(
                    size=font_sizes.get(abbrev, 10),
                    color="black",  # Black font
                    family="Arial Black"
                )
            )

    # Styling for black background
    fig_map.update_geos(
        fitbounds="locations",
        showcountries=False,
        showcoastlines=False,
        showland=True,
        landcolor="black",
        lakecolor="black",
        showlakes=True,
        bgcolor="black",
        projection_type="albers usa"
    )
    fig_map.update_traces(marker_line_width=1.2, marker_line_color="black")  # Black state borders
    fig_map.update_layout(
        title="Sales by State (US)",
        margin={"r":0,"t":30,"l":0,"b":0},
        height=500,
        paper_bgcolor="black",
        plot_bgcolor="black",
        geo_bgcolor="black",
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

















