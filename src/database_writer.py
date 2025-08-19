"""
database_writer.py
Class for writing training data, candidate models, and matched test points to an SQLite database using SQLAlchemy.
Handles table creation and data insertion with error handling and debug output.
"""

import os
from sqlalchemy import create_engine, Column, Float, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

class DatabaseWriter:
    """
    Handles writing results to the SQLite database.
    Each method inserts data and prints row counts for debugging.
    """

    def __init__(self, db_path="db/ideal.db"):
        # Ensure the 'db' directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.metadata = MetaData()

        # Define training data table schema
        self.training_data = Table(
            'training_data', self.metadata,
            Column('x', Float, primary_key=True),
            Column('y1', Float),
            Column('y2', Float),
            Column('y3', Float),
            Column('y4', Float)
        )

        # Define ideal functions (candidate models) table schema
        self.ideal_functions = Table(
            'ideal_functions', self.metadata,
            Column('x', Float, primary_key=True),
            *(Column(f'y{i}', Float) for i in range(1, 51))
        )

        # Define matched points table schema
        self.matched_points = Table(
            'matched_points', self.metadata,
            Column('x', Float),
            Column('y', Float),
            Column('ideal_func', String),
            Column('delta_y', Float)
        )

        # Create all tables in the database
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        print("Writing to DB file:", os.path.abspath("db/ideal.db"))

    def write_training_data(self, train_df):
        """
        Inserts training data into the database.
        Prints the number of rows inserted for verification.
        """
        if train_df.empty:
            print("Training DataFrame is empty. Nothing to write.")
            return
        data_to_insert = [
            {
                'x': row['x'],
                'y1': row['y1'],
                'y2': row['y2'],
                'y3': row['y3'],
                'y4': row['y4']
            }
            for _, row in train_df.iterrows()
        ]
        with self.engine.begin() as conn:
            conn.execute(self.training_data.insert(), data_to_insert)
            result = conn.execute(self.training_data.select())
            print("Rows in training_data table after insert:", len(result.fetchall()))

    def write_ideal_functions(self, ideal_df):
        """
        Inserts candidate models (ideal functions) into the database.
        Prints the number of rows inserted for verification.
        """
        if ideal_df.empty:
            print("Ideal Function DataFrame is empty. Nothing to write.")
            return
        data_to_insert = []
        for _, row in ideal_df.iterrows():
            entry = {'x': row['x']}
            for i in range(1, 51):
                col_name = f'y{i}'
                entry[col_name] = row.get(col_name, None)
            data_to_insert.append(entry)
        with self.engine.begin() as conn:
            conn.execute(self.ideal_functions.insert(), data_to_insert)
            result = conn.execute(self.ideal_functions.select())
            print("Rows in ideal_functions table after insert:", len(result.fetchall()))

    def write_matched_points(self, matched_points_df):
        """
        Inserts matched test points into the database.
        Prints the number of rows inserted for verification.
        """
        if matched_points_df.empty:
            print("Matched Points DataFrame is empty. Nothing to write.")
            return
        data_to_insert = [
            {
                'x': row['x'],
                'y': row['y'],
                'ideal_func': row['ideal_func'],
                'delta_y': row['delta_y']
            }
            for _, row in matched_points_df.iterrows()
        ]
        with self.engine.begin() as conn:
            conn.execute(self.matched_points.insert(), data_to_insert)
            result = conn.execute(self.matched_points.select())
            print("Rows in matched_points table after insert:", len(result.fetchall()))