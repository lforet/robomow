from robomow_motor_class_arduino import *


motor1 = robomow_motor()
print motor1.stats()

print motor1.isInitialized


for i in xrange(0, 110, 10):
	print motor1.forward(i)
	time.sleep(.05)
	print " engine at speed: ", i, '%'

print motor1.lmotor_speed
