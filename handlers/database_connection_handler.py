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
