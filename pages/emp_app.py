import streamlit as st
import pandas as pd
import numpy as np
import joblib

def run():
    # ❌ Hide the sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Load resources
    scaler = joblib.load("scaler.pkl")
    model = joblib.load("model.pkl")
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip()

    st.title("🎯 Employee Performance Score Prediction")
    st.write("Enter details below and predict your performance score.")

    # Input fields
    years = st.number_input("Years at company", 0, 15)
    salary = st.number_input("Monthly salary", 0, 100000)
    overtime = st.number_input("Overtime hours", 0, 100)
    promotions = st.number_input("Number of promotions", 0, 10)
    satisfaction = st.number_input("Satisfaction score (0.0–5.0)", 0.0, 5.0)

    x = [years, salary, overtime, promotions, satisfaction]

    if st.button("Predict"):
        x_array = scaler.transform([x])
        prediction = model.predict(x_array)[0]

        match = df[
            (df['Years_At_Company'] == years) &
            (df['Monthly_Salary'] == salary) &
            (df['Overtime_Hours'] == overtime) &
            (df['Promotions'] == promotions) &
            (df['Employee_Satisfaction_Score'] == satisfaction)
        ]

        emp_id = match.iloc[0]['Employee_ID'] if not match.empty else "Unknown"

        st.markdown(f"**Employee ID:** `{emp_id}`")
        st.markdown(f"**Performance Score:** `{prediction}`")

        if prediction in [4, 5]:
            st.success("🎉 You are eligible for a reward!")
            if st.button("🎁 Redeem Reward"):
                st.session_state["reward_claimed"] = True
                st.switch_page("pages/rewards.py")
        else:
            st.info("Not eligible for a reward.")

    # 🧾 Centered logout button at bottom
    st.markdown("""
        <style>
        .logout-button {
            display: flex;
            justify-content: center;
            position: fixed;
            bottom: 20px;
            left: 0;
            right: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.clear()
            st.rerun()
