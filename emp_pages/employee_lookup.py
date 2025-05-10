import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()  # Clean up any extra spaces

st.title("🔍 Find Employee by ID")

# Input field
emp_id = st.text_input("Enter Employee ID:")

# Update the column name below once you confirm it
column_name = "Employee_ID"  # ← Change this if needed based on actual column name

if emp_id:
    try:
        match = df[df[column_name].astype(str).str.strip().str.lower() == emp_id.strip().lower()]
        if not match.empty:
            st.success("Employee Found:")
            st.dataframe(match)
        else:
            st.error("No employee found with this ID.")
    except KeyError:
        st.error(f"Column '{column_name}' not found in the CSV. Please check column names above.")
