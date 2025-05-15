import numpy as np
import pandas as pd

def best_ideal_matches(train_df: pd.DataFrame, ideal_df: pd.DataFrame):
    """
    For each training function (y1-y4), find the best matching ideal function (y1-y50)
    using least squares (sum of squared differences) over the shared x values.

    Args:
        train_df (pd.DataFrame): Training data with columns ['x', 'y1', 'y2', 'y3', 'y4']
        ideal_df (pd.DataFrame): Ideal functions with columns ['x', 'y1', ..., 'y50']

    Returns:
        list of dict: Each dict contains:
            {
                'train_col': str,  # e.g. 'y1'
                'ideal_col': str,  # e.g. 'y17'
                'min_sse': float   # minimum sum of squared errors
            }
    """
    results = []
    # Get all training function columns except 'x'
    train_y_cols = [col for col in train_df.columns if col != 'x']
    # Get all ideal function columns except 'x'
    ideal_y_cols = [col for col in ideal_df.columns if col != 'x']

    # Merge on 'x' to ensure both DataFrames are aligned on the same x values
    merged = pd.merge(train_df[['x']], ideal_df, on='x', how='inner')

    # Loop through each training function column (y1-y4)
    for train_col in train_y_cols:
        min_sse = float('inf')  # Initialize minimum sum of squared errors as infinity
        best_ideal_col = None   # To store the best matching ideal function column name

        # Loop through each ideal function column (y1-y50)
        for ideal_col in ideal_y_cols:
            # Compute sum of squared errors between the training and ideal function for all x
            sse = np.sum((train_df[train_col].values - merged[ideal_col].values) ** 2)
            # If this ideal function is a better match (smaller SSE), update best match
            if sse < min_sse:
                min_sse = sse
                best_ideal_col = ideal_col

        # Store the result for this training function
        results.append({
            'train_col': train_col,      # Training function column name
            'ideal_col': best_ideal_col, # Best matching ideal function column name
            'min_sse': min_sse           # Minimum sum of squared errors
        })
    # Return the list of best matches for each training function
    return results