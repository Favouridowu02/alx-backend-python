#!/usr/bin/python3
"""
Batch processing users from a database using SQLAlchemy
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DB_URI = os.environ.get("DB_URI")

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user rows from the users table as dicts.
    Each batch is a list of dicts with length up to batch_size.
    """
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        offset = 0
        while True:
            result = conn.execute(
                text("SELECT * FROM users LIMIT :limit OFFSET :offset"),
                {"limit": batch_size, "offset": offset}
            )
            batch = [dict(row) for row in result]
            if not batch:
                break
            yield batch
            offset += batch_size

def batch_processing(batch_size):
    """
    This function processes each batch to filter users over the age of 25

    Arguments:
        batch_size: the batch size
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            try:
                age = int(user.get("age", 0))
            except (ValueError, TypeError):
                age = 0
            if age > 25:
                print(user)