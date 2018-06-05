#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import pygame, random, sys, socket, time
from pygame.locals import *


def socket_start():
    port = 6666
    ip = get_ip()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    try:
        soc.bind((ip, port))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()
    soc.listen(1)
    print('Socket now listening')
    # this will make an infinite loop needed for
    # not reseting server for every client
    conn, addr = soc.accept()
    ip, port = str(addr[0]), str(addr[1])
    print('Accepting connection 1 from ' + ip + ':' + port)
    phrase = 'Accepting connection 1 from ' + ip + ':' + port
    return conn, phrase


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


def send_to_bot(conn, phrase):
    res = phrase

    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def main():
    pygame.init()

    SCREENWIDTH = 400
    SCREENHEIGHT = 500

    size = (SCREENWIDTH, SCREENHEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Cleverest Technologies: Manual Control for PostBot")

    screen.fill((255, 255, 255))
    conn, phrase = socket_start()


    # Allowing the user to close the window...
    carryOn = True

    motion = [0, 0]
    direction = [0, 0]

    while carryOn:
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

        if motion == [1, 0] and direction == [0, 0]:
            text = "For"
        if motion == [0, 1] and direction == [0, 0]:
            text = "Back"
        if motion == [0, 1] and direction == [1, 0]:
            text = "Lef-Back"
        if motion == [0, 1] and direction == [0, 1]:
            text = "Right-Back"
        if motion == [1, 0] and direction == [1, 0]:
            text = "Left-For"
        if motion == [1, 0] and direction == [0, 1]:
            text = "Right-For"
        if motion == [0, 0] and direction == [1, 0]:
            text = "Left-Stop"
        if motion == [0, 0] and direction == [0, 1]:
            text = "Right-Stop"
        if motion == [0, 0] and direction == [0, 0]:
            text = "Stop"


        font = pygame.font.SysFont("helvetica", 98)
        screen.fill((255, 255, 255))
        text = "\n\n\n   " + text
        blit_text(screen, text, (20, 20), font)
        # Refresh Screen
        pygame.display.update()


    pygame.quit()


if __name__ == '__main__':
    main()

