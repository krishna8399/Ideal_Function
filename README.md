# Ideal Function Assignment Project

## Overview

This project matches training functions to candidate models using least squares, assigns test points based on deviation tolerance, stores results in a SQLite database, and visualizes the results.

## Unique Features

- Modular class-based design for data handling, matching, assignment, and database writing.
- Configurable tolerance for assignment.
- Extensive use of explanatory comments and helper functions.
- Consistent naming conventions for clarity.
- Interactive and static visualizations.
- Robust error handling and validation.

## Workflow

1. **Load Data:**  
   Training, candidate, and test datasets are loaded and validated using custom handler classes.

2. **Match Functions:**  
   Training functions are matched to candidate models using least squares via `FunctionMatcher`.

3. **Assign Test Points:**  
   Test points are assigned to candidate models if within a configurable tolerance using `TestAssigner`.

4. **Store Results:**  
   All results are written to a SQLite database using `DatabaseWriter`.

5. **Visualize:**  
   Results are visualized using Matplotlib and Bokeh.

## Usage

```bash
python src/main.py
```

## File Structure

- `src/data_loader.py` - Utility functions for loading and previewing CSV data.
- `src/data_handler.py` - Classes for managing and validating datasets.
- `src/function_matcher.py` - Matches training functions to candidate models.
- `src/test_assigner.py` - Assigns test points to candidate models.
- `src/database_writer.py` - Writes results to SQLite database.
- `src/main.py` - Main workflow script.

## Configuration

Tolerance for assignment is configurable via a utility function in `main.py`.

## Tests

See `tests/test_function_matcher.py` and `tests/test_assigner.py` for example unit tests.

## Author

Your Name, Matriculation Number, Course Code, University
