import streamlit as st

from sqlalchemy.sql import text


class DatabaseConnectionHandler:
    def __init__(self):
        self.conn = None

    def connect(self):
        """
        Connect to the database. Connection details are stored in secrets.toml
        """
        self.conn = st.connection("sql")

    def insert_job(self, job_number, job_name, client, job_link, test = False):
        """
        Insert a new job into the database.

        params:
            job_number (str): The job number.
            job_name (str): The job name.
            client (str): The client name.
            job_link (str): A link to the job details.
            test (bool): If True, the transaction will be rolled back instead of committed.
        """
        with self.conn.session as session:
            session.execute(
                text("INSERT INTO job_register.jobs (job_number, job_name, client, job_link) VALUES (:job_number, :job_name, :client, :job_link)"),
                {"job_number": job_number, "job_name": job_name, "client": client, "job_link": job_link}
            )
            if test:
                session.rollback()
            else:
                session.commit()

    def get_employee_time_entry_id(self, employee_id, job_number, work_date, hours_worked):
        """
        Get the employee time entry id for a given employee, job, and date.

        params:
            employee_id (int): The employee id.
            job_number (str): The job number.
            work_date (date): The date of the work.
            hours_worked (int): The number of hours worked.
        """
        with self.conn.session as session:
            result = session.execute(
                text("SELECT time_entry_id FROM job_register.employee_time WHERE employee_id = :employee_id AND job_number = :job_number AND work_date = :work_date AND hours_worked = :hours_worked"),
                {"employee_id": employee_id, "job_number": job_number, "work_date": work_date, "hours_worked": hours_worked}
            ).fetchone()

        return result[0] if result else None

    def insert_employee_time(self, employee_id, job_number, work_date, hours_worked, test = False):
        """
        Insert a new employee time entry into the database.

        params:
            employee_id (int): The employee id.
            job_number (str): The job number.
            work_date (date): The date of the work.
            hours_worked (float): The number of hours worked.
            test (bool): If True, the transaction will be rolled back instead of committed.
        """
        with self.conn.session as session:
            session.execute(
                text("INSERT INTO job_register.employee_time (employee_id, job_number, work_date, hours_worked) VALUES (:employee_id, :job_number, :work_date, :hours_worked)"),
                {"employee_id": employee_id, "job_number": job_number, "work_date": work_date, "hours_worked": hours_worked}
            )
            if test:
                session.rollback()
            else:
                session.commit()

    def get_mtcars(self):
        """
        Get the data from the mtcars table.
        """
        result = self.conn.query(f"SELECT * FROM job_register.mtcars")
        return result
    
    def get_all_jobs(self, cache_seconds = None):
        """
        Get all job numbers from the database.
        """
        result = self.conn.query(f"SELECT job_number FROM job_register.jobs INNER JOIN job_register.employee_time USING (job_number) GROUP BY job_number ORDER BY SUM(hours_worked) DESC", ttl = cache_seconds)
        return result["job_number"].to_list()
    
    def get_all_employees(self, cache_seconds = None):
        """
        Get all employee names from the database.
        """
        result = self.conn.query(f"SELECT employee_id, employee_name FROM job_register.employees", ttl = cache_seconds)
        return result

    def get_employee_id(self, employee_name):
        """
        Get the employee id from the employee name.

        params:
            employee_name (str): The name of the employee.  
        """

        with self.conn.session as session:
            result = session.execute(
                text("SELECT employee_id FROM job_register.employees WHERE employee_name = :employee_name"),
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

        for row in timesheet_data:
            self.insert_employee_time(
                employee_id = employee_id,
                job_number = row["job_number"],
                work_date = row["work_date"],
                hours_worked = row["hours_worked"],
                test = test
            )

    def get_query(self, query, params):
        """
        Get the data from the database based on a query and parameters.

        params:
            query (str): The SQL query to execute. Should use named parameters (e.g. :param_name).
            params (dict): A dictionary of parameters to pass to the query. Keys should match the named parameters in the query.
        """
        result = self.conn.query(sql = query, params = params)
        return result
            
