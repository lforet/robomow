from robomow_motor_class_arduino import *


motor1 = robomow_motor()
print "motor1.isConnected:", motor1.isConnected
#print motor1.com_stats()

while True:
	print motor1.motor_stats()
	time.sleep(.5)

'''
for x in range(2):
	print "forward"
	motor1.forward(100)
	time.sleep(1)
	print motor1.motor1_speed, motor1.motor2_speed
	print "rev"
	motor1.reverse(100)
	print motor1.motor1_speed, motor1.motor2_speed
	time.sleep(2)
	print "right"
	motor1.right(100)
	print motor1.motor1_speed, motor1.motor2_speed
	time.sleep(2)
	print "left"
	motor1.left(100)
	print motor1.motor1_speed, motor1.motor2_speed
	time.sleep(2)
	print "stop"
	motor1.stop()
	print motor1.motor1_speed, motor1.motor2_speed


for i in xrange(0, 101, 100):
	print "forward"
	print motor1.forward(i)
	time.sleep(1)
	print "l/r motors speeds: ", motor1.lmotor_speed, motor1.rmotor_speed 

	print "reverse"
	print motor1.reverse(i)
	time.sleep(1)
	print "l/r motors speeds: ", motor1.lmotor_speed, motor1.rmotor_speed

	print "left"
	print motor1.left(i)
	time.sleep(1)
	print "l/r motors speeds: ", motor1.lmotor_speed, motor1.rmotor_speed

	print "right"
	print motor1.right(i)
	time.sleep(1)
	print "l/r motors speeds: ", motor1.lmotor_speed, motor1.rmotor_speed 

	print "STOP"
	print motor1.stop()
	time.sleep(1)
	print "l/r motors speeds: ", motor1.lmotor_speed, motor1.rmotor_speed 
'''
