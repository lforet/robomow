import serial
import sys, time

PORT = "/dev/ttyACM0"

if len(sys.argv) > 1:
    PORT = sys.argv[1]

ser = serial.Serial(PORT, 9600, timeout=1)

print ser.portstr,
print ser.baudrate,
print ser.bytesize,
print ser.parity,
print ser.stopbits

'''
while 1:
    print "Trying to connect..."
    time.sleep(.1)
    ser.write("a")      # write a string
    time.sleep(.01)
    s = ser.readline()
    print  s
    #print ord(s)
    #if len(s) > 0: break

#s = ser.read(100)       # read up to one hundred bytes
#
print "break"

while 1:
    s = ser.readline()
    print "recieved from arduino: ", s
    time.sleep(.5)
    if len(s) < 1: break
    if ser.isOpen():
        print "Connected..."
'''
try:
	while True:
		print ser.write('z'.encode("ascii"))
		data = ser.readline().__repr__()
		if data:
			print "Received: %s." % data
		else:
			print "Looping."
except KeyboardInterrupt:
	print "Done."
except:
	raise
finally:
	ser.close()
	print "Closed port."


'''                        # or as much is in the buffer
#print s
ser.close()             # close port
if not ser.isOpen():
    print "Not Connected..."
ser.close()             # close port
'''
