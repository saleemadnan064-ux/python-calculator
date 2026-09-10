import sys
import math
import cmath
import ast
import operator

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QMessageBox,
)


# ============================================================
# SAFE EXPRESSION EVALUATOR
# ============================================================

class SafeEvaluator:
    """
    Safely evaluates basic calculator expressions.

    Supported:
        +
        -
        *
        /
        %
        **
        numbers
        parentheses
    """

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression, mode="eval")
        return cls._evaluate_node(tree.body)

    @classmethod
    def _evaluate_node(cls, node):

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Invalid value")

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):

            operator_function = cls.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError("Unsupported operator")

            left = cls._evaluate_node(node.left)
            right = cls._evaluate_node(node.right)

            return operator_function(left, right)

        if isinstance(node, ast.UnaryOp):

            operator_function = cls.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError("Unsupported operator")

            value = cls._evaluate_node(node.operand)

            return operator_function(value)

        raise ValueError("Invalid expression")


# ============================================================
# QUADRATIC EQUATION DIALOG
# ============================================================

class QuadraticDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Quadratic Equation")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        title = QLabel(
            "Solve ax² + bx + c = 0"
        )

        title.setObjectName("dialogTitle")

        layout.addWidget(title)

        form = QFormLayout()

        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        self.c_input = QLineEdit()

        self.a_input.setPlaceholderText("Enter a")
        self.b_input.setPlaceholderText("Enter b")
        self.c_input.setPlaceholderText("Enter c")

        form.addRow("a:", self.a_input)
        form.addRow("b:", self.b_input)
        form.addRow("c:", self.c_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def values(self):

        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())

            return a, b, c

        except ValueError:
            raise ValueError(
                "Please enter valid numbers."
            )


# ============================================================
# MAIN CALCULATOR
# ============================================================

