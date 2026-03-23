# 🛒 Retail Data Analysis Project

## 📌 Project Overview

This project focuses on analyzing a retail business dataset to extract meaningful insights related to **sales, customers, products, and regional performance**.

The complete workflow includes:

* Data Cleaning & Transformation using **Python**
* Data Storage using **MySQL**
* Data Visualization & Insights using **Power BI**

---

## 🚀 Tech Stack

* **Python** (Pandas, NumPy) → Data Cleaning & Preprocessing
* **MySQL** → Data Storage & Querying
* **Power BI** → Interactive Dashboard & Visualization

---

## 📂 Dataset Description

The project uses multiple datasets:

* **Orders**
* **Sales**
* **Products**
* **Customers**
* **Suppliers**
* **Inventory**

These datasets are cleaned, transformed, and integrated to build a unified analytical model.

---

## 🔄 Project Workflow

### 1️⃣ Data Cleaning (Python)

* Handled missing values
* Removed duplicates
* Standardized column formats
* Converted data types (dates, numeric fields)
* Feature engineering (Profit, Sales KPIs, etc.)

### 2️⃣ Data Storage (MySQL)

* Created relational database schema
* Loaded cleaned datasets into MySQL tables
* Established relationships using primary & foreign keys
* Performed SQL queries for validation and transformations

### 3️⃣ Data Visualization (Power BI)

* Connected Power BI to MySQL database
* Built interactive dashboards with filters and slicers
* Created KPIs and business insights

---

## 📊 Dashboards Created

### 📍 Executive Overview

* Total Sales: **46M**
* Total Customers: **4K**
* Total Profit: **4.65M**
* Total Orders: **15K**
* Profit Margin: **10.03%**
* Monthly Sales Trend
* Category-wise Sales Analysis
* Sales Channel (Online vs Offline)

---

### 🌍 Regional Analysis

* Top Region by Sales: **West**
* Highest Profit Region: **West**
* Total Cities: **12**
* Sales Distribution by Region
* Profit Comparison by Region
* City-wise Sales Performance

---

### 📦 Product Performance

* Top Selling Category: **Clothing**
* Total Products Sold: **45K**
* Best Selling Subcategory: **Laptop**
* Average Product Profit: **311.70**
* Top Products by Sales
* Category Performance (Year-wise)
* Quantity vs Profit Analysis

---

### 👥 Customer Behaviour

* Total Customers: **4K**
* Average Customer Spending: **11.90K**
* Online Sales %: **49.98%**
* Top Customer Revenue: **49K**
* Payment Method Analysis
* Top Customers
* Online vs Offline Customer Trends

---

## 📈 Key Insights

* **West region** is the highest contributor to both sales and profit
* **Clothing category** dominates sales volume
* Sales are almost evenly split between **Online and Offline channels**
* Certain cities like **Delhi, Bangalore, Chennai** contribute significantly
* High-value customers contribute a major share of revenue

---

## 🔮 Future Enhancements

* Implement **Sales Forecasting (Time Series Model)**
* Build **Recommendation System for Products**
* Add **Real-time Data Pipeline**
* Deploy dashboard to **Power BI Service**

---

## 📁 Project Structure

```
Retail-Data-Analysis/
│
├── data/
├── python/
│   └── data_cleaning.py
├── sql/
│   └── database_schema.sql
├── powerbi/
│   └── dashboard.pbix
├── README.md
```

---

## 🛠️ How to Run the Project

### Step 1: Data Cleaning

```bash
python data_cleaning.py
```

### Step 2: Load Data into MySQL

* Create database
* Import cleaned CSV files into MySQL tables

### Step 3: Connect Power BI

* Open Power BI
* Connect to MySQL database
* Load tables and build dashboard

---

## 💡 Conclusion

This project demonstrates an end-to-end **data analytics pipeline**, starting from raw data to actionable insights using industry-standard tools like Python, MySQL, and Power BI.

---

## 📬 Contact

If you have any questions or suggestions, feel free to connect!

---

⭐ Don’t forget to star this repository if you found it helpful!
