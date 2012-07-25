from robomow_motor_class import *


motor1 = robomow_motor("/dev/ttyUSB0")
print motor1.stats()

print motor1.isInitialized


for i in xrange(0, 110, 10):
	print motor1.reverse(i)
	time.sleep(.05)
	print " engine at speed: ", i, '%'

print i
