from telnet_commands import get_kawa_status, get_kawa_position, get_kawa_error, status_to_protocol_msg
import telnetlib, time, sys, os, telnet_commands

HOST = '127.0.0.1'
# PORT = 9105 # <= D+ controller
PORT = 10000 # > D+ controller
user = 'as'
i=0	


try:
	tc = telnet_commands.log_in(HOST, PORT, user)
	i = 0
	start = time.time()
	while tc:
		STATUS = get_kawa_status(tc)
		status = status_to_protocol_msg(tc, STATUS)
		print(status)
		i+=1

except KeyboardInterrupt: print('interrupted!')
except: print("Unexpected error:", sys.exc_info())

print("Received status and position with: ", i/(time.time()-start))
print("Disconnecting")
tc.close()