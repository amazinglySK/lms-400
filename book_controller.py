import book_view
from models.books import Books
from models.member import Member, MemberExceedingLimit


class BookController:
    def __init__(
        self, book_model: Books, member_model: Member, view: book_view.BookWindow
    ):
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
            self._view.set_response("Book added successfully")
        except:
            self._view.set_response("Something went wrong")

    def search_member(self):
        name = self._view.issueTab["member_search"].text().strip()
        # TODO : Check if the string is just a huge long space as well
        if name in ["", " "]:  # checks for blank strings
            return
        m = self._member.search_member_by_name(name)
        self._view.display_member_results(m)

    def issue_book(self):
        book_code = self._view.issueTab["selected_book_code"]
        member_code = self._view.issueTab["selected_member_code"]
        if book_code == 0 or member_code == 0:
            self._view.display_issue_msg("Please lock the options")
            return
        try:
            self._member.issue_book(member_code)
            self._book.borrow_book(book_code, member_code)
            self._view.display_issue_msg("Success!")
        except MemberExceedingLimit:
            self._view.display_issue_msg("The member exceeds limit")

    def search_book(self):
        name = self._view.issueTab["book_search"].text().strip()
        if name == "":
            return
        m = self._book.search_book_by_name(name)
        self._view.display_books_results(m)

    def get_all_books(self):
        d = self._book.get_all_books()
        self._view.display_books(d)

    def get_avail_books(self):
        d = self._book.get_avail_books()
        self._view.display_books(d, all=False)

    def _connectSignalsAndSlots(self):
        self._view.newBookTab["submit_btn"].clicked.connect(self.new_book)
        self._view.booksTab["get_all_books"].clicked.connect(self.get_all_books)
        self._view.booksTab["get_avail_books"].clicked.connect(self.get_avail_books)
        self._view.issueTab["member_search_btn"].clicked.connect(self.search_member)
        self._view.issueTab["book_search_btn"].clicked.connect(self.search_book)
        self._view.issueTab["issue_btn"].clicked.connect(self.issue_book)
