"""
data_handler.py
Classes for loading CSV data for training, ideal, and test datasets.
Includes inheritance and custom exception handling.
"""

import pandas as pd

class DataLoadError(Exception):
    """Custom exception for data loading errors."""
    pass

class DataHandler:
    """
    Base class for loading CSV data.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load(self):
        """
        Loads CSV data into a DataFrame.
        Raises DataLoadError if loading fails.
        """
        try:
            self.data = pd.read_csv(self.filepath)
        except Exception as e:
            raise DataLoadError(f"Failed to load {self.filepath}: {e}")

class TrainingDataHandler(DataHandler):
    """
    Handles loading of training data.
    Inherits from DataHandler.
    """
    def __init__(self, filepath):
        super().__init__(filepath)

class IdealFunctionHandler(DataHandler):
    """
    Handles loading of ideal function data.
    Inherits from DataHandler.
    """
    def __init__(self, filepath):
        super().__init__(filepath)

class TestDataHandler(DataHandler):
    """
    Handles loading of test data.
    Inherits from DataHandler.
    """
    def __init__(self, filepath):
        super().__init__(filepath)