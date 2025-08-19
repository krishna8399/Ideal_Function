"""
main.py
Main script for the Ideal Function Assignment project.

This script orchestrates the workflow:
- Loads training, candidate, and test datasets using object-oriented dataset managers.
- Matches each training function to its closest candidate model using least squares.
- Assigns test points to candidate models based on a configurable tolerance.
- Stores all results in a SQLite database using SQLAlchemy.
- Visualizes results using Matplotlib (static) and Bokeh (interactive).
- Prints efficiency metrics and summary statistics.

All modules are designed for clarity, modularity, and extensibility.
"""

import sys
import matplotlib.pyplot as plt
import statistics
from data_handler import TrainingDataHandler, IdealFunctionHandler, TestDataHandler, DataLoadError
from function_matcher import FunctionMatcher
from test_assigner import TestAssigner
from database_writer import DatabaseWriter

# Utility function for configurable tolerance
def calculate_tolerance(max_deviation):
    """
    Returns the tolerance for assignment based on max deviation.
    This makes the assignment logic flexible for future changes.
    """
    return (2 ** 0.5) * max_deviation

def load_datasets():
    """
    Loads all required datasets using custom managers.
    This modular approach makes error handling and future changes easier.
    """
    try:
        train_manager = TrainingDataHandler("data/train.csv")
        train_manager.load()
        training_data = train_manager.data

        candidate_manager = IdealFunctionHandler("data/ideal.csv")
        candidate_manager.load()
        candidate_models = candidate_manager.data

        test_manager = TestDataHandler("data/test.csv")
        test_manager.load()
        test_data = test_manager.data
    except DataLoadError as e:
        print("Failed to load one or more datasets. Please check file paths and formats.")
        sys.exit(1)
    return training_data, candidate_models, test_data

