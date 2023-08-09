from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout

from PyQt5.QtGui import QFont
from PyQt5 import QtCore


class BookCard(QWidget):
    def __init__(self, details, display_avail=False, lock_btn=False, modified=False):
        super(BookCard, self).__init__()
        card = QWidget()

        font = QFont("Bahnschrift", 12)
        self.title = QLabel(f"Name : {details['title']}", card)
        self.title.setFont(font)
        self.author = QLabel(f"Author : {details['author']}", card)
        self.author.setFont(font)
        if modified:
            self.fine = QLabel(f"Fine : {details['fine']}", card)
            self.fine.setFont(font)
        else:
            self.price = QLabel(f"Price : {details['price']}", card)
            self.price.setFont(font)

        self.card_vbox = QVBoxLayout()
        self.card_vbox.addWidget(self.title, 1)
        self.card_vbox.addWidget(self.author, 1)
        if modified:
            self.card_vbox.addWidget(self.fine)
        else:
            self.card_vbox.addWidget(self.price, 1)
        if display_avail:
            availability = QLabel(
                f"Available : {'yes' if details['member_code'] == 0 else 'no'}"
            )
            availability.setFont(font)
            self.card_vbox.addWidget(availability)
        if lock_btn:
            lock_btn_text = "Lock" if not modified else "Return"
            self.lock_btn = QPushButton(lock_btn_text)
            self.lock_btn.setFont(font)
            self.lock_btn.setFixedWidth(80)
            borrowed = details["member_code"] != 0
            if borrowed and not modified:
                self.lock_btn.setEnabled(False)
            self.card_vbox.addWidget(self.lock_btn)

        self.setLayout(self.card_vbox)
        self.setFixedHeight(140)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet("background-color : blue;")
