import book_view
from models.books import Books
from models.member import Member


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

        return

    def _connectSignalsAndSlots(self):
        self._view.newBookTab["submit_btn"].clicked.connect(self.new_book)
        return
