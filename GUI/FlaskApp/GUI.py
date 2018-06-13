#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup
import naboox.main as naboox


app = Flask(__name__)  # Creating new flask app


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
@app.route("/robot/")  # Root for hello page is index "/"
def robot():
    alert = "Выберите ячейку"
    file = "cells.json"
    cell = naboox.read_json(file)
    for i in range(len(cell)):
        for j in range(len(cell[i])):
            if cell[i][j] == 1:
                value = "Занято"
            else:
                value = "Свободно"
            exec("cell" + str(j) + str(i) + " = '" + value + "'")

    return render_template(
        "robot.html", **locals())


# ID to cells
# TODO: Баг! Непонятно, но не пишет в json
@app.route("/robot/<cellN>", methods=["GET", "POST"])
def cellz(cellN):
    alert = "Введите идентификационный номер клиента"
    i = int(cellN[4])
    j = int(cellN[5])
    data = [[0, 0], [0, 0], [0, 0], [0, 0]]
    if request.method == 'POST':  # If user POST by clicking submit button any text
        ID = request.form['id']
        data[int(j)][int(i)] = ID
        naboox.write_json(data, "cells_ID.json")
        alert = "Выберите ячейку"
        file = "cells.json"
        cell = naboox.read_json(file)
        for i in range(len(cell)):
            for j in range(len(cell[i])):
                if cell[i][j] == 1:
                    value = "Занято"
                else:
                    value = "Свободно"
                exec("cell" + str(j) + str(i) + " = '" + value + "'")

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


# Checking passcode
# TODO: Go to page of loading post
@app.route("/pass/", methods=["POST"])
def passngo():
    alert = "Введите пароль"
    passcode = request.form['passcode']
    ids, truepass = read_config()
    if passcode == truepass:
        msg = "Кто-то зашел в кабинет"
        naboox.send_tlg_msg(msg, ids)
        return render_template(
            "login.html", **locals())
    else:
        alert = "Вы ввели неправильный пароль"
        msg = "Кто-то пытался зайти в кабинет, используя неправильный пароль"
        naboox.send_tlg_msg(msg, ids)
        return render_template(
            "login.html", **locals())


def setup_all():
    data = [[0, 0], [0, 0], [0, 0], [0, 0]]
    naboox.write_json(data, "cells.json")
    naboox.write_json(data, "cells_ID.json")


# Main flask app
if __name__ == "__main__":
    setup_all()
    # It creates application in special IP
    app.run(host=naboox.get_ip(), port=8090, debug=True)

