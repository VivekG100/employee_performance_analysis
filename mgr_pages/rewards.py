import streamlit as st

st.title("🎁 Rewards Page")

if st.session_state.get("reward_claimed"):
    st.success("✅ Congratulations! You have successfully claimed your reward.")
    st.balloons()
else:
    st.warning("Please claim your reward from the prediction page first.")
