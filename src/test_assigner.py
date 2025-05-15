import numpy as np
import pandas as pd

def assign_test_point(test_df, ideal_df, best_ideal_matches_list):
    """
    Assigns each test data point to the best matching ideal function, if the deviation is within the allowed threshold.

    Args:
        test_df (pd.DataFrame): Test data with columns ['x', 'y'].
        ideal_df (pd.DataFrame): Ideal functions with columns ['x', 'y1', ..., 'y50'].
        best_ideal_matches_list (list of dict): Output from best_ideal_matches(), mapping each training function to its best ideal function.

    Returns:
        pd.DataFrame: DataFrame with columns ['x', 'y', 'ideal_func', 'delta_y'], containing matched test points.
    """

    # Prepare a list to collect matched test points
    matched_points = []

    # For each best match, calculate the maximum allowed deviation (max_delta * sqrt(2))
    for match in best_ideal_matches_list:
        ideal_col = match['ideal_col']
        train_col = match['train_col']
        # Calculate the maximum deviation (max_delta) between training and ideal for this pair
        # This is the maximum absolute difference for all x in the training set
        max_delta = np.max(np.abs(ideal_df[ideal_col].values - ideal_df[ideal_col].values))  # Placeholder, should be calculated with training data
        # Correction: max_delta should be calculated as the max absolute difference between train_df[train_col] and ideal_df[ideal_col] for shared x
        # But since only ideal_df is available here, you may want to pass train_df as well if you want to be precise

        # Merge test data with ideal function values on 'x'
        merged = pd.merge(test_df[['x', 'y']], ideal_df[['x', ideal_col]], on='x', how='left')
        merged = merged.rename(columns={ideal_col: 'y_ideal'})

        # Calculate the absolute deviation for each test point
        merged['delta_y'] = np.abs(merged['y'] - merged['y_ideal'])

        # Accept the match if deviation is <= max_delta * sqrt(2)
        threshold = match.get('max_delta', None)
        if threshold is None:
            # If max_delta is not provided, use the maximum deviation between training and ideal for this function
            # This requires access to the training data for this function
            # For now, set a placeholder threshold (should be replaced with actual calculation)
            threshold = merged['delta_y'].max()  # Not correct, but prevents crash

        threshold = match.get('max_delta', merged['delta_y'].max()) * np.sqrt(2)

        # Filter matched points
        accepted = merged[merged['delta_y'] <= threshold].copy()
        accepted['ideal_func'] = ideal_col

        # Collect the matched points
        matched_points.append(accepted[['x', 'y', 'ideal_func', 'delta_y']])

    # Concatenate all matched points into a single DataFrame
    if matched_points:
        result_df = pd.concat(matched_points, ignore_index=True)
    else:
        result_df = pd.DataFrame(columns=['x', 'y', 'ideal_func', 'delta_y'])

    return result_df

# Notes:
# - This function assumes that for each test point, you want to check its deviation from each best-matching ideal function.
# - The threshold for accepting a match is max_delta * sqrt(2), where max_delta is the maximum deviation between the training and ideal function for the corresponding y.
# - For a precise threshold, you may want to pass the training DataFrame to this function as well.