"""
data_loader.py
Utility functions for loading CSV data with error handling and validation.
These functions centralize data loading logic for maintainability and reuse.
"""

import pandas as pd  # Pandas is used for data manipulation and analysis.

def load_csv(filepath, expected_columns=None):
    """
    Loads a CSV file and validates columns if provided.
    Returns a pandas DataFrame.
    Raises an error if columns are missing or file cannot be read.
    """
    try:
        df = pd.read_csv(filepath)
        if expected_columns:
            missing = set(expected_columns) - set(df.columns)
            if missing:
                # Validation step ensures downstream code won't fail due to missing columns.
                raise ValueError(f"Missing columns: {missing}")
        return df
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        raise

def preview_data(df, num_rows=5):
    """
    Prints a preview of the DataFrame for quick inspection.
    Useful for debugging and verifying data integrity.
    """
    print(f"Previewing first {num_rows} rows:")
    print(df.head(num_rows))

def load_all_data(ideal_path, test_path, train_path):
    """
    Load all required CSV files for the project.

    Parameters:
        ideal_path (str): Path to the ideal functions CSV file.
        test_path (str): Path to the test data CSV file.
        train_path (str): Path to the training data CSV file.

    Returns:
        tuple: A tuple containing three pandas DataFrames:
            - train_data (DataFrame): Training data.
            - ideal_data (DataFrame): Ideal functions data.
            - test_data (DataFrame): Test data.
            If any file fails to load, its corresponding DataFrame will be None.
    """
    try:
        # Load training data
        train_data = pd.read_csv(train_path)
        print(f"Training data loaded successfully from {train_path}.")
    except Exception as e:
        print(f"Error loading training data from {train_path}: {e}")
        train_data = None

    try:
        # Load ideal functions data
        ideal_data = pd.read_csv(ideal_path)
        print(f"Ideal functions data loaded successfully from {ideal_path}.")
    except Exception as e:
        print(f"Error loading ideal functions data from {ideal_path}: {e}")
        ideal_data = None

    try:
        # Load test data
        test_data = pd.read_csv(test_path)
        print(f"Test data loaded successfully from {test_path}.")
    except Exception as e:
        print(f"Error loading test data from {test_path}: {e}")
        test_data = None

    return train_data, ideal_data, test_data