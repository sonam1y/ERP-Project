import streamlit as st
from login import login_page
from dashboard import dashboard_page

st.set_page_config(page_title="ERP System", layout="wide")

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# 🔁 ROLE SWITCHER (Always Visible)
with st.sidebar:
    st.title("ERP MENU")

    role_choice = st.radio(
        "Select Role",
        ["Admin", "Staff"],
        index=0 if st.session_state.role == "admin" else 1
        if st.session_state.role == "staff" else 0
    )

    selected_role = role_choice.lower()

    # 🔄 Auto logout when role changes
    if st.session_state.role and selected_role != st.session_state.role:
        st.session_state.logged_in = False
        st.session_state.role = selected_role
        st.session_state.username = None
        st.warning("Role changed. Please login again.")
        st.rerun()

    if st.session_state.logged_in:
        st.write(f"👤 {st.session_state.role.capitalize()}")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None
            st.rerun()

# 🧠 PAGE LOGIC
if not st.session_state.logged_in:
    login_page()
else:
    dashboard_page()