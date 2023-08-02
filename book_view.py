from PyQt5.QtWidgets import (
    QComboBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QLabel,
)
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

    def set_response(self, text):
        self.newBookTab["display"].setText(text)
