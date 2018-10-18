from bluepy.btle import Scanner
from multiprocessing import Process
import datetime

def scanLE(n):
    scanner = Scanner(n)
    devices = scanner.scan(0.5)
    print("Data from " + str(n))
    print(datetime.datetime.now())
    for dev in devices:
        print("Device %s, RSSI=%d dB" % (dev.addr, dev.rssi))

p0 = Process(target=scanLE, args=(0,))
p1 = Process(target=scanLE, args=(1,))
p0.start()
p1.start()
p0.join()
p1.join()
