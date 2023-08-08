from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt


class ScrollBoxContainer(QWidget):
    def __init__(self):
        super(ScrollBoxContainer, self).__init__()
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.vbox)

    def add_card(self, w: QWidget):
        self.vbox.addWidget(w)

    def clear(self):
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)
