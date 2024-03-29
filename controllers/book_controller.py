from views import BookWindow
from models import Books
from models import Member, MemberExceedingLimit


class BookController:
    def __init__(self, book_model: Books, member_model: Member, view: BookWindow):
        self._book = book_model
        self._member = member_model
        self._view = view

        self._connectSignalsAndSlots()

    def new_book(self):
        d = self._view.get_book_details()
        if any(
            [v in ["", " "] for v in d.values()]
        ):  # Checks if any of them are blank strings
            return
        try:
            self._book.add_new_book(d)
            self._view.show_msg("Book added successfully")
        except:
            self._view.show_msg("Something went wrong")
        finally:
            self._view.clear_response()

    def search_member(self):
        name = self._view.issueTab["member_search"].text().strip()
        if name in ["", " "]:  # checks for blank strings
            return
        m = self._member.search_member_by_name(name)
        if not m : return
        self._view.display_member_results(m)
        self._connectSignalsToNewlyAddedComp()

    def issue_book(self):
        book_code = self._view.issueTab["selected_book_code"]
        member_code = self._view.issueTab["selected_member_code"]
        if book_code == 0 or member_code == 0:
            self._view.show_msg("Please lock the options")
            return
        try:
            self._member.issue_book(member_code)
            self._book.borrow_book(book_code, member_code)
            self._view.show_msg("Success!")
        except MemberExceedingLimit:
            self._view.show_msg("The member exceeds limit")
        finally:
            self._view.clear_issue_lines()

    def search_book_for_issue(self):
        name = self._view.issueTab["book_search"].text().strip()
        if name == "":
            return
        m = self._book.search_book_by_name(name)
        if not m : return
        self._view.display_books_results(m)
        self._connectSignalsToNewlyAddedComp()

    def get_all_books(self):
        d = self._book.get_all_books()
        self._view.display_books(d)

    def get_avail_books(self):
        d = self._book.get_avail_books()
        self._view.display_books(d, all=False)

    def search_member_return(self):
        name = self._view.returnTab["member_search"].text().strip()
        if name == "":
            return
        m = self._member.search_member_by_name(name)
        if not m : return
        self._view.display_member_results_return(m)
        self._connectSignalsToNewlyAddedComp()

    def search_book(self):
        name = self._view.edit_book["book_search"].text().strip()
        if name in ["", " "]:  # checks for blank strings
            return
        m = self._book.search_book_by_name(name)
        if not m : return
        self._view.display_book_search_results(m)

    def edit_book(self):
        d = self._view.get_edit_details()
        book_code = self._view.edit_book["selected_book_code"]
        try:
            self._book.modify_book(book_code, d)
            self._view.show_msg("Details updated successfully")
            self._view.clear_update_line_edits()
            self._view.edit_book["stacked_wig"].setCurrentIndex(0)
        except Exception as err:
            print(err)
            self._view.show_msg("Something went wrong")

    def load_issued_books(self):
        mem_code = self._view.returnTab["selected_member_code"]
        books = self._book.get_issued_books_by_member(mem_code)
        self._view.display_books_results_return(books)
        self._connectSignalsToNewlyAddedComp()
        self._view.returnTab["stacked_wig"].setCurrentIndex(1)

    def return_book(self):
        book_code = self._view.returnTab["selected_book_code"]
        mem_code = self._view.returnTab["selected_member_code"]

        if book_code == 0 or mem_code == 0:
            self._view.show_msg("Something went wrong :(")
            return
        try:
            self._book.return_book(book_code)
            self._member.return_book(mem_code)
            self._view.show_msg("Returned successfully")
        except:
            self._view.show_msg("Something went wrong")

    def done_returning(self):
        self._view.clear_return_window()
        self._view.returnTab["stacked_wig"].setCurrentIndex(0)

    def _connectSignalsAndSlots(self):
        self._view.newBookTab["submit_btn"].clicked.connect(self.new_book)
        self._view.booksTab["get_all_books"].clicked.connect(self.get_all_books)
        self._view.booksTab["get_avail_books"].clicked.connect(self.get_avail_books)
        self._view.issueTab["member_search_btn"].clicked.connect(self.search_member)
        self._view.issueTab["book_search_btn"].clicked.connect(self.search_book_for_issue)
        self._view.issueTab["issue_btn"].clicked.connect(self.issue_book)
        self._view.returnTab["member_search_btn"].clicked.connect(
            self.search_member_return
        )
        self._view.returnTab["done_btn"].clicked.connect(self.done_returning)
        self._view.edit_book["book_search_btn"].clicked.connect(self.search_book)
        self._view.edit_book["book_update_btn"].clicked.connect(self.edit_book)

    def _connectSignalsToNewlyAddedComp(self):
        for b in self._view.returnTab["member_btns"]:
            b.clicked.connect(self.load_issued_books)

        for b in self._view.returnTab["book_btns"]:
            b.clicked.connect(self.return_book)
