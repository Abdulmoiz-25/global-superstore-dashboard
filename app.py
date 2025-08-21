import streamlit as st
import pandas as pd
import plotly.express as px
import os
import us
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

if 'State' in df.columns:  # use original df for reset option
    sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
    sales_state['State Abbrev'] = sales_state['State'].apply(
        lambda x: us.states.lookup(x).abbr if us.states.lookup(x) else None
    )
    sales_state = sales_state.dropna(subset=['State Abbrev'])

    # ✅ Choropleth map (only one)
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

    # ✅ Find top 5 states by sales
    top_states = sales_state.nlargest(5, 'Sales')['State Abbrev'].tolist()

    # ✅ Add dynamic state labels inside boundaries
    state_centers = {
        "AL": (-86.9023, 32.3182), "AK": (-152.4044, 64.2008), "AZ": (-111.0937, 34.0489),
        "AR": (-92.3731, 34.9697), "CA": (-119.4179, 36.7783), "CO": (-105.7821, 39.5501),
        "CT": (-72.7554, 41.6032), "DE": (-75.5277, 38.9108), "FL": (-81.5158, 27.6648),
        "GA": (-82.9001, 32.1656), "HI": (-155.5828, 19.8968), "ID": (-114.7420, 44.0682),
        "IL": (-89.3985, 40.6331), "IN": (-86.1349, 40.2672), "IA": (-93.0977, 41.8780),
        "KS": (-98.4842, 39.0119), "KY": (-84.2700, 37.8393), "LA": (-91.9623, 30.9843),
        "ME": (-69.4455, 45.2538), "MD": (-76.6413, 39.0458), "MA": (-71.3824, 42.4072),
        "MI": (-85.6024, 44.3148), "MN": (-94.6859, 46.7296), "MS": (-89.3985, 32.3547),
        "MO": (-91.8318, 37.9643), "MT": (-110.3626, 46.8797), "NE": (-99.9018, 41.4925),
        "NV": (-116.4194, 38.8026), "NH": (-71.5724, 43.1939), "NJ": (-74.4057, 40.0583),
        "NM": (-105.8701, 34.5199), "NY": (-75.4999, 43.0003), "NC": (-79.0193, 35.7596),
        "ND": (-101.0020, 47.5515), "OH": (-82.9071, 40.4173), "OK": (-97.0929, 35.4676),
        "OR": (-120.5542, 43.8041), "PA": (-77.1945, 41.2033), "RI": (-71.4774, 41.5801),
        "SC": (-81.1637, 33.8361), "SD": (-99.9018, 43.9695), "TN": (-86.5804, 35.5175),
        "TX": (-99.9018, 31.9686), "UT": (-111.0937, 39.3210), "VT": (-72.5778, 44.5588),
        "VA": (-78.6569, 37.4316), "WA": (-120.7401, 47.7511), "WV": (-80.4549, 38.5976),
        "WI": (-89.6165, 44.2685), "WY": (-107.2903, 43.0759)
    }

    min_sales, max_sales = sales_state['Sales'].min(), sales_state['Sales'].max()

    for i, row in sales_state.iterrows():
        abbrev = row['State Abbrev']
        if abbrev in state_centers:
            lon, lat = state_centers[abbrev]

            # scale font size dynamically between 9–16
            font_size = 9 + (row['Sales'] - min_sales) / (max_sales - min_sales) * 7

            # bold if in top 5
            font_weight = "bold" if abbrev in top_states else "normal"

            fig_map.add_scattergeo(
                lon=[lon], lat=[lat],
                text=row['State Abbrev'],  # show abbreviations
                mode='text',
                textfont=dict(size=font_size, color="black", family=f"Arial {font_weight}"),
                showlegend=False,
                hoverinfo="skip"
            )

    # ✅ Capture clicks
    selected_points = plotly_events(fig_map, click_event=True, hover_event=False)

    if selected_points:
        st.session_state.selected_state = selected_points[0]["text"]

    if st.session_state.selected_state:
        st.success(f"🔎 Dashboard filtered for: {st.session_state.selected_state}")
        filtered_df = filtered_df[filtered_df['State'] == st.session_state.selected_state]

    # ✅ Show only one map
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

