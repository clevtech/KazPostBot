import time
import math
from gpiozero import LED
from Webcam import Webcam
import cv2
import numpy as np


def gamma_correction(frame, power):
    frame = frame / 255.0
    frame = cv2.pow(frame, power)
    return np.uint8(frame * 255)


class MotorController:
    def __init__(self):
        self.front_motor = (LED(21), LED(20))
        self.back_motor = (LED(26), LED(19))
        self.steer_motor = (LED(23), LED(24))
        self.camera = Webcam()
        self.turn_in_process = False
        
    def forward(self):
        self.front_motor[0].off()
        self.front_motor[1].on()
        self.back_motor[0].off()
        self.back_motor[1].on()
        
    def backward(self):
        self.front_motor[0].on()
        self.front_motor[1].off()
        self.back_motor[0].on()
        self.back_motor[1].off()
        
    def steer_left(self):
        self.turn_in_process = False
        time.sleep(0.01)
        self.turn_in_process = True
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        self._wait_camera(30)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        self.turn_in_process = False
        
    def steer_right(self):
        self.turn_in_process = False
        time.sleep(0.01)
        self.turn_in_process = True
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        self._wait_camera(135)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        self.turn_in_process = False

    def steer_middle(self):
        self.turn_in_process = False
        time.sleep(0.01)
        self.turn_in_process = True
        print('started')
        if self._get_reading() < 77:
            self.steer_motor[0].off()
            self.steer_motor[1].on()
            self._wait_camera(60)
            print('1 waited')
            self.steer_motor[0].off()
            self.steer_motor[1].off()
        else:
            self.steer_motor[0].on()
            self.steer_motor[1].off()
            self._wait_camera(85)
            print('2 waited')
            self.steer_motor[0].off()
            self.steer_motor[1].off()
        self.turn_in_process = False
        
    def stop(self):
        self.front_motor[0].off()
        self.front_motor[1].off()
        self.back_motor[0].off()
        self.back_motor[1].off()

    def _get_reading(self):
        frame = self.camera.get_current_frame()
        gamma = gamma_correction(frame, 2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2)
        indexes = np.where(thresh.squeeze() == 0)[0]
        reading = int(np.median(indexes))
        return reading

    def _wait_camera(self, until, tolerance=10):
        while self.turn_in_process:
            frame = self.camera.get_current_frame()
            gamma = gamma_correction(frame, 2)
            gray = cv2.cvtColor(gamma, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2)
            cv2.imshow('frame', self._stripe_to_show(thresh))
            cv2.waitKey(1)
            indexes = np.where(thresh.squeeze() == 0)[0]
            reading = int(np.median(indexes))
            print(reading)
            if math.fabs(reading - until) <= tolerance:
                return
            
    def _stripe_to_show(self, stripe):
        stripe = stripe.reshape((1, -1))
        new_im = stripe
        for i in range(7):
            new_im = np.vstack((new_im, new_im))
        return new_im
        
if __name__ == '__main__':
    control = MotorController()
    control.steer_left()
##    control.steer_right()
##    control.steer_left()
##    control.steer_right()