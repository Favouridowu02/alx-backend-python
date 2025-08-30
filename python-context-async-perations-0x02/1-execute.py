import sqlite3
import functools
from datetime import datetime

class ExecuteQuery:
    """
    A class to represent a a reusable context manager that takes a query as input and executes it, managing both connection and the query execution
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
with ExecuteQuery("database.db") as db:
    db.execute("SELECT * FROM users WHERE age > ?", (25,))