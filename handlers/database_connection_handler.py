import streamlit as st


class DatabaseConnectionHandler:
    def __init__(self):
        self.conn = None

    def connect(self):
        """
        Connect to the database. Connection details are stored in secrets.toml
        """
        self.conn = st.connection("sql")

    def get_mtcars(self):
        """
        Get the data from the mtcars table.
        """
        result = self.conn.query(f"SELECT * FROM job_register.mtcars")
        return result
    
    def get_employee_id(self, employee_name):
        """
        Get the employee id from the employee name.

        params:
            employee_name (str): The name of the employee.  
        """

        with self.conn.session as session:
            result = session.execute(
                "SELECT employee_id FROM job_register.employees WHERE employee_name = :employee_name",
                {"employee_name": employee_name}
            ).fetchone()

        return result[0] if result else None
    
    def load_timesheet_data(self, timesheet_data, test = False):
        """
        Load the timesheet data into the database.

        params:
            timesheet_data (list): A list of dictionaries containing the timesheet data.
                Should be the result of the get_timesheet_data method from the TimesheetHandler class.
            test (bool): If True, the transaction will be rolled back instead of committed.
        """
        
        employee_id = self.get_employee_id(timesheet_data[0]["employee_name"])

        with self.conn.session as session:
            session.begin()
            for row in timesheet_data:
                session.execute(
                    "INSERT INTO job_register.employee_time (employee_id, job_number, work_date, hours_worked) VALUES (:employee_id, :job_number, :work_date, :hours_worked)",
                    {"employee_id": employee_id, "job_number": row["job_number"], "work_date": row["work_date"], "hours_worked": row["hours_worked"]}
                )
            if test:
                session.rollback()
            else:
                session.commit()
            
