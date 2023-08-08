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
    QMessageBox,
    QStackedWidget,
)

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from components.components import ScrollBoxContainer


class BookWindow(QMainWindow):
    def __init__(self):
        super(BookWindow, self).__init__()
        uic.loadUi("./ui/Book Window.ui", self)
        # TODO : Change the QLabels for displaying message to QMessageBox
        # NEW BOOK TAB
        self.newBookTab = {}
        self.newBookTab["submit_btn"] = self.findChild(QPushButton, "NewBookButton")
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

        self.booksTab["all_books_widget"] = ScrollBoxContainer()
        self.booksTab["available_books_widget"] = ScrollBoxContainer()

        self.booksTab["all_books"].setWidget(self.booksTab["all_books_widget"])
        self.booksTab["available_books"].setWidget(
            self.booksTab["available_books_widget"]
        )

        self.booksTab["get_all_books"] = self.findChild(QPushButton, "AllBooksButton")
        self.booksTab["get_avail_books"] = self.findChild(
            QPushButton, "AvailableBooksButton"
        )

        # ==========================================================================

        # ISSUE BOOKS TAB
        self.issueTab = {}

        self.issueTab["member_search"] = self.findChild(QLineEdit, "MemberSearchBox")
        self.issueTab["book_search"] = self.findChild(QLineEdit, "SearchBox")
        self.issueTab["member_search_btn"] = self.findChild(
            QPushButton, "MemberSearchButton"
        )
        self.issueTab["book_search_btn"] = self.findChild(QPushButton, "SearchButton")
        self.issueTab["issue_btn"] = self.findChild(QPushButton, "IssueButton")

        self.issueTab["members_area"] = self.findChild(
            QScrollArea, "MemberSearchResultBox"
        )
        self.issueTab["books_area"] = self.findChild(QScrollArea, "SearchResultBox")

        self.issueTab["members_area_widget"] = ScrollBoxContainer()

        self.issueTab["books_area_widget"] = ScrollBoxContainer()

        self.issueTab["books_area"].setWidget(self.issueTab["books_area_widget"])
        self.issueTab["members_area"].setWidget(self.issueTab["members_area_widget"])
        self.issueTab["selected_member_code"] = 0
        self.issueTab["selected_book_code"] = 0
        # ==========================================================================

        # RETURN BOOKS TAB
        self.returnTab = {}
        self.returnTab["name"] = self.findChild(QLabel, "NameLabel")
        self.returnTab["done_btn"] = self.findChild(QPushButton, "ReturnDoneButton")
        self.returnTab["stacked_wig"] = self.findChild(QStackedWidget, "ReturnStack")
        self.returnTab["member_search"] = self.findChild(
            QLineEdit, "ReturnMemberSearchBox"
        )
        self.returnTab["member_search_btn"] = self.findChild(
            QPushButton, "ReturnMemberSearchButton"
        )

        self.returnTab["members_area"] = self.findChild(
            QScrollArea, "ReturnMemberSearchResults"
        )
        self.returnTab["books_area"] = self.findChild(QScrollArea, "IssuedBooksBox")

        self.returnTab["members_area_widget"] = ScrollBoxContainer()
        self.returnTab["members_area"].setWidget(self.returnTab["members_area_widget"])

        self.returnTab["books_area_widget"] = ScrollBoxContainer()
        self.returnTab["books_area"].setWidget(self.returnTab["books_area_widget"])

        self.returnTab["selected_member_code"] = 0
        self.returnTab["selected_book_code"] = 0
        self.returnTab["member_btns"] = []
        self.returnTab["book_btns"] = []

    def _clearLayout(self, layout: QVBoxLayout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

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

    def display_member_results(self, details: list[dict]):
        self._clearLayout(self.issueTab["members_area_vbox"])
        for d in details:
            c = self._memberCard(d)
            self.issueTab["members_area_vbox"].addWidget(c)

    def display_member_results_return(self, details: list[dict]):
        self._clearLayout(self.returnTab["members_area_vbox"])
        for d in details:
            c = self._memberCardMod(d)
            self.returnTab["members_area_vbox"].addWidget(c)

    def display_books_results(self, details: list):
        self._clearLayout(self.issueTab["books_area_vbox"])
        for d in details:
            b = self._bookCard(d, display_avail=True, lock_btn=True)
            self.issueTab["books_area_vbox"].addWidget(b)

    def display_books_results_return(self, details: list):
        self._clearLayout(self.returnTab["books_area_vbox"])
        for d in details:
            b = self._bookCardMod(d)
            self.returnTab["books_area_vbox"].addWidget(b)

    def display_books(self, details: list, all=True):
        comp = "all_books_vbox" if all else "available_books_vbox"
        self._clearLayout(self.booksTab[comp])
        for d in details:
            b = self._bookCard(d)
            self.booksTab[comp].addWidget(b)

    def _memberCard(self, details: dict) -> QWidget:
        card = QWidget()

        font = QFont("Bahnschrift", 12)
        name = QLabel(f"Name : {details['name']}", card)
        name.setFont(font)
        phone = QLabel(f"Phone : {details['phone']}", card)
        phone.setFont(font)
        id = QLabel(f"Id : {details['member_code']}", card)
        id.setFont(font)
        lock_btn = QPushButton("Lock", card)
        lock_btn.setFont(font)

        def lock_func():
            self.issueTab["selected_member_code"] = details["member_code"]

        lock_btn.clicked.connect(lock_func)
        lock_btn.setFixedWidth(80)

        card_vbox = QVBoxLayout()
        card_vbox.addWidget(name, 1)
        card_vbox.addWidget(phone, 1)
        card_vbox.addWidget(id, 1)
        card_vbox.addWidget(lock_btn, 1)
        card.setLayout(card_vbox)
        card.setFixedHeight(120)
        card.setStyleSheet("background-color : red;")

        return card

    def _memberCardMod(self, details: dict) -> QWidget:
        card = QWidget()

        font = QFont("Bahnschrift", 12)
        name = QLabel(f"Name : {details['name']}", card)
        name.setFont(font)
        phone = QLabel(f"Phone : {details['phone']}", card)
        phone.setFont(font)
        id = QLabel(f"Id : {details['member_code']}", card)
        id.setFont(font)
        lock_btn = QPushButton("Lock", card)
        lock_btn.setFont(font)

        def lock_func():
            self.returnTab["selected_member_code"] = details["member_code"]
            self.returnTab["name"].setText(details["name"])

        lock_btn.clicked.connect(lock_func)
        lock_btn.setFixedWidth(80)

        card_vbox = QVBoxLayout()
        card_vbox.addWidget(name, 1)
        card_vbox.addWidget(phone, 1)
        card_vbox.addWidget(id, 1)
        card_vbox.addWidget(lock_btn, 1)
        self.returnTab["member_btns"].append(lock_btn)
        card.setLayout(card_vbox)
        card.setFixedHeight(120)
        card.setStyleSheet("background-color : red;")

        return card

    def _bookCard(self, details: dict, display_avail=False, lock_btn=False) -> QWidget:
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
        if display_avail:
            availability = QLabel(
                f"Available : {'yes' if details['member_code'] == 0 else 'no'}"
            )
            availability.setFont(font)
            card_vbox.addWidget(availability)
        if lock_btn:
            lock_btn = QPushButton("Lock", card)
            lock_btn.setFont(font)

            def lock_func():
                self.issueTab["selected_book_code"] = details["bookcode"]

            lock_btn.clicked.connect(lock_func)
            lock_btn.setFixedWidth(80)
            borrowed = details["member_code"] != 0
            if borrowed:
                lock_btn.setEnabled(False)
            else:
                lock_btn.clicked.connect(lock_func)
            card_vbox.addWidget(lock_btn)

        card.setLayout(card_vbox)
        card.setFixedHeight(140)
        card.setStyleSheet("background-color : blue;")

        return card

    def _bookCardMod(self, details: dict) -> QWidget:
        card = QWidget()

        font = QFont("Bahnschrift", 12)
        title = QLabel(f"Name : {details['title']}", card)
        title.setFont(font)
        author = QLabel(f"Author : {details['author']}", card)
        author.setFont(font)
        fine = QLabel(f"Fine : {details['fine']}", card)
        fine.setFont(font)

        card_vbox = QVBoxLayout()
        card_vbox.addWidget(title, 1)
        card_vbox.addWidget(author, 1)
        card_vbox.addWidget(fine, 1)
        lock_btn = QPushButton("Return", card)
        lock_btn.setFont(font)

        def lock_func():
            self.returnTab["selected_book_code"] = details["bookcode"]

        lock_btn.clicked.connect(lock_func)
        lock_btn.setFixedWidth(80)
        card_vbox.addWidget(lock_btn)
        self.returnTab["book_btns"].append(lock_btn)

        card.setLayout(card_vbox)
        card.setFixedHeight(140)
        card.setStyleSheet("background-color : blue;")

        return card

    def show_msg(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Alert")

        msg.exec()

    def clear_response(self):
        self.newBookTab["title"].clear()
        self.newBookTab["author"].clear()
        self.newBookTab["publisher"].clear()
        self.newBookTab["price"].setValue(0)

    def clear_issue_lines(self):
        self.issueTab["member_search"].clear()
        self.issueTab["book_search"].clear()
        self._clearLayout(self.issueTab["members_area_vbox"])
        self._clearLayout(self.issueTab["books_area_vbox"])

    def clear_return_window(self):
        self.returnTab["member_search"].clear()
        self.returnTab["name"].clear()
        self._clearLayout(self.returnTab["members_area_vbox"])
        self.returnTab["member_btns"] = []
        self.returnTab["book_btns"] = []
        self._clearLayout(self.returnTab["books_area_vbox"])
