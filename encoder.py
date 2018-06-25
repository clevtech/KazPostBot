import serial, time

class Encoder:
    def __init__(self):
##        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)       
        self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
        self.left, self.mid, self.right = None, None, None
        time.sleep(1)
    
    def get_reading(self):
        self.arduino.write("1".encode('utf8'))
        return int(float(self.arduino.readline()))


if __name__ == "__main__":
    enc = Encoder()
    while True:
        print(enc.get_reading())
        time.sleep(0.2)
