from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QMessageBox,
)

from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt
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
        # ============================================================

        # MEMBER ROSTER TAB
        self.member_roster = {}
        self.member_roster["scroll_area"] = self.findChild(
            QScrollArea, "MembersListArea"
        )
        self.member_roster["widget"] = QWidget()
        self.member_roster["vbox"] = QVBoxLayout()
        self.member_roster["vbox"].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.member_roster["load"] = self.findChild(QPushButton, "LoadButton")
        self.member_roster["widget"].setLayout(self.member_roster["vbox"])

        self.member_roster["scroll_area"].setWidget(self.member_roster["widget"])
        # ============================================================

        # DEFAULTERS TAB

        self.defaulters = {}
        self.defaulters["scroll_area"] = self.findChild(QScrollArea, "DefaultersArea")
        self.defaulters["widget"] = QWidget()
        self.defaulters["vbox"] = QVBoxLayout()
        self.defaulters["vbox"].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.defaulters["load"] = self.findChild(QPushButton, "DefaulterLoadButton")
        self.defaulters["widget"].setLayout(self.defaulters["vbox"])
        self.defaulters["scroll_area"].setWidget(self.defaulters["widget"])

        # ============================================================

    def displayMembers(self, members: dict):
        self._clearLayout(self.member_roster["vbox"])
        for m in members:
            c = self._memberCard(m["name"], m["phone"])
            self.member_roster["vbox"].addWidget(c)

    def displayDefaulters(self, members: dict):
        self._clearLayout(self.defaulters["vbox"])
        for m in members:
            c = self._memberCard(m["name"], m["phone"])
            self.defaulters["vbox"].addWidget(c)

    def _clearLayout(self, layout: QVBoxLayout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def _memberCard(self, name: str, phone: str) -> QWidget:
        card = QWidget()

        font = QFont("Bahnschrift", 12)
        name = QLabel(f"Name : {name}", card)
        name.setFont(font)
        phone = QLabel(f"Phone : {phone}", card)
        phone.setFont(font)

        card_vbox = QVBoxLayout()
        card_vbox.addWidget(phone, 1)
        card_vbox.addWidget(name, 1)
        card.setLayout(card_vbox)
        card.setFixedHeight(80)
        card.setStyleSheet("background-color : red;")

        return card

    def show_msg(self, text: str):
        msg = QMessageBox()
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Alert")

        msg.exec()

    def clearLineEdits(self):
        for k, v in self.new_mem.items():
            if k.endswith("LE"):
                v.setText("")

    def get_mem_details(self):
        name = self.new_mem["nameLE"].text()
        address = self.new_mem["addLE"].text()
        phone = self.new_mem["phoneLE"].text()

        return {"name": name, "address": address, "phone": phone}
