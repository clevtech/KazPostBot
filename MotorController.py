import time
import math
from gpiozero import LED
from UltraSonic import UltraSonic
import cv2
import numpy as np
import thread
from RPi import GPIO
from Encoder import Encoder


class MotorController:
    def __init__(self):     
        GPIO.setmode(GPIO.BCM)
        self.front_motor = (LED(21), LED(20))
        self.back_motor = (LED(26), LED(19))
        self.steer_motor = (LED(23), LED(24))
        self.stop()
        self.direction = 0
        self.encoder = Encoder()
        self._calibrate_encoder()
        time.sleep(0.2)
        self.turn('mid')
        self.steer_state = 'mid'
##        self.sonic = UltraSonic()
        
##        thread.start_new_thread(self._sonic_state, ())
        
    def _encoder_state(self):
        while True:
            self.encoder.work_step()
            time.sleep(0.001)
            print(self.encoder.encoder_value)
        
    def _sonic_state(self):
        while True:
            state = self.sonic.send_state()
            print(state)
            if self.direction == 1 and state == 'frw':
                self.stop()
            elif self.direction == 2 and state == 'bck':
                self.stop()
        
    def forward(self):
        self.direction = 1
        self.front_motor[0].off()
        self.front_motor[1].on()
        self.back_motor[0].off()
        self.back_motor[1].on()
        
    def backward(self):
        self.direction = 2
        self.front_motor[0].on()
        self.front_motor[1].off()
        self.back_motor[0].on()
        self.back_motor[1].off()
        
    def _calibrate_encoder(self):
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        time.sleep(1)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        time.sleep(0.2)
        self.encoder.encoder_last_A, self.encoder.encoder_last_B, self.encoder.encoder_value = GPIO.input(self.encoder.encoder[0]), GPIO.input(self.encoder.encoder[1]), 0
        thread.start_new_thread(self._encoder_state, ())
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        time.sleep(1)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        self.encoder.encoder_range = self.encoder.encoder_value
    
    def turn(self, goal, shift=0, tolerance=1):
        if goal == 'left': val = shift
        elif goal == 'right': val = self.encoder.encoder_range - shift
        elif goal == 'mid': val = int(self.encoder.encoder_range / 2)
        start_time = time.time()
        while math.fabs(self.encoder.encoder_value - val) > tolerance and time.time() - start_time < 0.5:
            if self.encoder.encoder_value < val:
                self.steer_motor[0].off()
                self.steer_motor[1].on()
            else:
                self.steer_motor[0].on()
                self.steer_motor[1].off()
            time.sleep(0.00001)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        if goal == 'left':
            self.steer_state = 'left'
            self.encoder.encoder_value = shift + 2
        elif goal == 'right': self.steer_state = 'right'
        elif goal == 'mid': self.steer_state = 'mid'
        
    def stop(self):
        self.direction = 0
        self.front_motor[0].off()
        self.front_motor[1].off()
        self.back_motor[0].off()
        self.back_motor[1].off()
    
    def test_right(self):
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        
    def test_left(self):
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        
    def test_stop(self):
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        
        
if __name__ == '__main__':
    control = MotorController()
    time.sleep(1)
    control.turn('left')
    time.sleep(1)
    control.turn('right')
    time.sleep(1)
    control.turn('mid')
    time.sleep(1)
    control.turn('left')
    time.sleep(1)
    control.turn('mid')
##    control.steer_right()
##    control.steer_left()
##    control.steer_right()
