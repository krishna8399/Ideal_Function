import pandas as pd
from src.data_loader import load_all_data
from src.function_matcher import best_ideal_matches
from src.test_assigner import assign_test_point
from src.database_writer import write_database

def test_load_all_data():
    """
    Test that all CSV files are loaded correctly and are not empty.
    """
    train, ideal, test = load_all_data("data/ideal.csv", "data/test.csv", "data/train.csv")
    assert train is not None, "Training data not loaded"
    assert ideal is not None, "Ideal data not loaded"
    assert test is not None, "Test data not loaded"
    assert not train.empty, "Training data is empty"
    assert not ideal.empty, "Ideal data is empty"
    assert not test.empty, "Test data is empty"
    # Check for expected columns
    for col in ['x', 'y1']:
        assert col in train.columns, f"Missing column {col} in training data"
        assert col in ideal.columns, f"Missing column {col} in ideal data"

def test_best_ideal_matches():
    """
    Test that the matching function returns a list of 4 dicts (one for each training function).
    """
    train, ideal, _ = load_all_data("data/ideal.csv", "data/test.csv", "data/train.csv")
    matches = best_ideal_matches(train, ideal)
    assert isinstance(matches, list), "Matches should be a list"
    assert len(matches) == 4, "Should return 4 matches (for y1-y4)"
    for match in matches:
        assert isinstance(match, dict), "Each match should be a dict"
        assert 'ideal_col' in match, "Match dict missing 'ideal_col' key"

def test_assign_test_point():
    """
    Test that test points are assigned and the output DataFrame contains the expected columns.
    """
    train, ideal, test = load_all_data("data/ideal.csv", "data/test.csv", "data/train.csv")
    matches = best_ideal_matches(train, ideal)
    matched = assign_test_point(test, ideal, matches)
    assert isinstance(matched, pd.DataFrame), "Output should be a DataFrame"
    for col in ['x', 'y', 'ideal_func', 'delta_y']:
        assert col in matched.columns, f"Missing column {col} in matched test points"

def test_write_database(tmp_path):
    """
    Test that matched test points can be written to a database file.
    """
    train, ideal, test = load_all_data("data/ideal.csv", "data/test.csv", "data/train.csv")
    matches = best_ideal_matches(train, ideal)
    matched = assign_test_point(test, ideal, matches)
    db_path = tmp_path / "test_ideal.db"
    write_database(matched, db_path=str(db_path))
    assert db_path.exists(), "Database file was not created"
    