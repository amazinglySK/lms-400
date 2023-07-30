class BookNotFoundError(Exception):
    def __init__(self):
        super().__init__("Book not found")


class BookAlreadyBorrowedError(Exception):
    def __init__(self):
        super().__init__("Book already borrowed")


class IncorrectDataStructure(Exception):
    def __init__(self):
        super().__init__("Incorrect data provided")
