import sys
from PyQt6.QtWidgets import QApplication
from .gui import MainWindow
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serial_port", default=None)
    parser.add_argument("--baud_rate", default=None)
    parser.add_argument("--autoconnect", action="store_true")
    args = parser.parse_args()
    app = QApplication(sys.argv)
    main_window = MainWindow(args.serial_port, args.baud_rate, args.autoconnect)
    main_window.show()
    app.exit(app.exec())


if __name__ == "__main__":
    main()
