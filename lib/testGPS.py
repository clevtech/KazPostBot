from flask import Flask
from flask_sockets import Sockets


app = Flask(__name__)
sockets = Sockets(app)

@sockets.route('/orientation')
def echo_socket(ws):
	f=open("orientation.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/geolocation')
def echo_socket(ws):
	f=open("geolocation.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()



@app.route('/')
def hello():
	return 'Hello World!'

if __name__ == "__main__":
	from gevent import pywsgi
	from geventwebsocket.handler import WebSocketHandler
	server = pywsgi.WSGIServer(('192.168.1.107', 5000), app, handler_class=WebSocketHandler)
	server.serve_forever()
