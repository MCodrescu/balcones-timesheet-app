from datetime import timedelta
from datetime import date
import streamlit as st

from handlers.database_connection_handler import DatabaseConnectionHandler

# Header
st.header("Job Report")

# Create a database connection handler
db_handler = DatabaseConnectionHandler()

# Connect to the database
db_handler.connect()

# Read SQL file for job report query
with open("sql/job_report.sql", "r") as f:
    job_report_query = f.read() 

# Get all job numbers from the database
all_job_numbers = db_handler.get_all_jobs()

job_numbers = st.multiselect("Select Job Numbers", options = all_job_numbers)
start_date = st.date_input("Start Date", value = date.today() - timedelta(days=30))
end_date = st.date_input("End Date", value = date.today())
submit_report = st.button("Submit Report")

# If the submit button is clicked, get the data from the database and display it in a table
if submit_report:

    # Get the data from the table
    data = db_handler.get_query(job_report_query, {
        "start_date": start_date,
        "end_date": end_date,
        "job_numbers": job_numbers
    })

    st.dataframe(data)