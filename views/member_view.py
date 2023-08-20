from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
)
from PyQt5 import uic

from components import ScrollBoxContainer
from components import MemberCard


class MemberWindow(QMainWindow):
    def __init__(self):
        super(MemberWindow, self).__init__()
        uic.loadUi("./ui/Member Window.ui", self)
        self.setFixedSize(self.size())

        # NEW MEMBER TAB
        self.new_mem = {
            "submit_btn": self.findChild(QPushButton, "NewMemberButton"),
            "nameLE": self.findChild(QLineEdit, "NameLineEdit"),
            "addLE": self.findChild(QLineEdit, "AddLineEdit"),
            "phoneLE": self.findChild(QLineEdit, "PhoneLineEdit"),
        }
        # ============================================================

        # MEMBER ROSTER TAB
        self.member_roster = {
            "load": self.findChild(QPushButton, "LoadButton"),
            "scroll_area": self.findChild(QScrollArea, "MembersListArea"),
            "widget": ScrollBoxContainer(),
        }
        self.member_roster["scroll_area"].setWidget(self.member_roster["widget"])
        # ============================================================

        # EDIT MEMBER TAB

        self.edit_mem = {
            "mem_search": self.findChild(QLineEdit, "MemberSearchLine"),
            # TODO : Add a button to go back to the search page
            "mem_search_btn": self.findChild(QPushButton, "MemberSearchButton"),
            "mem_update_btn": self.findChild(QPushButton, "SubmitButton"),
            "name": self.findChild(QLineEdit, "NameLine"),
            "phone": self.findChild(QLineEdit, "PhoneLine"),
            "address": self.findChild(QLineEdit, "AddressLine"),
            "scroll_area": self.findChild(QScrollArea, "SearchResultArea"),
            "widget": ScrollBoxContainer(),
            "stacked_wig": self.findChild(QStackedWidget, "EditMemberStack"),
        }
        self.edit_mem["scroll_area"].setWidget(self.edit_mem["widget"])
        self.edit_mem["selected_member_code"] = 0

        # ============================================================

    def displayMembers(self, members: dict):
        self.member_roster["widget"].clear()
        for m in members:
            c = MemberCard(m)
            self.member_roster["widget"].add_card(c)

    def display_mem_search_result(self, members: dict):
        self.edit_mem["widget"].clear()
        for m in members:
            c = MemberCard(m)
            c.createLockButton()
            c.lock_btn.clicked.connect(self._lock_func(m))
            self.edit_mem["widget"].add_card(c)

    def _lock_func(self, details: dict):
        def func():
            self.edit_mem["selected_member_code"] = details["member_code"]
            self.edit_mem["stacked_wig"].setCurrentIndex(1)
            self.edit_mem["name"].setText(details["name"])
            self.edit_mem["address"].setText(details["address"])
            self.edit_mem["phone"].setText(details["phone"])

        return func

    def show_msg(self, text: str):
        msg = QMessageBox()
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Alert")

        msg.exec()

    def clearLineEdits(self):
        for k, v in self.new_mem.items():
            if k.endswith("LE"):
                v.clear()

    def clear_update_line_edits(self):
        self.edit_mem["name"].clear()
        self.edit_mem["address"].clear()
        self.edit_mem["phone"].clear()
        self.edit_mem["mem_search"].clear()
        self.edit_mem["widget"].clear()

    def get_mem_details(self):
        name = self.new_mem["nameLE"].text()
        address = self.new_mem["addLE"].text()
        phone = self.new_mem["phoneLE"].text()

        return {"name": name, "address": address, "phone": phone}

    def get_edit_details(self):
        name = self.edit_mem["name"].text()
        address = self.edit_mem["address"].text()
        phone = self.edit_mem["phone"].text()
        return {"name": name, "address": address, "phone": phone}
