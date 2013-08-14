from mobot_lidar_class import *
import time

ml1 = mobot_lidar()
print ml1
#print ml1.ser
print dir(ml1)
time.sleep(3)
print ml1.ser
while True:
	print ml1.lidarData
	#gps2 = mobot_gps()
	#gps2.daemon=True
	#gps2.start()
	time.sleep(1)
