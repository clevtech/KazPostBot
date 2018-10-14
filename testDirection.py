#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

from flask import Flask, render_template, request, Markup, jsonify



app = Flask(__name__)  # Creating new flask app


@app.route('/data/right/<data>', methods=['GET'])
def ajax_request2(data):
    print("From R: " + str(data))
    return "OK"

@app.route('/data/left/<data>', methods=['GET'])
def ajax_request3(data):
    print("From L: " + str(data))
    return "OK"


# Main flask app
if __name__ == "__main__":
    app.run(host="192.168.8.100", port=7777, debug=True)
