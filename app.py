from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton
import mysql.connector
import sys

from views.book_view import BookWindow
from views.member_view import MemberWindow
from controllers.book_controller import BookController
from controllers.member_controller import MemberController
from models.books import Books
from models.member import Member


class DashboardView(QMainWindow):
    def __init__(self):
        super(DashboardView, self).__init__()
        uic.loadUi("./ui/Dashboard Window.ui", self)
        self.member_button = self.findChild(QPushButton, "members_button")
        self.books_button = self.findChild(QPushButton, "books_button")

        # Database
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="tiger", database="LMS"
        )
        self.book_model = Books(connection=self.conn)
        self.member_model = Member(connection=self.conn)

        self.member_button.clicked.connect(self._redirect_member)
        self.books_button.clicked.connect(self._redirect_books)

    def _redirect_member(self):
        self.w = MemberWindow()
        self.w_controller = MemberController(self.book_model, self.member_model, self.w)
        self.w.show()
        self.close()

    def _redirect_books(self):
        self.w = BookWindow()
        self.w_controller = BookController(self.book_model, self.member_model, self.w)
        self.w.show()
        self.close()


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
    r = app.exec()
    sys.exit(r)
