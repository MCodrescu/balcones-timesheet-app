import streamlit as st

from handlers.database_connection_handler import DatabaseConnectionHandler

st.header("Add New Job")
job_number = st.text_input("Job Number")
job_name = st.text_input("Job Name")
client = st.text_input("Client Name")
job_link = st.text_input("Job Link")
submit = st.button("Submit")

if submit:
    database_connection_handler = DatabaseConnectionHandler()
    database_connection_handler.connect()
    database_connection_handler.insert_job(job_number, job_name, client, job_link)
    st.success(f"Job {job_number} - {job_name} added to database!")