from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QVBoxLayout, QLabel, QPushButton
import mysql.connector
import webbrowser
import sys

from views import BookWindow
from views import MemberWindow
from controllers import BookController
from controllers import MemberController
from xlwriter import Writer
from models import Books
from models import Member


class DashboardView(QMainWindow):
    def __init__(self):
        super(DashboardView, self).__init__()
        uic.loadUi("./ui/Dashboard Window.ui", self)
        self.member_button = self.findChild(QPushButton, "members_button")
        self.books_button = self.findChild(QPushButton, "books_button")
        self.report_button = self.findChild(QPushButton, "ReportButton")

        # Database
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="tiger", database="LMS"
        )
        self.book_model = Books(connection=self.conn)
        self.member_model = Member(connection=self.conn)

        self.member_button.clicked.connect(self._redirect_member)
        self.books_button.clicked.connect(self._redirect_books)
        self.report_button.clicked.connect(self._download_report)

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

    def _download_report(self) : 
        filepath = QFileDialog.getExistingDirectory(self, "Select a folder")
        xl_writer = Writer(f"{filepath}/LMS-Report.xlsx")
        books = self.book_model.get_all_books(raw = True)
        book_header = self.book_model.struct
        members = self.member_model.get_all_members(raw = True)
        member_header = self.member_model.struct
        xl_writer.add_worksheet("Members", members, member_header)
        xl_writer.add_worksheet("Books", books, book_header)
        xl_writer.finish_task()

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("./ui/Main Window.ui", self)

        self.continue_button = self.findChild(QPushButton, "ContinueButton")
        self.continue_button.clicked.connect(self._on_dashboard_click)

        self.instruction_button = self.findChild(QPushButton, "Instructions")
        self.instruction_button.clicked.connect(lambda : webbrowser.open("https://github.com/amazinglysk/lms-400"))

    def _on_dashboard_click(self):
        self.w = DashboardView()
        self.w.show()


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    r = app.exec()
    sys.exit(r)
