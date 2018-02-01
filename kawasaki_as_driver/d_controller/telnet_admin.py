import telnetlib, time, sys, os, telnet_commands
from telnet_commands import abort_kill_all, load_as_file

HOST = '127.0.0.1'
PORT = 9105 # 
PORT = 10000
user = 'as'

file_location = "F:/roskawa_v0.5.as"

try:
	tc = telnet_commands.log_in(HOST, PORT, user)
	telnet_commands.abort_kill_all(tc)
	tc.write(b"ereset\r\n")
	print (tc.read_until(b">").decode("ascii"))
	load_as_file(tc, file_location)
	
	os.system("start /B start cmd.exe @cmd /k python read_status_where.py")
	time.sleep(3)
	tc.write(b"pcexe ros_init_queue\r\n")
	print (tc.read_until(b">").decode("ascii"))

	tc.write(b"pcexe ros_recv_server\r\n")
	print (tc.read_until(b">").decode("ascii"))
	#
	time.sleep(0.5)
	os.system("start /B start cmd.exe @cmd /k python test_send_poses.py")

	time.sleep(2.5)
	tc.write(b"Zpow on\r\n")
	print (tc.read_until(b">").decode("ascii"))

	tc.write(b"exe ros_move_kawa\r\n")
	print (tc.read_until(b">").decode("ascii"))
	
	time.sleep(20)

	tc.write(b"active = 0\r\n")
	print (tc.read_until(b">").decode("ascii"))

except: print("Unexpected error:", sys.exc_info())

print("Disconnecting")
tc.close()

# kawa_command(s, "pcexe ros_recv_server\r\n")
# kjkawa_command(s, "pcexe ros_send_server\r\n")

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