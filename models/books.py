from datetime import date
from .model import Model


class BookNotFoundError(Exception):
    def __init__(self):
        super().__init__("Book not found")


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
        self.max_days = 1

        try:
            self.cursor.execute(f"select * from {self.name}")
            r = self.cursor.fetchall()
        except:
            self.cursor.execute(
                f"create table {self.name}(bookcode int primary key auto_increment, sub_code varchar(20), title varchar(30), author varchar(30), publisher varchar(30), price int, member_code int default(0), doi date default(curdate()))"
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
        cmd = f"update {self.name} set {cmd} where bookcode = {book_code}"
        self.cursor.execute(cmd)
        self.conn.commit()
        return

    def get_book(self, book_code: int):
        try:
            self.cursor.execute(
                f"select * from {self.name} where bookcode = {book_code}"
            )
            result = self.cursor.fetchall()[0]
            return self._parse_result(result)
        except:
            raise BookNotFoundError

    def get_all_books(self, raw = False):
        self.cursor.execute(f"select * from {self.name}")
        results = self.cursor.fetchall()
        if raw :
            return results
        return self._parse_result(results)

    def search_book_by_name(self, name: str):
        self.cursor.execute(f"select * from {self.name} where title like '%{name}%'")
        results = self.cursor.fetchall()
        return self._parse_result(results)

    def get_avail_books(self):
        self.cursor.execute(f"select * from {self.name} where member_code = 0")
        results = self.cursor.fetchall()
        return self._parse_result(results)

    def borrow_book(self, book_code: int, member_code: int):
        self.modify_book(
            book_code,
            {
                "member_code": member_code,
                "doi": str(date.today()),
            },
        )

    def _calc_fine(self, delta: int):
        fine = 0
        if delta > 0 and delta < self.max_days:
            fine = delta * 0.5
        elif delta >= self.max_days and delta < 15:
            fine = delta * 1
        else:
            fine = delta * 2
        return fine

    def return_book(self, book_code: int):
        # Returning the book
        self.modify_book(book_code, {"member_code": 0})

    def get_subject_books(self, subcode: str):
        self.cursor.execute(f"select * from {self.name} where sub_code = '{subcode}'")
        result = self.cursor.fetchall()
        return self._parse_result(result)

    def get_issued_books(self):
        self.cursor.execute(f"select * from {self.name} where member_code != 0")
        result = self.cursor.fetchall()
        return self._parse_result(result)

    def get_issued_books_by_member(self, member_code: int):
        self.cursor.execute(
            f"select * from {self.name} where member_code = {member_code}"
        )
        books = self.cursor.fetchall()
        books = self._parse_result(books)
        for book in books:
            delta = date.today() - book["doi"]
            fine = self._calc_fine(delta.days)
            book["fine"] = fine
        return books

    def get_defaulter_books(self) -> list[dict]:
        # TODO : Probably use some kind of aggregate function to get unique defaulters
        self.cursor.execute(
            f"select * from {self.name} where datediff(curdate(), doi) >= {self.max_days} and member_code != 0"
        )
        result = self.cursor.fetchall()
        return self._parse_result(result)
