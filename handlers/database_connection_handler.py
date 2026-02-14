import os
import psycopg2
import pandas as pd

from psycopg2 import sql
import pandas.io.sql as sqlio
from streamlit import columns

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT")

class DatabaseConnectionHandler:
    def __init__(self):
        self.conn = None

    def connect(self, database):
        """
        Connect to the database. Database will depend on env: dev or prod.

        params:
            database (str): The database name.
        """
        self.conn = psycopg2.connect(
            host = DATABASE_URL,
            database = database,
            user = DATABASE_USER,
            password = DATABASE_PASSWORD,
            port = DATABASE_PORT
        )

    def get_table(self, table_name):
        """
        Get the data from a table.
        """

        # Start a cursor to execute queries
        cursor = self.conn.cursor()

        # Use identifier for table name to prevent SQL injection
        query = sql.SQL("SELECT * FROM job_register.{}").format(
            sql.Identifier(table_name)
        )

        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()

        # Get column names
        columns = [column[0] for column in cursor.description]

        # Create dictionary of results
        result = [dict(zip(columns, row)) for row in results]
        cursor.close()

        return result