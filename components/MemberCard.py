from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore


class MemberCard(QWidget):
    def __init__(self, details: dict):
        super(MemberCard, self).__init__()
        font = QFont("Bahnschrift", 12)
        self.text_styles = "border : none; color : #0a050f;"
        self.button_styles = "color : #faf7fd; background-color : #59248f;"
        self.card_style = "background-color : #deceef; border-radius : 5px;"
        self.name = QLabel(f"Name : {details['name']}")
        self.name.setFont(font)
        self.name.setStyleSheet(self.text_styles)
        self.phone = QLabel(f"Phone : {details['phone']}")
        self.phone.setFont(font)
        self.phone.setStyleSheet(self.text_styles)
        self.id = QLabel(f"Id : {details['member_code']}")
        self.id.setFont(font)
        self.id.setStyleSheet(self.text_styles)

        self.card_vbox = QVBoxLayout()
        self.card_vbox.addWidget(self.phone, 1)
        self.card_vbox.addWidget(self.name, 1)
        self.card_vbox.addWidget(self.id, 1)

        self.setLayout(self.card_vbox)
        self.setFixedHeight(120)

        # NOTE : This supposedly causes some performance issue. Keep a check
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet(self.card_style)

    def createLockButton(self):
        font = QFont("Bahnschrift", 12)
        self.lock_btn = QPushButton("Lock")
        self.lock_btn.setFont(font)
        self.lock_btn.setFixedWidth(80)
        self.lock_btn.setStyleSheet(self.button_styles)
        self.card_vbox.addWidget(self.lock_btn)
