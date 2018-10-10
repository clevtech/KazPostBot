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
			print(mystr2)
			angle = int(mystr2)
			print("Angle is:")
			print(angle)
			return angle
		except:
			raise


def turn(toAngle):
	angle = read_values()
	angle = math.radians(angle)
	angle = math.degrees(math.atan2(- math.sin(angle), - math.cos(angle)))
	global calibration_angle
	angle = ((angle + 360) % 360) - calibration_angle
	angle = toAngle - angle
	if angle < 5 and angle > -5:
		dir = "C"
	elif angle < 0:
		dir = "L"
	else:
		dir = "R"
	return dir


def check_kinect(mot):
	print("Checking kinect")
	start = 0
	while 1:
		check = kinect.motion()
		break
	if check != "G":
		start = time.time()
		move("S", mot)
		time.sleep(10)
	# while check != "G":
	# 	print("Something on kinect")
	# 	move("S", mot)
	# 	time.sleep(10)
	# 	check = kinect.motion()
	while check != "G":
		dir = check
		print("Going to: " + str(dir))
		if check != "G":
			move("U", mot)
			move(dir, mot)
		check = kinect.motion()
	move("S", mot)
	now = time.time()
	if start>0:
		return float(now)-float(start)
	else:
		return 0


def motion(mot, point):
	times, angle = take_points(point)
	move("S", mot)
	move("L", mot)
	move("R", mot)
	calibrate()
	for i in range(len(times)):
		start = time.time()
		now = time.time()
		stopping = 0
		while (now - start - stopping) < times[i]:
			# stopping = stopping + float(check_kinect(mot))
			move("U", mot)
			dir = turn(angle[i])
		calibrate()
		move("S", mot)
	return "Done"


def calibrate():
	angle = float(read_values())
	angle = math.radians(angle)
	angle = math.degrees(math.atan2(- math.sin(angle), - math.cos(angle)))
	angle = ((angle + 360) % 360)
	global calibration_angle
	calibration_angle = angle
	return "Done"


def take_points(phase):
	toAtime = [30, 25, 20]
	toAangle = [0, 30, 40]
	toBtime = [30, 80, 35]
	toBangle = [170, 270, 270]
	if phase == "A":
		return [toAtime, toAangle]
	else:
		return [toBtime, toBangle]


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


def main():
	while True:
		try:
			mot, box = ard.connect_to()
			if mot:
				print("Connected to motors: " + str(mot))
				print("==============================")
				break
		except:
			pass
	print("Starting going to point A")
	print("")
	motion(mot, "A")
	print("A is done")
	time.sleep(30)
	print("")
	print("Starting going to point B")
	motion(mot, "B")
	print("Job is done, am I good girl?")


if __name__ == "__main__":
	print("Inputs are okay")
	print("Starting moving")
	print("==============================")
	main()
