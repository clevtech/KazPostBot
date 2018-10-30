import lib.arduino_speak as ard
import time


def mot_start():
    while True:
        try:
            mot = ard.connect_to()
            break
        except:
            pass
    return mot

def send_to_bot(conn, phrase):
    time.sleep(0.1)
    ard.motion(conn, phrase)


def main():
    mot = mot_start()

    while 1:
        dir = input()

        if dir == "s":
            send_to_bot(mot, "S")
        elif dir == "w":
            send_to_bot(mot, "U")
        elif dir == "d":
            send_to_bot(mot, "R")
        elif dir == "a":
            send_to_bot(mot, "L")
        elif dir == "r":
            send_to_bot(mot, "C")
        time.sleep(0.1)


if __name__=="__main__":
    main()
