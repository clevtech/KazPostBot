#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"

import sys
import os
sys.path.append(os.path.abspath(os.path.pardir))
import requests
import xml.dom.minidom
import datetime
import lib.main as naboox


def send(type = "test"):
    url = "http://pls-test.post.kz/api/service/postamat?wsdl"
    headers = {'content-type': 'text/xml'}
    file_name = "./send.xml"
    IDs = naboox.read_json("cells_ID.json")
    NUMs = naboox.read_json("cells_numbers.json")
    with open(file_name, "r") as file:
        req = file.read()
        header = req.split("<!--date-->")[0]
        head = req.split("<!--date-->")[1].split("<!--number-->")[0]
        mid = req.split("<!--date-->")[1].split("<!--number-->")[1].split("<!--user-->")[0]
        tail = req.split("<!--date-->")[1].split("<!--number-->")[1].split("<!--user-->")[1]
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        print(header + date + head + "123123" + mid + "naboox" + tail)
    return 1

    body = []
    print(IDs)
    for i in range(len(IDs)):
        for j in range(len(IDs[i])):
            if IDs[i][j] != 0:
                print(IDs[i][j])
                body.append(header + date + head + IDs[i][j] + mid + "naboox" + tail)
    for bod in body:
        response = requests.post(url, data=request.encode('utf-8'), headers=headers)
        pretyy = xml.dom.minidom.parseString(response.content)
        pretty_xml_as_string = pretyy.toprettyxml()
        print(pretty_xml_as_string)
    return 1


if __name__ == "__main__":
    send("real")
