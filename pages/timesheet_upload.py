import streamlit as st

from handlers.database_connection_handler import DatabaseConnectionHandler
from handlers.timesheet_handler import TimesheetHandler

st.header("Timesheet Upload")
timesheet = st.file_uploader("Select File", type = ".xlsx")

if timesheet:
    timesheet_handler = TimesheetHandler()
    timesheet_handler.read_timesheet(timesheet)
    data_preview = timesheet_handler.get_timesheet_data()
    st.dataframe(data_preview)

    distinct_job_numbers = list(set([i["job_number"] for i in data_preview]))

    if len(distinct_job_numbers) >= 0:
        database_connection_handler = DatabaseConnectionHandler()
        database_connection_handler.connect()

        all_job_numbers = database_connection_handler.get_all_jobs()

        for job_number in distinct_job_numbers:
            if job_number not in all_job_numbers:
                st.error(f"Job number {job_number} does not exist in the database. Please add it before continuing.")
                st.stop()
            
        submit_timesheet_button = st.button("Submit Timesheet")

        if submit_timesheet_button:
            
            database_connection_handler.load_timesheet_data(data_preview, test = True)
            st.success("Timesheet data loaded into database!")

                