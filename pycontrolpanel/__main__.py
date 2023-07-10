import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QEventLoop
from .gui import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exit(app.exec())

if __name__ == "__main__":
    main()