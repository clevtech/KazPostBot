#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


class IRencoder:
    def __init__(self, ir=17):
        self.ir = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(self.ir, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def where_is(self):
        if GPIO.input(self.ir) == GPIO.LOW:
            return True
    
    def where_loop(self):
        previous = GPIO.HIGH
        while 1:
            if previous == GPIO.LOW and GPIO.input(self.ir) == GPIO.LOW:
                return True
            previous = GPIO.input(self.ir)
            time.sleep(0.1)
            


if __name__ == "__main__":
    detect = IRencoder()
    a = 0
    while 1:
        a += 1
        time.sleep(0.01)
        if detect.where_loop():
            print(a)
        