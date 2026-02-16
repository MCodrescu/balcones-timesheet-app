import streamlit as st

st.title("Balcones Timesheet Application")

pages = {
    "Actions": [
        st.Page("pages/timesheet_upload.py", title="Upload Timesheet")
    ],
    "Reports": [
        st.Page("pages/job_report.py", title="Job Report")
    ],
    "Manage" : [
        st.Page("pages/new_job.py", title="Add New Job")
    ]
}

pg = st.navigation(pages, position="top")
pg.run()

