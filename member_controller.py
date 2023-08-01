from member_view import MemberWindow
from models.books import Books
from models.member import Member


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
            self._view.setDisplayText("New Member Added")
            self._view.clearLineEdits()
        except:
            self._view.setDisplayText("Oops something went wrong")

    def load_all_mem_details(self):
        members = self._mem_model.get_all_members()
        self._view.displayMembers(members)

    def _connectSignalsAndSlots(self):
        self._view.new_mem["submit_btn"].clicked.connect(self.add_mem)
        self._view.member_roster["load"].clicked.connect(self.load_all_mem_details)
