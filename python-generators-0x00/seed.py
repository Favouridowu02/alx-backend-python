#!/usr/bin/env python3
"""
This module contains functions that seeds to the database
"""
from sqlalchemy import create_engine

def connect_db():
    """
        This Function is used to connect with the Database
    """
    engine = create_engine('mysql+pymysql://user:password@localhost:3306')
    print("connections successfully")
    return engine

def create_database(connection):
    """
        This Function is used to create a database

        Args:
            connection: The database connection object
    """
    with connection.connect() as conn:
        conn.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created if not exist successfully")

def connect_to_prodev():
    """
        This Function is used to connect to the ALX_prodev database
    """
    return create_engine('mysql+pymysql://user:password@localhost:3306/ALX_prodev')

def create_table(connection):
    """
        This Function creates a table user_data if it does not exists with the required fields
    """
    with connection.connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_data
                user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                age DECIMAL NOT NULL
            )
        """)
        print("Table user_data created if not exist successfully")

def insert_data(connection, data):
    """
        This Function inserts data into the user_data table from a CSV file

        Args:
            connection: The database connection object
            data: The path to the CSV file containing user data
    """
    with connection.connect() as conn:
        conn.execute("""
            LOAD DATA INFILE '{}'
            INTO TABLE user_data
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\\n'
            IGNORE 1 ROWS
            (name, email, age)
        """.format(data))