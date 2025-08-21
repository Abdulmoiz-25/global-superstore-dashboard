# 📘 DeveloperHub Task 10 – Global Superstore Dashboard

## 📌 Project Objective

The project aims to **analyze sales, profit, and performance** of the **Global Superstore dataset** through a combination of:

1. **Exploratory Data Analysis (EDA)** – insights into sales, profit, regions, categories, and customers.  
2. **Predictive Modeling** – forecasting profit based on sales.  
3. **Interactive Dashboard** – enabling business decision-making with filters, KPIs, and geospatial charts.  

---

## 📁 Dataset

* **Name**: Global Superstore Dataset  
* **Source**: [Kaggle – Global Superstore](https://www.kaggle.com/datasets)  
* **Features include**:  
  * **Order Information**: Order ID, Order Date, Ship Date, Ship Mode  
  * **Customer Details**: Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region  
  * **Product Details**: Category, Sub-Category, Product Name  
  * **Performance Metrics**: Sales, Quantity, Discount, Profit  

---

## 🛠️ Tools & Libraries Used

* **Python (Colab / Jupyter)** – data analysis & model building  
* **Streamlit** – dashboard development and deployment  
* **Pandas, NumPy** – data cleaning & preprocessing  
* **Matplotlib, Seaborn** – static EDA plots  
* **Plotly Express** – interactive visualizations  
* **Scikit-learn** – predictive modeling (Linear Regression)  

---

## 🚀 Approach

### 🔍 1. Problem Statement & Objective

* **Problem**: Measure performance and identify key growth areas for the Global Superstore.  
* **Objectives**:  
  * Calculate **total sales & profit**  
  * Identify **high-performing regions, categories, and sub-categories**  
  * Highlight **top customers**  
  * Build a **predictive model** for profit  
  * Create an **interactive dashboard**  

---

### 📂 2. Dataset Loading

* Default dataset `Global_Superstore2.csv` integrated into the repo.  
* In **Colab Notebook**: option to upload CSV/Excel files.  
* Dataset preview and shape displayed for validation.  

---

### 🧹 3. Data Cleaning & Preprocessing

* Missing postal codes filled with `0`  
* Dates (`Order Date`, `Ship Date`) converted to datetime  
* Duplicate records removed  
* Descriptive statistics generated  

---

### 📊 4. Exploratory Data Analysis (EDA)

* **Total Sales & Profit**  
* **Sales by Region** – bar chart  
* **Profit by Category** – bar chart  
* **Top 5 Customers** – ranked sales visualization  

**Insights reveal:**  
* California, New York, and Texas are **top revenue states**  
* Furniture & Technology drive sales but **profitability varies**  
* **High discounts reduce profits**  

---

### 🤖 5. Model Building & Evaluation

* **Model**: Linear Regression (Profit ~ Sales)  
* **Split**: 80/20 train-test  
* **Results**:  
  * Mean Squared Error (MSE): `42184.16`  
  * R² Score: `0.02` (weak linear correlation → indicates need for advanced models)  

---

### 📉 6. Visualizations

* **EDA (Matplotlib / Seaborn)** – static insights  
* **Interactive (Plotly)** – bar charts for Sales by Region, Profit by Category, and Top Customers  
* **Dashboard (Streamlit)**:  
  * KPIs → Sales, Profit, Orders, Profit Margin  
  * Monthly Sales Trends  
  * Regional & Category Analysis  
  * Discount vs Profit relationship  
  * Choropleth Map (US Sales with black boundaries & state labels)  

---

## 📊 Key Features

* 📈 **Business Insights** – customers, products, categories, and trends  
* 🌍 **Geospatial Analysis** – sales by US states  
* 🔮 **Predictive Analytics** – simple regression baseline  
* 🖥️ **Interactive Dashboard** – real-time filtering & KPIs  

---


## 🌐 Live App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://global-superstore-dashboard-i2s7yr2tcica4cjhdwmff3.streamlit.app/)

---

## 📚 Useful Links

* [Streamlit Documentation](https://docs.streamlit.io/)  
* [Plotly Express](https://plotly.com/python/plotly-express/)  
* [Scikit-learn](https://scikit-learn.org/stable/)  
* [Global Superstore Dataset](https://www.kaggle.com/datasets)  

---

> 🔖 Submitted as part of the **DevelopersHub Internship Program**
