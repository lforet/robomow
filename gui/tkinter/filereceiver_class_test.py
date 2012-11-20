from FileReceiver import *
from threading import *
import time

s = FileReceiver()
#line below stops thread when main program stops
s.daemon = True
s.start()

for i in range (10):
	print i
	time.sleep(1)

