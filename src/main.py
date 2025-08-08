# main.py - Starting point of the project.
# This script executes all steps: data loading >> least square matching >> test assignment >> database storing.

# Import necessary modules
import sys  # For exiting the program on error

from data_loader import load_all_data                   # Loads all CSV files into DataFrames
from function_matcher import best_ideal_matches         # Finds the best ideal function for each training function
from test_assigner import assign_test_point             # Assigns test data points to ideal functions based on deviation
from database_writer import write_database              # Writes matched test points to an SQLite database

# ------------ STEP 1: Load all CSV files ------------
# Load training, ideal, and test datasets from the data folder
train_data_function, ideal_data_function, test_data_function = load_all_data(
    "data/ideal.csv",      # Ideal functions file
    "data/test.csv",       # Test data file
    "data/train.csv"       # Training data file
)
# Data loading completed.

# ------------ STEP 2: Validate data loading ------------
# Exit if any file failed to load
if any(data_frame is None for data_frame in (train_data_function, ideal_data_function, test_data_function)):
    print("One or more data files failed to load.")
    sys.exit(1)  # Exit the program with code 1.

# ------------ STEP 3: Perform least square matching ------------
# For each training function (y1-y4), find the best matching ideal function (y1-y50) using least squares.
# Returns a list of dicts, each with the best ideal function for a training function.
best_ideal_matches_list = best_ideal_matches(
    train_data_function,   # Training data
    ideal_data_function    # Ideal functions
)

print("best_ideal_matches_list:", best_ideal_matches_list)  # Debug: Show matching results

# ------------ STEP 4: Assign test points to matching functions ------------
# For each test point, assign it to the closest ideal function if deviation is within allowed threshold.
# Returns a DataFrame of matched test points.
matched_test_points = assign_test_point(
    test_data_function,        # Test data
    ideal_data_function,       # Ideal functions
    best_ideal_matches_list    # Best matches for training functions
)

# ------------ STEP 5: Write results to the database ------------
# Store matched test points in an SQLite database, creating the table if needed.
write_database(
    matched_test_points,       # DataFrame of matched test points
    db_path="db/ideal.db"      # Path to the SQLite database
)

# ------------ STEP 6: Visualization using Matplotlib ------------
import matplotlib.pyplot as plt

# Overlay plots: Show each training function vs. its best-matching ideal function in a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for i in range(1, 5):
    ax = axes[i-1]
    train_col = f'y{i}'
    # Plot training function
    ax.plot(train_data_function['x'], train_data_function[train_col], 'o-', label=f'Training {train_col}')
    ideal_info = best_ideal_matches_list[i-1]

    # Extract the ideal function column name from the match info
    ideal_col = ideal_info.get('ideal_col')
    if ideal_col and ideal_col in ideal_data_function.columns:
        # Plot the matched ideal function
        ax.plot(ideal_data_function['x'], ideal_data_function[ideal_col], '--', label=f'Ideal {ideal_col}')
        ax.set_title(f'{train_col} vs. {ideal_col}')
    else:
        ax.set_title(f"Column {ideal_col} not found")
        continue

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

plt.tight_layout()
plt.show()

# Histogram: Show distribution of deviations for matched test points
if 'delta_y' in matched_test_points.columns:
    plt.figure(figsize=(7, 4))
    plt.hist(matched_test_points['delta_y'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Histogram of Test Point Deviations')
    plt.xlabel('Deviation (|y_test - y_ideal|)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
else:
    print("Column 'delta_y' not found in matched_test_points. Histogram skipped.")

# Uncomment below to use a custom visualizer module if available
# from visualizer import plot_matches
# plot_matches(training_df, ideal_df, matched_functions)

# ------------ Final confirmation message ------------
print("All steps completed successfully. Results have been written to the database.")

# ------------ Efficiency metrics ------------
# Calculate and print model efficiency statistics
total_test_points = len(test_data_function)
matched_points = len(matched_test_points)
matching_rate = matched_points / total_test_points * 100
print(f"\nModel Efficiency Metrics:")
print(f"Matching Rate: {matching_rate:.2f}% ({matched_points}/{total_test_points} test points matched)")

# Print deviation statistics if available
if 'delta_y' in matched_test_points.columns:
    mean_deviation = matched_test_points['delta_y'].mean()
    max_deviation = matched_test_points['delta_y'].max()
    min_deviation = matched_test_points['delta_y'].min()
    print(f"Mean deviation: {mean_deviation:.4f}")
    print(f"Max deviation: {max_deviation:.4f}")
    print(f"Min deviation: {min_deviation:.4f}")

# Print count of matched ideal functions
if 'ideal_func' in matched_test_points.columns:
    print("\nMatched Ideal Function Counts:")
    print(matched_test_points['ideal_func'].value_counts())



