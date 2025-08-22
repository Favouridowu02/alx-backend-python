from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DB_URI = os.environ.get("DB_URI")

def stream_user_ages():
    """
    Generator that yields user ages one by one from the users table.
    """
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT age FROM users"))
        for row in result:
            # row['age'] may be None or string, so handle conversion
            try:
                age = int(row['age'])
                yield age
            except (ValueError, TypeError, KeyError):
                continue

def print_average_age():
    """
    Computes and prints the average age of users using the stream_user_ages generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    print_average_age()
    