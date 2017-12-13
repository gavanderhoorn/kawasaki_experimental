.PROGRAM ros_init_queue () ; 
  size = 20
  front = 0
  rear = 0
  active = 1
.END
.PROGRAM ros_send_server()
$send_state = "0, initiating"
.send_port = 11111
.send_msgs_per_sec = 0.5
.buf_n = 1
.tout = 0.1
  
; WHILE active == 1 DO
  $send_state = "1, connecting"
  print $send_state
  CALL open_socket(.send_port, .send_sock_id)
  PRINT "\n Kawasaki can start sending poses on port: ", .send_port
  
  $send_state = "2, Sending current pose"
  PRINT $send_state
  WHILE active == 1 DO
    CALL encode_ros_pose(.$pose)
    .$send_buf[1] = .$pose
    tcp_send .ret, .send_sock_id, .$send_buf[1], .buf_n, .tout
    TWAIT .send_msgs_per_sec
  END
$send_state = "3, Closing send server"  
PRINT "Closing send server"
CALL close_socket(.send_port, .send_sock_id)
; END
.END
.PROGRAM ros_recv_server () ; 
$recv_state = "0, initiating"
.recv_port = 11112
.recv_msgs_per_sec = 0.1
.timeout_recv = 0.01
.max_length = 255
.num = 0
  
;WHILE active == 1 DO
  $recv_state = "1, connecting"
  print $recv_state
  CALL open_socket(.recv_port, .recv_sock_id)
  PRINT "\n Kawasaki can start receiving poses on port: ", .recv_port
  $recv_state = "2, receiving and queueing"
  WHILE active == 1 DO
    tcp_recv .ret, .recv_sock_id, .$recv_buff[1], .num, .timeout_recv, .max_length
    IF .ret == 0 THEN
      print "received msg"
      .$msg = .$recv_buff[1]
      print "decoding msg"
      CALL decode_ros_pose(.$msg, .joint1, .joint2, .joint3, .joint4, .joint5, .joint6, .header)
      print "inserting into queue"
      WAIT NOT (front == 0 AND rear == size -1) AND NOT (front == rear + 1)
      CALL queue_insert(.header, .joint1, .joint2, .joint3, .joint4, .joint5, .joint6)
    END
    TWAIT .recv_msgs_per_sec  
  END
  
  $recv_state = "3, Closing recv server"  
  PRINT "Closing recv server"
  CALL close_socket(.recv_port, .recv_sock_id)
;END
.END
.PROGRAM ros_move_kawa()
CP ON
SPEED 10 ALWAYS
ACCURACY 200 ALWAYS
while active == 1 DO
  if not front == 0 THEN
    POINT .#pos = #PPOINT(queue[front,2], queue[front,3], queue[front,4], queue[front,5], queue[front,6], queue[front,7])
    JMOVE .#pos
    CALL queue_del
  ELSE
    TWAIT 0.1
  END
END
.END
.PROGRAM open_socket (.port,.sockid) ; 
  
PRINT "Listening on port: ", .port

begin:
TCP_LISTEN .ret, .port
IF .ret <0 THEN
  TWAIT 0.1
  GOTO begin
END
  
accept:
TCP_ACCEPT .sockid, .port, 1
TCP_END_LISTEN .ret, .port

IF .sockid < 0 THEN
  GOTO begin
  TWAIT 0.1
END

print "Connected on port:", .port
.END
.PROGRAM close_socket (.port, .sockid) ;
  
PRINT "closing sockid: ", .sockid
tcp_close ret, .sockid
IF ret < 0 THEN
  PRINT "TCP_close error", $ERROR (ret)
  tcp_close ret1, .sockid
  IF ret1 < 0 THEN
    PRINT "TCP_CLOSE error id=", .sockid
  END
ELSE
  PRINT "TCP_CLOSE OK id =", .sockid
  
END
TCP_END_LISTEN ret, .port
IF ret < 0 THEN
  PRINT "Stop listen error port= ", .port
ELSE
  PRINT "Stopped listening OK port= ", .port
