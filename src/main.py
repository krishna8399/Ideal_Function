"""
main.py
Main script for the Ideal Function Assignment project.

This script orchestrates the workflow:
- Loads training, ideal, and test datasets using object-oriented data handlers.
- Matches each training function to its best-fitting ideal function using least squares.
- Assigns test points to ideal functions based on deviation criteria.
- Stores all results in a SQLite database using SQLAlchemy.
- Visualizes results using both Matplotlib (static) and Bokeh (interactive).
- Prints efficiency metrics and summary statistics.

All modules are designed for clarity, modularity, and extensibility.
"""

import sys
import matplotlib.pyplot as plt
from data_handler import TrainingDataHandler, IdealFunctionHandler, TestDataHandler, DataLoadError
from function_matcher import FunctionMatcher
from test_assigner import TestAssigner
from database_writer import DatabaseWriter

# STEP 1: Load all CSV files using OOP handlers
try:
    # Load training data
    train_handler = TrainingDataHandler("data/train.csv")
    train_handler.load()
    train_data_function = train_handler.data

    # Load ideal functions
    ideal_handler = IdealFunctionHandler("data/ideal.csv")
    ideal_handler.load()
    ideal_data_function = ideal_handler.data

    # Load test data
    test_handler = TestDataHandler("data/test.csv")
    test_handler.load()
    test_data_function = test_handler.data
except DataLoadError as e:
    # Exit if any file fails to load
    print(e)
    sys.exit(1)

# STEP 2: Match training functions to ideal functions using least squares
matcher = FunctionMatcher(train_data_function, ideal_data_function)
best_ideal_matches_list = matcher.best_ideal_matches()
print("Best ideal matches:", best_ideal_matches_list)  # Debug output

# STEP 3: Assign test points to ideal functions based on deviation criterion
assigner = TestAssigner(test_data_function, ideal_data_function, best_ideal_matches_list, train_data_function)
matched_test_points = assigner.assign()

# STEP 4: Write all results to the database using SQLAlchemy
db_writer = DatabaseWriter(db_path="db/ideal.db")
db_writer.write_training_data(train_data_function)
db_writer.write_ideal_functions(ideal_data_function)
db_writer.write_matched_points(matched_test_points)

# STEP 5: Visualize results using Matplotlib
# Overlay plots: Show each training function vs. its best-matching ideal function in a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()
for i in range(1, 5):
    ax = axes[i-1]
    train_col = f'y{i}'
    ax.plot(train_data_function['x'], train_data_function[train_col], 'o-', label=f'Training {train_col}')
    ideal_info = best_ideal_matches_list[i-1]
    ideal_col = ideal_info.get('ideal_col')
    if ideal_col and ideal_col in ideal_data_function.columns:
        ax.plot(ideal_data_function['x'], ideal_data_function[ideal_col], '--', label=f'Ideal {ideal_col}')
        ax.set_title(f'Matplotlib Overlay: {train_col} vs. {ideal_col}')
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
    plt.title('Matplotlib Histogram: Test Point Deviations')
    plt.xlabel('Deviation (|y_test - y_ideal|)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
else:
    print("Column 'delta_y' not found in matched_test_points. Histogram skipped.")

# STEP 6: Interactive visualization using Bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot, column
from bokeh.palettes import Category10
from bokeh.models import ColumnDataSource, Div
import numpy as np

# Set output file for Bokeh visualizations (opens in browser)
output_file("ideal_function_bokeh_visualizations.html")

# Overlay plots: Training vs. Ideal Functions (interactive, 2x2 grid)
plots = []
for i in range(1, 5):
    train_col = f'y{i}'
    ideal_info = best_ideal_matches_list[i-1]
    ideal_col = ideal_info.get('ideal_col')
    p = figure(title=f"Bokeh Overlay: {train_col} vs. {ideal_col}", width=400, height=300, x_axis_label='x', y_axis_label='y')
    p.line(train_data_function['x'], train_data_function[train_col], legend_label=f"Training {train_col}", color="blue", line_width=2)
    if ideal_col and ideal_col in ideal_data_function.columns:
        p.line(ideal_data_function['x'], ideal_data_function[ideal_col], legend_label=f"Ideal {ideal_col}", color="red", line_dash="dashed", line_width=2)
    p.legend.location = "top_left"
    plots.append(p)
grid = gridplot([[plots[0], plots[1]], [plots[2], plots[3]]])

# Scatter plot: Test points colored by assigned ideal function
if 'ideal_func' in matched_test_points.columns:
    unique_funcs = matched_test_points['ideal_func'].unique()
    color_map = {func: Category10[10][i % 10] for i, func in enumerate(unique_funcs)}
    colors = matched_test_points['ideal_func'].map(color_map)
    source = ColumnDataSource(data=dict(
        x=matched_test_points['x'],
        y=matched_test_points['y'],
        ideal_func=matched_test_points['ideal_func'],
        color=colors
    ))
    p_scatter = figure(title="Bokeh Scatter: Test Point Assignments", width=600, height=400, x_axis_label='x', y_axis_label='y', tools="pan,wheel_zoom,box_zoom,reset,hover")
    p_scatter.scatter('x', 'y', color='color', legend_field='ideal_func', source=source, size=8)
    p_scatter.legend.title = "Ideal Function"
    p_scatter.legend.location = "top_left"
else:
    p_scatter = Div(text="<b>Bokeh Scatter: Test Point Assignments</b><br>Column 'ideal_func' not found in matched_test_points. Scatter plot skipped.")

# Interactive histogram: Distribution of deviations for matched test points
if 'delta_y' in matched_test_points.columns:
    hist, edges = np.histogram(matched_test_points['delta_y'], bins=30)
    p_hist = figure(title="Bokeh Histogram: Test Point Deviations", width=600, height=400, x_axis_label='Deviation', y_axis_label='Count')
    p_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="skyblue", line_color="black")
else:
    p_hist = Div(text="<b>Bokeh Histogram: Test Point Deviations</b><br>Column 'delta_y' not found in matched_test_points. Histogram skipped.")

# Combine all Bokeh plots into a single layout and show once
show(column(
    Div(text="<h2>Bokeh Overlay: Training vs. Ideal Functions</h2>"),
    grid,
    Div(text="<h2>Bokeh Scatter: Test Point Assignments</h2>"),
    p_scatter,
    Div(text="<h2>Bokeh Histogram: Test Point Deviations</h2>"),
    p_hist
))

# STEP 7: Print efficiency metrics and summary
total_test_points = len(test_data_function)
matched_points = len(matched_test_points)
matching_rate = matched_points / total_test_points * 100
print(f"\nModel Efficiency Metrics:")
print(f"Matching Rate: {matching_rate:.2f}% ({matched_points}/{total_test_points} test points matched)")

if 'delta_y' in matched_test_points.columns:
    mean_deviation = matched_test_points['delta_y'].mean()
    max_deviation = matched_test_points['delta_y'].max()
    min_deviation = matched_test_points['delta_y'].min()
    print(f"Mean deviation: {mean_deviation:.4f}")
    print(f"Max deviation: {max_deviation:.4f}")
    print(f"Min deviation: {min_deviation:.4f}")

if 'ideal_func' in matched_test_points.columns:
    print("\nMatched Ideal Function Counts:")
    print(matched_test_points['ideal_func'].value_counts())

print("All steps completed successfully. Results have been written to the database.")

# ------------ End of main.py ------------
