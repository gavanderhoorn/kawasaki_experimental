import socket,time, telnet_commands

TCP_IP = "192.168.0.1"
TCP_IP = "127.0.0.1"
TCP_PORT = 9111
BUFFER_SIZE = 512
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("Connected")

pose1 = "0x02|87|10|-91|-185|-40|-172|0x03"# input("pose?:") 
pose2 = "0x02|8|110|-41|-155|-40|-172|0x03"# input("pose?:") 
pose3 = "0x02|87|50|-91|-195|-60|-122|0x03"# input("pose?:") 
pose4 = "0x02|0|100|-1|-125|-45|-10|0x03"# input("pose?:") 

while True:
	for pose in [pose1, pose2, pose3, pose4]:
		print(pose)
		s.send(pose.encode())
		time.sleep(0.1)
	time.sleep(3)
	# 0x02|
	# 0x02|10|joint_1|joint_2|joint_3|joint_4|joint_5|joint_6|0x03
	# 0x02|87|10|-91|-185|-40|-172|0x03