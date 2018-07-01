#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import requests
import xml.dom.minidom
import naboox.main as naboox
import datetime


def send(type = "test"):
    url = "http://89.218.48.181:8080/smsgate/?wsdl"
    headers = {'content-type': 'text/xml'}
    IDs = naboox.read_json("cells_ID.json")
    PINs = naboox.read_json("cells_PIN.json")
    if type == "test":
        file_name = "./request-test.xml"
    else:
        file_name = "./request.xml"
    with open(file_name, "r") as file:
        req = file.read()
        head = req.split("<!--body-->")[0]
        mid = req.split("<!--body-->")[1]
        mid_ID = mid.split("[ID]")[0]
        mid_date = mid.split("[ID]")[1].split("[date]")[0]
        mid_pin = mid.split("[ID]")[1].split("[date]")[1].split("[pin]")[0]
        mid_tail = mid.split("[ID]")[1].split("[date]")[1].split("[pin]")[1]
        tail = req.split("<!--body-->")[2]

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    naboox.write_json(datetime.datetime.now().timestamp(), "start.json")

    body = []
    for i in range(len(IDs)):
        for j in range(len(IDs)):
            if int(IDs[i][j]) > 0:
                body.append(mid_ID + str(IDs[i][j]) + mid_date + \
                          str(date) + mid_pin + str(PINs[i][j]) + mid_tail)
    request = head

    for bod in body:
        request = request + bod
    request = request + tail

    response = requests.post(url, data=request.encode('utf-8'), headers=headers)

    pretyy = xml.dom.minidom.parseString(response.content)
    pretty_xml_as_string = pretyy.toprettyxml()
    return 1



if __name__ == "__main__":
    send()

