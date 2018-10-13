#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
	import kinect
	import arduino_speak as ard
except:
	import lib.kinect as kinect
	import lib.arduino_speak as ard
import time
from geographiclib.geodesic import Geodesic
import sys
import glob
import serial
import math
import urllib.request
import freenect
import socket
from numpy import *
from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler



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


def check_kinect(mot):
	print("Checking kinect")
	while 1:
        try:
    		check = kinect.motion()
    		break
        except:
            pass
	while check != "G":
		print("Something on kinect")
		move("S", mot)
		time.sleep(10)
		check = kinect.motion()
	# while check != "G":
	# 	dir = check
	# 	print("Going to: " + str(dir))
	# 	if check != "G":
	# 		move("U", mot)
	# 		move(dir, mot)
	# 	check = kinect.motion()


def points1(phase):
    BLES = ["12:3b:6a:1b:50:1a", "12:3b:6a:1b:4f:74"]
    BACK = []
    if phase = "A":
        return BLES
    else:
        return BACK


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
    if R < 60 or L < 60:
        return "DONE"
    try:
        diff = L - R
        if -3 > diff or diff > 3:
            if R > L:
                return "R"
            if L > R:
                return "L"
    except:
        return "S"


def motion(mot, phase, left, right):
    points = points1(phase)
	move("S", mot)
	move("L", mot)
	move("R", mot)
	for point in points:
		while 1:
            check_kinect(mot)
			move("U", mot)
			dir = direct(point, left, right)
            if dir == "DONE":
                break
            else:
                move(dir, mot)
		move("S", mot)
	return "Done"


def move(dir, mot):
    previous = "S"

	if dir == "S":
		ard.motion(mot, "S")
	if dir == "U":
		ard.motion(mot, "U")
	if dir == "D":
		ard.motion(mot, "D")
	if dir == "R":
        if previous == "L":
            ard.motion(mot, "C")
            ard.motion(mot, "R")
        else:
		    ard.motion(mot, "R")
	if dir == "L":
        if previous == "R":
            ard.motion(mot, "C")
            ard.motion(mot, "L")
        else:
		    ard.motion(mot, "L")
	if dir == "C":
		ard.motion(mot, "C")

    if dir == "R" or dir == "L" or dir == "C":
        previous = dir


def main():
	while True:
		try:
			mot, box = ard.connect_to()
            left, right = connect_to()
            if mot and box and left and right:
			    break
		except:
			pass
	print("Starting going to point A")
	print("")
	motion(mot, "A", left, right)
	print("A is done")
	time.sleep(30)
	print("")
	print("Starting going to point B")
	motion(mot, "B", left, right)
	print("Job is done, am I good girl?")


if __name__ == "__main__":
	print("Inputs are okay")
	print("Starting moving")
	print("==============================")
	main()
