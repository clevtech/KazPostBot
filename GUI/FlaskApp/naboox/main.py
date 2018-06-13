#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import telepot, socket

"""
Cheat sheet of Bauyrzhan Ospan.
"""


# Send message (msg) to users in the list (ids)
def send_tlg_msg(msg, ids):
    bot = telepot.Bot('610077316:AAFakq71aegcWzsRHQLxopH762gtNl1eCkw')
    for id in ids:
        bot.sendMessage(str(id), str(msg))


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

