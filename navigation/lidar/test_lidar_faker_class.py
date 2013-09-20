
import lidar_faker_class
import time

lidar = lidar_faker_class.lidar_faker()
while True:	
	time.sleep(.05)
	print lidar.x_degree, lidar.y_degree, lidar.dist, lidar.quality, lidar.rpm
