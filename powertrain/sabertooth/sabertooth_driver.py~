#!/usr/bin/python
import serial
import time

PORT = "/dev/ttyUSB0"

#if len(sys.argv) > 1:
#    PORT = sys.argv[1]

ser = serial.Serial(PORT, 9600, timeout=1)

print ser.portstr,
print ser.baudrate,
print ser.bytesize,
print ser.parity,
print ser.stopbits

print ser

print "sending command"
time.sleep(1)

for i in xrange(80, 127, 1):
	ser.write (chr(int(hex(i),16)))
	time.sleep (.3)
	percent = i/127.0
	print i, " engine at speed: ", percent*100, '%'
time.sleep(5)
for i in xrange(127, 65, -1):
	ser.write (chr(int(hex(i),16)))
	time.sleep (.2)
	percent = i/127.0
	print i, " engine at speed: ", percent*100, '%'
ser.write (chr(int(hex(0),16)))
print "closing port"
time.sleep(2)
print 'port closed'
ser.close() 
print hex(127)
print chr(0x50)

