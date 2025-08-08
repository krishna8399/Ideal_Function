"""
test_main.py
Unit tests for all major modules in the Ideal Function Assignment project.
"""

import pandas as pd
from src.data_handler import TrainingDataHandler, IdealFunctionHandler, TestDataHandler, DataLoadError
from src.function_matcher import FunctionMatcher
from src.test_assigner import TestAssigner
from src.database_writer import DatabaseWriter

def test_training_data_handler():
    """Test loading of training data."""
    handler = TrainingDataHandler("data/train.csv")
    handler.load()
    assert handler.data is not None
    assert not handler.data.empty

def test_ideal_function_handler():
    """Test loading of ideal function data."""
    handler = IdealFunctionHandler("data/ideal.csv")
    handler.load()
    assert handler.data is not None
    assert not handler.data.empty

def test_test_data_handler():
    """Test loading of test data."""
    handler = TestDataHandler("data/test.csv")
    handler.load()
    assert handler.data is not None
    assert not handler.data.empty

def test_function_matcher():
    """Test matching of training functions to ideal functions."""
    train = pd.read_csv("data/train.csv")
    ideal = pd.read_csv("data/ideal.csv")
    matcher = FunctionMatcher(train, ideal)
    matches = matcher.best_ideal_matches()
    assert isinstance(matches, list)
    assert len(matches) == 4

def test_test_assigner():
    """Test assignment of test points to ideal functions."""
    train = pd.read_csv("data/train.csv")
    ideal = pd.read_csv("data/ideal.csv")
    test = pd.read_csv("data/test.csv")
    matcher = FunctionMatcher(train, ideal)
    matches = matcher.best_ideal_matches()
    assigner = TestAssigner(test, ideal, matches, train)
    matched = assigner.assign()
    assert isinstance(matched, pd.DataFrame)
    assert 'delta_y' in matched.columns

def test_database_writer(tmp_path):
    """Test writing all tables to the database."""
    train = pd.read_csv("data/train.csv")
    ideal = pd.read_csv("data/ideal.csv")
    test = pd.read_csv("data/test.csv")
    matcher = FunctionMatcher(train, ideal)
    matches = matcher.best_ideal_matches()
    assigner = TestAssigner(test, ideal, matches, train)
    matched = assigner.assign()
    db_path = tmp_path / "test_ideal.db"
    db_writer = DatabaseWriter(db_path=str(db_path))
    db_writer.write_training_data(train)
    db_writer.write_ideal_functions(ideal)
    db_writer.write_matched_points(matched)
    assert db_path.exists()
