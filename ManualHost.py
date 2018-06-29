import socket
import time

class ManualHost:
    def __init__(self, host='10.12.96.20', port=6666):
        self.sock = socket.socket()
        while True:
            try:
                self.sock.connect((host, port))
                break
            except:
                time.sleep(10)
    def read(self):
        data = self.sock.recv(1024).decode()
        return data
    
    def send(self, message):
        try:
            self.sock.send(message.encode())
            return True
        except:
            return False