from views import MemberWindow
from models import Books
from models import Member


class MemberController:
    def __init__(
        self, book_model: Books, member_model: Member, member_view: MemberWindow
    ):
        self._view = member_view
        self._mem_model = member_model
        self._book_model = book_model

        self._connectSignalsAndSlots()

    def add_mem(self):
        details = self._view.get_mem_details()

        try:
            self._mem_model.new(details)
            self._view.show_msg("New Member Added")
        except:
            self._view.show_msg("Oops something went wrong")
        finally:
            self._view.clearLineEdits()

    def load_all_mem_details(self):
        members = self._mem_model.get_all_members()
        self._view.displayMembers(members)

    def load_defaulters(self):
        fine_books = self._book_model.get_defaulter_books()
        members = []
        member_codes = []
        for f in fine_books:
            if f["member_code"] != 0:
                if f["member_code"] not in member_codes:
                    m = self._mem_model.get_member(f["member_code"])
                    member_codes.append(f["member_code"])
                    members.append(m)
        self._view.displayDefaulters(members)

    def search_member(self):
        name = self._view.edit_mem["mem_search"].text().strip()
        if name in ["", " "]:  # checks for blank strings
            return
        m = self._mem_model.search_member_by_name(name)
        self._view.display_mem_search_result(m)

    def edit_member(self):
        d = self._view.get_edit_details()
        mem_code = self._view.edit_mem["selected_member_code"]
        # TODO : Apply some data sanitation method
        try:
            self._mem_model.update_details(d, mem_code)
            self._view.show_msg("Details updated successfully")
            self._view.clear_update_line_edits()
            self._view.edit_mem["stacked_wig"].setCurrentIndex(0)
        except Exception as err:
            print(err)
            self._view.show_msg("Something went wrong")

    def _connectSignalsAndSlots(self):
        self._view.new_mem["submit_btn"].clicked.connect(self.add_mem)
        self._view.member_roster["load"].clicked.connect(self.load_all_mem_details)
        self._view.defaulters["load"].clicked.connect(self.load_defaulters)
        self._view.edit_mem["mem_search_btn"].clicked.connect(self.search_member)
        self._view.edit_mem["mem_update_btn"].clicked.connect(self.edit_member)
