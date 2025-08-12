"""
database_writer.py
Class for writing training data, ideal functions, and matched test points to an SQLite database using SQLAlchemy.
"""

import os
from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

class DatabaseWriter:
    """
    Handles writing training data, ideal functions, and matched test points to an SQLite database using SQLAlchemy.
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
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('x', Float),
            Column('y1', Float),
            Column('y2', Float),
            Column('y3', Float),
            Column('y4', Float)
        )

        # Define ideal functions table schema
        ideal_columns = [Column('x', Float)]
        ideal_columns += [Column(f'y{i}', Float) for i in range(1, 51)]
        self.ideal_functions = Table(
            'ideal_functions', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            *ideal_columns
        )

        # Define matched test points table schema
        self.matched_points = Table(
            'matched_points', self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('x', Float),
            Column('y', Float),
            Column('ideal_func', String),
            Column('delta_y', Float)
        )

        # Create all tables if they don't exist
        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        print("Writing to DB file:", os.path.abspath("db/ideal.db"))

    def write_training_data(self, train_df):
        """
        Writes training data to the database.
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
        Writes ideal functions to the database.
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

    def write_matched_points(self, matched_test_points):
        """
        Writes matched test points to the database.
        """
        if matched_test_points.empty:
            print("Matched Test Points DataFrame is empty. Nothing to write.")
            return
        data_to_insert = [
            {
                'x': row['x'],
                'y': row['y'],
                'ideal_func': row['ideal_func'],
                'delta_y': row['delta_y']
            }
            for _, row in matched_test_points.iterrows()
        ]
        with self.engine.begin() as conn:
            conn.execute(self.matched_points.insert(), data_to_insert)
            result = conn.execute(self.matched_points.select())
            print("Rows in matched_points table after insert:", len(result.fetchall()))

        print(matched_test_points.shape)