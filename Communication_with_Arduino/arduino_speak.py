import sys
import glob
import serial
import time


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyACM*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usbmodem*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# types: Sonar - sonar arduino, Box - box controlling arduino
# returns serial connection
def connect_to(type):
    arduinos = serial_ports()
    ser = []
    for i in range(len(arduinos)):
        ser.append(serial.Serial(arduinos[i], 115200))
        time.sleep(1)
        ser[i].write("?".encode())
        # time.sleep(0.1)
        types = ser[i].readline().strip().decode("utf-8")
        if types == type:
            return ser[i]


def sonar_read():
    ser = connect_to("Sonar")
    while 1:
        obstacle = ser.readline().strip().decode("utf-8")
        # TODO: do smt with this code
        # If distance is less than 100 cm it sends 1
        print(obstacle)


def open_doar(num, ser):
    time.sleep(1)
    ser.write(str(num).encode())
    while 1:
        door = ser.readline().strip().decode("utf-8")
        if num == int(door):
            return True
        else:
            return False


def init_doar():
    ser = connect_to("Box")
    return ser


if __name__ == '__main__':
    # sonar_read()
    # ser = init_doar()
    # print(open_doar(2, ser))
    ser = connect_to("Sonar")
    while 1:
        raw_input()
        obstacle = ser.readline().strip().decode("utf-8")
        # TODO: do smt with this code
        # If distance is less than 100 cm it sends 1
        print(obstacle)

