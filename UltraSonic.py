import thread
import RPi.GPIO as GPIO
import time

class UltraSonic:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.sonic1 = (10, 9)
        GPIO.setup(self.sonic1[0], GPIO.OUT)
        GPIO.setup(self.sonic1[1], GPIO.IN)
        self.sonic2 = (3, 4)
        GPIO.setup(self.sonic2[0], GPIO.OUT)
        GPIO.setup(self.sonic2[1], GPIO.IN)
        self.sonic3 = (27, 22)
        GPIO.setup(self.sonic3[0], GPIO.OUT)
        GPIO.setup(self.sonic3[1], GPIO.IN)
        
        
    def _measure_distance(self, sonic):
        GPIO.output(sonic[0], True)
        time.sleep(0.00001)
        GPIO.output(sonic[0], False)
        loop_start = time.time()
        while GPIO.input(sonic[1]) == 0:
            pulse_start = time.time()
            if time.time() - loop_start > 0.007:
                return 200
        while GPIO.input(sonic[1]) == 1:
            pulse_end = time.time()
            if time.time() - loop_start > 0.007:
                return 200
        try:
            pulse_duration = pulse_end - pulse_start
            distance = round(pulse_duration * 17150, 2)
        except:
            return 200
        return distance
        
    def send_state(self, thresh=100):
        frw_sonic_vals = [self._measure_distance(self.sonic1), self._measure_distance(self.sonic2), self._measure_distance(self.sonic3)]
        frw_least_distance = min(frw_sonic_vals)
##        print(frw_sonic_vals)
##        bck_sonic_vals
##        bck_least_distance
        if frw_least_distance < thresh:
            return 'frw'
##        elif bck_least_distance < thresh:
##            return 'bck'
        return 'ok'
        
if __name__ == "__main__":
    us = UltraSonic()
    while True:
        us.send_state(True)
        time.sleep(0.5)
            
            
            