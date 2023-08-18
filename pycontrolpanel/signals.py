from PyQt6.QtCore import QObject, pyqtSignal


class Button:
    CW = 1
    CCW = -1

    def __init__(self, direction, button) -> None:
        self.direction = direction
        self.button = button


class ControllerSignals(QObject):
    """Class for handling Qt Signals that can be used during measurement.
    Singleton instance.
    """

    _instance = None
    button_pressed = pyqtSignal(Button)
