"""
test_assigner.py
Class for assigning test points to ideal functions based on deviation criterion.
"""

import pandas as pd
import numpy as np

class TestAssigner:
    """
    Assigns each test point to the closest ideal function if deviation is within allowed threshold.
    """
    def __init__(self, test_df, ideal_df, matches, train_df):
        self.test_df = test_df
        self.ideal_df = ideal_df
        self.matches = matches
        self.train_df = train_df

    def assign(self):
        """
        Returns a DataFrame of matched test points with columns: x, y, ideal_func, delta_y.
        Only assigns points that meet the deviation criterion.
        """
        results = []
        # Iterate over each test point
        for idx, row in self.test_df.iterrows():
            x = row['x']
            y = row['y']
            assigned = False
            # Try to assign to one of the four chosen ideal functions
            for match in self.matches:
                ideal_col = match['ideal_col']
                # Find the corresponding ideal y value for this x
                ideal_row = self.ideal_df[self.ideal_df['x'] == x]
                if not ideal_row.empty:
                    y_ideal = ideal_row.iloc[0][ideal_col]
                    delta_y = abs(y - y_ideal)
                    # Calculate max allowed deviation for assignment
                    train_col = match['train_col']
                    train_row = self.train_df[self.train_df['x'] == x]
                    if not train_row.empty:
                        train_y = train_row.iloc[0][train_col]
                        max_dev = np.max(np.abs(self.train_df[train_col] - self.ideal_df[ideal_col]))
                        threshold = max_dev * np.sqrt(2)
                        if delta_y <= threshold:
                            results.append({
                                'x': x,
                                'y': y,
                                'ideal_func': ideal_col,
                                'delta_y': delta_y
                            })
                            assigned = True
                            break
            if not assigned:
                # Optionally, add unmatched points or skip
                pass
        return pd.DataFrame(results)