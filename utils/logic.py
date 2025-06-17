import random


def generate_combination(sample, size):
    return random.sample(sample, size)


def insert_combination_to_db(combination):
    # Simulate DB logic (e.g., later use pyodbc or SQLAlchemy)
    print(f"Inserting combination into DB: {combination}")
    return True
