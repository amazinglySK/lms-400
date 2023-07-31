from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic


class MemberWindow(QMainWindow):
    def __init__(self):
        super(MemberWindow, self).__init__()
        uic.loadUi("./ui/Member Window.ui", self)

        # NEW MEMBER TAB
        self.new_mem = {}
        self.new_mem["submit_btn"] = self.findChild(QPushButton, "NewMemberButton")
        self.new_mem["nameLE"] = self.findChild(QLineEdit, "NameLineEdit")
        self.new_mem["addLE"] = self.findChild(QLineEdit, "AddLineEdit")
        self.new_mem["phoneLE"] = self.findChild(QLineEdit, "PhoneLineEdit")
        self.new_mem["submit_btn"].clicked.connect(self._handle_new_mem)
        # ============================================================

    def _handle_new_mem(self):
        name = self.new_mem["nameLE"].text()
        address = self.new_mem["addLE"].text()
        phone = self.new_mem["phoneLE"].text()
        print(name, address, phone)
