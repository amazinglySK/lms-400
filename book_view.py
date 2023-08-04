from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QLabel,
    QVBoxLayout,
    QScrollArea,
)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic


class BookWindow(QMainWindow):
    def __init__(self):
        super(BookWindow, self).__init__()
        uic.loadUi("./ui/Book Window.ui", self)

        # NEW BOOK TAB
        self.newBookTab = {}
        self.newBookTab["submit_btn"] = self.findChild(QPushButton, "NewBookButton")
        self.newBookTab["display"] = self.findChild(QLabel, "display_text")
        self.newBookTab["title"] = self.findChild(QLineEdit, "Title")
        self.newBookTab["author"] = self.findChild(QLineEdit, "Author")
        self.newBookTab["publisher"] = self.findChild(QLineEdit, "Publisher")
        self.newBookTab["price"] = self.findChild(QSpinBox, "Price")
        self.newBookTab["subject"] = self.findChild(QComboBox, "Subject")

        # ==========================================================================

        # ALL BOOKS TAB
        self.booksTab = {}
        self.booksTab["all_books"] = self.findChild(QScrollArea, "AllBooksScrollArea")
        self.booksTab["available_books"] = self.findChild(
            QScrollArea, "AvailableBooksScrollArea"
        )

        self.booksTab["all_books_widget"] = QWidget()
        self.booksTab["all_books_vbox"] = QVBoxLayout()
        self.booksTab["all_books_vbox"].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.booksTab["all_books_widget"].setLayout(self.booksTab["all_books_vbox"])

        self.booksTab["available_books_widget"] = QWidget()
        self.booksTab["available_books_vbox"] = QVBoxLayout()
        self.booksTab["available_books_vbox"].setAlignment(Qt.AlignmentFlag.AlignTop)
        self.booksTab["available_books_widget"].setLayout(
            self.booksTab["available_books_vbox"]
        )

        self.booksTab["all_books"].setWidget(self.booksTab["all_books_widget"])
        self.booksTab["available_books"].setWidget(
            self.booksTab["available_books_widget"]
        )

        self.booksTab["get_all_books"] = self.findChild(QPushButton, "AllBooksButton")
        self.booksTab["get_avail_books"] = self.findChild(
            QPushButton, "AvailableBooksButton"
        )

    def get_book_details(self):
        title = self.newBookTab["title"].text()
        author = self.newBookTab["author"].text()
        publisher = self.newBookTab["publisher"].text()
        price = self.newBookTab["price"].value()
        subject = self.newBookTab["subject"].currentText()
        d = {
            "title": title,
            "author": author,
            "publisher": publisher,
            "price": price,
            "sub_code": subject,
        }

        return d

    def display_books(self, details: list, all=True):
        comp = "all_books_vbox" if all else "available_books_vbox"
        for d in details:
            b = self._bookCard(d)
            self.booksTab[comp].addWidget(b)

    def _bookCard(self, details: dict) -> QWidget:
        card = QWidget()

        font = QFont("Bahnschrift", 12)
        title = QLabel(f"Name : {details['title']}", card)
        title.setFont(font)
        author = QLabel(f"Author : {details['author']}", card)
        author.setFont(font)
        price = QLabel(f"Price : {details['price']}", card)
        price.setFont(font)

        card_vbox = QVBoxLayout()
        card_vbox.addWidget(title, 1)
        card_vbox.addWidget(author, 1)
        card_vbox.addWidget(price, 1)
        card.setLayout(card_vbox)
        card.setFixedHeight(120)
        card.setStyleSheet("background-color : blue;")

        return card

    def set_response(self, text):
        self.newBookTab["display"].setText(text)
