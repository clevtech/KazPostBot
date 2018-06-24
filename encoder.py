from RPi import GPIO
from time import sleep

A = 17
B = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

angle = 0
ALastState = GPIO.input(A)
BLastState = GPIO.input(B)

try:
    while True:
        AState = GPIO.input(A)
        BState = GPIO.input(B)
        if ALastState == False and BLastState == False:
            if AState == True and BState == False:
                angle += 1
            elif AState == False and BState == True:
                angle -= 1
        elif ALastState == False and BLastState == True:
            if AState == False and BState == False:
                angle += 1
            elif AState == True and BState == True:
                angle -= 1
        elif ALastState == True and BLastState == False:
            if AState == True and BState == True:
                angle += 1
            elif AState == False and BState == False:
                angle -= 1
        elif ALastState == True and BLastState == True:
            if AState == False and BState == True:
                angle += 1
            elif AState == True and BState == False:
                angle -= 1
        print(angle)
        ALastState = AState
        BLastState = BState
        sleep(0.001)
finally:
        GPIO.cleanup()

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