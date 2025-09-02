import sqlite3
import functools
from datetime import datetime

class ExecuteQuery:
    """
    A class-based custom context manager that executes a given query with parameters
    and returns the result.
    """
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Usage example
with ExecuteQuery("database.db", "SELECT * FROM users WHERE age > ?", (25,)) as result:
    print(result)