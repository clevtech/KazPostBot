from bluepy.btle import Scanner, DefaultDelegate
import time


last_value = "Center"


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


def scan():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(1)
    myDevices = ["12:3b:6a:1b:4f:74", "12:3b:6a:1b:50:1a"]
    Devices = {}
    for my in myDevices:
        Devices[my] = 0
    for dev in devices:
        for my in myDevices:
            if str(dev.addr) == my:
                metres = pow(10, ((dev.rssi + 59)/(-40)))
                Devices[my] = metres

    return Devices

def main():
    time.sleep(1)
    global last_value
    while 1:
        while 1:
            try:
                devices = scan()
                break
            except:
                raise
        x = (devices["12:3b:6a:1b:4f:74"] - devices["12:3b:6a:1b:50:1a"])
        if x < 0:
            x = -x
        if x > 0.7:
            if devices["12:3b:6a:1b:4f:74"] > devices["12:3b:6a:1b:50:1a"]:
                if last_value == "Turn L":
                    print("Turn L")
                else:
                    print("Center")
                last_value = "Turn L"
            elif devices["12:3b:6a:1b:4f:74"] < devices["12:3b:6a:1b:50:1a"]:
                if last_value == "Turn R":
                    print("Turn R")
                else:
                    print("Center")
                last_value = "Turn R"
        else:
            print("Center")


if __name__ == "__main__":
    main()
