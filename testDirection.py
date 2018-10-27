from bluepy.btle import Scanner
from multiprocessing import Process
import multiprocessing
import datetime

manager = multiprocessing.Manager()


def scanLE(n, devices1):
    scanner = Scanner(n)
    devices = scanner.scan(1)
    for dev in devices:
        devices1.append(str(dev.addr + "," + str(dev.rssi) + "," + str(n)))


def scan(MAC):
    devices1 = manager.list()
    p0 = Process(target=scanLE, args=(2, devices1, ))
    p1 = Process(target=scanLE, args=(1, devices1, ))
    p0.start()
    p1.start()
    p0.join()
    p1.join()
    right, left = -100, -100
    for device in devices1:
        mac = device.split(",")[0]
        if mac == MAC:
            side = device.split(",")[2]
            rssi = device.split(",")[1]
            if side == "1":
                right = int(rssi)
            else:
                left = int(rssi)
    return right, left


def main():
    while 1:
        r, l = scan("12:3b:6a:1b:50:1e")
        if (l - r) > 4 or (l - r) < -4:
            if l<r:
                print("Right")
            elif r<l:
                print("Left")
        else:
            print("Center")
        print("R:" + str(r) + " L:" + str(l))


def main2():
    devices1 = manager.list()
    MAC = "12:3b:6a:1b:50:1e"
    p1 = Process(target=scanLE, args=(1, devices1, ))
    p1.start()
    p1.join()
    for device in devices1:
        mac = device.split(",")[0]
        if mac == MAC:
            print(device)


if __name__=="__main__":
    while 1:
        main()
#    scanLE(0, [])
