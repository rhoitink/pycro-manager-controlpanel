from PyQt6.QtCore import QThread
from .signals import ControllerSignals, Button
from serial.serialutil import SerialException

class ButtonParser:
    DIRECTION_MASK = 0b00000010 # this bit is 1 for CW and 0 for CCW
    BUTTON_MASK = 0b000111 # after bit shift by 2 to the right, these bits contain info on the knob that is turned from 1 for the rightmost button to 7 for the leftmost
    NUM_BUTTONS = 7

    def __init__(self, response):
        self.response = response

        if self.response & self.DIRECTION_MASK > 0:
            self.direction = 1
        else:
            self.direction = -1
        self.button = Button(self.direction, self.NUM_BUTTONS - int(self.response >> 2 & self.BUTTON_MASK)) # return button, leftmost button is 0 and rightmost button is 6

class ResponseReader(QThread):
    def __init__(self, ser):
        super(ResponseReader, self).__init__()
        self.ser = ser
        self.signals = ControllerSignals()

    def run(self):
        while self.ser.is_open:
            try:
                response = int.from_bytes(self.ser.read(1), "little")
                self.signals.button_pressed.emit(ButtonParser(response).button)
            except TypeError:
                continue
            except AttributeError:
                continue