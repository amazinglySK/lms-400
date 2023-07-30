import mysql.connector
from datetime import date

from .exceptions import BookAlreadyBorrowedError, BookNotFoundError


"""
-   [x] Addition of records to library file
-   [x] Modification of records of library file
-   [x] Issue of book
-   [x] Return of books - <= 7 days = 0.5 / day - <= 15 days = 1 / day - 15+ days = 2/day
-   [x] Searching for availability of a particular book in the library
-  	[x] Subject wise book list 
-	[x] List of books issued to members 
- 	[x] List of available books 

"""


class Books:
    def __init__(self):
        self.name = "books"
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="tiger", database="lms"
        )
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
        except:
            self.cursor.execute(
                f"create table {self.name}(bookcode int, sub_code varchar(10), title varchar(15), author varchar(15), publisher varchar(15), price int, member_code default(0) int, doi date"
            )

    def _parse_result(self, data, struct=None):
        if type(data) == list:
            converted = []
            for i in data:
                d = self._parse_result(i)
                converted.append(d)
            return converted
        else:
            d = {}
            i = 0
            struct = (
                struct if struct else self.struct
            )  # Use the default if not provided
            for k in struct:
                d[k] = data[i]
                i += 1
            return d

    def _check_data(self, data) -> tuple:
        col_names = []
        values = []
        for i in data.keys():
            if i not in self.struct:
                raise Exception("Incorrect data structure")
            col_names.append(i)
            if type(data[i]) == int:
                values.append(data[i])
            else:
                values.append(f"'{data[i]}'")
        return col_names, values

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
        cmd = command_str[0:-1]  # Omitting the final ","
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
                book["book_code"], {"member_code": member_code}
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

    def borrow_book(self, book_code: int):
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
