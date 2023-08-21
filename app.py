from PyQt5.QtWidgets import QApplication
import sys

from views import LoginWindow, Window, check_credentials

if __name__ == "__main__":
    app = QApplication([])

    # Login check
    if not check_credentials():
        login = LoginWindow()
        login.show()
    else:
        main_window = Window(check_credentials())
        main_window.show()
        
    r = app.exec()
    sys.exit(r)
