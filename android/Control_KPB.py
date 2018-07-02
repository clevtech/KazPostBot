#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import socket, sys



def socket_start():
    port = 6666
    ip = get_ip()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    while 1:
        try:
            soc.bind((ip, port))
            break
        except:
            pass

    soc.listen(1)
    print('Socket now listening')
    # this will make an infinite loop needed for
    # not reseting server for every client
    conn, addr = soc.accept()
    ip, port = str(addr[0]), str(addr[1])
    print('Accepting connection 1 from ' + ip + ':' + port)
    phrase = 'Accepting connection 1 from ' + ip + ':' + port
    return conn, phrase



def send_to_bot(conn, phrase):
    res = phrase

    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client


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


def play():
    motion = [0, 0]
    direction = [0, 0]

    while 1:
        event = pygame.event.wait()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if direction[0] == 0:
                direction[0] = 1
                send_to_bot(conn, "Left is pressed")
        if keys[pygame.K_RIGHT]:
            if direction[1] == 0:
                direction[1] = 1
                send_to_bot(conn, "Right is pressed")
        if keys[pygame.K_UP]:
            if motion[0] == 0:
                motion[0] = 1
                send_to_bot(conn, "Up is pressed")
        if keys[pygame.K_DOWN]:
            if motion[1] == 0:
                motion[1] = 1
                send_to_bot(conn, "Down is pressed")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if direction[0] == 1:
                    direction[0] = 0
                    send_to_bot(conn, "Left is released")
            if event.key == pygame.K_RIGHT:
                if direction[1] == 1:
                    direction[1] = 0
                    send_to_bot(conn, "Right is released")
            if event.key == pygame.K_UP:
                if motion[0] == 1:
                    motion[0] = 0
                    send_to_bot(conn, "Up is released")
            if event.key == pygame.K_DOWN:
                if motion[1] == 1:
                    motion[1] = 0
                    send_to_bot(conn, "Down is released")