class Calculator(QMainWindow):

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.setWindowTitle("Professional Calculator")

        self.resize(560, 760)

        self.setMinimumSize(
            480,
            650
        )

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.just_calculated = False

        # ----------------------------------------------------
        # Main widget
        # ----------------------------------------------------

        self.central_widget = QWidget()

        self.setCentralWidget(
            self.central_widget
        )

        self.main_layout = QVBoxLayout(
            self.central_widget
        )

        self.main_layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        self.main_layout.setSpacing(12)

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.create_title()
        self.create_display()
        self.create_buttons()

        # ----------------------------------------------------
        # Styling
        # ----------------------------------------------------

        self.apply_stylesheet()

    # ========================================================
    # TITLE
    # ========================================================

    def create_title(self):

        title = QLabel(
            "SCIENTIFIC CALCULATOR"
        )

        title.setObjectName(
            "appTitle"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        self.main_layout.addWidget(
            title
        )

    # ========================================================
    # DISPLAY
    # ========================================================

    def create_display(self):

        self.display = QLineEdit()

        self.display.setObjectName(
            "display"
        )

        self.display.setAlignment(
            Qt.AlignRight
        )

        self.display.setReadOnly(
            True
        )

        self.display.setMinimumHeight(
            90
        )

        font = QFont(
            "Segoe UI",
            28
        )

        font.setBold(True)

        self.display.setFont(
            font
        )

        self.main_layout.addWidget(
            self.display
        )

    # ========================================================
    # BUTTON CREATION
    # ========================================================

    def create_button(
        self,
        text,
        callback,
        button_type="number"
    ):

        button = QPushButton(text)

        button.setMinimumHeight(
            58
        )

        button.setFont(
            QFont(
                "Segoe UI",
                14
            )
        )

        button.setProperty(
            "buttonType",
            button_type
        )

        button.clicked.connect(
            callback
        )

        return button

    # ========================================================
    # BUTTON GRID
    # ========================================================

    def create_buttons(self):

        grid = QGridLayout()

        grid.setSpacing(
            8
        )

        self.main_layout.addLayout(
            grid
        )

        # ----------------------------------------------------
        # Scientific buttons
        # ----------------------------------------------------

        scientific_buttons = [
            ("sin", self.sin),
            ("cos", self.cos),
            ("tan", self.tan),
            ("sin⁻¹", self.asin),
            ("cos⁻¹", self.acos),
            ("tan⁻¹", self.atan),
            ("log", self.log),
            ("1/x", self.inverse),
        ]

        positions = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
        ]

        for (
            (text, callback),
            (row, column)
        ) in zip(
            scientific_buttons,
            positions
        ):

            button = self.create_button(
                text,
                callback,
                "scientific"
            )

            grid.addWidget(
                button,
                row,
                column
            )

        # ----------------------------------------------------
        # Second scientific row
        # ----------------------------------------------------

        extra_buttons = [
            ("x²", self.square),
            ("x³", self.cube),
            ("√x", self.square_root),
            ("π", self.pi),
        ]

        for column, (
            text,
            callback
        ) in enumerate(extra_buttons):

            button = self.create_button(
                text,
                callback,
                "scientific"
            )

            grid.addWidget(
                button,
                2,
                column
            )

        # ----------------------------------------------------
        # Third scientific row
        # ----------------------------------------------------

        extra_buttons_2 = [
            ("eˣ", self.exp),
            ("10ˣ", self.ten_power),
            ("%", self.percentage),
            ("MOD", self.mod),
        ]

        for column, (
            text,
            callback
        ) in enumerate(extra_buttons_2):

            button = self.create_button(
                text,
                callback,
                "scientific"
            )

            grid.addWidget(
                button,
                3,
                column
            )

        # ----------------------------------------------------
        # Main calculator
        # ----------------------------------------------------

        buttons = [
            ("C", self.clear, "clear"),
            ("DEL", self.delete_last, "clear"),
            ("(", lambda: self.insert("("), "operator"),
            (")", lambda: self.insert(")"), "operator"),

            ("7", lambda: self.number("7"), "number"),
            ("8", lambda: self.number("8"), "number"),
            ("9", lambda: self.number("9"), "number"),
            ("÷", lambda: self.insert("/"), "operator"),

            ("4", lambda: self.number("4"), "number"),
            ("5", lambda: self.number("5"), "number"),
            ("6", lambda: self.number("6"), "number"),
            ("×", lambda: self.insert("*"), "operator"),

            ("1", lambda: self.number("1"), "number"),
            ("2", lambda: self.number("2"), "number"),
            ("3", lambda: self.number("3"), "number"),
            ("−", lambda: self.insert("-"), "operator"),

            ("0", lambda: self.number("0"), "number"),
            (".", lambda: self.insert("."), "number"),
            ("+", lambda: self.insert("+"), "operator"),
            ("=", self.calculate, "equal"),
        ]

        start_row = 4

        for index, (
            text,
            callback,
            button_type
        ) in enumerate(buttons):

            row = start_row + index // 4
            column = index % 4

            button = self.create_button(
                text,
                callback,
                button_type
            )

            grid.addWidget(
                button,
                row,
                column
            )

        # ----------------------------------------------------
        # Quadratic equation
        # ----------------------------------------------------

        quadratic_button = self.create_button(
            "QUADRATIC",
            self.quadratic,
            "scientific"
        )

        grid.addWidget(
            quadratic_button,
            9,
            0,
            1,
            4
        )

    # ========================================================
    # INPUT
    # ========================================================

    def number(self, value):

        if self.just_calculated:

            self.display.clear()

            self.just_calculated = False

        self.display.insert(
            value
        )

    # --------------------------------------------------------

    def insert(self, value):

        if self.just_calculated:

            self.display.clear()

            self.just_calculated = False

        self.display.insert(
            value
        )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear(self):

        self.display.clear()

        self.just_calculated = False

    # ========================================================
    # DELETE
    # ========================================================

    def delete_last(self):

        text = self.display.text()

        self.display.setText(
            text[:-1]
        )

    # ========================================================
    # CALCULATE
    # ========================================================

    def calculate(self):

        expression = self.display.text().strip()

        if not expression:
            return

        try:

            result = SafeEvaluator.evaluate(
                expression
            )

            result = self.format_result(
                result
            )

            self.display.setText(
                result
            )

            self.just_calculated = True

        except ZeroDivisionError:

            self.show_error(
                "Cannot divide by zero."
            )

        except Exception:

            self.show_error(
                "Invalid mathematical expression."
            )

    # ========================================================
    # RESULT FORMAT
    # ========================================================

    @staticmethod
    def format_result(result):

        if isinstance(result, float):

            if math.isfinite(result):

                if result.is_integer():
                    return str(
                        int(result)
                    )

                return f"{result:.12g}"

        return str(result)

    # ========================================================
    # GET NUMBER
    # ========================================================

    def get_number(self):

        text = self.display.text().strip()

        if not text:

            raise ValueError(
                "Enter a number first."
            )

        return float(text)

    # ========================================================
    # TRIGONOMETRY
    # ========================================================

    def sin(self):

        try:

            number = self.get_number()

            result = math.sin(
                math.radians(number)
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # --------------------------------------------------------

    def cos(self):

        try:

            number = self.get_number()

            result = math.cos(
                math.radians(number)
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # --------------------------------------------------------

    def tan(self):

        try:

            number = self.get_number()

            result = math.tan(
                math.radians(number)
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # ========================================================
    # INVERSE TRIGONOMETRY
    # ========================================================

    def asin(self):

        try:

            value = self.get_number()

            if not -1 <= value <= 1:
                raise ValueError(
                    "sin⁻¹ input must be between -1 and 1."
                )

            result = math.degrees(
                math.asin(value)
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # --------------------------------------------------------

    def acos(self):

        try:

            value = self.get_number()

            if not -1 <= value <= 1:
                raise ValueError(
                    "cos⁻¹ input must be between -1 and 1."
                )

            result = math.degrees(
                math.acos(value)
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # --------------------------------------------------------

    def atan(self):

        try:

            value = self.get_number()

            result = math.degrees(
                math.atan(value)
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # ========================================================
    # LOG
    # ========================================================

    def log(self):

        try:

            number = self.get_number()

            if number <= 0:
                raise ValueError(
                    "Logarithm requires a positive number."
                )

            result = math.log10(
                number
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:
            self.show_error(
                str(error)
            )

    # ========================================================
    # INVERSE
    # ========================================================

    def inverse(self):

        try:

            number = self.get_number()

            if number == 0:
                raise ZeroDivisionError

            result = 1 / number

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except ZeroDivisionError:

            self.show_error(
                "Cannot calculate 1/0."
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # SQUARE
    # ========================================================

    def square(self):

        try:

            number = self.get_number()

            result = number ** 2

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # CUBE
    # ========================================================

    def cube(self):

        try:

            number = self.get_number()

            result = number ** 3

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # SQUARE ROOT
    # ========================================================

    def square_root(self):

        try:

            number = self.get_number()

            if number < 0:

                result = cmath.sqrt(
                    number
                )

                self.display.setText(
                    str(result)
                )

            else:

                result = math.sqrt(
                    number
                )

                self.display.setText(
                    self.format_result(result)
                )

            self.just_calculated = True

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # PI
    # ========================================================

    def pi(self):

        if self.just_calculated:

            self.display.clear()

            self.just_calculated = False

        self.display.insert(
            str(math.pi)
        )

    # ========================================================
    # EXP
    # ========================================================

    def exp(self):

        try:

            number = self.get_number()

            result = math.exp(
                number
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except OverflowError:

            self.show_error(
                "The result is too large."
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # 10 POWER
    # ========================================================

    def ten_power(self):

        try:

            number = self.get_number()

            result = 10 ** number

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except OverflowError:

            self.show_error(
                "The result is too large."
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # PERCENTAGE
    # ========================================================

    def percentage(self):

        try:

            expression = self.display.text()

            if not expression:
                return

            result = SafeEvaluator.evaluate(
                expression
            )

            result = result / 100

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # MOD / ABSOLUTE VALUE
    # ========================================================

    def mod(self):

        try:

            number = self.get_number()

            result = abs(
                number
            )

            self.display.setText(
                self.format_result(result)
            )

            self.just_calculated = True

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # QUADRATIC EQUATION
    # ========================================================

    def quadratic(self):

        dialog = QuadraticDialog(
            self
        )

        if dialog.exec_() != QDialog.Accepted:
            return

        try:

            a, b, c = dialog.values()

            if a == 0:

                raise ValueError(
                    "Coefficient 'a' cannot be zero."
                )

            discriminant = (
                b ** 2
                - 4 * a * c
            )

            root = cmath.sqrt(
                discriminant
            )

            x1 = (
                -b + root
            ) / (2 * a)

            x2 = (
                -b - root
            ) / (2 * a)

            result = (
                f"x₁ = {self.format_complex(x1)}\n"
                f"x₂ = {self.format_complex(x2)}"
            )

            self.display.setText(
                result.replace("\n", "  ")
            )

            self.just_calculated = True

        except Exception as error:

            self.show_error(
                str(error)
            )

    # ========================================================
    # COMPLEX NUMBER FORMAT
    # ========================================================

    @staticmethod
    def format_complex(value):

        if abs(value.imag) < 1e-12:

            return f"{value.real:.10g}"

        return (
            f"{value.real:.10g}"
            f"{value.imag:+.10g}i"
        )

    # ========================================================
    # ERROR MESSAGE
    # ========================================================

    def show_error(self, message):

        QMessageBox.warning(
            self,
            "Calculator Error",
            message
        )

    # ========================================================
    # KEYBOARD SUPPORT
    # ========================================================

    def keyPressEvent(self, event):

        key = event.key()

        # Numbers
        if (
            Qt.Key_0
            <= key
            <= Qt.Key_9
        ):

            self.number(
                str(
                    key - Qt.Key_0
                )
            )

            return

        # Operators
        operators = {
            Qt.Key_Plus: "+",
            Qt.Key_Minus: "-",
            Qt.Key_Asterisk: "*",
            Qt.Key_Slash: "/",
            Qt.Key_Percent: "%",
            Qt.Key_ParenLeft: "(",
            Qt.Key_ParenRight: ")",
            Qt.Key_Period: ".",
        }

        if key in operators:

            self.insert(
                operators[key]
            )

            return

        # Enter
        if key in (
            Qt.Key_Return,
            Qt.Key_Enter,
        ):

            self.calculate()

            return

        # Backspace
        if key == Qt.Key_Backspace:

            self.delete_last()

            return

        # Escape
        if key == Qt.Key_Escape:

            self.clear()

            return

        super().keyPressEvent(
            event
        )

    # ========================================================
    # PROFESSIONAL STYLING
    # ========================================================

    def apply_stylesheet(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }

            QWidget {
                background-color: #121212;
                color: #FFFFFF;
            }

            QLabel#appTitle {
                color: #BDBDBD;
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 2px;
                padding: 4px;
            }

            QLineEdit#display {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #333333;
                border-radius: 14px;
                padding: 12px 18px;
                selection-background-color: #3F51B5;
            }

            QPushButton {
                border: none;
                border-radius: 12px;
                padding: 8px;
                font-weight: 600;
            }

            QPushButton[buttonType="number"] {
                background-color: #2A2A2A;
                color: #FFFFFF;
            }

            QPushButton[buttonType="number"]:hover {
                background-color: #383838;
            }

            QPushButton[buttonType="number"]:pressed {
                background-color: #444444;
            }

            QPushButton[buttonType="operator"] {
                background-color: #3F51B5;
                color: #FFFFFF;
            }

            QPushButton[buttonType="operator"]:hover {
                background-color: #536DFE;
            }

            QPushButton[buttonType="operator"]:pressed {
                background-color: #303F9F;
            }

            QPushButton[buttonType="scientific"] {
                background-color: #252525;
                color: #BDBDBD;
                border: 1px solid #383838;
            }

            QPushButton[buttonType="scientific"]:hover {
                background-color: #333333;
                color: #FFFFFF;
            }

            QPushButton[buttonType="scientific"]:pressed {
                background-color: #414141;
            }

            QPushButton[buttonType="clear"] {
                background-color: #6D3434;
                color: #FFFFFF;
            }

            QPushButton[buttonType="clear"]:hover {
                background-color: #854040;
            }

            QPushButton[buttonType="equal"] {
                background-color: #00A8CC;
                color: #FFFFFF;
                font-size: 18px;
            }

            QPushButton[buttonType="equal"]:hover {
                background-color: #12BFE3;
            }

            QPushButton[buttonType="equal"]:pressed {
                background-color: #0089A7;
            }

            QDialog {
                background-color: #1E1E1E;
            }

            QDialog QLabel {
                color: #FFFFFF;
            }

            QLabel#dialogTitle {
                font-size: 17px;
                font-weight: bold;
                padding-bottom: 10px;
            }

            QDialog QLineEdit {
                background-color: #2A2A2A;
                color: #FFFFFF;
                border: 1px solid #444444;
                border-radius: 7px;
                padding: 8px;
            }

            QDialog QPushButton {
                background-color: #3F51B5;
                color: #FFFFFF;
                min-width: 80px;
            }

            QDialog QPushButton:hover {
                background-color: #536DFE;
            }

            QMessageBox {
                background-color: #1E1E1E;
            }
        """)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Professional Calculator"
    )

    app.setStyle(
        "Fusion"
    )

    calculator = Calculator()

    calculator.show()

    sys.exit(
        app.exec_()
    )


if __name__ == "__main__":
    main()