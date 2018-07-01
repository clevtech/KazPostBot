#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup, jsonify
import socket



# Get IP as string of the host machine
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


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("robot.html")


@app.route('/direction', methods=['POST'])
def ajax_request():
    print("Baby")
    return jsonify()


# Main flask app
if __name__ == "__main__":
    # It creates application in special IP
    app.run(host=get_ip(), port=7777, debug=True)

