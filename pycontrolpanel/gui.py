from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
import serial
from .parser import ResponseReader
from .signals import ControllerSignals

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Python Control Panel")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QGridLayout()

        self.com_label = QLabel("Serial port")
        self.com_input = QLineEdit()
        layout.addWidget(self.com_label, 0, 0)
        layout.addWidget(self.com_input, 0, 1)
        
        self.baudrate_label = QLabel("Baud rate")
        self.baudrate_input = QLineEdit()
        layout.addWidget(self.baudrate_label, 0, 2)
        layout.addWidget(self.baudrate_input, 0, 3)
        

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect)
        layout.addWidget(self.connect_btn, 0, 4)

        self.disconnect_btn = QPushButton("Disonnect")
        self.disconnect_btn.clicked.connect(self.connect)
        self.disconnect_btn.setDisabled(True)
        layout.addWidget(self.disconnect_btn, 0, 5)

        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.close)

        layout.addWidget(self.quit_btn)
        self.centralWidget.setLayout(layout)

    def connect(self):
        self.connect_btn.setDisabled(True)
        self.disconnect_btn.setDisabled(False)
        self.serial = serial.Serial(self.com_input.text(), int(self.baudrate_input.text()))
        self.serial_reader = ResponseReader(self.serial)
        self.serial_reader.signals.button_pressed.connect(self.button_parser)
        self.serial_reader.finished.connect(self.close_serial)
        self.serial_reader.start()

    def disconnect(self):
        self.serial_reader.quit()
        self.connect_btn.setDisabled(False)
        self.disconnect_btn.setDisabled(True)

    def close_serial(self):        
        self.serial.close()
        del self.serial

    def button_parser(self, btn):
        print(btn.direction, btn.button)
