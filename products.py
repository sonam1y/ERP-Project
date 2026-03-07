import streamlit as st
import pandas as pd
from db import get_connection

def products_page():
    st.markdown("<h2 style='color:#7D3C98;'>📦 Product Management</h2>", unsafe_allow_html=True)
    conn = get_connection()
    cur = conn.cursor()

    # SHOW PRODUCTS
    df = pd.read_sql("SELECT * FROM products", conn)
    st.subheader("📋 Product List")
    st.dataframe(df)

    st.divider()

    # ADD PRODUCT
    st.subheader("➕ Add Product")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)

    if st.button("Add Product"):
        cur.execute(
            "INSERT INTO products(name,price,stock) VALUES(%s,%s,%s)",
            (name, price, stock)
        )
        conn.commit()
        st.success("✅ Product Added")
        st.rerun()

    st.divider()

    # UPDATE PRODUCT
    st.subheader("✏️ Update Product")

    product_names = df["name"].tolist()
    selected = st.selectbox("Select Product", product_names)

    prod = df[df["name"] == selected].iloc[0]

    new_price = st.number_input("New Price", value=float(prod["price"]))
    new_stock = st.number_input("New Stock", value=int(prod["stock"]))

    if st.button("Update Product"):
        cur.execute(
            "UPDATE products SET price=%s, stock=%s WHERE name=%s",
            (new_price, new_stock, selected)
        )
        conn.commit()
        st.success("✏️ Product Updated")
        st.rerun()

    st.divider()

    # DELETE PRODUCT
    st.subheader("🗑️ Delete Product")

    delete_product = st.selectbox("Product to Delete", product_names, key="del_prod")

    if st.button("Delete Product"):
        cur.execute("""
            SELECT COUNT(*) FROM order_items
            WHERE product_id = (SELECT id FROM products WHERE name=%s)
        """, (delete_product,))
        count = cur.fetchone()[0]

        if count > 0:
            st.error("❌ Product used in orders, cannot delete")
        else:
            cur.execute("DELETE FROM products WHERE name=%s", (delete_product,))
            conn.commit()
            st.success("🗑️ Product Deleted")
            st.rerun()