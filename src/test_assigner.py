"""
test_assigner.py
Assigns each test point to the closest candidate model if within tolerance.
Encapsulates assignment logic for clarity and future extension.
"""

import pandas as pd
import numpy as np

class TestAssigner:
    """
    Assigns test points to candidate models based on deviation tolerance.
    Modular design allows for easy changes to assignment logic.
    """
    def __init__(self, test_data, candidate_models, best_matches, training_data, tolerance_func=None):
        self.test_data = test_data
        self.candidate_models = candidate_models
        self.best_matches = best_matches
        self.training_data = training_data
        self.tolerance_func = tolerance_func

    def assign(self):
        """
        Assigns each test point to a candidate model if deviation is within tolerance.
        Returns a DataFrame of matched points.
        """
        assigned = []
        for idx, row in self.test_data.iterrows():
            x_val, y_val = row['x'], row['y']
            match_info = self._find_assignment(x_val, y_val)
            if match_info:
                assigned.append(match_info)
        return pd.DataFrame(assigned, columns=['x', 'y', 'ideal_func', 'delta_y'])

    def _find_assignment(self, x_val, y_val):
        """
        Helper to find assignment for a single test point.
        Checks each candidate model for tolerance and returns assignment info if matched.
        """
        for match in self.best_matches:
            candidate_col = match['ideal_col']
            candidate_row = self.candidate_models[self.candidate_models['x'] == x_val]
            if candidate_row.empty:
                continue
            candidate_y = candidate_row[candidate_col].values[0]
            delta_y = abs(y_val - candidate_y)
            train_col = match['train_col']
            train_row = self.training_data[self.training_data['x'] == x_val]
            if train_row.empty:
                continue
            train_y = train_row[train_col].values[0]
            max_dev = abs(train_y - candidate_y)
            tolerance = self.tolerance_func(max_dev) if self.tolerance_func else (2 ** 0.5) * max_dev
            if delta_y <= tolerance:
                return {'x': x_val, 'y': y_val, 'ideal_func': candidate_col, 'delta_y': delta_y}
        return None