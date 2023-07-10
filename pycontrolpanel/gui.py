from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QSlider
from PyQt6.QtCore import Qt
import serial
from .parser import ResponseReader
from .signals import ControllerSignals, Button

class MainWindow(QMainWindow):
    def __init__(self, serial_port : str = None , baud_rate : str = None, autoconnect : bool = False) -> None:
        super().__init__()

        self.setWindowTitle("Python Control Panel")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QGridLayout()

        self.com_label = QLabel("Serial port")
        self.com_input = QLineEdit()
        if serial_port is not None:
            self.com_input.setText(serial_port)
        layout.addWidget(self.com_label, 0, 0)
        layout.addWidget(self.com_input, 0, 1)
        
        self.baudrate_label = QLabel("Baud rate")
        self.baudrate_input = QLineEdit()
        if baud_rate is not None:
            self.baudrate_input.setText(baud_rate)
        layout.addWidget(self.baudrate_label, 1, 0)
        layout.addWidget(self.baudrate_input, 1, 1)
        

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect)
        layout.addWidget(self.connect_btn, 2, 0)

        self.disconnect_btn = QPushButton("Disonnect")
        self.disconnect_btn.clicked.connect(self.disconnect)
        self.disconnect_btn.setDisabled(True)
        layout.addWidget(self.disconnect_btn, 2, 1)

        self.sliders = []
        self.sliderLabels = []
        for i in range(8):
            self.sliderLabels.append(QLabel())
            self.sliderLabels[-1].setNum(0)
            self.sliders.append(QSlider(Qt.Orientation.Horizontal))
            self.sliders[-1].setMinimum(-100)
            self.sliders[-1].valueChanged.connect(self.sliderLabels[-1].setNum)
            layout.addWidget(self.sliders[-1], i+3, 1)
            layout.addWidget(self.sliderLabels[-1], i+3, 0)

        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.close)

        layout.addWidget(self.quit_btn)
        self.centralWidget.setLayout(layout)

        if autoconnect == True:
            self.connect()

    def connect(self):
        self.connect_btn.setDisabled(True)
        self.disconnect_btn.setDisabled(False)
        self.serial = serial.Serial(self.com_input.text(), int(self.baudrate_input.text()))
        self.serial_reader = ResponseReader(self.serial)
        self.serial_reader.signals.button_pressed.connect(self.button_parser)
        self.serial_reader.start()

    def disconnect(self):
        self.serial_reader.exit()  
        self.connect_btn.setDisabled(False)
        self.disconnect_btn.setDisabled(True)
        self.serial.close()

    def button_parser(self, btn: Button):
        if btn.button <= 8:
            self.sliders[btn.button-1].setValue(self.sliders[btn.button-1].value() + btn.direction)
