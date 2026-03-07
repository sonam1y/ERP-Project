import streamlit as st
from db import get_connection

def login_page():
    st.markdown("<h1 style='color:#2E86C1;'>🔐 ERP Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[0]
            st.success(f"Welcome {user[0].upper()}")
            st.rerun()
        else:
            st.error("Invalid Credentials")