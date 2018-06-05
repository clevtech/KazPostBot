from MotorController import MotorController
from ManualHost import ManualHost

control = MotorController()
host = ManualHost()

while True:
    cmd = host.read()
    if cmd in ['b', 'f', 'l', 'r', 's']:
        if cmd == 'b':
            control.backward()
        elif cmd == 'f':
            control.forward()
        elif cmd == 'l':
            control.steer_left()
        elif cmd == 'r':
            control.steer_right()
        elif cmd == 's':
            control.stop()