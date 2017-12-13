import socket

TCP_IP = "192.168.0.1"
TCP_PORT = 11112
BUFFER_SIZE = 512
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
	pose = raw_input("pose?:") 
	s.send(str(pose))

	# 0x02|
	# 0x02|10|joint_1|joint_2|joint_3|joint_4|joint_5|joint_6|0x03