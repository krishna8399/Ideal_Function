"""
function_matcher.py
Matches each training function to the closest candidate model using least squares.
Encapsulates matching logic for clarity and future extensibility.
"""

import numpy as np

class FunctionMatcher:
    """
    Matches training functions to candidate models using least squares.
    Designed for modularity and easy replacement of matching logic.
    """
    def __init__(self, training_data, candidate_models):
        self.training_data = training_data
        self.candidate_models = candidate_models

    def select_closest_function(self):
        """
        For each training function, finds the candidate model with the lowest sum of squared errors.
        Returns a list of dicts with match info.
        """
        matches = []
        for i in range(1, 5):
            train_col = f'y{i}'
            best_candidate, min_sse = self._find_best_candidate(train_col)
            matches.append({
                'train_col': train_col,
                'ideal_col': best_candidate,
                'min_sse': min_sse
            })
        return matches

    def best_ideal_matches(self):
        # For compatibility with main.py; both names supported.
        return self.select_closest_function()

    def _find_best_candidate(self, train_col):
        """
        Helper to find the closest candidate model for a given training column.
        Uses sum of squared errors as the matching criterion.
        """
        min_sse = float('inf')
        best_candidate = None
        train_y = self.training_data[train_col].values
        for candidate_col in [col for col in self.candidate_models.columns if col.startswith('y')]:
            candidate_y = self.candidate_models[candidate_col].values
            sse = np.sum((train_y - candidate_y) ** 2)
            if sse < min_sse:
                min_sse = sse
                best_candidate = candidate_col
        return best_candidate, min_sse