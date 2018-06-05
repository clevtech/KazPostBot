import time
import math
from gpiozero import LED
from RPi import GPIO

class MotorController:
    def __init__(self):
        self.encoder_A = 17
        self.encoder_B = 18
        self.front_motor = (LED(21), LED(20))
        self.back_motor = (LED(19), LED(26))
        self.steer_motor = (LED(23), LED(24))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.encoder_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.encoder_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.encoder_value = 0
        self.encoder_last_A = GPIO.input(self.encoder_A)
        self.encoder_last_B = GPIO.input(self.encoder_B)
        
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
        self.steer_motor[0].on()
        self.steer_motor[1].off()
        self._wait_encoder(7)
        self.steer_motor[0].off()
        self.steer_motor[1].off()
        
    def steer_right(self):
        self.steer_motor[0].off()
        self.steer_motor[1].on()
        self._wait_encoder(7)
        self.steer_motor[0].off()
        self.steer_motor[1].off()

    def steer_middle(self):
        return
        
    def stop(self):
        self.front_motor[0].off()
        self.front_motor[1].off()
        self.back_motor[0].off()
        self.back_motor[1].off()

    def _wait_encoder(self, until, tolerance=5):
        while True:
            a_state = GPIO.input(self.encoder_A)
            b_state = GPIO.input(self.encoder_B)
            if self.encoder_last_A == 0 and self.encoder_last_B == 0:
                if a_state == 1 and b_state == 0:
                    self.encoder_value += 1
                elif a_state == 0 and b_state == 1:
                    self.encoder_value -= 1
            elif self.encoder_last_A == 0 and self.encoder_last_B == 1:
                if a_state == 0 and b_state == 0:
                    self.encoder_value += 1
                elif a_state == 1 and b_state == 1:
                    self.encoder_value -= 1
            elif self.encoder_last_A == 1 and self.encoder_last_B == 0:
                if a_state == 1 and b_state == 1:
                    self.encoder_value += 1
                elif a_state == 0 and b_state == 0:
                    self.encoder_value -= 1
            elif self.encoder_last_A == 1 and self.encoder_last_B == 1:
                if a_state == 0 and b_state == 1:
                    self.encoder_value += 1
                elif a_state == 1 and b_state == 0:
                    self.encoder_value -= 1
            print(self.encoder_value)
            self.encoder_last_A = a_state
            self.encoder_last_B = b_state
            if math.fabs(self.encoder_value - until) <= tolerance:
                return
            time.sleep(0.01)

        
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