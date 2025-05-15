# Ideal_Function
Assignment1 

Ideal Function Approximation Project
Course: DLMDSPWP01 – Python Programming
Program: IU International University of Applied Sciences
Assignment Type: Written Final Assignment

📘 Objective
The aim of this assignment is to develop a modular Python application that identifies the best-fitting "ideal functions" to approximate four noisy training functions using a least-squares method.

After mapping the training functions to ideal ones, the system evaluates a test dataset to determine whether the test points match any of the mapped ideal functions within a defined deviation.

🧠 Key Goals
Load and process provided datasets:
training_data.csv: 4 training functions with noise
ideal_functions.csv: 50 mathematically ideal functions
test_data.csv: unseen data points for classification
For each training function, find the ideal function that best fits it using least square error.
Use a deviation threshold (√2 × max error) to match test data to mapped ideal functions.
Store results in a relational SQLite database.
Create interactive visualizations of the results.
Apply core Object-Oriented Programming principles in the solution.
💡 Summary
This project simulates a real-world machine learning preprocessing pipeline where noisy training data is mapped to mathematical ideal models for further inference.

The final solution must be clean, modular, reusable, and follow professional Python practices.
