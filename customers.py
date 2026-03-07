import streamlit as st
import pandas as pd
from db import get_connection

def customers_page():
    st.markdown("<h2 style='color:#1F618D;'>👥 Customer Management</h2>", unsafe_allow_html=True)
    conn = get_connection()
    cur = conn.cursor()

    # SHOW CUSTOMERS
    df = pd.read_sql("SELECT * FROM customers", conn)
    st.subheader("📋 Customer List")
    st.dataframe(df)

    st.divider()

    # ADD CUSTOMER
    st.subheader("➕ Add Customer")
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone")

    if st.button("Add Customer"):
        cur.execute(
            "INSERT INTO customers(name,phone) VALUES(%s,%s)",
            (name, phone)
        )
        conn.commit()
        st.success("✅ Customer Added")
        st.rerun()

    st.divider()

    # UPDATE CUSTOMER
    st.subheader("✏️ Update Customer")

    customer_names = df["name"].tolist()
    selected = st.selectbox("Select Customer", customer_names)

    cust = df[df["name"] == selected].iloc[0]

    new_name = st.text_input("New Name", value=cust["name"])
    new_phone = st.text_input("New Phone", value=cust["phone"])

    if st.button("Update Customer"):
        cur.execute(
            "UPDATE customers SET name=%s, phone=%s WHERE id=%s",
            (new_name, new_phone, int(cust["id"]))
        )
        conn.commit()
        st.success("✏️ Customer Updated")
        st.rerun()

    st.divider()

    # DELETE CUSTOMER
    st.subheader("🗑️ Delete Customer")

    delete_customer = st.selectbox("Customer to Delete", customer_names, key="del_cust")

    if st.button("Delete Customer"):
        cur.execute("""
            SELECT COUNT(*) FROM orders
            WHERE customer_id = (SELECT id FROM customers WHERE name=%s)
        """, (delete_customer,))
        count = cur.fetchone()[0]

        if count > 0:
            st.error("❌ Customer has orders, cannot delete")
        else:
            cur.execute("DELETE FROM customers WHERE name=%s", (delete_customer,))
            conn.commit()
            st.success("🗑️ Customer Deleted")
            st.rerun()