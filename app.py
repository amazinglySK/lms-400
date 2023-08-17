from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QMainWindow, QApplication, QMessageBox, QVBoxLayout, QLabel, QPushButton
import mysql.connector
import webbrowser
import sys
import os

from views import BookWindow
from views import MemberWindow
from controllers import BookController
from controllers import MemberController
from xlwriter import Writer
from models import Books
from models import Member




def check_credentials(): 
    try :
        with open("cred.txt", 'r') as file : 
            l = file.readlines()
            [db, user, pwd] = l
            if not l : 
                print("Empty credentials")
                raise Exception

            conn = mysql.connector.connect(host = "localhost", user = user, password = pwd, database = db)
            if not conn.is_connected() : 
                print("Not connected")
                raise Exception

            return conn

    except Exception as err : 
        print(err)
        return False

class DashboardView(QMainWindow):
    def __init__(self, connection):
        # Database
        self.conn = connection
        self.book_model = Books(connection=self.conn)
        self.member_model = Member(connection=self.conn)
        
        # UI
        super(DashboardView, self).__init__()
        uic.loadUi("./ui/Dashboard Window.ui", self)
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

class LoginWindow(QMainWindow) : 
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi("./ui/Login Window.ui", self)

        self.database = self.findChild(QLineEdit, "DbName")
        self.username = self.findChild(QLineEdit, "DbUsername")
        self.pwd = self.findChild(QLineEdit, "DbPassword")
        self.login_btn = self.findChild(QPushButton, "LoginButton")

        self.login_btn.clicked.connect(self._login)

    def _login(self) : 
        details = [self.database.text(), self.username.text(), self.pwd.text()]
        with open('cred.txt', 'w') as file : 
            file.write("\n".join(details))

        if not check_credentials() :
            msg = QMessageBox()
            msg.setText("Invalid Credentials")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Alert")
            msg.show()
            return

        self.window = Window(check_credentials())
        self.window.show()
        self.close()

class Window(QMainWindow):
    def __init__(self, connection):
        super(Window, self).__init__()
        uic.loadUi("./ui/Main Window.ui", self)

        self.continue_button = self.findChild(QPushButton, "ContinueButton")
        self.continue_button.clicked.connect(self._on_dashboard_click)

        self.instruction_button = self.findChild(QPushButton, "Instructions")
        self.instruction_button.clicked.connect(lambda : webbrowser.open("https://github.com/amazinglysk/lms-400"))

        self.conn = connection


    def _on_dashboard_click(self):
        self.w = DashboardView(self.conn)
        self.w.show()


if __name__ == "__main__":
    app = QApplication([])
    if not check_credentials() :
        login = LoginWindow()
        login.show()
    else : 
        main_window = Window(check_credentials())
        main_window.show()
    r = app.exec()
    sys.exit(r)
