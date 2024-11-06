#Author : I Putu Prima Ananda (ipprimaananda@gmail.com)
#madewithlove Nov 2024
#
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QFormLayout, QDoubleSpinBox, QComboBox, QStackedWidget, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Function for Bisection Method
def bisection_method(f, a, b, tol):
    if f(a) * f(b) >= 0:
        return None, "Bisection method fails. The function must have opposite signs at a and b."

    midpoints = []
    iteration_count = 0
    c = a
    while (b - a) / 2.0 > tol:
        iteration_count += 1
        c = (a + b) / 2.0
        midpoints.append(c)
        if f(c) == 0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c, midpoints, iteration_count

# Function for Newton Backward Interpolation
def newton_backward_interpolation(x, y, value):
    n = len(x)
    if n != len(y):
        raise ValueError("The lengths of x and y must be the same.")
    if n < 2:
        raise ValueError("There must be at least two data points for interpolation.")
    
    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y

    # Fill the difference table
    for j in range(1, n):
        for i in range(n-1, j-2, -1):
            diff_table[i, j] = diff_table[i, j-1] - diff_table[i-1, j-1]

    # Check for uniform spacing
    spacing = x[1] - x[0]
    if not all(np.isclose(x[i] - x[i-1], spacing) for i in range(2, n)):
        raise ValueError("x values must be equally spaced.")

    u = (value - x[-1]) / spacing  # Calculate the u value for interpolation
    result = diff_table[-1, 0]
    u_term = 1

    # Calculate the interpolated value using the backward difference
    for i in range(1, n):
        u_term *= (u + i - 1) / i
        result += u_term * diff_table[n-1, i]

    return result, diff_table


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bisection Method & Newton Interpolation Backward")
        self.setGeometry(100, 100, 1230, 650)  # Set default window size

        # Main layout
        main_layout = QHBoxLayout()

        # Left side for method selection and input forms (30% width)
        input_layout = QVBoxLayout()

        # Button for About
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        input_layout.addWidget(about_button)
        
        # Dropdown to select method
        self.method_select = QComboBox()
        self.method_select.addItems(["Select Method", "Bisection Method", "Newton Backward Interpolation"])
        self.method_select.currentIndexChanged.connect(self.method_selected)
        input_layout.addWidget(self.method_select)

        # Stacked widget to hold different methods' input/output forms
        self.stacked_widget = QStackedWidget()

        # Bisection Method Widgets
        self.bisection_widget = QWidget()
        bisection_layout = QFormLayout()
        self.function_input = QLineEdit('x**3 - x - 2')
        self.a_input = QDoubleSpinBox()
        self.a_input.setValue(1.0)
        self.b_input = QDoubleSpinBox()
        self.b_input.setValue(2.0)
        self.tol_input = QLineEdit("0.000001")
        self.bisection_button = QPushButton("Compute Bisection Method")

        # Add results display labels for Bisection Method
        self.iteration_count_label = QLabel("Max Iteration: ")
        self.midpoint_label = QLabel("Root: ")

        bisection_layout.addRow("Function f(x):", self.function_input)
        bisection_layout.addRow("Start (a):", self.a_input)
        bisection_layout.addRow("End (b):", self.b_input)
        bisection_layout.addRow("Tolerance:", self.tol_input)
        bisection_layout.addRow(self.bisection_button)
        bisection_layout.addRow(self.iteration_count_label)
        bisection_layout.addRow(self.midpoint_label)

        self.bisection_widget.setLayout(bisection_layout)
        self.stacked_widget.addWidget(self.bisection_widget)

        # Interpolation Widgets
        self.interpolation_widget = QWidget()
        interpolation_layout = QFormLayout()
        self.data_points_input = QLineEdit("[(1, 2), (2, 3), (3, 5)]")
        self.interp_value_input = QDoubleSpinBox()
        self.interp_value_input.setValue(2.5)
        self.interpolation_button = QPushButton("Compute Interpolation")

        interpolation_layout.addRow("Data Points (x, y):", self.data_points_input)
        interpolation_layout.addRow("Interpolate Value:", self.interp_value_input)
        interpolation_layout.addRow(self.interpolation_button)
        
        # Create QLabel for displaying interpolation result below the button
        self.interpolation_result_label = QLabel("Interpolated Value:")
        interpolation_layout.addRow(self.interpolation_result_label)

        self.interpolation_widget.setLayout(interpolation_layout)
        self.stacked_widget.addWidget(self.interpolation_widget)

        # Add stacked widget to input layout
        input_layout.addWidget(self.stacked_widget)

        # Connect buttons to their respective functions
        self.bisection_button.clicked.connect(self.compute_bisection)
        self.interpolation_button.clicked.connect(self.compute_interpolation)

        # Right side for results display (70% width)
        self.result_display = QLabel()
        self.result_display.setAlignment(Qt.AlignTop)
        self.result_display.setWordWrap(True)
        self.result_display.setFont(QFont("Arial", 10))

        # Add input and results layout to main layout with stretch
        main_layout.addLayout(input_layout, 3)
        main_layout.addWidget(self.result_display, 7)

        self.setLayout(main_layout)
        self.stacked_widget.setCurrentIndex(0)

    def show_about(self):
        about_message = (
            "Program Bisection Method & Newton Backward Interpolation\n"
            "S2 Ilmu Komputer - Universitas Pendidikan Ganesha\n"
            "Oleh:\n"
            "I Putu Prima Ananda - 2429101017\n"
            "Ni Putu Ria Anggreni - 2429101009\n"
            "Yudi Anantha - 2429101011\n"
            "Mony Artha - 2429101006"
        )
        QMessageBox.about(self, "About", about_message)
    
    def method_selected(self):
        method_index = self.method_select.currentIndex()
        if method_index == 1:
            self.stacked_widget.setCurrentIndex(0)
        elif method_index == 2:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(-1)
        self.result_display.setText("")

    def compute_bisection(self):
        f_str = self.function_input.text()
        a = self.a_input.value()
        b = self.b_input.value()
        try:
            tol = float(self.tol_input.text())
            if not (0.1 >= tol >= 0.0000000001):
                raise ValueError("Tolerance must be between 0.1 and 0.0000000001")
            f = lambda x: eval(f_str)
            root, midpoints, iteration_count = bisection_method(f, a, b, tol)
            if root is None:
                self.result_display.setText("Error: Bisection method fails. The function must have opposite signs at a and b.")
            else:
                result_text = (f"Root found: {root}\nIterations: {iteration_count}\n"
                               f"Converged value: {midpoints[-1] if midpoints else 'N/A'}\nTolerance: {tol}")
                self.result_display.setText(result_text)

                self.iteration_count_label.setText(f"Max Iteration: {iteration_count}")
                self.midpoint_label.setText(f"Root: {midpoints[-1] if midpoints else 'N/A'}")

            
                # Plotting using matplotlib embedded plot
                fig, ax = plt.subplots(figsize=(10, 6))
                x_values = np.linspace(a, b, 100)
                y_values = [f(x) for x in x_values]
                ax.plot(x_values, y_values, label=f"f(x) = {f_str}")
                ax.axhline(0, color="gray", linestyle="--")
                ax.scatter(midpoints, [f(mid) for mid in midpoints], color="red", marker="x", label="Midpoints Iteration")
                ax.scatter(midpoints[-1], f(midpoints[-1]), color="green", marker="o", label="Root")
                ax.legend()

                # Save plot to temporary file and display in QLabel
                plot_path = "temp_plot.png"
                fig.savefig(plot_path)
                plt.close(fig)

                self.result_display.setPixmap(QPixmap(plot_path))
                self.result_display.setScaledContents(True)
                os.remove(plot_path)

        except Exception as e:
            self.result_display.setText(f"Error: {e}")

    def compute_interpolation(self):
        data_points_str = self.data_points_input.text()
        value = self.interp_value_input.value()
        try:
            data_points = eval(data_points_str)
            x = [point[0] for point in data_points]
            y = [point[1] for point in data_points]
            result, diff_table = newton_backward_interpolation(x, y, value)

            # Display the interpolated value below the button
            self.interpolation_result_label.setText(f"Interpolated Value at x = {value}: {result:.4f}")

            # Prepare the output string with Δy displayed in the result_display QLabel
            result_text = f"Interpolated Value at x = {value}: {result}\n\n"
            
            # Create dynamic headers for the difference table
            headers = ["x", "y"]
            num_deltas = len(diff_table[0])
            for i in range(1, num_deltas): 
                headers.append(f"Δ^{i}y")
            
            # Add headers to the result_text
            result_text += "{:<10}".format("x") + "{:<10}".format("y") + "".join(f"{h:<10}" for h in headers[2:]) + "\n"
            result_text += "-" * 10 * len(headers) + "\n"  # Add a separator line
            
            # Populate the result text with data from the difference table
            for i in range(len(diff_table)):
                row = f"{x[i]:<10}{y[i]:<10}"
                row += "".join(f"{diff_table[i][j]:<10.4f}" if not np.isnan(diff_table[i][j]) else " " * 10 for j in range(1, num_deltas))
                result_text += row + "\n"

            self.result_display.setText(result_text)

            # Plotting the interpolation result and original points
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot original data points
            ax.scatter(x, y, color="blue", label="Data Points")
            
            # Plot interpolated point
            ax.scatter(value, result, color="red", marker="x", label=f"Interpolated at x = {value}")
            
            # Generate additional x values to make a smooth curve
            x_range = np.linspace(min(x), max(x), 100)
            interpolated_y = [newton_backward_interpolation(x, y, xi)[0] for xi in x_range]
            
            # Plot the interpolation curve
            ax.plot(x_range, interpolated_y, color="green", linestyle="--", label="Interpolation Curve")
            
            ax.legend()
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Newton Backward Interpolation")
            
            # Save plot to temporary file and display in QLabel
            plot_path = "temp_interp_plot.png"
            fig.savefig(plot_path)
            plt.close(fig)

            # Display plot in QLabel
            self.result_display.setPixmap(QPixmap(plot_path))
            self.result_display.setScaledContents(True)
            os.remove(plot_path)

        except Exception as e:
            self.result_display.setText(f"Error: {e}")


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())

