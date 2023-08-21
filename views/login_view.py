import mysql.connector
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QPushButton, QMessageBox)
from .main_view import Window
from PyQt5 import uic


def check_credentials():
    try:
        with open("cred.txt", "r") as file:
            l = file.readlines()
            [db, user, pwd] = l
            if not l:
                print("Empty credentials")
                raise Exception

            conn = mysql.connector.connect(
                host="localhost", user=user, password=pwd, database=db
            )
            if not conn.is_connected():
                print("Not connected")
                raise Exception

            return conn

    except Exception as err:
        print(err)
        return False


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        uic.loadUi("./ui/Login Window.ui", self)
        self.setFixedSize(self.size())

        self.database = self.findChild(QLineEdit, "DbName")
        self.username = self.findChild(QLineEdit, "DbUsername")
        self.pwd = self.findChild(QLineEdit, "DbPassword")
        self.login_btn = self.findChild(QPushButton, "LoginButton")

        self.login_btn.clicked.connect(self._login)

    def _login(self):
        details = [self.database.text(), self.username.text(), self.pwd.text()]
        with open("cred.txt", "w") as file:
            file.write("\n".join(details))

        if not check_credentials():
            msg = QMessageBox()
            msg.setText("Invalid Credentials")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Alert")
            msg.show()
            return

        self.window = Window(check_credentials())
        self.window.show()
        self.close()
