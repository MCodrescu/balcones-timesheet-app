import streamlit as st

st.title("Balcones")

pages = {
    "Timesheet": [
        st.Page("pages/timesheet_upload.py", title="Upload")
    ],
    "Reports": [
        st.Page("pages/reports.py", title="Job Report")
    ]
}

pg = st.navigation(pages, position="top")
pg.run()

