#!/usr/bin/env python


from maxsonar_class import *
import time

sensor1 = MaxSonar()

while 1:
	print sensor1.distances_cm()
	time.sleep(.1)

