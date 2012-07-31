import serial
import sys, time

PORT = "/dev/ttyUSB0"

if len(sys.argv) > 1:
    PORT = sys.argv[1]

ser = serial.Serial(PORT, 9600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, timeout=1,  dsrdtr=False, xonxoff=False, rtscts=False)


print ser.name,
print ser.baudrate,
print ser.bytesize,
print ser.parity,
print ser.stopbits,
print ser.dsrdtr

while 1:
    print "Trying to connect..."
    time.sleep(.2)
    #ser.write("r")      # write a string
    #time.sleep(.05)
    #s = ser.read()
    s = ser.readline()
    #print s
    if len(s) > 0: break

#s = ser.read(100)       # read up to one hundred bytes
#
while 1:
    s = ser.readline()
    print "recieved from arduino: ", s
    if len(s) < 1: break
    if ser.isOpen():
        print "Connected..."

                        # or as much is in the buffer
#print s
ser.close()             # close port
if not ser.isOpen():
    print "Not Connected..."
ser.close()             # close port

