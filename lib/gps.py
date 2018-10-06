#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
from geographiclib.geodesic import Geodesic
import sys
import glob
import math


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


def connect_to(type):
    arduinos = serial_ports()
    for i in range(len(arduinos)):
        ser = serial.Serial(arduinos[i], "115200")
        print("Connected to " + str(arduinos[i]))
        time.sleep(10)
        ser.write("?".encode())
        ser.flush()
        types = ser.readline()
        types = types.strip().decode("utf-8")
        print("Output is: " + str(types))
        if types == type:
            return ser


def get_direction(NOW, GOAL, angle):
    geod = Geodesic.WGS84
    initGPS = NOW
    goalGPS = GOAL
    g = geod.Inverse(initGPS[0], initGPS[1], goalGPS[0], goalGPS[1])
    degrees = g["azi1"]
    distance = g['s12']
    print("Distance is: " + str(distance))
    degrees = (degrees + 360) % 360
    print("Degrees to go is: " + str(degrees))
    angle = math.radians(angle)
    angle = math.degrees(math.atan2(-math.sin(angle), math.cos(angle)))
    angle = degrees - angle
    print("Angle to turn is: " + str(angle))
    if angle < 20 and angle > -20:
        dir = "C"
    elif angle < 0:
        dir = "L"
    else:
        dir = "R"
    print("Direction is: " + str(dir))
    #print("Distance to point is: " + str(distance))
    if distance > 5:
        return dir
    else:
        return "Done"


def read_GPS(ser, GOAL):
    while 1:
        ser.write("g".encode())
        GPS = ser.readline().strip().decode("utf-8")
        print("Raw output from gps is: " + str(GPS))
        try:
            GPS1 = GPS.split(",")
            NOW = [float(GPS1[0]), float(GPS1[1])]
            angle = float(GPS1[2]) - 110
            print("Our gps now is: " + str(NOW))
            print("Our angle now is: " + str(angle))
            if int(NOW[0]) == 0:
                print("Returning stop")
                return "S"
            else:
                print("Our GPS is: " + str(NOW) + " and angle is: " + str(angle))
                print("Getting direction")
                dir = get_direction(NOW, GOAL, angle)
                return dir
        except:
            return "S"


if __name__ == '__main__':
    while 1:
        ser = connect_to("GPS")
        if ser:
            break
    GOAL_string = "51.093636,71.399268"
    print("Goal is " + str(GOAL_string))
    goal = GOAL_string.split(",")
    GOAL = [float(goal[0]), float(goal[1])]
    while 1:
        dir = read_GPS(ser, GOAL)
        print("We need to go to: " + dir)
        print("=================================")
        time.sleep(10)
