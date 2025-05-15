import sqlite3
import pandas as pd

def write_database(matched_test_points: pd.DataFrame, db_path="db/ideal.db"):
    """
    Writes the matched test points to an SQLite database.
    If the table does not exist, it will be created.

    Args:
        matched_test_points (pd.DataFrame): DataFrame containing columns ['x', 'y', 'ideal_func', 'delta_y'].
        db_path (str): Path to the SQLite database file.
    """

    # Connect to the SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS matched_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        x REAL,
        y REAL,
        ideal_func TEXT,
        delta_y REAL
    );
    """
    cursor.execute(create_table_query)

    # Prepare the data for insertion
    # Only keep the required columns and convert to list of tuples
    records_to_insert = matched_test_points[['x', 'y', 'ideal_func', 'delta_y']].values.tolist()

    # Insert the data into the table
    insert_query = """
    INSERT INTO matched_points (x, y, ideal_func, delta_y)
    VALUES (?, ?, ?, ?)
    """
    cursor.executemany(insert_query, records_to_insert)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print(f"Successfully wrote {len(records_to_insert)} matched test points to the database at {db_path}.")

# Notes:
# - This function will create the database file and table if they do not exist.
# - Each call appends new records to the table 'matched_points'.
# - The table includes an auto-incrementing primary key 'id' for uniqueness.