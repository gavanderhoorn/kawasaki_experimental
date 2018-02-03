import telnetlib, time, sys, os, telnet_commands
from telnet_commands import abort_kill_all, load_as_file, get_kawa_id, id_to_robot_type_msg, get_kawa_status, status_to_protocol_msg
from telnet_commands import is_motion_possible


HOST = '127.0.0.1'
PORT = 9105 # 
PORT = 10000
user = 'as'

current_path = os.path.dirname(os.path.realpath(__file__))
file_location = current_path + "\Kawasaki_code.as"

try:
	tc = telnet_commands.log_in(HOST, PORT, user)
	
	ID = get_kawa_id(tc)
	print(id_to_robot_type_msg(ID))

	abort_kill_all(tc)
	
	tc.write(b"ereset\r\n")	
	print (tc.read_until(b">").decode("ascii"))
 	
	load_as_file(tc, file_location)

	tc.write(b"Zpow on\r\n")
	print (tc.read_until(b">").decode("ascii"))

	STATUS = get_kawa_status(tc)
	if is_motion_possible(tc, STATUS) != True:
		print("Motion is not possible :(")

	tc.write(b"pcexe 1: ros_init_queue\r\n")
	print (tc.read_until(b">").decode("ascii"))

	os.system("start /B start cmd.exe @cmd /k python read_status.py")

	tc.write(b"pcexe 2: ros_send_server\r\n")
	print (tc.read_until(b">").decode("ascii"))

	os.system("start /B start cmd.exe @cmd /k python test_receive_poses.py")

	tc.write(b"pcexe ros_recv_server\r\n")
	print (tc.read_until(b">").decode("ascii"))

	os.system("start /B start cmd.exe @cmd /k python test_send_poses.py")

	tc.write(b"exe ros_move_kawa\r\n")
	print (tc.read_until(b">").decode("ascii"))
	
	time.sleep(10)
	
	tc.write(b"active = 0\r\n")
	print (tc.read_until(b">").decode("ascii"))
	
	telnet_commands.abort_kill_all(tc)

	tc.write(b"ereset\r\n")	
	print (tc.read_until(b">").decode("ascii"))

except: print("Unexpected error:", sys.exc_info())

print("Disconnecting")
tc.close()