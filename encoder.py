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