from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QGroupBox, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

import sys
class TrapecioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle("Método de Regla del Trapecio con Calculadora Avanzada")
        self.setGeometry(100, 100, 900, 700)
        # Obtener las dimensiones de la pantalla
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Obtener las dimensiones de la ventana
        window_width = 900
        window_height = 700

        # Calcular las posiciones X e Y para centrar la ventana
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Establecer la geometría de la ventana para que aparezca centrada
        self.setGeometry(x, y, window_width, window_height)

        # Layout principal
        main_layout = QVBoxLayout()
        # Título en la interfaz principal
        title_label = QLabel("Método de Regla del Trapecio con Calculadora Avanzada")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Puedes personalizar el estilo
        main_layout.addWidget(title_label)

        # Entrada de datos
        input_layout = QGridLayout()
        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("Escribe aquí la función f(x), ej: sin(x) + e**x - pi")
        input_layout.addWidget(QLabel("Función f(x):"), 0, 0)
        input_layout.addWidget(self.func_input, 0, 1, 1, 3)

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Ej: 0 debe ser menor que b")
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Ej: 2 debe ser mayor que a" )
        self.n_input = QLineEdit()
        self.n_input.setPlaceholderText("Ej: 4")

        input_layout.addWidget(QLabel("Límite inferior (a):"), 1, 0)
        input_layout.addWidget(self.a_input, 1, 1)
        input_layout.addWidget(QLabel("Límite superior (b):"), 1, 2)
        input_layout.addWidget(self.b_input, 1, 3)
        input_layout.addWidget(QLabel("Número de subintervalos (n):"), 2, 0)
        input_layout.addWidget(self.n_input, 2, 1)

        self.calculate_btn = QPushButton("Calcular")
        self.calculate_btn.clicked.connect(self.run_trapecio)
        input_layout.addWidget(self.calculate_btn, 3, 0, 1, 4)

        # Calculadora
       
        calculator_layout = QGridLayout()
        self.calculator_display = QLineEdit()
        self.calculator_display.setReadOnly(True)
        calculator_layout.addWidget(self.calculator_display, 0, 0, 1, 4)

        # Resultados
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        # Organizar layouts
        main_layout.addLayout(input_layout)

        main_layout.addWidget(QLabel("Resultados:"))
        main_layout.addWidget(self.result_text)

        # Tabla para los resultados
        self.result_table = QTableWidget()
        main_layout.addWidget(self.result_table)

        self.setLayout(main_layout)

    def calculator_button_clicked(self):
        sender = self.sender().text()
        if sender == "C":
            self.calculator_display.clear()
        elif sender == "←":
            current_text = self.calculator_display.text()
            self.calculator_display.setText(current_text[:-1])
        elif sender == "Insertar en f(x)":
            self.func_input.setText(self.calculator_display.text())
        else:
            self.calculator_display.setText(self.calculator_display.text() + sender)
            
    

    

    def run_trapecio(self):
        
        try:
            # Leer entradas del usuario
            funcion = self.func_input.text()
            a = self.a_input.text()
            b = self.b_input.text()
            n = self.n_input.text()

            # Validar función y entradas
            def sec(x):
                return 1 / math.cos(x)

            def csc(x):
                return 1 / math.sin(x)

            def atan(x):
                return math.atan(x)
            
            if n.isdigit():
                n = int(n)
            else:
                n = eval(n, {"x": 0, "e": math.e, "pi": math.pi, "sin": math.sin, "cos": math.cos, "tan": math.tan, 
                            "ln": math.log, "sec": sec, "csc": csc, "atan": atan})

            a = eval(a, {"x": 0, "e": math.e, "pi": math.pi, "sin": math.sin, "cos": math.cos, "tan": math.tan, 
                        "ln": math.log, "sec": sec, "csc": csc, "atan": atan})
            b = eval(b, {"x": 0, "e": math.e, "pi": math.pi, "sin": math.sin, "cos": math.cos, "tan": math.tan, 
                        "ln": math.log, "sec": sec, "csc": csc, "atan": atan})

            # Validar que n es un valor positivo
            if n <= 0:
                self.result_text.append("El número de subintervalos debe ser mayor que 0.")
                return

            # Definir la función
            def f(x):
                return eval(funcion, {"x": x, "e": math.e, "pi": math.pi, "sin": math.sin, "cos": math.cos, "tan": math.tan, "ln": math.log})

            # Aproximación de la segunda derivada (usando la fórmula de diferencia central)
            def second_derivative(f, x, h=1e-5):
                return (f(x + h) - 2 * f(x) + f(x - h)) / h**2

            # Método de la regla del trapecio
            h = (b - a) / n
            x = [a + i * h for i in range(n + 1)]
            y = [f(xi) for xi in x]

            # Calcular el error (utilizamos el punto medio del intervalo como aproximación de xi)
            mid_point = (a + b) / 2
            f_double_prime = second_derivative(f, mid_point)
            error = -(b - a) * h**2 * f_double_prime / 12

            # Coeficientes: el primero y el último son 1, el resto son 2
            coef = [1] + [2] * (n - 1) + [1]

            integral = (h / 2) * (y[0] + 2 * sum(y[1:-1]) + y[-1])

            # Mostrar resultados en la interfaz
            self.result_text.append(f"Resultados de la integración:")
            self.result_text.append(f"Intervalo: [{a:.5f}, {b:.5f}]")
            self.result_text.append(f"Subintervalos (n): {n}")
            self.result_text.append(f"Paso (h): {h:.5f}")
            self.result_text.append(f"Integral aproximada: {integral:.5f}")
            self.result_text.append(f"Error en la aproximación: {error:.5f}")

            # Mostrar pasos
            self.result_text.append(f"\nPasos para la solución:")
            self.result_text.append(f"1. Definir h = (b - a) / n = ({b:.5f} - {a:.5f}) / {n} = {h:.5f}")
            self.result_text.append(f"2. Calcular los valores de x:")
            for i in range(n + 1):
                self.result_text.append(f"   x{i} = {x[i]:.5f}")
            self.result_text.append(f"3. Calcular los valores de f(x):")
            for i in range(n + 1):
                self.result_text.append(f"   f(x{i}) = {y[i]:.5f}")
            
            self.result_text.append(f"4. Aplicar la fórmula de la regla del trapecio:")
            self.result_text.append(f"   Integral = (h / 2) * (f(x0) + 2 * sum(f(xi)) + f(xn))")
            self.result_text.append(f"   Integral = ({h / 2:.5f} / 2) * ({y[0]:.5f} + 2 * sum{y[1:-1]} + {y[-1]:.5f})")
            self.result_text.append(f"   Integral = {integral:.5f}")
            # Mostrar pasos para calcular el error
            self.result_text.append(f"\nPasos para calcular el error:")
            self.result_text.append(f"1. La fórmula del error es: E_T = - (b - a) * h^2 * f''(ξ) / 12")
            self.result_text.append(f"2. Calculamos la segunda derivada de la función f(x):")
            self.result_text.append(f"   Usamos una aproximación numérica de la segunda derivada en el punto medio del intervalo.")
            self.result_text.append(f"   f''(ξ) = {f_double_prime:.5f} en el punto medio ξ = {mid_point:.5f}")
            self.result_text.append(f"3. Calculamos el error usando la fórmula del error.")
            self.result_text.append(f"   E_T = - ({b} - {a}) * {h}^2 * {f_double_prime:.5f} / 12 = {error:.5f}")


            # Crear la tabla
            self.result_table.setRowCount(n + 2)
            self.result_table.setColumnCount(5)
            self.result_table.setHorizontalHeaderLabels(['i', 'xi', 'Coeficiente', 'f(xi)', 'Coef * f(xi)'])
            for i in range(n + 1):
                self.result_table.setItem(i, 0, QTableWidgetItem(str(i)))
                self.result_table.setItem(i, 1, QTableWidgetItem(f"{x[i]:.5f}"))
                self.result_table.setItem(i, 2, QTableWidgetItem(str(coef[i])))
                self.result_table.setItem(i, 3, QTableWidgetItem(f"{y[i]:.5f}"))
                self.result_table.setItem(i, 4, QTableWidgetItem(f"{(coef[i] * y[i]):.5f}"))

            # Sumar la fila final de la tabla
            self.result_table.setItem(n + 1, 0, QTableWidgetItem("Σ"))
            self.result_table.setItem(n + 1, 4, QTableWidgetItem(f"{integral:.5f}"))

            self.show_graph(a, b, f, x, y, n)

        except Exception as e:
            self.result_text.append(f"Error: {e}")


    def show_graph(self, a, b, f, x, y, n):
        # Crear un gráfico de la función
        fig, ax = plt.subplots()
        x_vals = np.linspace(a, b, 100)
        y_vals = [f(val) for val in x_vals]

        ax.plot(x_vals, y_vals, label="f(x)")
        ax.fill_between(x, y, color="orange", alpha=0.3)

        # Dibujar las líneas verticales en cada intervalo
        for xi in x:
            ax.axvline(x=xi, color='r', linestyle='--', alpha=0.6)

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Método de Regla del Trapecio")

        ax.legend()
        canvas = FigureCanvas(fig)
        canvas.draw()

        # Mostrar gráfico en ventana emergente
        graph_window = QDialog(self)
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(canvas)
        graph_window.setLayout(graph_layout)
        graph_window.setWindowTitle("Gráfico de la Función y Regla del Trapecio")
        graph_window.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrapecioApp()
    ex.show()
    sys.exit(app.exec())

