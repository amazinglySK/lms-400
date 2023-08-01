from datetime import date
from .model import Model


class BookNotFoundError(Exception):
    def __init__(self):
        super().__init__("Book not found")


class BookAlreadyBorrowedError(Exception):
    def __init__(self):
        super().__init__("Book already borrowed")


class IncorrectDataStructure(Exception):
    def __init__(self):
        super().__init__("Incorrect data provided")


class Books(Model):
    def __init__(self, connection):
        super().__init__(connection, "books")
        self.cursor = self.conn.cursor()
        self.struct = [
            "bookcode",
            "sub_code",
            "title",
            "author",
            "publisher",
            "price",
            "member_code",
            "doi",
        ]

        try:
            self.cursor.execute(f"select * from {self.name}")
            r = self.cursor.fetchall()
        except:
            self.cursor.execute(
                f"create table {self.name}(bookcode int primary key, sub_code varchar(10), title varchar(15), author varchar(15), publisher varchar(15), price int, member_code int default(0), doi date)"
            )
            self.conn.commit()

    def add_new_book(self, data: dict):
        col_names, values = self._check_data(data)
        col_str = ", ".join(col_names)
        val_str = ", ".join(values)
        self.cursor.execute(f"insert into {self.name} ({col_str}) values({val_str})")
        self.conn.commit()
        return

    def modify_book(self, book_code: int, data: dict):
        col_names, values = self._check_data(data)
        command_str = ""
        for c, v in zip(col_names, values):
            command_str += f"{c} = {v},"
        cmd = command_str[:-1]  # Omitting the final ","
        cmd = f"update {self.name} set {cmd} where book_code == {book_code}"
        self.cursor.execute(cmd)
        self.conn.commit()
        return

    def get_book(self, book_code: int):
        try:
            self.cursor.execute(
                f"select * from {self.name} where book_code == {book_code}"
            )
            result = self.cursor.fetchall()[0]
            return self._parse_result(result)
        except:
            raise BookNotFoundError

    def get_all_books(self):
        self.cursor.execute(f"select * from {self.name}")
        results = self.cursor.fetchall()
        return results

    def borrow_book(self, book_code: int, member_code: int):
        book = self.get_book(book_code)
        if book["member_code"] == 0:
            self.modify_book(
                book["book_code"],
                {
                    "member_code": member_code,
                    "doi": str(date.today()),
                },
            )  # Borrowing the book
        else:
            raise BookAlreadyBorrowedError

    def _calc_fine(self, delta):
        d = 0
        fine = 0
        while delta != 0:
            if d <= 7:
                fine += 0.5
            if d > 7 and d <= 15:
                fine += 1
            else:
                fine += 2
            delta -= 1
            d += 1
        return fine

    def return_book(self, book_code: int):
        book = self.get_book(book_code)
        # Returning the book
        self.modify_book(book["book_code"], {"member_code": 0})
        delta = self.book["doi"] - date.today()
        fine = self._calc_fine(delta)
        return fine

    def get_subject_books(self, subcode: str):
        self.cursor.execute(f"select * from {self.name} where sub_code == '{subcode}'")
        result = self.cursor.fetchall()
        return self._parse_result(result)

    def get_issued_books(self):
        self.cursor.execute(f"select * from {self.name} where member_code != 0")
        result = self.cursor.fetchall()
        return self._parse_result(result)

    def get_defaulter_books(self, member_code: int):
        self.cursor.execute(
            f"select * from {self.name} where datediff(curdate(), doi) >= 7"
        )
        result = self.cursor.fetchall()
        return self._parse_result(result)