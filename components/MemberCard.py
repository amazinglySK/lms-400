from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore


class MemberCard(QWidget):
    def __init__(self, details: dict, type="simple"):
        super(MemberCard, self).__init__()
        if type == "simple":
            font = QFont("Bahnschrift", 12)
            self.name = QLabel(f"Name : {details['name']}")
            self.name.setFont(font)
            self.phone = QLabel(f"Phone : {details['phone']}")
            self.phone.setFont(font)

            self.card_vbox = QVBoxLayout()
            self.card_vbox.addWidget(self.phone, 1)
            self.card_vbox.addWidget(self.name, 1)

            self.setLayout(self.card_vbox)
            self.setFixedHeight(80)

            # NOTE : This supposedly causes some performance issue. Keep a check
            self.setAttribute(QtCore.Qt.WA_StyledBackground)
            self.setStyleSheet("background-color: red")
        elif type == "buttoned":
            font = QFont("Bahnschrift", 12)
            self.name = QLabel(f"Name : {details['name']}")
            self.name.setFont(font)
            self.phone = QLabel(f"Phone : {details['phone']}")
            self.phone.setFont(font)
            self.id = QLabel(f"Id : {details['member_code']}")
            self.id.setFont(font)
            self.lock_btn = QPushButton("Lock")
            self.lock_btn.setFont(font)

            self.lock_btn.clicked.connect(self.lock_func)
            self.lock_btn.setFixedWidth(80)

            self.card_vbox = QVBoxLayout()
            self.card_vbox.addWidget(self.name, 1)
            self.card_vbox.addWidget(self.phone, 1)
            self.card_vbox.addWidget(id, 1)
            self.card_vbox.addWidget(self.lock_btn, 1)
            self.setLayout(self.card_vbox)
            self.setFixedHeight(120)
            self.setStyleSheet("background-color : red;")
