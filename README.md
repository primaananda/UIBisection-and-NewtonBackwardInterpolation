# UIBisection-and-NewtonBackwardInterpolation
Tugas UI Bisection Method dan Newton Backward Interpolation

# Bisection Method & Newton Backward Interpolation App

This application provides implementations of the Bisection Method and Newton Backward Interpolation using a graphical user interface built with PyQt5.

## Features

- **Bisection Method**: Find roots of a function using the Bisection Method.
- **Newton Backward Interpolation**: Interpolate values based on given data points.

## Requirements

-To run this application, you need to have Anaconda installed on your machine.
-Python 3.11
-Matplotlib
-Numpy
-PyQt5

## Setup Instructions

Follow the steps below to set up the environment and run the application:

1. **Create a new Anaconda environment**:
   ```bash
   conda create -n myenv python=3.11
2. Activate the environment:
    ```bash
   conda activate myenv
3. Install required packages: Use the following command to install NumPy, Matplotlib, and PyQt5:
    ```bash
    conda install numpy matplotlib pyqt=5
4. Run the application: You can run the application using Python:
    ```bash
    python your_script_name.py
5. Create an executable file: If you want to create a standalone executable, you can use PyInstaller. First, install PyInstaller:
    ```bash
    pip install pyinstaller

6. Then, build the executable with the following command:
    ```bash
    pyinstaller --onefile --windowed your_script_name.py

After running this command, you will find the executable in the dist folder.

Authors
This application was developed by:
I Putu Prima Ananda

About the Application
Functionality Overview

**Bisection Method:**

Input a function in terms of x.
Set the interval [a, b] and the desired tolerance.
Compute and display the root, iteration count, and a plot of the function with midpoints.

**Newton Backward Interpolation:**

Input data points as a list of tuples.
Specify the value to interpolate.
Display the interpolated value and the difference table.
License
This project is open-source. Feel free to use and modify it as needed.
