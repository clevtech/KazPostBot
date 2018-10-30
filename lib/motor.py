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
import os
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
from bluepy.btle import Scanner
from multiprocessing import Process
import multiprocessing
import datetime

manager = multiprocessing.Manager()
previous = "S"
os.system('sudo chmod 666 /dev/ttyACM*')


def scanLE(n, devices1):
    scanner = Scanner(n)
    devices = scanner.scan(1)
    for dev in devices:
        devices1.append(str(dev.addr + "," + str(dev.rssi) + "," + str(n)))


def scan(MAC):
    os.system("sudo hciconfig hci1 up")
    os.system("sudo hciconfig hci2 up")
    global manager
    devices1 = manager.list()
    p0 = Process(target=scanLE, args=(2, devices1, ))
    p1 = Process(target=scanLE, args=(1, devices1, ))
    p0.start()
    p1.start()
    time.sleep(1)
    p0.join()
    p1.join()
    right, left = -100, -100
    for device in devices1:
        mac = device.split(",")[0]
        if mac == MAC:
            side = device.split(",")[2]
            rssi = device.split(",")[1]
            if side == "1":
                right = int(rssi)
            else:
                left = int(rssi)
    return right, left


def direct(MAC):
    r, l = scan(MAC)
    if r > -75 or l > -75:
        return "DONE"
    else:
        if (l - r) > 4 or (l - r) < -4:
            if l<r:
                return "R"
            elif r<l:
                return "L"
        else:
            return "C"
        print("R:" + str(r) + " L:" + str(l))


def check_kinect(mot):
    print("Checking kinect")
    while 1:
        try:
            check = kinect.motion()
            break
        except:
            pass
    if check != "G":
        print("Something on kinect")
        move("S", mot, 0)
        time.sleep(10)
        check = kinect.motion()
        print("Value of check after sleep is: " + str(check))
    while check != "G":
        dir = check
        print("Going to: " + str(dir))
        if dir != "S":
            move("U", mot, 0)
            move(dir, mot, 0)
        check = kinect.motion()


def points1(phase):
    BLES = ["12:3b:6a:1b:50:1e"]
    BACK = []
    if phase == "A":
        return BLES
    else:
        return BACK


def motion(mot, phase):
    points = points1(phase)
    try:
        move("S", mot, 0)
        # move("L", mot, 0)
        # move("R", mot, 0)
        for point in points:
            while 1:
                check_kinect(mot)
                move("U", mot, 0)
                dir = direct(point)
                if dir == "DONE":
                    break
                else:
                    move(dir, mot, 0)
            move("S", mot, 0)
        return "Done"
    except:
        while True:
            try:
                mot = ard.connect_to()
                if mot:
                    break
            except:
                pass

def move(dir, mot, type):
    print("GO to: " + str(dir))
    try:
        if type == 1:
            print(dir)
            return 0
        global previous
        if dir != "S":
            ard.motion(mot, "U")
            time.sleep(0.1)

        if dir == "S":
            ard.motion(mot, "S")
        if dir == "D":
            ard.motion(mot, "D")
        if dir == "R":
            ard.motion(mot, "R")
            # else:
            #     time.sleep(0.1)
            #     ard.motion(mot, "R")
        if dir == "L":
            ard.motion(mot, "L")
            # if previous == "R":
            #     ard.motion(mot, "C")
            #     time.sleep(0.1)
            #     ard.motion(mot, "L")
            # else:
            #     time.sleep(0.1)
            #     ard.motion(mot, "L")
        if dir == "C":
            ard.motion(mot, "C")

        if dir == "R" or dir == "L" or dir == "C":
            previous = dir
    except:
        while True:
            try:
                mot = ard.connect_to()
                if mot:
                    break
            except:
                pass
        time.sleep(0.1)
        ard.motion(mot, "S")
        raise


def main():
    while True:
        try:
            mot = ard.connect_to()
            if mot:
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
    # while 1:
    #     mot = 0
    #     check_kinect(mot)
