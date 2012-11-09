#!/usr/bin/env python


from maxsonar_class import *
import time
import re

sensor1 = MaxSonar()

while 1:
	data  = str(sensor1.distances_cm())
	if len(data) > 1:
		print "data=", data
		#s1_data = re.search('s1', data)
		#print s1_data.span()
		s1_data = data[(data.find('s1:')+3):(data.find('s2:'))]
		s2_data = data[(data.find('s2:')+3):(data.find('s3:'))]
		s3_data = data[(data.find('s3:')+3):(data.find('s4:'))]
		s4_data = data[(data.find('s4:')+3):(data.find('s5:'))]
		s5_data = data[(data.find('s5:')+3):(len(data)-1)]
		print s1_data, s2_data, s3_data, s4_data, s5_data 
	time.sleep(.1)

