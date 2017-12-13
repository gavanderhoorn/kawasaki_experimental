import socket

TCP_IP = "192.168.0.1"
TCP_PORT = 11111
BUFFER_SIZE = 124
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
	reply = s.recv(BUFFER_SIZE)
	print "Kawasaki pose update: ", reply