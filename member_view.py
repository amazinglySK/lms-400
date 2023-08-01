from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel
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
        self.new_mem["display"] = self.findChild(QLabel, "NewMemDisplay")
        # ============================================================

    def setDisplayText(self, text: str):
        self.new_mem["display"].setText(text)
        self.new_mem["display"].setFocus()

    def clearLineEdits(self):
        for k, v in self.new_mem.items():
            if k.endswith("LE"):
                v.setText("")

    def get_mem_details(self):
        name = self.new_mem["nameLE"].text()
        address = self.new_mem["addLE"].text()
        phone = self.new_mem["phoneLE"].text()

        return {"name": name, "address": address, "phone": phone}
