import streamlit as st

st.title("Balcones")

def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Microsoft", on_click=st.login)

if not st.user.is_logged_in:
    login_screen()
else:
    st.switch_page("pages/home.py")

st.button("Log out", on_click=st.logout)

