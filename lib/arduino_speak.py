#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
        ports = glob.glob('/dev/ttyACM*')
        print(ports)
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usbmodem*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = ports
    return result


# types: Sonar - sonar arduino, Box - box controlling arduino
# returns serial connection
def connect_to(type):
    arduinos = serial_ports()
    print(arduinos)
    ser = []
    for i in range(len(arduinos)):
        ser.append(serial.Serial(arduinos[i], 115200))
        time.sleep(1)
        ser[i].write("?".encode())
        # time.sleep(0.1)
        types = ser[i].readline().strip().decode("utf-8")
        print(types)
        if types == "MOT":
            mot = ser[i]
    return mot
    # TODO: return both box and mot


def open_doar(i, j, ser):
    if i == 0:
        num = j
    else:
        num = j + 4
    ser.write(str(num).encode())
    door = ser.readline().strip().decode("utf-8")
    ser.close()


def init_doar():
    ser = connect_to("Box")
    return ser


def init_motor():
    mot = connect_to("MOT")
    return mot


def read_values():
    while 1:
        try:
            fp2 = urllib.request.urlopen("http://0.0.0.0:5000/ANGLE/")
            mybytes2 = fp2.read()
            mystr2 = mybytes2.decode("utf8")
            print(mystr2)
            fp2.close()
            mystr2 = mystr2.split(".")[0]
            angle = float(mystr2)
            print(angle)
            return angle
        except:
            return 0


def motion(ser, direction):
    start = time.time()
    startAngle = read_values()
    if direction == "U":
        ser.write(str(1).encode())
    if direction == "D":
        ser.write(str(2).encode())
    if direction == "S":
        ser.write(str(0).encode())
    if direction == "C":
        ser.write(str(3).encode())
    if direction == "R":
        ser.write(str(4).encode())
    if direction == "L":
        ser.write(str(5).encode())
    endAngle = read_values()
    endtime = time.time()
    string = "Start time: " + str(start) + ", End time: " + str(endtime) + ", Difference: " + str(endtime-start) + ", Start angle is: " + str(startAngle) + ", end angle is: " + str(endAngle) + ";"
    f=open("log.txt","a")
    print(string, file=f)
    f.close()

if __name__ == "__main__":
    print("Connecting")
    ser = connect_to("GPS")
    print("connected to " + str(ser))
