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


# Login page, no authorisation with password
# TODO: create hello page with logo of the robot and login button
@app.route("/")  # Root for login page is index "/"
def login():
    alert = "Введите пароль"
    return render_template(
        "login.html", **locals())


# Login page, no authorisation with password
# TODO: Go to page of loading post
@app.route("/pass/", methods=["POST"])  # Root for login page is index "/"
def login2():
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


# Main flask app
if __name__ == "__main__":

    # It creates application in special IP
    app.run(host=naboox.get_ip(), port=8090, debug=True)

