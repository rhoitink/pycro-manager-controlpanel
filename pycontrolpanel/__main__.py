import serial

ser = None

class ReponseParser:
    DIRECTION_MASK = 0b00100000
    BUTTON_MASK = 0b00001111

    def __init__(self, response):
        self.response = response

        if self.response & self.DIRECTION_MASK > 0:
            self.direction = 1
        else:
            self.direction = -1
        self.button = int(self.response & self.BUTTON_MASK)

def setup():
    global ser
    ser = serial.Serial("COM4", 9600)

def parse():
    if ser is None:
        exit("Serial port could not be opened, quitting...")
    while True:
        response = int.from_bytes(ser.read(1), "little")
        parsed = ReponseParser(response)
        print(parsed.direction, parsed.button)

def main():
    setup()
    parse()
    if ser is not None:
        ser.close()

if __name__ == "__main__":
    main()