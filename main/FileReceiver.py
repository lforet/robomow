# USAGE: python FileReciever.py

import socket, time, string, sys, urlparse
from threading import *

#------------------------------------------------------------------------

class FileReceiver ( Thread ):

    def __init__( self, command_port, data_port ):
        Thread.__init__( self )
	self.cmd_port = command_port
	self.data_port = data_port

	
    def run(self):
        self.process()

    def bindmsock( self ):
        self.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msock.bind(('', self.data_port))
        self.msock.listen(2)
		#self.msock.settimeout(2)
        print '[Media] Listening on port ', self.data_port

    def acceptmsock( self ):
        self.mconn, self.maddr = self.msock.accept()
        print '[Media] Got connection from', self.maddr
    
    def bindcsock( self ):
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csock.bind(('', self.cmd_port))
        self.csock.listen(2)
        #self.csock.settimeout(2)
        print '[Control] Listening on port ', self.cmd_port

    def acceptcsock( self ):
        self.cconn, self.maddr = self.csock.accept()
        print '[Control] Got connection from', self.maddr
        
        while 1:
            data = self.cconn.recv(1024)
            if not data: break
            if data[0:4] == "SEND": self.filename = data[5:]
            print '[Control] Getting ready to receive "%s"' % self.filename
            break

    def transfer( self ):
        print '[Media] Starting media transfer for "%s"' % self.filename

        f = open(self.filename,"wb")
        while 1:
            data = self.mconn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print '[Media] Got "%s"' % self.filename
        print '[Media] Closing media transfer for "%s"' % self.filename
    
    def close( self ):
        self.cconn.close()
        self.csock.close()
        self.mconn.close()
        self.msock.close()

    def process( self ):
        while 1:
            try:
		        self.bindcsock()
		        #time.sleep(1)
		        self.acceptcsock()
		        #time.sleep(1)
		        self.bindmsock()
		        #time.sleep(1)
		        self.acceptmsock()
		        #time.sleep(1)
		        self.transfer()
		        #time.sleep(1)
		        self.close()
		        time.sleep(.1)
            except:
                print "file xfer failed"
                self.close()
                time.sleep(.2)
                pass
#------------------------------------------------------------------------

#s = StreamHandler()
#s.start()
