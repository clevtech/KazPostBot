import socket, time
# Sample socket app for connect from lower RPI to higher RPI
# Done by @Naboo to @Batyr


# Function to listen socket connection
def read_from_socket(mySocket):
    # data is decoded message from higher RPI
    data = mySocket.recv(1024).decode()
    # return message data
    return data


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def Main():
    # Connect to Higher RPI
    host = get_ip() # Here goes IP address of the Higher RPI
    port = 6666 # It is socket port of the higher RPI
    mySocket = socket.socket() # Creating socket
    mySocket.connect((host, port)) # Defying socket ip and port

    while 1:
        # Receiving data
        data = read_from_socket(mySocket)

        # Printing received message
        print(data)


    # Closing socket connection
    mySocket.close()


if __name__ == '__main__':
    while 1:
        try:
            Main()
        except:
            print("No server, wait 20 sec")
            time.sleep(20)

