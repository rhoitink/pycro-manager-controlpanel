from PyQt6.QtCore import QThread
from .signals import ControllerSignals, Button

class ButtonParser:
    DIRECTION_MASK = 0b00100000
    BUTTON_MASK = 0b00001111

    def __init__(self, response):
        self.response = response

        if self.response & self.DIRECTION_MASK > 0:
            self.direction = 1
        else:
            self.direction = -1
        self.button = Button(self.direction, int(self.response & self.BUTTON_MASK))

class ResponseReader(QThread):
    def __init__(self, ser):
        super(ResponseReader, self).__init__()
        self.ser = ser
        self.signals = ControllerSignals()

    def run(self):
        while True:
            response = int.from_bytes(self.ser.read(1), "little")
            self.signals.button_pressed.emit(ButtonParser(response).button)