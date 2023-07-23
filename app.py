from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton


class AnotherWindow(QMainWindow):
    def __init__(self):
        super(AnotherWindow, self).__init__()
        uic.loadUi("./ui/Dashboard Window.ui", self)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("./ui/Main Window.ui", self)

        self.continue_button = self.findChild(QPushButton, "ContinueButton")
        self.continue_button.clicked.connect(self._on_dashboard_click)

    def _on_dashboard_click(self):
        self.w = AnotherWindow()
        self.w.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
