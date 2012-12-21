# Echo server program
import socket
import time
import math

HOST = ''                 # Symbolic name meaning the local host
PORT = 8095             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
#next line spcifies how long in seconds to wait for a connection
#s.settimeout(5.0)

def read_line(s):
    ret = ''

    while True:
        c = s.recv(1)

        if c == '\n' or c == '':
            break
        else:
            ret += c

    return ret
    

print "listening..."
s.listen(1)
print "made connection..."

try:
    print "waiting to accept.."
    conn, addr = s.accept()
    print "accepted connection from client.."
    while conn <> "":
        s.listen(1)
        #print time.time()
        #print s.gettimeout()
        print 'Connected by', addr
        #data = conn.recv(1024)
        data = read_line(conn)
        data1 = data.split(',')
        #if not data: break
        #print 'Received from remote: ', data 
        if len(data1) > 0 : print "data1:", data1
        #conn.send("ACK")
        try:
            compass = math.degrees(float(data1[11]))
            if compass < 0: compass = compass + 360
            print "compass:", round(compass)
        except:
            pass
        #time.sleep(.1) 
    
except IOError as detail:
    print "connection lost", detail

try:
    print "closing Socket"
    s.close()
except NameError as detail:
    print "No socket to close", detail
