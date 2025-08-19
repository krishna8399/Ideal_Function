import pytest
import pandas as pd
from src.function_matcher import FunctionMatcher

@pytest.fixture
def sample_training_data():
    # Minimal sample for testing
    return pd.DataFrame({
        'x': [1, 2, 3],
        'y1': [1.0, 2.0, 3.0],
        'y2': [2.0, 3.0, 4.0],
        'y3': [3.0, 4.0, 5.0],
        'y4': [4.0, 5.0, 6.0]
    })

@pytest.fixture
def sample_candidate_models():
    return pd.DataFrame({
        'x': [1, 2, 3],
        'y1': [1.1, 2.1, 3.1],
        'y2': [2.1, 3.1, 4.1],
        'y3': [3.1, 4.1, 5.1],
        'y4': [4.1, 5.1, 6.1],
        'y5': [5.1, 6.1, 7.1]
    })

def test_select_closest_function(sample_training_data, sample_candidate_models):
    matcher = FunctionMatcher(sample_training_data, sample_candidate_models)
    matches = matcher.select_closest_function()
    assert isinstance(matches, list), "Matches should be a list"
    assert all('train_col' in m and 'ideal_col' in m for m in matches), "Each match should have train_col and ideal_col"