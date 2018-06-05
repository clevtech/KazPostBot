import time
from gpiozero import LED
import math

class MotorController:
    def __init__(self):
        self.front_motor = (LED(21), LED(20))
        self.back_motor = (LED(19), LED(26))
        self.steer_motor = (LED(23), LED(24))
        
    def forward(self):
        self.front_motor[0].off()
        self.front_motor[1].on()
        
    def backward(self):
        self.front_motor[0].on()
        self.front_motor[1].off()
        
    def steer_left(self):
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        time.sleep(0.8)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        
    def steer_right(self):
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        time.sleep(1.5)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        
        
    def stop(self):
        self.front_motor[0].off()
        self.front_motor[1].off()
        
if __name__ == '__main__':
    control = MotorController()
    control.steer_right()
##    control.backward()
##    time.sleep(0.8)
##    control.stop()
##    control.forward()
##    time.sleep(0.8)
##    control.stop()
##    control.steer_left()
##    control.steer_right()