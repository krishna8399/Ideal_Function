"""
function_matcher.py
Class for matching training functions to ideal functions using least squares.
"""

import numpy as np

class FunctionMatcher:
    """
    Matches each training function to the best-fitting ideal function using least squares.
    """
    def __init__(self, train_df, ideal_df):
        self.train_df = train_df
        self.ideal_df = ideal_df

    def best_ideal_matches(self):
        """
        Returns a list of dicts with the best ideal function for each training function.
        Each dict contains train_col, ideal_col, and min_sse.
        """
        matches = []
        # Loop through each training function (y1-y4)
        for i in range(1, 5):
            train_col = f'y{i}'
            min_sse = float('inf')
            best_ideal_col = None
            # Compare with each ideal function (y1-y50)
            for ideal_col in [col for col in self.ideal_df.columns if col.startswith('y')]:
                sse = np.sum((self.train_df[train_col] - self.ideal_df[ideal_col]) ** 2)
                if sse < min_sse:
                    min_sse = sse
                    best_ideal_col = ideal_col
            matches.append({
                'train_col': train_col,
                'ideal_col': best_ideal_col,
                'min_sse': min_sse
            })
        return matches