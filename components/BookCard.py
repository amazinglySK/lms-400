from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout

from PyQt5.QtGui import QFont
from PyQt5 import QtCore


class BookCard(QWidget):
    # Modified stands for return tab buttons
    # lock_btn decides if there needs to be button
    # display_avail decides if availability needs to be displayed
    def __init__(self, details):
        super(BookCard, self).__init__()
        self.details = details
        self.book_code = details["bookcode"]
        self.text_styles = "border : none; color : #0a050f;"
        self.button_styles = "color : #faf7fd; background-color : #59248f;"
        self.card_style = "background-color : #deceef; border-radius : 5px;"
        self.font = QFont("Bahnschrift", 12)
        self.title = QLabel(f"Name : {details['title']}")
        self.title.setStyleSheet(self.text_styles)
        self.title.setFont(self.font)
        self.author = QLabel(f"Author : {details['author']}")
        self.author.setFont(self.font)
        self.author.setStyleSheet(self.text_styles)
        self.price = QLabel(f"Price : {details['price']}")
        self.price.setFont(self.font)
        self.price.setStyleSheet(self.text_styles)

        self.card_vbox = QVBoxLayout()
        self.card_vbox.addWidget(self.title, 1)
        self.card_vbox.addWidget(self.author, 1)
        self.card_vbox.addWidget(self.price, 1)
        self.setLayout(self.card_vbox)
        self.setFixedHeight(140)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet(self.card_style)

    def show_availability(self):
        self.availability = QLabel(
            f"Available : {'yes' if self.details['member_code'] == 0 else 'no'}"
        )
        self.availability.setFont(self.font)
        self.availability.setStyleSheet(self.text_styles)
        self.card_vbox.addWidget(self.availability)

    def show_lock_btn(self, type: str):
        self.lock_btn = QPushButton(type)
        self.lock_btn.setFont(self.font)
        self.lock_btn.setStyleSheet(self.button_styles)
        self.lock_btn.setFixedWidth(80)
        if type == "Lock":
            borrowed = self.details["member_code"] != 0
            if borrowed:
                self.lock_btn.setEnabled(False)
        self.card_vbox.addWidget(self.lock_btn)

    def show_fine(self):
        self.price.setParent(None)
        self.fine = QLabel(f"Fine : {self.details['fine']}")
        self.fine.setFont(self.font)
        self.fine.setStyleSheet(self.text_styles)
        self.card_vbox.insertWidget(self.card_vbox.count() - 1, self.fine)
