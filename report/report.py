import xlsxwriter
from models import Books, Member
from datetime import date


class Report:
    def __init__(self, file_name: str, book_model: Books, member_model: Member):
        self.wb = xlsxwriter.Workbook(file_name)
        self.books = book_model
        self.member = member_model

    def _defaulters(self):
        defaulter_books = self.books.get_defaulter_books()
        defaulters = {}
        for b in defaulter_books:
            m_code = b["member_code"]
            if m_code not in defaulters:
                defaulters[m_code] = [b["title"]]
            else:
                defaulters[m_code].append(b["title"])

        defaulters_table = []
        for code, books in defaulters.items():
            member_details = self.member.get_member(code)
            name = member_details["name"]
            defaulters_table.append((code, name, ", ".join(books)))

        self._add_worksheet("Defaulters", defaulters_table, ["member_code", "name", "books"])

    def _sub_book_list(self):
        sub_wise = self.books.get_subject_books()
        ws = self.wb.add_worksheet("Subject-wise books")
        header = ["sub_code", "book_code", "title", "author", "publisher"]
        for col, i in enumerate(header):
            ws.write(0, col, i)
        lrow = 0

        # Writing to the worksheet
        for sub, v in sub_wise.items() : 
            start = lrow+1
            stop = lrow+len(v)

            # If there's only one book under a subject
            if len(v) == 1:
                ws.write(start, 0, sub)

            for i, d in enumerate(v):
                for j, c in enumerate(d):
                    ws.write(start + i, j+1, c) 

            # Merging the subject name column
            ws.merge_range(start, 0, stop, 0, sub)
            lrow = stop

    def _avail_books(self):
        available_books = self.books.get_avail_books(raw=True)
        self._add_worksheet("Available Books", available_books, self.books.struct)

    def _member_list(self):
        members = self.member.get_all_members(raw = True)
        self._add_worksheet("Members", members, self.member.struct)
    
    def _book_list(self):
        books = self.books.get_all_books(raw = True)
        self._add_worksheet("Books", books, self.books.struct)

    def _add_worksheet(self, w_name: str, data: list[tuple], header: list[str]):
        ws = self.wb.add_worksheet(w_name)

        for col, i in enumerate(header):
            ws.write(0, col, i)
            
        for i, d in enumerate(data):
            for j, c in enumerate(d):
                if type(c) == date:
                    c = str(c)
                ws.write(i + 1, j, c)

    def create_report(self) : 
        self._book_list()
        self._member_list()
        self._avail_books()
        self._sub_book_list()
        self._defaulters()
        self.wb.close()
