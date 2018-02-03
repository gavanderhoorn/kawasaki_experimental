import socket,time, telnet_commands

TCP_IP = "192.168.0.1"
TCP_IP = "127.0.0.1"
TCP_PORT = 9111
BUFFER_SIZE = 512
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("Connected")
joints = "87|10|-91|-185|-40|-172|0.1"

def joints_to_msg(joints):
	pose = "0x02|0x01|" + str(len("|11|"+joints+"|0x03")) + "|11|" + joints + "|0x03" 
	return pose

pose1 = joints_to_msg("87|10|-91|-185|-40|-172|0.2")    # input("pose?:") 
pose2 = joints_to_msg("8|110|-41|-155|-40|-172|0.3") # input("pose?:") 
pose3 = joints_to_msg("87|50|-91|-195|-60|-122|0.3") # input("pose?:") 
pose4 = joints_to_msg("0|100|-10|-125|-45|-10|0.1") # input("pose?:") 

while True:
	for pose in [pose1, pose2, pose3, pose4]:
		print("Sending: ", pose)
		s.send(pose.encode())
		time.sleep(0.1)		
	time.sleep(3)
	# 0x02|
	# 0x02|10|joint_1|joint_2|joint_3|joint_4|joint_5|joint_6|0x03
	# 0x02|87|10|-91|-185|-40|-172|0x03