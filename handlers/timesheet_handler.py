import io

import pandas as pd

class TimesheetHandler:
    def __init__(self):
        self.timesheet_io = None
        self.timesheet_df = None
        self.timesheet_data = None

    def read_timesheet(self, file: io.BytesIO):
        """
        Read a timesheet and extract import data such as jobs and hours.
        We expect an exact timesheet format. 
        
        params:
            file (io.BytesIO): Should be the file data from the streamlit file upload.
        """
        self.timesheet_io = file
        self.timesheet_df = pd.read_excel(file)

        # Grab employee name
        employee_name = self.timesheet_df.iloc[1, 3]

        # Iterate over the days of the week to get the hours worked by job number
        full_result = []
        for i in range(0, 7):
            work_date = self.timesheet_df.iloc[3, i]

            jobs_hours = (
                self.timesheet_df
                .iloc[5:31, i:9]
                .rename(columns={self.timesheet_df.columns[i]: "hours_worked", "Unnamed: 8": "job_number"}, inplace=False)
                [["job_number", "hours_worked"]]
                .dropna(inplace=False)
                .query("hours_worked > 0", inplace=False)
                .reset_index(drop=True, inplace=False)
                .assign(work_date = work_date)
                .assign(employee_name = employee_name)
            )

            result = jobs_hours.to_dict(orient="records")

            if len(jobs_hours) > 0:
                full_result.extend(result)

        self.timesheet_data = full_result

    def get_timesheet_data(self):
        """
        Get the processed timesheet data.

        Returns:
            list: A list of dictionaries containing the timesheet data.
        """
        
        return self.timesheet_data 
