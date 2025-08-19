"""
data_handler.py
Classes for managing training, candidate, and test datasets.
Each handler loads and validates its respective dataset, raising a custom error if loading fails.
"""

from src.data_loader import load_csv

class DataLoadError(Exception):
    """Custom exception for data loading errors to make error handling explicit."""
    pass

class TrainingDataHandler:
    """
    Handles loading and validation of training data.
    Using a class allows for future extension (e.g., preprocessing, feature engineering).
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load(self):
        # Load training data and validate expected columns.
        try:
            self.data = load_csv(self.filepath, expected_columns=['x', 'y1', 'y2', 'y3', 'y4'])
        except Exception as e:
            # Raise a custom error for clarity in main workflow.
            raise DataLoadError(f"Training data load failed: {e}")

class IdealFunctionHandler:
    """
    Handles loading and validation of candidate models (ideal functions).
    This class can be extended for model selection or filtering.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load(self):
        # Load candidate models and validate expected columns.
        expected_cols = ['x'] + [f'y{i}' for i in range(1, 51)]
        try:
            self.data = load_csv(self.filepath, expected_columns=expected_cols)
        except Exception as e:
            raise DataLoadError(f"Candidate models load failed: {e}")

class TestDataHandler:
    """
    Handles loading and validation of test data.
    Encapsulating this logic makes it easier to add test data checks or transformations.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load(self):
        # Load test data and validate expected columns.
        try:
            self.data = load_csv(self.filepath, expected_columns=['x', 'y'])
        except Exception as e:
            raise DataLoadError(f"Test data load failed: {e}")