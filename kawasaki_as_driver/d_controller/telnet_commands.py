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
	for command in ["pcabort", "pckill\r\ny", "abort", "kill\r\ny"]:
		tc.write(command.encode() + b"\r\n")
		print (tc.read_until(b">").decode("ascii"))

def get_status_position(tc):
	tc.write(b"status\r\n")
	tc.write(b"where\r\n")
	time.sleep(0.001)
	return tc.read_very_eager().decode("ascii")