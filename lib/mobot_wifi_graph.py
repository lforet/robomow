import matplotlib.pyplot as plt
import numpy as np
import time
import thread
import math
import random
from mobot_wifi_consume import *
from matplotlib import mpl
import sys

import matplotlib.colors as mcolors

def drange(start, stop, step):
		r = start
		while r < stop:
			yield r
			r += step

def closest(target, collection):
    return min((abs(target - i), i) for i in collection)[1]

def calculate_color(val):
	#R=(255*val)/100
	R=(255*(100-val))/100;
	#G=(255*(100-val))/100; 
	G=(255*val)/100
	B=0
	#print R,G,B
	to_return = [normalize_val(R, 0, 255),normalize_val(G, 0, 255),B]
	return to_return

def normalize_val(val, floor, ceiling):
		return float (int(((float(val) - floor) / ceiling) * 100)) / 100

def calculate_color2(val):
	temp = int(translate(val, 0, 80, 0, 4))
	color = []
	n = 5

	R = (1.0 - (0.25 * temp))
	G = (0.25 * temp)
	B = 0
	color = [R,G,B]
	#print 'val:', val, '   temp:', temp, '   color:', color
	return color
		
def translate(sensor_val, in_from, in_to, out_from, out_to):
    out_range = out_to - out_from
    in_range = in_to - in_from
    in_val = sensor_val - in_from
    val=(float(in_val)/in_range)*out_range
    out_val = out_from+val
    return out_val

def animate():


	n= 100
	# http://www.scipy.org/Cookbook/Matplotlib/Animations
	x = []
	y = [0] * 100
	for i in range(n):
		x.append(i)
	cdict = {'red':   ((0.0, 1.0, 1.0),
		               (1.0, 0.0, 0.0)),

		     'green': ((0.0, 0.0, 0.0),
		               (1.0, 1.0, 1.0)),

		     'blue':  ((0.0, 0.0, 0.0),
		               (1.0, 0.0, 0.0))
		    }
	cmap = mcolors.LinearSegmentedColormap('my_colormap', cdict, 5)
	#cmap = mpl.cm.cool
	#norm = mpl.colors.Normalize(vmin=100, vmax=0)
	#bounds = [0, 25, 50, 75, 100]
	#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	cax = ax.imshow((x,y), cmap=cmap)	
	cbar = fig.colorbar(cax, orientation='vertical')

	wifi = consume_wifi('wifi.1', '192.168.1.180')

	while True:
		time.sleep(.2)
		y = y[1:]
		
		signal_value = wifi.signal_strength
		print signal_value 

		try:
			val = int(wifi.signal_strength)		
			if val < 0: val = 0
			#print val
		except:
			val = 0
			#val = random.randint(0,100)
			pass
		y.append(val)
		
		plt.cla()
		plt.xticks(xrange(0,100,10))#, endpoint=True))
		plt.yticks(xrange(0,100,10))#, endpoint=True))
		plt.xlabel('10 seconds')
		plt.ylabel('Strength')
		plt.grid(True)
		plt.ylim([0,100])
		plt.xlim([0,100])
		plt.grid(True)
		#from mpl_toolkits.axes_grid1 import make_axes_locatable
		#divider = make_axes_locatable(plt.gca())
		#cax = plt.append_axes("right", "5%", pad="3%")
		#cbar = plt.colorbar(fig, orientation='vertical')
		#plt.tight_layout()
		colors = []
		#print y
		for i in range(len(x)):
			#colors.append(calculate_color(y[i]))
			colors.append(calculate_color2(y[i]))
		print val , colors[99]
		 
		plt.bar(x , y, 1, color=colors)
		fig.canvas.draw()
		#raw_input('ll')

#print int(translate(100, 0, 255, 1, 5))
#sys.exit()


fig, ax = plt.subplots(1,1,1,dpi=60)

win = fig.canvas.manager.window
win.after(10, animate)
plt.show ()

