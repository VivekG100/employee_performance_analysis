import streamlit as st

st.set_page_config(page_title="Manager Dashboard", page_icon="📋")

if st.session_state.get("role") != "Manager":
    st.warning("Access denied. Manager login required.")
    st.stop()

st.title("📋 Manager Dashboard")
st.write("Welcome, Manager! You can access employee data and rewards.")

# Add links or tools here (like full employee list, reward history, etc.)
