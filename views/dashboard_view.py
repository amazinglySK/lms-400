from PyQt5.QtWidgets import (QPushButton, QFileDialog, QMainWindow)
from PyQt5 import uic

from views import BookWindow
from views import MemberWindow
from controllers import BookController
from controllers import MemberController
from report import Report
from models import Books
from models import Member



class DashboardView(QMainWindow):
    def __init__(self, connection):
        # Database
        self.conn = connection
        self.book_model = Books(connection=self.conn)
        self.member_model = Member(connection=self.conn)

        # UI
        super(DashboardView, self).__init__()
        uic.loadUi("./ui/Dashboard Window.ui", self)
        self.setFixedSize(self.size())
        self.member_button = self.findChild(QPushButton, "members_button")
        self.books_button = self.findChild(QPushButton, "books_button")
        self.report_button = self.findChild(QPushButton, "ReportButton")

        # Connecting signals
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

    def _download_report(self):
        url, extension = QFileDialog.getSaveFileName(
            self, "Save report", filter=".xlsx"
        )
        filepath = url + extension
        if not filepath:
            return
        r=Report(filepath,book_model=self.book_model, member_model=self.member_model)
        r.create_report()

