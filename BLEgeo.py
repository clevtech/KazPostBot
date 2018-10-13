import sys
import glob
import serial
import time
import urllib.request


def serial_ports():
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/ttyUSB*')
		print(ports)
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.usbmodem*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = ports
	return result


# types: Sonar - sonar arduino, Box - box controlling arduino
# returns serial connection
def connect_to():
	arduinos = serial_ports()
	print(arduinos)
	ser = []
	for i in range(len(arduinos)):
		ser.append(serial.Serial(arduinos[i], 115200))
		time.sleep(1)
		ser[i].write("?".encode())
		# time.sleep(0.1)
		types = ser[i].readline().strip().decode("utf-8")
		print(types)
		if types == "L":
			left = ser[i]
		if types == "R":
			right = ser[i]
	return left, right


def get_value(left):

    left.write("b".encode())
    line = str(left.readline().strip().decode("utf-8"))
    lines = line.split(";")
    add = []
    sig = []
    for l in lines:
        if len(str(l)) > 3:
            adres = l.split("M:")[1].split(" S:")[0]
            signal = int(l.split(" S:")[1])
            add.append(adres)
            sig.append(signal)

    return add, sig


left, right = connect_to()
while 1:

    addL, sigL = get_value(left)
    addR, sigR = get_value(right)

    print(addL)
    print(sigL)
    print(addR)
    print(sigR)
