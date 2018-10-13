import sys
import glob
import serial
import time
import urllib.request


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyUSB*')
        print(ports)
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usbmodem*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = ports
    return result


# types: Sonar - sonar arduino, Box - box controlling arduino
# returns serial connection
def connect_to():
    arduinos = serial_ports()
    print(arduinos)
    ser = []
    for i in range(len(arduinos)):
        ser.append(serial.Serial(arduinos[i], 115200))
        time.sleep(1)
        ser[i].flush()
        ser[i].write("?".encode())
        # time.sleep(0.1)
        types = ser[i].readline().strip().decode("utf-8")
        print(types)
        if types == "L":
            left = ser[i]
        if types == "R":
            right = ser[i]
    return left, right


def points(n):
    BLES = ["12:3b:6a:1b:50:1a", "12:3b:6a:1b:4f:74"]
    return str(BLES[n])



def get_value(left):

    left.write("b".encode())
    line = str(left.readline().strip().decode("utf-8"))
    lines = line.split(";")
    add = []
    sig = []
    for l in lines:
        if len(str(l)) > 3:
            adres = l.split("M:")[1].split(" S:")[0]
            signal = int(l.split(" S:")[1])
            add.append(adres)
            sig.append(signal)

    return add, sig


def direct(point, left, right):
    addL, sigL = get_value(left)
    addR, sigR = get_value(right)

    for i in range(len(addL)):
        if str(addL[i]) == str(point):
            print("RSSI from L is: " + str(sigL[i]))
            L = -sigL[i]
    for i in range(len(addR)):
        if str(addR[i]) == str(point):
            print("RSSI from R is: " + str(sigR[i]))
            R = -sigR[i]
    try:
        diff = L - R
        if -3 > diff or diff > 3:
            if R > L:
                return "R"
            if L > R:
                return "L"
    except:
        return "S"


def motion():
    left, right = connect_to()
    while 1:

        addL, sigL = get_value(left)
        addR, sigR = get_value(right)

        for i in range(len(addL)):
            if addL[i] == points(0):
                print("RSSI from L is: " + str(sigL[i]))
                L = -sigL[i]
        for i in range(len(addR)):
            if addR[i] == points(0):
                print("RSSI from R is: " + str(sigR[i]))
                R = -sigR[i]

        diff = L - R
        if -3 > diff or diff > 3:
            if R > L:
                print("Turn R")
            if L > R:
                print("Turn L")
        print()
