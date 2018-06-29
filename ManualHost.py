import socket
import time
import client_init.find_host as find_host

class ManualHost:
    def __init__(self, port=6666):
        self.sock = socket.socket()
        with open("hosts.txt", ) as file:
            hosts = file.readlines()
            hosters = []
            for host in hosts:
                hosters.append(host.replace("\n", ""))

        old_host = True

        for i in range(len(hosters)):
            try:
                self.sock.connect((hosters[i], port))
                old_host = False
                break
            except:
                pass

        if old_host:
            number = 0
            while True:
                host = str(find_host.nmap_host())
                print(host)
                if host:
                    try:
                        self.sock.connect((host, port))
                        break
                    except:
                        number = number + 1
                        time.sleep(1)


    def read(self):
        data = self.sock.recv(1024).decode()
        return data
    
    def send(self, message):
        try:
            self.sock.send(message.encode())
            return True
        except:
            return False


if __name__=="__main__":
    host = ManualHost()
    host.send("FUCK!")

