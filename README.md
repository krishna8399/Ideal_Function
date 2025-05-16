# Ideal Function Finder

A Python-based tool to match and analyze ideal mathematical functions against given training and test data. The project includes automated deviation analysis, visualizations, database export, and unit testing — all in one!

## Project Overview
**Course:** DLMDSPWP01 – Python Programming  
**Program:** IU International University of Applied Sciences  
**Assignment Type:** Written Final Assignment

**Objective**  
Develop a modular Python application that identifies the best-fitting "ideal functions" to approximate four noisy training functions using a least-squares method. After mapping the training functions to ideal ones, the system evaluates a test dataset to determine whether the test points match any of the mapped ideal functions within a defined deviation.

---

## Key Features
- Load and analyze CSV datasets (training, test, ideal functions)
- Match training data to ideal functions with minimal deviation
- Identify matching test points based on a deviation threshold
- Visualize results using interactive Bokeh plots
- Save matched data into an SQLite database
- Includes unit tests for reliability

---

## Project Structure

```plaintext
Ideal_Function/
├── data/                # Input CSV files
│   ├── ideal.csv
│   ├── test.csv
│   └── train.csv
├── src/                 # Core logic modules
│   ├── data_loader.py
│   ├── deviation_calculator.py
│   ├── ideal_matcher.py
│   ├── plotter.py
│   └── sqlite_exporter.py
├── test/                # Unit tests
│   └── test_functions.py
├── main.py              # Project entry point
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Technologies Used
- Python 3.8+
- Pandas for data manipulation
- NumPy for numerical computations
- Bokeh for plotting
- SQLite3 for database export
- PyTest for unit testing

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/krishna8399/Ideal_Function.git
cd Ideal_Function

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
# or
source venv/bin/activate # On Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run the Application

```bash
python main.py
```

This will:
- Load train.csv, test.csv, and ideal.csv
- Match ideal functions
- Visualize matched data
- Save outputs to an SQLite database

> **Note:** Ensure the data folder contains the required CSV files.

---

## Running Unit Tests

```bash
pytest
```

---

## Convert to a Desktop Executable (Optional)
To create a standalone executable using PyInstaller:

```bash
pyinstaller --onefile main.py
```

The output will be found in the `dist/` folder as `main.exe` (on Windows).

---

## Acknowledgments
This project was developed as part of a data analysis and function matching assignment, showcasing Python skills in data science, visualization, and packaging.
