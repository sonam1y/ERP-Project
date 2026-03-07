import streamlit as st
import pandas as pd
from db import get_connection

def dashboard_page():
    st.markdown("<h1 style='color:#28B463;'>📊 ERP Dashboard</h1>", unsafe_allow_html=True)

    conn = get_connection()

    products = pd.read_sql("SELECT COUNT(*) AS total FROM products", conn)
    customers = pd.read_sql("SELECT COUNT(*) AS total FROM customers", conn)
    orders = pd.read_sql("SELECT COUNT(*) AS total FROM orders", conn)
    sales = pd.read_sql("SELECT SUM(total) AS total FROM orders", conn)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Products", products.iloc[0][0])
    col2.metric("👥 Customers", customers.iloc[0][0])
    col3.metric("🧾 Orders", orders.iloc[0][0])
    col4.metric("💰 Sales", f"₹ {sales.iloc[0][0] or 0}")

    st.subheader("📈 Sales per Order")

    chart_data = pd.read_sql(
        "SELECT order_date, total FROM orders", conn
    )

    if not chart_data.empty:
        st.line_chart(chart_data.set_index("order_date"))