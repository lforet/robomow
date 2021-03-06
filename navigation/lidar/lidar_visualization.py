

from lidar_class import *
import time
from visual import *




#setup the window, view, etc
scene.forward = (1, -1, 0)
scene.background = (0.1, 0.1, 0.2)
scene.title = "ProtoX1 Lidar Distance"

class grid:
    """A graphical grid, with two level of subdivision.

    The grid can be manipulated (moved, showed/hidden...) by acting on self.frame.
    """
    
    def __init__(self, size=100, small_interval=10, big_interval=50):
        self.frame = frame(pos=(0,0,0))
        for i in range(-size, size+small_interval, small_interval):
            if i %big_interval == 0:
                c = color.gray(0.65)
            else:
                c = color.gray(0.25)
            curve(frame=self.frame, pos=[(i,0,size),(i,0,-size)], color=c)
            curve(frame=self.frame, pos=[(size,0,i),(-size,0,i)], color=c)

#grid where major intervals are 1m, minor intervals are 10cm
my_grid = grid(size=4000, small_interval = 100, big_interval=1000)
my_grid.frame.pos.y=-5

while True:
	rate(60) # synchonous repaint at 60fps
	if scene.kb.keys: # event waiting to be processed?
		s = scene.kb.getkey() # get keyboard info
		if s == "q": # stop motor
		    sys.exit(-1)
