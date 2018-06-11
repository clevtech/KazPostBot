import time
import math
from gpiozero import LED
from Webcam import Webcam
from UltraSonic import UltraSonic
import cv2
import numpy as np
import thread


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
        self.sonic = UltraSonic()
        self.turn_in_process = False
        self.direction = 0
        thread.start_new_thread(self._sonic_state, ())
        
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
        
    def steer_left(self):
        print('steer left')
        self.turn_in_process = False
        time.sleep(0.01)
        self.turn_in_process = True
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        print(self._wait_camera(30))
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        
    def steer_right(self):
        print('steer right')
        self.turn_in_process = False
        time.sleep(0.01)
        self.turn_in_process = True
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        print(self._wait_camera(90))
        self.steer_motor[0].off()
        self.steer_motor[1].off()

    def steer_middle(self):
        print('steer middle')
        self.turn_in_process = False
        time.sleep(0.01)
        self.turn_in_process = True
        if self._get_reading() < 70:
            print('->')
            self.steer_motor[0].off()
            self.steer_motor[1].on()
            print(self._wait_camera(60))
            self.steer_motor[0].off()
            self.steer_motor[1].off()
        else:
            print('<-')
            self.steer_motor[0].on()
            self.steer_motor[1].off()
            print(self._wait_camera(77))
            self.steer_motor[0].off()
            self.steer_motor[1].off()
        self.turn_in_process = False
        
    def stop(self):
        self.direction = 0
        self.front_motor[0].off()
        self.front_motor[1].off()
        self.back_motor[0].off()
        self.back_motor[1].off()

    def _get_reading(self):
        median_reading = []
        for i in range(1):
            frame = self.camera.get_current_frame()
            gamma = gamma_correction(frame, 1.5)
            gray = cv2.cvtColor(gamma, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 1)
            median = cv2.medianBlur(thresh,3)
            indexes = np.where(median == 0)
            reading = int(sum(indexes[1]) / len(indexes[1]))
            median_reading.append(reading)
        median_reading = np.median(median_reading)
        return int(median_reading)

    def _wait_camera(self, until, tolerance=5):
        while self.turn_in_process:
            frame = self.camera.get_current_frame()
            gamma = gamma_correction(frame, 1.5)
            gray = cv2.cvtColor(gamma, cv2.COLOR_BGR2GRAY)
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 1)
            median = cv2.medianBlur(thresh,3)
            indexes = np.where(median == 0)
            reading = int(sum(indexes[1]) / len(indexes[1]))
            frame[:, reading - 2 : reading + 2, 2] = 255
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            if math.fabs(reading - until) <= tolerance:
                return math.fabs(reading - until)
            
    def _stripe_to_show(self, stripe):
        stripe = stripe.reshape((1, -1))
        new_im = stripe
        for i in range(7):
            new_im = np.vstack((new_im, new_im))
        return new_im
    
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
    control.turn_in_process = True
    control._wait_camera(200)
##    control.steer_right()
##    control.steer_left()
##    control.steer_right()