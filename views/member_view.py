from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
)

from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5 import QtCore

from components import ScrollBoxContainer
from components import MemberCard


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
        # ============================================================

        # MEMBER ROSTER TAB
        self.member_roster = {}
        self.member_roster["load"] = self.findChild(QPushButton, "LoadButton")
        self.member_roster["scroll_area"] = self.findChild(
            QScrollArea, "MembersListArea"
        )
        self.member_roster["widget"] = ScrollBoxContainer()
        self.member_roster["scroll_area"].setWidget(self.member_roster["widget"])
        # ============================================================

        # DEFAULTERS TAB

        self.defaulters = {}
        self.defaulters["scroll_area"] = self.findChild(QScrollArea, "DefaultersArea")
        self.defaulters["widget"] = ScrollBoxContainer()
        self.defaulters["load"] = self.findChild(QPushButton, "DefaulterLoadButton")
        # TODO : Add area to show all the pending books in the library
        self.defaulters["scroll_area"].setWidget(self.defaulters["widget"])

        # ============================================================

        # EDIT MEMBER TAB

        self.edit_mem = {}
        self.edit_mem["mem_search"] = self.findChild(QLineEdit, "MemberSearchLine")
        # TODO : Add a button to go back to the search page
        self.edit_mem["mem_search_btn"] = self.findChild(
            QPushButton, "MemberSearchButton"
        )
        self.edit_mem["mem_update_btn"] = self.findChild(QPushButton, "SubmitButton")
        self.edit_mem["name"] = self.findChild(QLineEdit, "NameLine")
        self.edit_mem["phone"] = self.findChild(QLineEdit, "PhoneLine")
        self.edit_mem["address"] = self.findChild(QLineEdit, "AddressLine")

        self.edit_mem["scroll_area"] = self.findChild(QScrollArea, "SearchResultArea")
        self.edit_mem["widget"] = ScrollBoxContainer()
        self.edit_mem["scroll_area"].setWidget(self.edit_mem["widget"])

        self.edit_mem["stacked_wig"] = self.findChild(QStackedWidget, "EditMemberStack")
        self.edit_mem["selected_member_code"] = 0

        # ============================================================

    def displayMembers(self, members: dict):
        self.member_roster["widget"].clear()
        for m in members:
            c = MemberCard(m)
            self.member_roster["widget"].add_card(c)

    def displayDefaulters(self, members: dict):
        self.defaulters["widget"].clear()
        for m in members:
            c = MemberCard(m)
            self.defaulters["widget"].add_card(c)

    def display_mem_search_result(self, members: dict):
        self.edit_mem["widget"].clear()
        for m in members:
            c = MemberCard(m, "buttoned")
            # FIXIT : self.lock_func() picks up the MemberCard component instead of the window
            c.lock_btn.clicked.connect(lambda _: self.lock_func(m))
            self.edit_mem["widget"].add_card(c)

    def lock_func(self, details: dict):
        self.edit_mem["selected_member_code"] = details["member_code"]
        self.edit_mem["stacked_wig"].setCurrentIndex(1)
        self.edit_mem["name"].setText(details["name"])
        self.edit_mem["address"].setText(details["address"])
        self.edit_mem["phone"].setText(details["phone"])

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
