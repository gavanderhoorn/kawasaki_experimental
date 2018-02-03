import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 9112
BUFFER_SIZE = 4096
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
	reply = s.recv(BUFFER_SIZE).decode("ascii")
	print("Kawasaki pose update: ", reply)