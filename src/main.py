# main.py - Starting point of the project.
# This script executes all steps: data loading >> least square matching >> test assignment >> database storing.

# Import necessary modules
import sys  # Provides functions and variables to interact with the Python runtime environment.

from data_loader import load_all_data                   # Module to load all the CSV files.
from function_matcher import best_ideal_matches         # Module to find the best function for training.
from test_assigner import assign_test_point             # Module to assign the test data to matching functions.
from database_writer import write_database              # Module to write the results into the database (SQLite).

# ------------ STEP 1: Load all CSV files ------------
# Files to be loaded:
# - "training_data.csv": Contains x, y1–y4 (training set).
# - "ideal_functions.csv": Contains x, y1–y50 (perfect functions).
# - "test_data.csv": Contains x, y (unlabeled values to match).

train_data_function, ideal_data_function, test_data_function = load_all_data(
    "data/ideal.csv",  # Path to the ideal functions file.
    "data/test.csv",        # Path to the test data file.
    "data/train.csv"        # Path to the training data file.
)

# Data loading completed.

# ------------ STEP 2: Validate data loading ------------
# Check if any of the files failed to load. If so, exit the program with an error message.

if any(data_frame is None for data_frame in (train_data_function, ideal_data_function, test_data_function)):
    print("One or more data files failed to load.")
    sys.exit(1)  # Exit the program with code 1.

# ------------ STEP 3: Perform least square matching ------------
# For each training data function y1-y4, find the best matching ideal function y1-y50 using least squares matching.
# This function returns a list of tuples, where each tuple contains the index of the best matching ideal function.
# Find the best ideal function for each training data point using least squares matching.

best_ideal_matches_list = best_ideal_matches(
    train_data_function,  # Training data.
    ideal_data_function    # Ideal functions.
)

# ------------ STEP 4: Assign test points to matching functions ------------
# For each (x, y) in the test data, compare it with y_ideal(x) for each ideal function.
# then accept the match if deviation is <= max_delta × √2 (per assignment rules).
# This function returns a new Dataframe with matched test points.
matched_test_points = assign_test_point(
    test_data_function,  # Test data.
    ideal_data_function,  # Ideal functions.
    best_ideal_matches_list  # Best matching ideal functions for training data.
)

# ------------ STEP 5: Write results to the database ------------
# Write the matched test points to the database (SQLite).
# Store assigned x, y, delta_y and the index of the ideal function in the database.
# create a new table if it doesn't exist.
write_database(
    matched_test_points,  # Matched test points.
    db_path="db/ideal.db"  # Path to the SQLite database.
    )

# -----------------------------------------------
# Step 6: Optional visualization step (if implemented)
# -----------------------------------------------
# from visualizer import plot_matches
# plot_matches(training_df, ideal_df, matched_functions)

#final confirmation message
print("All steps completed successfully. Results have been written to the database.")
# Note: The above code assumes that the functions in the imported modules are implemented correctly.
# The database will be created if it doesn't exist, and the results will be stored in a new table.

