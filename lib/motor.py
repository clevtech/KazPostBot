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


def to_point(ser, mot, point):
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
                    dir = gps.read_GPS(ser, GOAL)
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
            mot, ser = ard.init_motor()
            if mot and ser:
                print("Connected to motors: " + str(mot))
                break
        except:
            pass
    # while 1:
    #     ser = gps.connect_to("GPS")
    #     print("Connected to GPS: " + str(ser))
    #     if ser:
    #         break

    print("Starting going to point A")
    print("")
    to_point(ser, mot, "A")
    print("A is done")
    time.sleep(30)
    print("")
    print("Starting going to point B")
    to_point(ser, mot, "B")
    print("Job is done, am I good girl?")

if __name__ == "__main__":
    print("Inputs are okay")
    print("Starting moving")
    print("==============================")
    main()
