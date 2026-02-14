import os
import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_PORT = os.environ["DATABASE_PORT"]

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

        # Prepare the query with placeholders
        query = "SELECT * FROM %s;"

        # Execute the query with values
        cursor.execute(query, (table_name))
        results = cursor.fetchall()
        cursor.close()

        return results