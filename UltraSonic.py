import sys
import glob
import serial
import time

class UltraSonic:
    def __init__(self):
        self.front = self._connect_to('Sonar')
        
    def get_state(self):
        self.front.write("?".encode())
        obstacle = self.front.readline().strip().decode("utf-8")
        if obstacle == '1':
            return 'frw'
        return 'ok'
    
    def _serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.usbmodem*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
    def _connect_to(self, type):
        arduinos = self._serial_ports()
        ser = []
        for i in range(len(arduinos)):
            ser.append(serial.Serial(arduinos[i], 115200))
            time.sleep(1)
            ser[i].write("?".encode())
            # time.sleep(0.1)
            types = ser[i].readline().strip().decode("utf-8")
            if types == type:
                return ser[i]
    
if __name__ == "__main__":
    sonic = UltraSonic()
    while True:
        print(sonic.get_state())

##import thread
##import RPi.GPIO as GPIO
##import time
##
##class UltraSonic:
##    def __init__(self):
##        GPIO.setmode(GPIO.BCM)
##        self.flu = (2, 3)
##        GPIO.setup(self.flu[0], GPIO.OUT)
##        GPIO.setup(self.flu[1], GPIO.IN)
##        self.fmu = (27, 22)
##        GPIO.setup(self.fmu[0], GPIO.OUT)
##        GPIO.setup(self.fmu[1], GPIO.IN)
##        self.fru = (10, 9)
##        GPIO.setup(self.fru[0], GPIO.OUT)
##        GPIO.setup(self.fru[1], GPIO.IN)
##        
##        
##    def _measure_distance(self, sonic):
##        GPIO.output(sonic[0], True)
##        time.sleep(0.00001)
##        GPIO.output(sonic[0], False)
##        loop_start = time.time()
##        while GPIO.input(sonic[1]) == 0:
##            pulse_start = time.time()
##            if time.time() - loop_start > 0.007:
##                return 200
##        while GPIO.input(sonic[1]) == 1:
##            pulse_end = time.time()
##            if time.time() - loop_start > 0.007:
##                return 200
##        try:
##            pulse_duration = pulse_end - pulse_start
##            distance = round(pulse_duration * 17150, 2)
##        except:
##            return 200
##        return distance
##        
##    def send_state(self, thresh=100):
##        frw_sonic_vals = [self._measure_distance(self.flu), self._measure_distance(self.fmu), self._measure_distance(self.fru)]
##        frw_least_distance = min(frw_sonic_vals)
##        print(frw_sonic_vals)
####        bck_sonic_vals
####        bck_least_distance
##        if frw_least_distance < thresh:
##            return 'frw'
####        elif bck_least_distance < thresh:
####            return 'bck'
##        return 'ok'
##        
##if __name__ == "__main__":
##    us = UltraSonic()
##    while True:
##        us.send_state()
##        time.sleep(0.5)
##            
##            
##            