import streamlit as st
import pandas as pd
import numpy as np
import joblib

def run():
    st.title("📋 Manager Dashboard")

    # Sidebar navigation
    page = st.sidebar.selectbox("Select a Page", ["Prediction", "Employee Lookup", "Rewards"])

    # Load data and model
    scaler = joblib.load("scaler.pkl")
    model = joblib.load("model.pkl")
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip()

    # 1️⃣ Prediction Page
    if page == "Prediction":
        st.subheader("🧠 Predict Employee Performance")

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
            st.markdown(f"**Predicted Performance Score:** `{prediction}`")

            if prediction in [4, 5]:
                st.success("🎉 Eligible for reward!")
            else:
                st.info("Not eligible for reward.")

    # 2️⃣ Employee Lookup Page
    elif page == "Employee Lookup":
        st.subheader("🔍 Search Employee by ID")

        emp_id_input = st.text_input("Enter Employee ID:")

        if emp_id_input:
            result = df[df['Employee_ID'].astype(str).str.lower() == emp_id_input.strip().lower()]
            if not result.empty:
                st.success("Employee found:")
                st.dataframe(result)
            else:
                st.error("No matching employee found.")

    # 3️⃣ Rewards Page
    elif page == "Rewards":
        st.subheader("🎁 Rewards Info")

        if st.session_state.get("reward_claimed"):
            st.success("✅ An employee has claimed a reward this session.")
        else:
            st.info("No rewards claimed in this session.")

    # 4️⃣ Bottom-Centered Logout Button
    st.markdown("""
        <style>
        .logout-button {
            position: fixed;
            bottom: 20px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            z-index: 9999;
        }
        </style>
        <div class="logout-button">
            <form action="">
                <button name="logout-button" type="submit" style="
                    background-color: #ff4b4b;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;">
                    🚪 Logout
                </button>
            </form>
        </div>
    """, unsafe_allow_html=True)

    # Streamlit button handler
    if "logout-button" in st.query_params:
        st.session_state.clear()
        st.rerun()
