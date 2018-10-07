#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import kinect
import gps
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
import arduino_speak as ard
from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


calibration_angle = 0
motion_time = 0


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def read_values():
    while 1:
		try:
			fp2 = urllib.request.urlopen("http://" + str(get_ip())+":5000/ANGLE/")
			mybytes2 = fp2.read()
			mystr2 = mybytes2.decode("utf8")
			print(mystr2)
			fp2.close()
			mystr2 = mystr2.split(".")[0]
			angle = float(mystr2)
			print(angle)
            return angle
		except:
			raise


def turn(toAngle):
    angle = read_values()
    angle = math.radians(angle)
	angle = math.degrees(math.atan2(- math.sin(angle), - math.cos(angle)))
	angle = ((angle + 360) % 360)
    angle = toAngle - angle
    if angle < 5 and angle > -5:
		dir = "C"
	elif angle < 0:
		dir = "L"
	else:
		dir = "R"
    return dir


def check_kinect():
    print("Checking kinect")
    while 1:
        check = kinect.motion()
        break
    if check != "G":
        start = time.time()
    while check != "G":
        print("Something on kinect")
        move("S", mot)
        time.sleep(10)
        check = kinect.motion()
    # while check != "G":
    #     dir = check
    #     print("Going to: " + str(dir))
    #     if check != "S":
    #         move("U", mot)
    #         move(dir, mot)
    #     check = kinect.motion()
    now = time.time()
    if start:
        return now-start
    else:
        return 0


def motion(mot, point):
    GPS, times, angle = take_points(point)
    for i in len(range(GPS)):
        start = time.time()
        now = time.time()
        stopping = 0
        while (now - start - stopping) < times:
            stopping = stopping + check_kinect()
            move("U", mot)
            dir = turn(angle)
        move("S", mot)
    return "Done"


def read_GPS(GOAL):
    NOW = [0, 0]
    angle = read_values()
	geod = Geodesic.WGS84
	g = geod.Inverse(float(NOW[0]), float(NOW[1]), float(GOAL[0]), float(GOAL[1]))
	degrees = g["azi1"]
	distance = g['s12']
	print("Distance is: " + str(distance))
	degrees = (degrees + 360) % 360
	print("Degrees to go is: " + str(degrees))
	angle = math.radians(angle)
	angle = math.degrees(math.atan2(- math.sin(angle), - math.cos(angle)))
	angle = ((angle + 360) % 360)
	print("Our angle is: " + str(angle))
	angle = degrees - angle
	print("Angle to turn is: " + str(angle))
	if angle < 10 and angle > -10:
		dir = "C"
	elif angle < 0:
		dir = "L"
	else:
		dir = "R"
	print("Direction is: " + str(dir))
	if distance > 5:
		return dir
	else:
		return "Done"


def calibrate():
	while 1:
		try:
			fp = urllib.request.urlopen("http://" + str(get_ip())+":5000/GPS/")
			mybytes = fp.read()
			# print(mybytes)
			mystr = mybytes.decode("utf8")
			fp.close()
			GPS = str(mystr)
			# print("Raw GPS is: " + GPS)
			longitude = GPS.split('"longitude":')[1].split(",")[0]
			latitude = GPS.split('"latitude":')[1].split('}')[0]
			NOW = [latitude, longitude]
			print(NOW)
			fp2 = urllib.request.urlopen("http://" + str(get_ip())+":5000/ANGLE/")
			mybytes2 = fp2.read()
			mystr2 = mybytes2.decode("utf8")
			print(mystr2)
			fp2.close()
			mystr2 = mystr2.split(".")[0]
			angle = float(mystr2)
			print(angle)
			break
		except:
			raise
	geod = Geodesic.WGS84
	g = geod.Inverse(float(NOW[0]), float(NOW[1]), float(GOAL[0]), float(GOAL[1]))
	degrees = g["azi1"]
	degrees = (degrees + 360) % 360
	angle = math.radians(angle)
	angle = math.degrees(math.atan2(- math.sin(angle), - math.cos(angle)))
	angle = (angle + 360) % 360
	global calibration_angle
	calibration_angle = - degrees + angle
	return "Done"


def take_points(phase):
    toA = ["51.093829,71.399326", "51.093374,71.399171", "51.093414,71.398713", "51.093480,71.398224"]
	toAtime = []
    toAangle = []
    toB = ["51.093688,71.398188", "51.093891,71.398276", "51.094331,71.398443"]
	toBtime = []
    toBangle = []
    if phase == "A":
        return [toA, toAtime, toAangle]
    else:
        return [toB, toBtime, toBangle]


def move(dir, mot):
    if dir == "S":
        ard.motion(mot, "S")
    if dir == "U":
        ard.motion(mot, "U")
    if dir == "D":
        ard.motion(mot, "D")
    if dir == "R":
        ard.motion(mot, "R")
    if dir == "L":
        ard.motion(mot, "L")
    if dir == "C":
        ard.motion(mot, "C")


def to_point(mot, point):
    goals = take_points(point)
    dir = "S"
    try:
        for GOAL1 in goals:
            print("Going to point: " + GOAL1)
            goal = GOAL1.split(",")
            print("Matrix of point is: " + str(goal))
            GOAL = [float(goal[0]), float(goal[1])]
            print("Starting moving")
            while dir != "Done":
                try:
                    print("Checking kinect")
                    check = kinect.motion()
                    if check != "G":
                        print("Something on kinect")
                        move("S", mot)
                        time.sleep(2)
                    while check != "G":
                        dir = check
                        print("Going to: " + str(dir))
                        if check != "S":
                            move("U", mot)
                            move(dir, mot)
                    print("Checking GPS")
                    dir = read_GPS(GOAL)
                    print("Going to: " + str(dir))
                    move("U", mot)
                    move(dir, mot)
                except:
                    print("Something went wrong, stopping")
                    move("S", mot)
                    time.sleep(10)
                    pass
            print("Came to point, stopping and doing next")
            move("S", mot)
            time.sleep(10)
            print("=========================================")
    except:
        pass
        print("Something globally went wrong, stopping")
        move("S", mot)
        time.sleep(10)


def main():
    while True:
        try:
            mot = ard.init_motor()
            if mot:
                print("Connected to motors: " + str(mot))
                break
        except:
            pass
    print("Starting going to point A")
    print("")
    to_point(mot, "A")
    print("A is done")
    time.sleep(30)
    print("")
    print("Starting going to point B")
    to_point(mot, "B")
    print("Job is done, am I good girl?")


if __name__ == "__main__":
	print("Inputs are okay")
	print("Starting moving")
	print("==============================")
	main()
