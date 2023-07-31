from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton

import member_view


class DashboardView(QMainWindow):
    def __init__(self):
        super(DashboardView, self).__init__()
        uic.loadUi("./ui/Dashboard Window.ui", self)
        self.member_button = self.findChild(QPushButton, "members_button")
        self.books_button = self.findChild(QPushButton, "books_button")

        self.member_button.clicked.connect(self._redirect_member)

    def _redirect_member(self):
        self.w = member_view.MemberWindow()
        self.w.show()
        self.close()

    # def _redirect_books(self):
    #     self.w = BooksMainWindow()
    #     self.w.show()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("./ui/Main Window.ui", self)

        self.continue_button = self.findChild(QPushButton, "ContinueButton")
        self.continue_button.clicked.connect(self._on_dashboard_click)

    def _on_dashboard_click(self):
        self.w = DashboardView()
        self.w.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