END
exit:
.END
.PROGRAM encode_ros_pose (.$pose) ; 
HERE .#CP
DECOMPOSE .CP[0] = .#CP
.$S = "|"
.$pose = $CHR (2) + $ENCODE (/L, .$S, .CP[0], .$S, .CP[1], .$S, .CP[2], .$S, .CP[3], .$S, .CP[4], .$S, .CP[5], .$S) + $CHR (3) + $CHR (10)
.END
.PROGRAM decode_ros_pose (.$msg,.joint1,.joint2,.joint3,.joint4,.joint5,.joint6,.header) ; 
.$header = $DECODE (.$msg, $CHR (2) + "|", 1)
.$header = $DECODE (.$msg, "|", 0)
; print "header: ",.$header
.$joint1 = $DECODE (.$msg, "|", 1)
.$joint1 = $DECODE (.$msg, "|", 0)
.joint1 = VAL (.$joint1)
; PRINT "joint1: ", .joint1
.$joint2 = $DECODE (.$msg, "|", 1)
.$joint2 = $DECODE (.$msg, "|", 0)
.joint2 = VAL (.$joint2)
; PRINT "joint2: ",.joint2
.$joint3 = $DECODE (.$msg, "|", 1)
.$joint3 = $DECODE (.$msg, "|", 0)
.joint3 = VAL (.$joint3)
; PRINT "joint3: ",.joint3
.$joint4 = $DECODE (.$msg, "|", 1)
.$joint4 = $DECODE (.$msg, "|", 0)
.joint4 = VAL (.$joint4)
; PRINT "joint4: ",.joint4
.$joint5 = $DECODE (.$msg, "|", 1)
.$joint5 = $DECODE (.$msg, "|", 0)
.joint5 = VAL (.$joint5)
; PRINT "joint5: ",.joint5
.$joint6 = $DECODE (.$msg, "|", 1)
.$joint6 = $DECODE (.$msg, "|", 0)
.joint6 = VAL (.$joint6)
; PRINT "joint6: ", .joint6
.$footer = $DECODE (.$msg, "|", 1)
.$footer = $DECODE (.$msg, "|", 0)
; PRINT "footer:", .$footer
.END
.PROGRAM queue_insert (.header, .joint1, .joint2, .joint3, .joint4, .joint5, .joint6) ;
  
;Queue is full
IF front == 1 AND rear == size -1 OR front == rear + 1 THEN
  print "Queue is full\n"
  GOTO add_queue
END
;if queue is empty
IF rear == 0 THEN
  rear = rear + 1
  front = front + 1
  print "Queue was empty\n"
  GOTO add_queue
END
;if rear is past at max size start at front
IF rear == size - 1 AND front > 1 THEN
  rear = 1
  print "Queue is looped\n"
  goto add_queue
ELSE
  rear = rear + 1
  print "Queue is normal\n"
  goto add_queue
END
  
add_queue:
; queue[rear, 1] = .header
queue[rear, 2] = .joint1
queue[rear, 3] = .joint2
queue[rear, 4] = .joint3
queue[rear, 5] = .joint4
queue[rear, 6] = .joint5
queue[rear, 7] = .joint6
print "Added to queue"
print "front:", front, "rear:", rear
  
.END
.PROGRAM queue_del ()
; Queue is empty
if front == 0 THEN
  print "Queue is empty "
  GOTO exit
END
; Queue has one object, delete and reset
if front == rear AND front != 0 THEN
  front =  0
  rear =  0
  print "Queue has one object"
  GOTO exit
END
; Front is at the end of loop, return to begin value
if front == size - 1 THEN
  front = 1
  print "loop front of queue"
  GOTO exit
ELSe
  front = front + 1
  print "just move front"
  GOTO exit
END
exit:
print "front:", front, "rear:", rear
.END
.PROGRAM T_close_sockets () ; 
  ; *******************************************************************
  ;
  ; Program:      close_sockets
  ; Comment:      
  ; Author:       Guus
  ;
  ; Date:         12/6/2017
  ;
  ; *******************************************************************
  ;
.send_port = 11111
.recv_port = 11112  
  CALL close_socket(.send_port, send_sock_id)
  CALL close_socket(.recv_port, recv_sock_id)
.END
.PROGRAM T_stop_listenR () ; 
  ; *******************************************************************
  ;
  ; Program:      close_sockets
  ; Comment:      
  ; Author:       Guus
  ;
  ; Date:         12/6/2017
  ;
  ; *******************************************************************
  ;
.send_port = 11111
.recv_port = 11112  
TCP_END_LISTEN ret, .recv_port
IF ret < 0 THEN
  PRINT "Cant stop listening= ", .recv_port
ELSE
  PRINT "Stopped listening on port= ", .recv_port
END
.END
.PROGRAM T_stop_listenS () ; 
  ; *******************************************************************
  ;
  ; Program:      close_sockets
  ; Comment:      
  ; Author:       Guus
  ;
  ; Date:         12/6/2017
  ;
  ; *******************************************************************
  ;
.send_port = 11111
.recv_port = 11112  
TCP_END_LISTEN ret, .send_port
IF ret < 0 THEN
  PRINT "Cant stop listening= ", .send_port
ELSE
  PRINT "Stopped listening on port= ", .send_port
END
.END
.PROGRAM Comment___ () ; Comments for IDE. Do not use.
	; @@@ PROJECT @@@
	; @@@ HISTORY @@@
	; @@@ INSPECTION @@@
	; @@@ PROGRAM @@@
	; 0:ros_init_queue
	; 0:ros_send_server
	; 0:ros_recv_server
	; 0:ros_move_kawa
	; 0:open_socket
	; 0:close_socket
	; 0:encode_ros_pose
	; 0:decode_ros_pose
	; 0:queue_insert
	; 0:queue_del
	; 0:T_close_sockets
	; 0:T_stop_listenR
	; 0:T_stop_listenS
	; @@@ TRANS @@@
	; @@@ JOINTS @@@
	; @@@ REALS @@@
	; @@@ STRINGS @@@
	; @@@ INTEGER @@@
	; @@@ SIGNALS @@@
	; @@@ TOOLS @@@
	; @@@ BASE @@@
	; @@@ FRAME @@@
	; @@@ BOOL @@@
.END