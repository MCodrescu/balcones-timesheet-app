import streamlit as st

st.title("Balcones Timesheet Application")

pages = {
    "Timesheet": [
        st.Page("pages/timesheet_upload.py", title="Upload")
    ],
    "Reports": [
        st.Page("pages/job_report.py", title="Job Report")
    ]
}

pg = st.navigation(pages, position="top")
pg.run()

