# Ideal Function Assignment Project

## Overview
This project loads training, ideal, and test datasets, matches training functions to ideal functions using least squares, assigns test points, stores results in a SQLite database (via SQLAlchemy), and visualizes results with Matplotlib and Bokeh.

## Data Privacy & Submission
**Note:**  
As required by the assignment guidelines, the actual data files (`train.csv`, `ideal.csv`, `test.csv`) are **not included** in this submission.  
To run the code, you will need to request access to the datasets.

## Features
- Object-oriented design with inheritance
- Custom exception handling
- SQLAlchemy database integration
- Interactive Bokeh and static Matplotlib visualizations
- Unit tests for all major modules

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python src/main.py
```
- Interactive Bokeh visualizations will open in your browser as `ideal_function_bokeh_visualizations.html`.

## Testing
```bash
pytest
```

## Project Structure
- `src/`: Source code modules
- `test/`: Unit tests
- `db/`: SQLite database (auto-created)
- `data/`: Input CSV files (**not included in submission**)

## Git Workflow Example
```bash
git clone <repo-url>
cd <repo-folder>
git checkout develop
git add <changed-files>
git commit -m "Describe your changes"
git push origin develop
# Create a pull request on your Git platform
```

## License
See [LICENSE](LICENSE).

## Author / Student Details

- Name: Krishna Singh
- Matriculation ID: 4252576
- Course: DLMDSPWP01 – Programming with Python
- University: IU International University of Applied Sciences https://www.iu.org
