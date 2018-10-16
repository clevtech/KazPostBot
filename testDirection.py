#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup, jsonify

L = -100
R = -100


app = Flask(__name__)  # Creating new flask app


def get_value(point):
    global L
    global R
    rawL = L.split(";")[:-1]
    rawR = R.split(";")[:-1]
    for each in rawL:
        add = str(each.split("M:")[1].split("S:")[0])
        if str(add).lowercase() == str(point).lowercase():
            L = int(each.split("S:")[1])
            break
    for each in rawR:
        add = str(each.split("M:")[1].split("S:")[0])
        if str(add).lowercase() == str(point).lowercase():
            R = int(each.split("S:")[1])
            break
    return L, R


def direct(point):
    L, R = get_value(point)
    if R > -60 and L > -60:
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


@app.route('/data/right/<data>', methods=['GET'])
def ajax_request2(data):
    print("From R: " + str(data))
    global R
    R = data
    return "OK"

@app.route('/data/left/<data>', methods=['GET'])
def ajax_request3(data):
    print("From L: " + str(data))
    global L
    L = data
    return "OK"


@app.route("/")
def index():
    global R
    global L
    dir = direct()
    return dir


# Main flask app
if __name__ == "__main__":
    app.run(host="192.168.8.100", port=7777, debug=True)
