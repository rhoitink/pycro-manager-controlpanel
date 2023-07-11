from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QSlider
from PyQt6.QtCore import Qt
import serial
from .parser import ResponseReader
from .signals import ControllerSignals, Button
from pycromanager import Bridge
import numpy as np

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
        self.connect_btn.clicked.connect(self.connect_all)
        layout.addWidget(self.connect_btn, 2, 0)

        self.disconnect_btn = QPushButton("Disonnect")
        self.disconnect_btn.clicked.connect(self.disconnect_all)
        self.disconnect_btn.setDisabled(True)
        layout.addWidget(self.disconnect_btn, 2, 1)

        self.sliders = []
        self.slider_labels = []
        self.slider_values = []
        self.slider_mappings = [
            ('RCM', 'Laser 1 Power', 0, 100), # group, prop, min, max
            ('RCM', 'Laser 2 Power', 0, 100),
            ('RCM', 'Laser 3 Power', 0, 100),
            ('RCM', 'Laser 4 Power', 0, 100),
        ]
        for i, (group, prop, _, _) in enumerate(self.slider_mappings):
            self.slider_labels.append(QLabel())
            self.slider_labels[-1].setText(prop)
            self.slider_values.append(QLabel())
            self.slider_values[-1].setNum(10)
            self.sliders.append(QSlider(Qt.Orientation.Horizontal))
            self.sliders[-1].setMinimum(0)
            self.sliders[-1].valueChanged.connect(self.slider_values[-1].setNum)
            layout.addWidget(self.slider_labels[-1], i+3, 0)
            layout.addWidget(self.sliders[-1], i+3, 1)
            layout.addWidget(self.slider_values[-1], i+3, 2)

        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.close)

        layout.addWidget(self.quit_btn)
        self.centralWidget.setLayout(layout)

        if autoconnect == True:
            self.connect_all()

    def connect_all(self):
        self.connect_serial()
        self.connect_pycromanager()

    def disconnect_all(self):
        self.disconnect_serial()
        self.disconnect_pycromanager()

    def connect_pycromanager(self):
        try:
            self.bridge = Bridge() ## docs at: https://pycro-manager--372.org.readthedocs.build/en/372/index.html
            self.mmcore = self.bridge.get_core()
            
            for i, (mmgroup, mmprop, propmin, propmax) in enumerate(self.slider_mappings):
                self.sliders[i].setMinimum(propmin)
                self.sliders[i].setMaximum(propmax)
                self.sliders[i].setValue(int(self.mmcore.get_property(mmgroup, mmprop)))
        except TimeoutError:
            print("Could not connect to micromanager")
            self.close()

    def disconnect_pycromanager(self):
        self.bridge.close()
        self.bridge = None

    def connect_serial(self):
        self.serial = serial.Serial(self.com_input.text(), int(self.baudrate_input.text()))
        self.serial_reader = ResponseReader(self.serial)
        self.serial_reader.signals.button_pressed.connect(self.button_parser)
        self.serial_reader.start()
        self.connect_btn.setDisabled(True)
        self.disconnect_btn.setDisabled(False)

    def disconnect_serial(self):
        self.serial_reader.exit()  
        self.serial.close()
        self.connect_btn.setDisabled(False)
        self.disconnect_btn.setDisabled(True)

    def button_parser(self, btn: Button):
        if btn.button - 1 < len(self.slider_mappings):
            mmgroup, mmprop, propmin, propmax = self.slider_mappings[btn.button - 1]
            current_value = int(self.mmcore.get_property(mmgroup, mmprop))
            new_value = int(np.clip(current_value + btn.direction, propmin, propmax))
            self.sliders[btn.button-1].setValue(new_value)
            self.mmcore.set_property(mmgroup, mmprop, new_value)
            print(mmprop, new_value)

