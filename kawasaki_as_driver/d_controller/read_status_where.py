from telnet_commands import get_status_position
import telnetlib, time, sys, os, telnet_commands

HOST = '127.0.0.1'
# PORT = 9105 # <= D+ controller
PORT = 10000 # > D+ controller
user = 'as'

try:
	tc = telnet_commands.log_in(HOST, PORT, user)
	start = time.time()
	i=0
	while (time.time()-start) < 20:
		status_position = get_status_position(tc)
		print(status_position)
		i+=1
		time.sleep(0.05)
except KeyboardInterrupt: print('interrupted!')
except: print("Unexpected error:", sys.exc_info())

print("Received status and position with: ", i/(time.time()-start))
print("Disconnecting")
tc.close()