from MotorController import MotorController
from ManualHost import ManualHost
import thread

control = MotorController()
host = ManualHost()

##cmd = None
while True:
    cmd = host.read()
    if cmd in ['Left is pressed', 'Right is pressed',
               'Up is pressed', 'Down is pressed',
               'Left is released', 'Right is released',
               'Up is released', 'Down is released']:
        if cmd == 'Left is pressed':
            thread.start_new_thread(control.turn, ('left',))
        elif cmd == 'Right is pressed':
            thread.start_new_thread(control.turn, ('right',))
        elif cmd == 'Up is pressed':
            is_frw = True
            thread.start_new_thread(control.forward, ())
        elif cmd == 'Down is pressed':
            is_frw = False
            thread.start_new_thread(control.backward, ())
        elif cmd == 'Left is released' or cmd == 'Right is released':
            thread.start_new_thread(control.turn, ('mid',))
        elif cmd == 'Up is released' or cmd == 'Down is released':
            thread.start_new_thread(control.stop, ())