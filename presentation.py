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
while True:
    try:
        mot = ard.connect_to()
        box = ard.connect_to_box()
        break
    except:
        pass




def setup_all():
    data = [[0, 0, 0, 0], [0, 0, 0, 0]]
    naboox.write_json(data, "cells_ID.json")
    naboox.write_json(data, "cells_PIN.json")
    make_PIN()


def check_time():
    #timer1 = naboox.read_json("start.json")
    timer1 = 120
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


ids, passcode4, timer4 = read_config()
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
    alert = "Выберите ячейку и мой IP: " + str(naboox.get_ip()) + ":7777/robot-control/"
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
    alert = "Введите номер мобильного телефона клиента: " + str(naboox.get_ip()) + ":7777/robot-control/"
    i = int(cellN[4])
    j = int(cellN[5])

    if request.method == 'POST':  # If user POST by clicking submit button any text
        while 1:
            try:
                box = ard.connect_to_box()
                break
            except:
                pass
        ard.open_doar(i, j, box)
        ID = request.form['id']
        file = "cells_ID.json"
        data = naboox.read_json(file)
        data[int(i)][int(j)] = ID
        naboox.write_json(data, file)
        alert = "Выберите ячейку: " + str(naboox.get_ip()) + ":7777/robot-control/"
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
    alert = "Введите пароль от посылки из СМС, и закройте крышку после себя, пожалуйста"
    if request.method == 'POST':  # If user POST by clicking submit button any text
        PIN = request.form['passcode']
        file = "cells_PIN.json"
        passc = naboox.read_json(file)
        file = "cells_ID.json"
        cell = naboox.read_json(file)
        for i in range(len(passc)):
            for j in range(len(passc[i])):
                print("Checking " + str(i) + str(j))
                if int(PIN) == int(passc[i][j]):
                    while 1:
                        try:
                            box = ard.connect_to_box()
                            break
                        except:
                            pass
                    ard.open_doar(i, j, box)
                    msg = "Отдал посылку клиента: " + str(cell[i][j])
                    naboox.send_tlg_msg(msg, ids)
                    cell[i][j] = 0
                    naboox.write_json(cell, "cells_ID.json")
                    value = "Открыто на 10 секунд"
                    exec("cell" + str(i) + str(j) + " = '" + value + "'")
                    return render_template(
                        "robot2.html", **locals())
        msg = "Вводят неправильный пароль"
        naboox.send_tlg_msg(msg, ids)
        alert = "Неправильный пароль"

    file = "cells_ID.json"
    cell = naboox.read_json(file)

    value = 0
    for i in range(len(cell)):
        for j in range(len(cell[i])):
            if cell[i][j] != 0:
                value = 1
    if value == 0:
        alert = "Еду домой"
        return render_template(
            "robot3.html", **locals())
    else:
        return render_template(
            "pin.html", **locals())


@app.route("/wayhome/", methods=["GET", "POST"])
def homeway():
    print("Go Home!")
    msg = "Я поехал домой"
    naboox.send_tlg_msg(msg, ids)
    # x = input("Доехал домой?")
    alert = "Мой IP: " + str(naboox.get_ip()) + ":7777/robot-control/"
    msg = "Я приехал домой и мой IP: " + str(naboox.get_ip())
    naboox.send_tlg_msg(msg, ids)
    return render_template(
        "hello.html", **locals())

# Login page, no authorisation with password
@app.route("/sended/<i>/", methods=["GET", "POST"])
def sended(i):
    if int(i) == 0:
        # naboox.write_json(time.time(), "start.json")
        msg = "Я поехал доставлять посылки"
        naboox.send_tlg_msg(msg, ids)
        time.sleep(10)
        # x = input("Доехал?")
        smsgate.send("real")
        msg = "Я приехал на АстанаХаб"
        naboox.send_tlg_msg(msg, ids)
    alert = "Чтобы получить посылку нажмите:"
    return render_template(
        "sended.html", **locals())


# Main flask app
if __name__ == "__main__":
    # time.sleep(300)
    id, passcode4, timer4 = read_config()
    msg = "Я включился, мой IP: " + str(naboox.get_ip())
    naboox.send_tlg_msg(msg, id)
    app.run("0.0.0.0", port=7777, debug=True)
