# Echo client program
import socket
import time


HOST = '127.0.0.1'    # The remote host
PORT = 50008              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = 0

#try n times to connect
for i in range(10):  
    try:
        s.connect((HOST, PORT))
        print "connected with server..."
        connected = 1
        break
    except IOError as detail:
      print "No server to connect to...", detail[0], detail [1]
      time.sleep(1)

#send 10 heartbeat signals or could just keep s.connect every 1 second
if connected == 1:
    while 1:  
        try:
            s.send('sending Heartbeat signal...')
            data = s.recv(1024)
            if data <> "":
                print 'Received and ACK from server...', repr(data)
            else:
                print "ACK not received from server"
                break
            print s.getpeername(), s.family, s.proto, s.type
            time.sleep(1)
        except IOError as detail:
            print detail
            break
        #except IOError as detail:
        #  print "No server to connect to...", detail[0], detail [1]
        #  break
else:
    print "Tried but never reached server..."
    
try:
    print "closing Socket"
    s.close()
except NameError as detail:
    print "No socket to close", detail

