import streamlit as st
from pages import emp_app, mgr_dashboard

# Must be first Streamlit call
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Dummy user database
USERS = {
    "employee1": {"password": "emp123", "role": "Employee"},
    "manager1": {"password": "mgr123", "role": "Manager"},
}

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ========================
# 🔐 LOGIN PAGE (NO SIDEBAR)
# ========================
if not st.session_state.logged_in:
    # Hide sidebar using CSS
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Page title and app heading
    st.title("🔐 Secure Login")
    st.markdown("<h2 style='text-align: center;'>Employee Performance Analysis System</h2>", unsafe_allow_html=True)

    # Login form
    role = st.selectbox("Select Role", ["Employee", "Manager"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = USERS.get(username)

        if user and user["password"] == password and user["role"] == role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.rerun()
        else:
            st.error("❌ Invalid username, password, or role.")

# ========================
# ✅ AFTER LOGIN
# ========================
else:
    if st.session_state.role == "Employee":
        emp_app.run()
    elif st.session_state.role == "Manager":
        mgr_dashboard.run()
