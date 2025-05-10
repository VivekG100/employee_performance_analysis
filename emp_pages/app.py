import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model and scaler
scaler = joblib.load("scaler.pkl")
model = joblib.load("model.pkl")

# Load the CSV data
df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()  # Clean column names

# Styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1522202176988-66273c2fd55f");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Employee Performance Score Prediction")
st.divider()
st.write("Enter the values below and click the button to predict performance.")

# Input fields for prediction
years = st.number_input("Enter the years at company", min_value=0, max_value=15, value=0)
salary = st.number_input("Enter monthly salary", min_value=0, max_value=100000, value=0)
overtime = st.number_input("Enter overtime hours", min_value=0, max_value=100, value=0)
promotions = st.number_input("Enter promotions", min_value=0, max_value=10, value=0)
satisfaction = st.number_input("Enter employee satisfaction", min_value=0.0, max_value=5.0)

x = [years, salary, overtime, promotions, satisfaction]

st.divider()
if st.button("Predict the performance score!"):
    x1 = np.array(x)
    x_array = scaler.transform([x1])
    prediction = model.predict(x_array)[0]

    # Try to match input with a row in data.csv
    match = df[
        (df['Years_At_Company'] == years) &
        (df['Monthly_Salary'] == salary) &
        (df['Overtime_Hours'] == overtime) &
        (df['Promotions'] == promotions) &
        (df['Employee_Satisfaction_Score'] == satisfaction)
    ]
    if not match.empty:
        emp_id = match.iloc[0]['Employee_ID']
    else:
        emp_id = "Unknown"

    # Display result
    st.markdown(
        f"<h1 style='font-size:28px; color:yellow;'>Employee ID: {emp_id}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h1 style='font-size:28px; color:lightgreen;'>Performance Score: {prediction}</h1>",
        unsafe_allow_html=True
    )

        # 🎯 Reward eligibility
    if prediction in [4, 5]:
        st.success("🎉 You are eligible for a reward!")

        # ✅ Redeem Reward Button → redirects to rewards page
        if st.button("🎁 Redeem Reward"):
            st.session_state["reward_claimed"] = True
            st.query_params.update({"pages": "rewards.py"})
            st.rerun()
    else:
        st.info("No reward eligibility at this time.")



