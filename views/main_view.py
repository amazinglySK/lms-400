from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton
import webbrowser

from .dashboard_view import DashboardView

class Window(QMainWindow):
    def __init__(self, connection):
        super(Window, self).__init__()
        uic.loadUi("./ui/Main Window.ui", self)
        self.setFixedSize(self.size())

        self.continue_button = self.findChild(QPushButton, "ContinueButton")
        self.continue_button.clicked.connect(self._on_dashboard_click)

        self.instruction_button = self.findChild(QPushButton, "Instructions")
        self.instruction_button.clicked.connect(
            lambda: webbrowser.open("https://github.com/amazinglysk/lms-400")
        )

        self.conn = connection

    def _on_dashboard_click(self):
        self.w = DashboardView(self.conn)
        self.w.show()
