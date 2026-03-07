import streamlit as st
import pandas as pd
from db import get_connection
from datetime import date

def orders_page():
    st.markdown("<h2 style='color:#117864;'>🧾 Order Management</h2>", unsafe_allow_html=True)
    conn = get_connection()
    cur = conn.cursor()

    # SHOW ORDERS
    orders_df = pd.read_sql("""
        SELECT o.id, c.name customer, o.total, o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
    """, conn)

    st.subheader("📋 Orders List")
    st.dataframe(orders_df)

    st.divider()

    # CREATE ORDER
    st.subheader("➕ Create Order")

    customers = pd.read_sql("SELECT id,name FROM customers", conn)
    products = pd.read_sql("SELECT id,name,price,stock FROM products", conn)

    customer = st.selectbox("Customer", customers["name"])
    product = st.selectbox("Product", products["name"])
    qty = st.number_input("Quantity", min_value=1)

    if st.button("Place Order"):
        prod = products[products["name"] == product].iloc[0]

        if qty > prod["stock"]:
            st.error("❌ Not enough stock")
            return

        total = qty * prod["price"]

        cur.execute(
            "INSERT INTO orders(customer_id,total,order_date) VALUES(%s,%s,%s)",
            (
                int(customers[customers["name"] == customer]["id"].iloc[0]),
                total,
                date.today()
            )
        )
        order_id = cur.lastrowid

        cur.execute(
            "INSERT INTO order_items(order_id,product_id,quantity,price) VALUES(%s,%s,%s,%s)",
            (order_id, int(prod["id"]), qty, prod["price"])
        )

        cur.execute(
            "UPDATE products SET stock = stock - %s WHERE id=%s",
            (qty, int(prod["id"]))
        )

        conn.commit()
        st.success("✅ Order Created")
        st.rerun()

    st.divider()

    # DELETE ORDER
    st.subheader("🗑️ Delete Order")

    order_ids = orders_df["id"].tolist()
    delete_order = st.selectbox("Select Order ID", order_ids)

    if st.button("Delete Order"):
        cur.execute("DELETE FROM order_items WHERE order_id=%s", (delete_order,))
        cur.execute("DELETE FROM orders WHERE id=%s", (delete_order,))
        conn.commit()
        st.success("🗑️ Order Deleted")
        st.rerun()