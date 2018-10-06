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
import freenect
from numpy import *
import arduino_speak as ard
from flask import Flask
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/orientation')
def echo_socket(ws):
	f=open("orientation.txt","w")
	while True:
		message = ws.receive()
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/geolocation')
def echo_socket(ws):
	f=open("geolocation.txt","w")
	while True:
		message = ws.receive()
		ws.send(message)
		print(message, file=f)
	f.close()


@app.route('/')
def hello():
	main()
	return 'Hello World!'


def read_GPS(GOAL):
    while 1:
        try:
            with open("geolocation.txt", 'r') as geo:
                GPS = str(geo.readline())
                print(GPS)
                longitude = GPS.split('"longitude":')[1].split(",")[0]
                latitude = GPS.split('"latitude":')[1].split('}')[0]
                NOW = [longitude, latitude]
                break
        except:
            pass

    geod = Geodesic.WGS84
    g = geod.Inverse(NOW[0], NOW[1], GOAL[0], GOAL[1])

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
    if distance > 5:
        return dir
    else:
        return "Done"


def take_points(phase):
    toA = ["51.093829,71.399326", "51.093374,71.399171", "51.093414,71.398713", "51.093480,71.398224"]
    toB = ["51.093688,71.398188", "51.093891,71.398276", "51.094331,71.398443"]

    if phase == "A":
        return toA
    else:
        return toB

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
	# server = pywsgi.WSGIServer(('192.168.8.100', 5000), app, handler_class=WebSocketHandler)
	# server.serve_forever()
	main()
