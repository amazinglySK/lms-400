from PyQt5.QtWidgets import (
    QComboBox,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QLabel,
    QScrollArea,
    QMessageBox,
    QStackedWidget,
)

from PyQt5 import uic

from components import ScrollBoxContainer
from components import MemberCard
from components import BookCard


class BookWindow(QMainWindow):
    def __init__(self):
        super(BookWindow, self).__init__()
        uic.loadUi("./ui/Book Window.ui", self)
        self.setFixedSize(self.size())

        # NEW BOOK TAB
        self.newBookTab = {
            "submit_btn": self.findChild(QPushButton, "NewBookButton"),
            "title": self.findChild(QLineEdit, "Title"),
            "author": self.findChild(QLineEdit, "Author"),
            "publisher": self.findChild(QLineEdit, "Publisher"),
            "price": self.findChild(QSpinBox, "Price"),
            "subject": self.findChild(QComboBox, "Subject"),
        }
        # ==========================================================================

        # ALL BOOKS TAB
        self.booksTab = {
            "all_books": self.findChild(QScrollArea, "AllBooksScrollArea"),
            "available_books": self.findChild(QScrollArea, "AvailableBooksScrollArea"),
            "all_books_widget": ScrollBoxContainer(),
            "available_books_widget": ScrollBoxContainer(),
            "get_all_books": self.findChild(QPushButton, "AllBooksButton"),
            "get_avail_books": self.findChild(QPushButton, "AvailableBooksButton"),
        }

        self.booksTab["all_books"].setWidget(self.booksTab["all_books_widget"])
        self.booksTab["available_books"].setWidget(
            self.booksTab["available_books_widget"]
        )
        # ==========================================================================

        # ISSUE BOOKS TAB
        self.issueTab = {
            "member_search": self.findChild(QLineEdit, "MemberSearchBox"),
            "book_search": self.findChild(QLineEdit, "SearchBox"),
            "member_search_btn": self.findChild(QPushButton, "MemberSearchButton"),
            "book_search_btn": self.findChild(QPushButton, "SearchButton"),
            "issue_btn": self.findChild(QPushButton, "IssueButton"),
            "members_area": self.findChild(QScrollArea, "MemberSearchResultBox"),
            "books_area": self.findChild(QScrollArea, "SearchResultBox"),
            "members_area_widget": ScrollBoxContainer(),
            "books_area_widget": ScrollBoxContainer(),
            "selected_member_code": 0,
            "selected_book_code": 0,
        }

        self.issueTab["books_area"].setWidget(self.issueTab["books_area_widget"])
        self.issueTab["members_area"].setWidget(self.issueTab["members_area_widget"])
        # ==========================================================================

        # RETURN BOOKS TAB
        self.returnTab = {
            "name": self.findChild(QLabel, "NameLabel"),
            "done_btn": self.findChild(QPushButton, "ReturnDoneButton"),
            "stacked_wig": self.findChild(QStackedWidget, "ReturnStack"),
            "member_search": self.findChild(QLineEdit, "ReturnMemberSearchBox"),
            "member_search_btn": self.findChild(
                QPushButton, "ReturnMemberSearchButton"
            ),
            "members_area": self.findChild(QScrollArea, "ReturnMemberSearchResults"),
            "books_area": self.findChild(QScrollArea, "IssuedBooksBox"),
            "members_area_widget": ScrollBoxContainer(),
            "books_area_widget": ScrollBoxContainer(),
            "selected_member_code": 0,
            "selected_book_code": 0,
            "member_btns": [],
            "book_btns": [],
        }
        self.returnTab["members_area"].setWidget(self.returnTab["members_area_widget"])
        self.returnTab["books_area"].setWidget(self.returnTab["books_area_widget"])
        # ==========================================================================

        # EDIT BOOKS TAB
        self.edit_book = {
            "book_search": self.findChild(QLineEdit, "BookSearchLine"),
            # TODO : Add a button to go back to the search page
            "book_search_btn": self.findChild(QPushButton, "BookSearchButton"),
            "book_update_btn": self.findChild(QPushButton, "BookEditSubmitButton"),
            "title": self.findChild(QLineEdit, "BookTitleLine"),
            "author": self.findChild(QLineEdit, "BookAuthorLine"),
            "publisher": self.findChild(QLineEdit, "BookPublisherLine"),
            "price": self.findChild(QSpinBox, "PriceBox"),
            "subject": self.findChild(QComboBox, "BookSubjectBox"),
            "scroll_area": self.findChild(QScrollArea, "BookSearchResultArea"),
            "widget": ScrollBoxContainer(),
            "stacked_wig": self.findChild(QStackedWidget, "EditBookStack"),
        }
        self.edit_book["scroll_area"].setWidget(self.edit_book["widget"])
        self.edit_book["selected_book_code"] = 0
        # ============================================================

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

    def get_edit_details(self):
        title = self.edit_book["title"].text()
        author = self.edit_book["author"].text()
        publisher = self.edit_book["publisher"].text()
        price = self.edit_book["price"].value()
        subject = self.edit_book["subject"].currentText()

        d = {
            "title": title,
            "author": author,
            "publisher": publisher,
            "price": price,
            "sub_code": subject,
        }

        return d

    def display_books(self, details: list, all=True):
        comp = "all_books_widget" if all else "available_books_widget"
        self.booksTab[comp].clear()
        for d in details:
            b = BookCard(d)
            self.booksTab[comp].add_card(b)

    def display_member_results(self, details: list[dict]):
        self.issueTab["members_area_widget"].clear()
        for d in details:
            c = MemberCard(d)
            c.createLockButton()
            c.lock_btn.clicked.connect(self._lock_func(d))
            self.issueTab["members_area_widget"].add_card(c)

    def _lock_func(self, details):
        def func():
            self.issueTab["selected_member_code"] = details["member_code"]

        return func

    def display_book_search_results(self, details: list[dict]):
        self.edit_book["widget"].clear()
        for d in details:
            c = BookCard(d)
            c.show_lock_btn(type="Lock")
            c.lock_btn.clicked.connect(self._lock_book_to_edit(d))
            self.edit_book["widget"].add_card(c)

    def _lock_book_to_edit(self, details: dict):
        def func():
            self.edit_book["selected_book_code"] = details["bookcode"]
            self.edit_book["stacked_wig"].setCurrentIndex(1)
            self.edit_book["title"].setText(details["title"])
            self.edit_book["author"].setText(details["author"])
            self.edit_book["publisher"].setText(details["publisher"])
            index = self.edit_book["subject"].findText(details["sub_code"])
            self.edit_book["subject"].setCurrentIndex(index)
            self.edit_book["price"].setValue(details["price"])

        return func

    def display_books_results(self, details: list):
        self.issueTab["books_area_widget"].clear()
        for d in details:
            b = BookCard(d)
            b.show_availability()
            b.show_lock_btn(type="Lock")
            b.lock_btn.clicked.connect(self.issue_btn_func(d))
            self.issueTab["books_area_widget"].add_card(b)

    def issue_btn_func(self, details):
        def func():
            self.issueTab["selected_book_code"] = details["bookcode"]

        return func

    def display_member_results_return(self, details: list[dict]):
        self.returnTab["members_area_widget"].clear()
        for d in details:
            c = MemberCard(d)
            c.createLockButton()
            c.lock_btn.clicked.connect(self._lock_func_member_return(d))
            self.returnTab["member_btns"].append(c.lock_btn)
            self.returnTab["members_area_widget"].add_card(c)

    def _lock_func_member_return(self, details):
        def func():
            self.returnTab["selected_member_code"] = details["member_code"]
            self.returnTab["name"].setText(details["name"])

        return func

    def display_books_results_return(self, details: list):
        self.returnTab["books_area_widget"].clear()
        for d in details:
            b = BookCard(d)
            b.show_lock_btn(type="Return")
            b.show_fine()
            b.lock_btn.clicked.connect(self._lock_func_book_return(d))
            self.returnTab["book_btns"].append(b.lock_btn)
            self.returnTab["books_area_widget"].add_card(b)

    def _lock_func_book_return(self, details):
        def func():
            self.returnTab["selected_book_code"] = details["bookcode"]

        return func

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
        self.issueTab["members_area_widget"].clear()
        self.issueTab["books_area_widget"].clear()

    def clear_return_window(self):
        self.returnTab["member_search"].clear()
        self.returnTab["name"].clear()
        self.returnTab["members_area_widget"].clear()
        self.returnTab["books_area_widget"].clear()
        self.returnTab["member_btns"] = []
        self.returnTab["book_btns"] = []

    def clear_update_line_edits(self):
        self.edit_book["book_search"].clear()
        self.edit_book["title"].clear()
        self.edit_book["author"].clear()
        self.edit_book["publisher"].clear()
        self.edit_book["price"].clear()
        self.edit_book["subject"].setCurrentIndex(0)
        self.edit_book["widget"].clear()
