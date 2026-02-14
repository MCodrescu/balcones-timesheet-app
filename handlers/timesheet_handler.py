import io

import pandas as pd

class TimesheetHandler:
    def __init__(self):
        self.timesheet_io = None
        self.timesheet_df = None
    def read_timesheet(self, file: io.BytesIO):
        """
        Read a timesheet and extract import data such as jobs and hours.
        
        params:
            file (io.BytesIO): Should be the file data from the streamlit file upload.
        """
        self.timesheet_io = file
        self.timesheet_df = pd.read_excel(file)

    def get_timesheet_data(self):
        
        return self.timesheet_df
