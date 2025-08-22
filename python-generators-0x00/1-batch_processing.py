#!/usr/bin/python3
"""
"""

import csv

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of user rows from user_data.csv as dicts.
    Each batch is a list of dicts with length up to batch_size.
    """
    batch = []
    with open("user_data.csv", "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

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

 