#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup
import time
import naboox.main as naboox
import random


app = Flask(__name__)  # Creating new flask app



def setup_all():
    data = [[0, 0, 0, 0], [0, 0, 0, 0]]
    naboox.write_json(data, "cells_ID.json")
    naboox.write_json(data, "cells_PIN.json")


def make_PIN():

    PIN = random.sample(range(1000, 9999), 8)
    PIN = [PIN[0:4], PIN[4:8]]
    naboox.write_json(PIN, "cells_PIN.json")


def read_config():
    with open("config.txt", "r") as file:
        lines = file.readlines()

    # Parsing passcode
    ids = []
    for line in lines:
        if line[0:9] == "passcode:":
            passcode = line.replace('\n', '').replace('\r', '').replace(" ", "").replace("passcode:", '')
        if line[0:3] == "id:":
            ids.append(line.replace('\n', '').replace('\r', '').replace(" ", "").replace("id:", ''))

    return ids, passcode


# Hello page
@app.route("/")  # Root for hello page is index "/"
def hello():
    return render_template(
        "hello.html", **locals())


# Choosing cell to load
@app.route("/robot/", methods=["GET", "POST"])  # Root for hello page is index "/"
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
        ids, truepass = read_config()
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
# TODO: Баг! Непонятно, но не пишет в json
@app.route("/robot/<cellN>", methods=["GET", "POST"])
def cellz(cellN):
    alert = "Введите номер мобильного телефона клиента"
    i = int(cellN[4])
    j = int(cellN[5])
    if request.method == 'POST':  # If user POST by clicking submit button any text
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
    alert = "Введите пароль"
    return render_template(
        "login.html", **locals())


# Login page, no authorisation with password
@app.route("/send/", methods=["GET", "POST"])
def send():
    time.sleep(20)
    # Едет до чего-то
    # Отправляет СМС
    # Создает ПИН коды
    alert = "Введите пароль от посылки из СМС"
    return render_template(
        "pin.html", **locals())


# Main flask app
if __name__ == "__main__":
    make_PIN()
    # setup_all()
    # # It creates application in special IP
    # app.run(host=naboox.get_ip(), port=7777, debug=True)

