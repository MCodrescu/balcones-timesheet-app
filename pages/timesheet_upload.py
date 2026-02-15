import streamlit as st

from handlers.timesheet_handler import TimesheetHandler

st.header("Timesheet Upload")
timesheet = st.file_uploader("Select File", type = ".xlsx")

if timesheet:
    timesheet_handler = TimesheetHandler()
    timesheet_handler.read_timesheet(timesheet)
    st.dataframe(timesheet_handler.get_timesheet_data())