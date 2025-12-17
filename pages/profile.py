import streamlit as st
from db import change_username, change_password
from darkmode import apply_theme

# HIDE DETAILS PAGE FROM SIDEBAR
st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:nth-child(3) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
# DarkMode
apply_theme()

st.title("👤 Profile Settings")

# Cek login
if "user" not in st.session_state:
    st.error("You must login first!")
    st.stop()

user = st.session_state["user"]

st.write(f"### Welcome, **{user['username']}**!")
st.markdown("---")

st.subheader("Change Username")
new_username = st.text_input("New Username", value=user['username'])

if st.button("Save Username"):
    if new_username.strip() == "":
        st.error("Username cannot be empty.")
    else:
        success = change_username(user['id'], new_username)
        if success:
            st.success("Username updated! Please login again.")
        else:
            st.error("Failed to update username. Username might already exist.")

st.markdown("---")

st.subheader("Change Password")
new_password = st.text_input("New Password", type="password")

if st.button("Save Password"):
    if new_password.strip() == "":
        st.error("Password cannot be empty.")
    else:
        success = change_password(user['id'], new_password)
        if success:
            st.success("Password updated successfully!")
        else:
            st.error("Failed to update password.")

st.markdown("---")
st.info("Changes take effect immediately.")
