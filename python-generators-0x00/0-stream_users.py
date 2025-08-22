#!/usr/bin/python3
"""
    This module contains functions that stream user data from the database
"""

def stream_users():
    """
    This function streams user data from a CSV file line by line.
    """
    with open("user_data.csv", "r") as f:
        for row in f:
            yield row

# Make the module return the function when imported
import sys
sys.modules[__name__] = stream_users