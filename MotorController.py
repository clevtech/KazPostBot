import time
import math
from gpiozero import LED
from UltraSonic import UltraSonic
import cv2
import numpy as np
import thread
from RPi import GPIO
from IRencoder import IRencoder


class MotorController:
    def __init__(self):
        self.calibrating = False
        GPIO.setmode(GPIO.BCM)
        self.front_motor = (LED(20), LED(21))
        self.back_motor = (LED(26), LED(19))
        self.steer_motor = (LED(24), LED(23))
        self.switch = LED(4)
        self.switch.on()
        self.stop()
        self.direction = 0
        self.steer = 0
        self.ir = IRencoder()
        self.calibrate_steer()
        self.brake = False
        self.sonic = UltraSonic()
        thread.start_new_thread(self._sonic_state, ())
        
    def _sonic_state(self):
        while True:
            state = self.sonic.get_state()
            print(state)
            if self.direction == 1 and state == 'frw':
                self.stop()
            elif self.direction == 2 and state == 'bck':
                self.stop()
            time.sleep(0.2)
        
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

    def calibrate_steer(self):
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        time.sleep(0.4)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        time.sleep(0.5)
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        while not self.ir.is_white():
            time.sleep(0.02)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        self.steer = 1

    def turn(self, goal):
        self.brake = False
        if self.steer == 0:
            if goal == 'left':
                return
            elif goal == 'mid':
                self.steer_motor[0].off()
                self.steer_motor[1].on()
                while not self.ir.is_white() and not self.brake:
                    time.sleep(0.02) # tune this
                self.steer_motor[0].off()
                self.steer_motor[1].off()
                self.steer = 1
            elif goal == 'right':
                self.steer_motor[0].off()
                self.steer_motor[1].on()
                # time.sleep(0.7) # tune this
                start_time = time.time()
                while (time.time() - start_time < 0.65) and not self.brake:
                    time.sleep(0.02)
                self.steer_motor[0].off()
                self.steer_motor[1].off()
                self.steer = 2
        elif self.steer == 1:
            if goal == 'left':
                self.steer_motor[0].on()
                self.steer_motor[1].off()
                # time.sleep(0.35) # tune this
                start_time = time.time()
                while (time.time() - start_time < 0.35) and not self.brake:
                    time.sleep(0.02)
                self.steer_motor[0].off()
                self.steer_motor[1].off()
                self.steer = 0
            elif goal == 'mid':
                return
            elif goal == 'right':
                self.steer_motor[0].off()
                self.steer_motor[1].on()
                # time.sleep(0.35)  # tune this
                start_time = time.time()
                while (time.time() - start_time < 0.35) and not self.brake:
                    time.sleep(0.02)
                self.steer_motor[0].off()
                self.steer_motor[1].off()
                self.steer = 2
        elif self.steer == 2:
            if goal == 'left':
                self.steer_motor[0].on()
                self.steer_motor[1].off()
                # time.sleep(0.7) # tune this
                start_time = time.time()
                while (time.time() - start_time < 0.7) and not self.brake:
                    time.sleep(0.02)
                self.steer_motor[0].off()
                self.steer_motor[1].off()
                self.steer = 0
            elif goal == 'mid':
                self.steer_motor[0].on()
                self.steer_motor[1].off()
                while not self.ir.is_white() and not self.brake:
                    time.sleep(0.02)  # tune this
                self.steer_motor[0].off()
                self.steer_motor[1].off()
                self.steer = 1
            elif goal == 'right':
                return
    # def _calibrate_encoder(self):
    #     self.calibrating = True
    #     self.stop()
    #     self.steer_motor[0].on()
    #     self.steer_motor[1].off()
    #     time.sleep(1)
    #     self.steer_motor[0].off()
    #     self.steer_motor[1].off()
    #     time.sleep(0.2)
    #     self.encoder.left = self.encoder.get_reading()
    #     self.steer_motor[0].off()
    #     self.steer_motor[1].on()
    #     time.sleep(1)
    #     self.steer_motor[0].off()
    #     self.steer_motor[1].off()
    #     self.encoder.right = self.encoder.get_reading()
    #     self.encoder.mid = self.encoder.right / 2
    #     self.calibrating = False
    #     self.turn('mid')
    
    # def turn(self, goal, shift=0, tolerance=5):
    #     print(goal)
    #     try:
    #         if self.calibrating: return
    #         if goal == 'left': val = shift + self.encoder.left
    #         elif goal == 'right': val = self.encoder.right - shift
    #         elif goal == 'mid': val = int((self.encoder.right - self.encoder.left) / 2 + self.encoder.left)
    #         start_time = time.time()
    #         while math.fabs(self.encoder.get_reading() - val) > tolerance and time.time() - start_time < 0.5:
    #             print(math.fabs(self.encoder.get_reading() - val))
    #             if math.fabs(self.encoder.get_reading() - val) > 60:
    #                 self.steer_motor[0].off()
    #                 self.steer_motor[1].off()
    #                 self._calibrate_encoder()
    #                 return
    #             if self.encoder.get_reading() < val:
    #                 self.steer_motor[0].off()
    #                 self.steer_motor[1].on()
    #             else:
    #                 self.steer_motor[0].on()
    #                 self.steer_motor[1].off()
    #             time.sleep(0.075)
    #         self.steer_motor[0].off()
    #         self.steer_motor[1].off()
    #     except:
    #         self.turn('mid')
        
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
##    time.sleep(1)
##    control.turn('mid')
##    time.sleep(1)
##    control.turn('left')
##    time.sleep(1)
##    control.turn('mid')
##    control.steer_right()
##    control.steer_left()
##    control.steer_right()
