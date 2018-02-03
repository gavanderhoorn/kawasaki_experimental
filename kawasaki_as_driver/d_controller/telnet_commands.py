from telnetlib import IAC, DO, DONT, WILL, WONT, SB, SE, TTYPE, NAOFFD, ECHO
import telnetlib, time

def process_option(socket, cmd, opt):
	#
	# Sources 
	# https://github.com/rapid7/metasploit-framework/blob/master/lib/msf/core/exploit/telnet.rb
	# https://github.com/jquast/x84/blob/cf3dff9be7280f424f6bcb0ea2fe13d16e7a5d97/x84/default/telnet.py
	# 
	env_term = b"VT100"
	IS = b'\00'
	if cmd == WILL and opt == ECHO: #hex:ff fb 01 name:IAC WILL ECHO description:(I will echo)
			socket.sendall(IAC + DO + opt) #hex(ff fd 01), name(IAC DO ECHO), descr(please use echo)
	elif cmd == DO and opt == TTYPE: #hex(ff fd 18), name(IAC DO TTYPE), descr(please send environment type)
			socket.sendall(IAC + WILL + TTYPE) #hex(ff fb 18), name(IAC WILL TTYPE), descr(Dont worry, i'll send environment type)
	elif cmd == SB:
		socket.sendall(IAC + SB + TTYPE + IS + env_term + IS + IAC + SE)
		# hex(ff fa 18 00 b"VT100" 00 ff f0) name(IAC SB TTYPE iS VT100 IS IAC SE) descr(Start subnegotiation, environment type is VT100, end negotation)
	elif cmd == SE: # server letting us know sub negotiation has ended
		pass # do nothing
	else: print("Unexpected command")

def log_in(HOST, PORT, user):
	tc = telnetlib.Telnet()
	print("connecting to", HOST, PORT)
	tc.set_option_negotiation_callback(process_option)
	tc.open(HOST, PORT, 1)
	time.sleep(0.5)
	print(tc.read_until(b"n: ").decode("ascii"))
	time.sleep(0.3)
	tc.write(user.encode() + b"\r\n")
	time.sleep(0.3)
	print (tc.read_until(b">").decode("ascii"))
	return tc

def load_as_file(tc, file_location=None):
	try: inputfile = open(file_location, 'r')
	except: pass
	if file_location != None and inputfile != None:
		file_text = inputfile.read() # Store Kawa-as code from file in local varianle
		inputfile.close()		
		n = 486 # Max amount of characters that can be accepted per write to kawa.
		text_split = [file_text[i:i+n] for i in range(0, len(file_text), n)] #Split AS code in sendable blocks
		#Perform load .as file protocol
		tc.write(b"load ROSin_Kawa.as\r\n")
		print(tc.read_until(b'.as').decode("ascii"))
		tc.write(b'\x02A    0\x17')
		print(tc.read_until(b"\x17").decode("ascii"))
		#Start sending the actual .as file in blocks
		for i in range(0, len(text_split), 1):
			tc.write(b'\x02C    0' + text_split[i].encode() + b'\x17')
			print(tc.read_until(b"\x17").decode("ascii"))
		tc.write(b'\x02' + b'C    0' + b'\x1a\x17')
		#Finish transfering .as file and start confirmation
		print(tc.read_until(b"Confirm !").decode("ascii"))
		tc.write(b'\r\n')
		print(tc.read_until(b"E\x17").decode("ascii"))
		tc.write(b'\x02' + b'E    0' + b'\x17')
		#Read until command prompt and continue
		print(tc.read_until(b">").decode("ascii"))
	else: print("File not found")

def power_on_and_off(tc):
	for command in ["zpow on", "zpow off"]:
		tc.write(command.encode() + b"\r\n")
		print (tc.read_until(b">").decode("ascii"))
		time.sleep(4)

def abort_kill_all(tc):
	for command in ["pcabort", "pckill\r\n1", "abort", "kill\r\n1"]:
		tc.write(command.encode() + b"\r\n")
		print (tc.read_until(b">").decode("ascii"))

def get_kawa_status(tc):
	tc.write(b"status\r\n")
	return tc.read_until(b">").decode("ascii")

def get_kawa_position(tc):
	tc.write(b"where\r\n")
	time.sleep(0.02)
	return tc.read_very_eager().decode("ascii")
	#return tc.read_until(b">").decode("ascii")

def get_kawa_error(tc):
	tc.write(b"errlog\r\n")
	return tc.read_until(b">").decode("ascii")

def get_kawa_id(tc):
	tc.write(b"ID\r\n")
	return tc.read_until(b">").decode("ascii")

def status_to_protocol_msg(tc, STATUS):
	robot_status = (STATUS.find("Robot status:"))
	environment = (STATUS.find("Environment:"))
	stepper_status = (STATUS.find("Stepper status:"))

	drives_powered  = STATUS[robot_status:environment].find("Motor power OFF")        == -1
	in_error        = STATUS[robot_status:environment].find("During error condition") != -1
	in_motion       = STATUS[robot_status:environment].find("Now moving program")     != -1

	if STATUS[robot_status:environment].find("REPEAT mode") != -1:
		mode = "Repeat_mode"
	else: mode = "Teach_mode"

	if in_error == False:
		error_code = None
	else:
		# get errorcode with errlog
		ERRORLOG = get_kawa_error(tc)
		error_code = ERRORLOG[ERRORLOG.find(" (E")+2: ERRORLOG.find(" (E")+7]

	if drives_powered == True and in_error == False and mode == "Repeat_mode":
		motion_possible = True
	else: motion_possible = False

	e_stopped = None

	#print(drives_powered, e_stopped, error_code, in_error, in_motion, mode, motion_possible)

	status_message = ("|13|" + str(drives_powered) + '|' + str(e_stopped) + '|' + str(error_code) + '|' + 
		str(in_error) + '|' + str(in_motion) + '|' + str(mode) + '|' + str(motion_possible) + "|0x03")

	status = ('0x02|0x01|' + str(len(status_message)) + status_message)
	return status


def is_motion_possible(tc, STATUS):
	robot_status = (STATUS.find("Robot status:"))
	environment = (STATUS.find("Environment:"))

	drives_powered  = STATUS[robot_status:environment].find("Motor power OFF")        == -1
	in_error        = STATUS[robot_status:environment].find("During error condition") != -1

	if STATUS[robot_status:environment].find("REPEAT mode") != -1:
		mode = "Repeat_mode"
	else: mode = "Teach_mode"

	if drives_powered == True and in_error == False and mode == "Repeat_mode":
		motion_possible = True
	else: motion_possible = False

	return motion_possible

def position_to_protocol_msg(WHERE):
	jt6 = WHERE.find("JT6")
	Xmm = WHERE.find("X[mm]")
	
	joints = WHERE[jt6+3:Xmm-4]
	joints = " ".join(joints.split()).replace(" ", "|")

	joint_position = ("0x02|0x01|" + str(len(joints)+len("|0x03")) + "|10|" + joints + "|0x03")
	return joint_position

def id_to_robot_type_msg(ID):
	name = ID.find("Robot name:")
	axis = ID.find("Num of axes")
	robot_type = ID[name:axis-1]
	return robot_type