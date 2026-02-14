import streamlit as st


class DatabaseConnectionHandler:
    def __init__(self):
        self.conn = None

    def connect(self):
        """
        Connect to the database. Database will depend on env: dev or prod.

        params:
            env (str): The environment name.

        """
        self.conn = st.connection("balcones", type = "sql")

    def get_table(self, table_name):
        """
        Get the data from a table.
        """
        result = self.conn.query(f"SELECT * FROM job_register.{table_name}")
        return result
