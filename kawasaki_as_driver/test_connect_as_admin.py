import socket, os, time, select

def connect_admin_kawasaki():
	TCP_IP = "192.168.0.1"
	TCP_PORT = 23
	BUFFER_SIZE = 1024
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	time.sleep(0.01)
	# s.setblocking(1)
	# print "Kawasaki reply: ", s.recv(1024)
	s.recv(6)
	s.send("FFFB18".decode("hex"))
	s.recv(3)
	s.send('FFFA18'.decode("hex"))
	s.recv(3)
	s.send('005654313030FFF0'.decode("hex"))
	for i in range(53):
		temp = str(s.recv(1))
		if str(temp) != "\n": print temp,
	s.send("as\r\n")
	temp = ""
	while temp != ">":
		temp = str(s.recv(1))
		if str(temp) != "\n": print temp,
	return s
# 
def kawa_command(s, msg):
	# print msg+"\r"
 	s.send(msg)
  	temp = ""
  	while temp != ">":
		temp = str(s.recv(1))
		if str(temp) != "\n": print temp,

def kawa_command2(s, msg):
	# print msg+"\r"
 	s.send(msg)
 	time.sleep(0.5)
  	print s.recv(256)
	

def kawa_kill(s, pcexe=True, exe=False):
	if pcexe:
		print "pcabort\r(aborting pc programs)"
		s.send("pcabort\r\n")
	  	temp = ""
	  	while temp != ">":
			temp = str(s.recv(1))
		print temp,

		print "pckill\r(killing pc programs)"
	 	s.send("pckill\r\n")
	  	temp = ""
	  	while temp != ")": # or temp != ">":
			temp = str(s.recv(1))
		print temp,

		print "1\r(Confirming kill)"
		s.send("1\r\n")
		while temp != ">":
			temp = str(s.recv(1))
		print temp,
	if exe:
		print "abort\r(aborting pc programs)"
		s.send("abort\r\n")
	  	temp = ""
	  	while temp != ">":
			temp = str(s.recv(1))
		print temp,

		print "kill\r(killing pc programs)"
	 	s.send("kill\r\n")
	  	temp = ""
	  	while temp != ")": # or temp != ">":
			temp = str(s.recv(1))
		print temp,

		print "1\r(Confirming kill)"
		s.send("1\r\n")
		while temp != ">":
			temp = str(s.recv(1))
		print temp,

s = connect_admin_kawasaki()
# kawa_command2(s, "LOAD kip2.as\r\n")

# kawa_command(s, "pcexe ros_recv_server\r\n")
# kawa_command(s, "pcexe ros_send_server\r\n")
# kawa_command(s, "pcexe movetest\r\n")

# kawa_command(s, "pcexe movetest\r\n")
# time.sleep(1)

# kawa_kill(s)
# 
# kawa_command(s, "pcexe send_pos_server\r\n")
# time.sleep(1)
# os.system("start /B start cmd.exe @cmd /k python receive_pos.py")
# time.sleep(3)
# 
# kawa_command(s, "exe recv_pos_server\r\n")
# time.sleep(1)
# os.system("start /B start cmd.exe @cmd /k python send_pos.py")
# 
# time.sleep(20)
# kawa_command(s, "active = 0\r\n")
# 
# time.sleep(5)
# kawa_kill(s, pcexe=True, exe=True)
# #  time.sleep(2)
# 
# s.close()
# print "Finished!!!"