def visualize_with_matplotlib(training_data, candidate_models, best_matches):
    """
    Visualizes training functions vs. candidate models and deviation histogram.
    This helps users understand the matching and assignment quality.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for i in range(1, 5):
        ax = axes[i-1]
        train_col = f'y{i}'
        ax.plot(training_data['x'], training_data[train_col], 'o-', label=f'Training {train_col}')
        ideal_info = best_matches[i-1]
        candidate_col = ideal_info.get('ideal_col')
        if candidate_col and candidate_col in candidate_models.columns:
            ax.plot(candidate_models['x'], candidate_models[candidate_col], '--', label=f'Candidate {candidate_col}')
            ax.set_title(f'Matplotlib Overlay: {train_col} vs. {candidate_col}')
        else:
            ax.set_title(f"Column {candidate_col} not found")
            continue
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
    plt.tight_layout()
    plt.show()

def visualize_deviation_histogram(matched_points):
    """
    Plots histogram of deviations to show assignment quality.
    """
    if 'delta_y' in matched_points.columns:
        plt.figure(figsize=(7, 4))
        plt.hist(matched_points['delta_y'], bins=30, color='skyblue', edgecolor='black')
        plt.title('Matplotlib Histogram: Test Point Deviations')
        plt.xlabel('Deviation (|y_test - y_candidate|)')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.show()
    else:
        print("Column 'delta_y' not found in matched_points. Histogram skipped.")

# STEP 1: Load all CSV files using OOP managers
training_data, candidate_models, test_data = load_datasets()

# STEP 2: Match training functions to candidate models using least squares
matcher = FunctionMatcher(training_data, candidate_models)
best_matches = matcher.best_ideal_matches()  # If you rename in function_matcher.py, use select_closest_function()
print("Best matches:", best_matches)

# STEP 3: Assign test points to candidate models based on deviation criterion
assigner = TestAssigner(test_data, candidate_models, best_matches, training_data)
matched_points = assigner.assign()

# STEP 4: Write all results to the database using SQLAlchemy
db_writer = DatabaseWriter(db_path="db/ideal.db")

print("Training data shape:", training_data.shape)
print(training_data.head())
print("Candidate models shape:", candidate_models.shape)
print(candidate_models.head())
print("Matched test points shape:", matched_points.shape)
print(matched_points.head())

db_writer.write_training_data(training_data)
db_writer.write_ideal_functions(candidate_models)
db_writer.write_matched_points(matched_points)

# STEP 5: Visualize results using Matplotlib
visualize_with_matplotlib(training_data, candidate_models, best_matches)
visualize_deviation_histogram(matched_points)

# STEP 6: Interactive visualization using Bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot, column
from bokeh.palettes import Category10
from bokeh.models import ColumnDataSource, Div
import numpy as np

output_file("ideal_function_bokeh_visualizations.html")

plots = []
for i in range(1, 5):
    train_col = f'y{i}'
    ideal_info = best_matches[i-1]
    candidate_col = ideal_info.get('ideal_col')
    p = figure(title=f"Bokeh Overlay: {train_col} vs. {candidate_col}", width=400, height=300, x_axis_label='x', y_axis_label='y')
    p.line(training_data['x'], training_data[train_col], legend_label=f"Training {train_col}", color="blue", line_width=2)
    if candidate_col and candidate_col in candidate_models.columns:
        p.line(candidate_models['x'], candidate_models[candidate_col], legend_label=f"Candidate {candidate_col}", color="red", line_dash="dashed", line_width=2)
    p.legend.location = "top_left"
    plots.append(p)
grid = gridplot([[plots[0], plots[1]], [plots[2], plots[3]]])

if 'ideal_func' in matched_points.columns:
    unique_funcs = matched_points['ideal_func'].unique()
    color_map = {func: Category10[10][i % 10] for i, func in enumerate(unique_funcs)}
    colors = matched_points['ideal_func'].map(color_map)
    source = ColumnDataSource(data=dict(
        x=matched_points['x'],
        y=matched_points['y'],
        ideal_func=matched_points['ideal_func'],
        color=colors
    ))
    p_scatter = figure(title="Bokeh Scatter: Test Point Assignments", width=600, height=400, x_axis_label='x', y_axis_label='y', tools="pan,wheel_zoom,box_zoom,reset,hover")
    p_scatter.scatter('x', 'y', color='color', legend_field='ideal_func', source=source, size=8)
    p_scatter.legend.title = "Candidate Model"
    p_scatter.legend.location = "top_left"
else:
    p_scatter = Div(text="<b>Bokeh Scatter: Test Point Assignments</b><br>Column 'ideal_func' not found in matched_points. Scatter plot skipped.")

if 'delta_y' in matched_points.columns:
    hist, edges = np.histogram(matched_points['delta_y'], bins=30)
    p_hist = figure(title="Bokeh Histogram: Test Point Deviations", width=600, height=400, x_axis_label='Deviation', y_axis_label='Count')
    p_hist.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="skyblue", line_color="black")
else:
    p_hist = Div(text="<b>Bokeh Histogram: Test Point Deviations</b><br>Column 'delta_y' not found in matched_points. Histogram skipped.")

show(column(
    Div(text="<h2>Bokeh Overlay: Training vs. Candidate Models</h2>"),
    grid,
    Div(text="<h2>Bokeh Scatter: Test Point Assignments</h2>"),
    p_scatter,
    Div(text="<h2>Bokeh Histogram: Test Point Deviations</h2>"),
    p_hist
))

# STEP 7: Print efficiency metrics and summary
total_test_points = len(test_data)
matched_points_count = len(matched_points)
matching_rate = matched_points_count / total_test_points * 100
print(f"\nModel Efficiency Metrics:")
print(f"Matching Rate: {matching_rate:.2f}% ({matched_points_count}/{total_test_points} test points matched)")

if 'delta_y' in matched_points.columns:
    mean_deviation = statistics.mean(matched_points['delta_y'])
    max_deviation = max(matched_points['delta_y'])
    min_deviation = min(matched_points['delta_y'])
    print(f"Mean deviation: {mean_deviation:.4f}")
    print(f"Max deviation: {max_deviation:.4f}")
    print(f"Min deviation: {min_deviation:.4f}")

if 'ideal_func' in matched_points.columns:
    print("\nMatched Candidate Model Counts:")
    print(matched_points['ideal_func'].value_counts())

print("All steps completed successfully. Results have been written to the database.")

# ------------ End of main.py ------------
