#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2018, KazPostBot"
__version__ = "1.0.1"
__maintainer__ = "Bauyrzhan Ospan"
__email__ = "bospan@cleverest.tech"
__status__ = "Development"


import pygame, random, sys, time
from pygame.locals import *
import lib.arduino_speak as ard


def mot_start():
    while True:
        try:
            mot = ard.connect_to()
            break
        except:
            pass
    return mot


def send_to_bot(conn, phrase):
    time.sleep(0.1)
    ard.motion(conn, phrase)


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
    pygame.display.set_caption("Cleverest Technologies")

    screen.fill((255, 255, 255))
    conn = socket_start()


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
                send_to_bot(conn, "L")
        if keys[pygame.K_RIGHT]:
            if direction[1] == 0:
                direction[1] = 1
                send_to_bot(conn, "R")
        if keys[pygame.K_UP]:
            if motion[0] == 0:
                motion[0] = 1
                send_to_bot(conn, "U")
        if keys[pygame.K_DOWN]:
            if motion[1] == 0:
                motion[1] = 1
                send_to_bot(conn, "D")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if direction[0] == 1:
                    direction[0] = 0
                    send_to_bot(conn, "C")
            if event.key == pygame.K_RIGHT:
                if direction[1] == 1:
                    direction[1] = 0
                    send_to_bot(conn, "C")
            if event.key == pygame.K_UP:
                if motion[0] == 1:
                    motion[0] = 0
                    send_to_bot(conn, "S")
            if event.key == pygame.K_DOWN:
                if motion[1] == 1:
                    motion[1] = 0
                    send_to_bot(conn, "S")

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
