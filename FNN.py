#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math, time
from geographiclib.geodesic import Geodesic
import sys
import glob
import serial



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


# types: Sonar - sonar arduino, MOT - box controlling arduino
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


def get_direction(NOW, GOAL, angle):
    geod = Geodesic.WGS84

    initGPS = NOW

    while NOW[0] == 0:
        time.sleep(1)

    goalGPS = GOAL
    g = geod.Inverse(initGPS[0], initGPS[1], goalGPS[0], goalGPS[1])
    degrees = g["azi1"]
    distance = g['s12']

    degrees = (degrees + 360) % 360
    degrees = degrees - angle

    if angle < 20 and angle > -20:
        dir = "center"
    elif angle < 0:
        dir = "left"
    else:
        dir = "right"

    print(distance)
    if distance > 3:
        return dir
    else:
        return "done"

if __name__ == '__main__':
    # ser = connect_to("GPS")
    GOAL_string = input("Where to go?:(divide by ';') ")
    goal = GOAL_string.split(";")
    GOAL = [float(goal[0]), float(goal[1])]
    while 1:
        # ser.write("g".encode())
        # GPS = ser.readline().strip().decode("utf-8")
        GPS = input("Where we are?: ")
        GPS = GPS.split(";")
        NOW = [float(GPS[0]), float(GPS[1])]
        angle = float(GPS[2])
        dir = get_direction(NOW, GOAL, angle)
        time.sleep(1)
        print(dir)
