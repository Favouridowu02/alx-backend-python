import sqlite3
import functools
from datetime import datetime

class DatabaseConnection:
    """
    A class to represent a database connection.
    """
    def __init__(self, db_name):
        self.db_name = db_name
    def __enter__(self):
        print(f"Connecting to the database: {self.db_name}")
        self.conn = sqlite3.connect(database=self.db_name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Disconnecting from the database: {self.db_name}")
        self.conn.close()

# Run the Query
with DatabaseConnection("database.db") as db:
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    for user in users:
        print(user)