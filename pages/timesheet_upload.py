import streamlit as st

from handlers.database_connection_handler import DatabaseConnectionHandler
from handlers.timesheet_handler import TimesheetHandler

# Timesheet upload page. Allows users to upload an excel file with timesheet data, preview the data, and submit it to the database. 
# The timesheet data is validated against the database to ensure that all job numbers in the timesheet exist in the database before allowing submission.
st.header("Timesheet Upload")
timesheet = st.file_uploader("Select File", type = ".xlsx")

if timesheet:

    # Read the timesheet data and display a preview
    timesheet_handler = TimesheetHandler()
    timesheet_handler.read_timesheet(timesheet)
    data_preview = timesheet_handler.get_timesheet_data()
    st.dataframe(data_preview)

    # Get the distinct job numbers from the timesheet data and validate them against the database
    distinct_job_numbers = list(set([i["job_number"] for i in data_preview]))

    if len(distinct_job_numbers) >= 0:
        database_connection_handler = DatabaseConnectionHandler()
        database_connection_handler.connect()

        employee_id = database_connection_handler.get_employee_id(data_preview[0]["employee_name"])

        # Check if the timesheet data is already loaded
        employee_time_entry_id = database_connection_handler.get_employee_time_entry_id(
            employee_id = employee_id,
            job_number = data_preview[0]["job_number"],
            work_date = data_preview[0]["work_date"],
            hours_worked = data_preview[0]["hours_worked"]
        )

        if employee_time_entry_id:
            st.warning("Some of this timesheet data appears to already be loaded in the database.")

        all_job_numbers = database_connection_handler.get_all_jobs(cache_seconds=0)

        # Validate that all job numbers in the timesheet exist in the database
        for job_number in distinct_job_numbers:
            if job_number not in all_job_numbers:
                st.error(f"Job number {job_number} does not exist in the database. Please add it before continuing.")
                st.stop()
            
        submit_timesheet_button = st.button("Submit Timesheet")

        if submit_timesheet_button:
            
            # Submit the timesheet data to the database
            database_connection_handler.load_timesheet_data(data_preview)
            st.success("Timesheet data loaded into database!")

                