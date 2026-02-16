import streamlit as st

st.title("Balcones")

def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Microsoft", on_click=st.login)

if not st.user.is_logged_in:
    login_screen()
else:
    pages = {
        "Timesheet": [
            st.Page("pages/timesheet_upload.py", title="Upload")
        ],
        "Reports": [
            st.Page("pages/reports.py", title="Reports")
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()

st.button("Log out", on_click=st.logout)

