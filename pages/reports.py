import streamlit as st

from handlers.database_connection_handler import DatabaseConnectionHandler

def get_data():
    """
    Get the data from the database.
    """

    # Create a database connection handler
    db_handler = DatabaseConnectionHandler()

    # Connect to the database
    db_handler.connect()

    # Get the data from the table
    data = db_handler.get_mtcars()

    return data

st.dataframe(get_data())