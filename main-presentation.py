#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup, jsonify
import time
import lib.main as naboox
import lib.motor as motor
import random
import smsgate
import lib.arduino_speak as ard
import datetime, socket


app = Flask(__name__)  # Creating new flask app
# while True:
#     try:
#         mot, box = ard.connect_to()
#         break
#     except:
#         pass


def setup_all():
    data = [[0, 0, 0, 0], [0, 0, 0, 0]]
    naboox.write_json(data, "cells_ID.json")
    naboox.write_json(data, "cells_PIN.json")
    naboox.write_json(time.time(), "start.json")
    make_PIN()


def check_time():
    timer1 = naboox.read_json("start.json")
    elapsed_time = time.time() - timer1
    ids, passcode, timer = read_config()
    if elapsed_time > timer:
        return True
    else:
        return False


def make_PIN():
    PIN = random.sample(range(1000, 9999), 8)
    PIN = [PIN[0:4], PIN[4:8]]
    naboox.write_json(PIN, "cells_PIN.json")


def read_config():
    with open("config.txt", "r") as file:
        lines = file.readlines()
    ids = []
    for line in lines:
        if line[0:9] == "passcode:":
            passcode = line.replace('\n', '').replace('\r', '').replace(" ", "").replace("passcode:", '')
        if line[0:3] == "id:":
            ids.append(line.replace('\n', '').replace('\r', '').replace(" ", "").replace("id:", ''))
        if line[0:6] == "timer:":
            timer = line.replace('\n', '').replace('\r', '').replace(" ", "").replace("timer:", '')

    return ids, passcode, float(timer)

# Pages started


@app.route('/robot-control/')
def robcont():
    return render_template("robot-control.html")


@app.route('/robot-control/<direction>', methods=['POST'])
def ajax_request(direction):
    print(str(direction))
    direction = str(direction).replace("\n", '').replace("\r", '').replace("/", "")
    if direction == "u-p":
        ard.motion(mot, "U")
        print("Up is pressed")
    elif direction == "d-p":
        ard.motion(mot, "D")
    elif direction == "r-p":
        ard.motion(mot, "R")
    elif direction == "l-p":
        ard.motion(mot, "L")

    elif direction == "u-r":
        ard.motion(mot, "S")
    elif direction == "d-r":
        ard.motion(mot, "S")
    elif direction == "r-r":
        ard.motion(mot, "C")
    elif direction == "l-r":
        ard.motion(mot, "C")
    return jsonify()


# Hello page
@app.route("/")  # Root for hello page is index "/"
def hello():
    return render_template(
        "hello.html", **locals())


# Choosing cell to load
@app.route("/robot/", methods=["GET", "POST"])
def robot():
    alert = "Выберите ячейку"
    file = "cells_ID.json"
    cell = naboox.read_json(file)

    for i in range(len(cell)):
        for j in range(len(cell[i])):
            if cell[i][j] != 0:
                value = "Занято"
            else:
                value = "Свободно"
            command = "cell" + str(i) + str(j) + " = '" + value + "'"
            exec(command)

    if request.method == "POST":
        passcode = request.form['passcode']
        ids, truepass, timer = read_config()
        if passcode == truepass:
            msg = "Кто-то зашел в кабинет"
            naboox.send_tlg_msg(msg, ids)
            return render_template(
                "robot.html", **locals())
        else:
            alert = "Вы ввели неправильный пароль"
            msg = "Кто-то пытался зайти в кабинет, используя неправильный пароль"
            naboox.send_tlg_msg(msg, ids)
            return render_template(
                "login.html", **locals())
    return render_template(
        "robot.html", **locals())


# ID to cells
@app.route("/robot/<cellN>", methods=["GET", "POST"])
def cellz(cellN):
    alert = "Введите номер мобильного телефона клиента"
    i = int(cellN[4])
    j = int(cellN[5])

    if request.method == 'POST':  # If user POST by clicking submit button any text
        # ard.open_doar(i, j, ard.init_doar())
        ID = request.form['id']
        file = "cells_ID.json"
        data = naboox.read_json(file)
        data[int(i)][int(j)] = ID
        naboox.write_json(data, file)
        alert = "Выберите ячейку"
        cell = naboox.read_json(file)
        for i in range(len(cell)):
            for j in range(len(cell[i])):
                if cell[i][j] != 0:
                    value = "Занято"
                else:
                    value = "Свободно"
                exec("cell" + str(i) + str(j) + " = '" + value + "'")

        return render_template(
            "robot.html", **locals())
    return render_template(
        "cell.html", **locals())


# Login page, no authorisation with password
@app.route("/login/")
def login():
    setup_all()
    alert = "Введите пароль"
    return render_template(
        "login.html", **locals())


# Login page, no authorisation with password
@app.route("/send/", methods=["GET", "POST"])
def send():
    time.sleep(5)
    smsgate.send("real")
    alert = "Введите пароль от посылки из СМС, и закройте крышку после себя, пожалуйста"
    if request.method == 'POST':  # If user POST by clicking submit button any text
        PIN = request.form['passcode']
        file = "cells_PIN.json"
        passc = naboox.read_json(file)
        file = "cells_ID.json"
        cell = naboox.read_json(file)
        for i in range(len(passc)):
            for j in range(len(passc[i])):
                if int(PIN) == int(passc[i][j]):
                    # ard.open_doar(i, j, ard.init_doar())
                    cell[i][j] = 0
                    naboox.write_json(cell, "cells_ID.json")
    return render_template(
        "pin.html", **locals())


# Login page, no authorisation with password
@app.route("/sended/<i>/", methods=["GET", "POST"])
def sended(i):
    if int(i) == 0:
        time.sleep(10)
        # motor.motion(mot, "A")
        smsgate.send("test")
    alert = "Чтобы получить посылку нажмите:"
    return render_template(
        "sended.html", **locals())


# Main flask app
if __name__ == "__main__":
    app.run(host=naboox.get_ip(), port=7777, debug=True)
    # make_PIN()
    # check_time()
