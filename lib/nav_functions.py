import sys
sys.path.append( "/home/mobot/projects/robomow/lib/" )

from heapq import heappush, heappop # for priority queue
import math
import time
import random
from gps_functions import *
import simplekml


class node:
    xPos = 0 # x position
    yPos = 0 # y position
    distance = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate
    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        # d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return(d)

# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, num_of_directions, xA, yA, xB, yB):
	if num_of_directions == 4:
		 dx = [1, 0, -1, 0]
		 dy = [0, 1, 0, -1]
	elif num_of_directions == 8:
		 dx = [1, 1, 0, -1, -1, -1, 0, 1]
		 dy = [0, 1, 1, 1, 0, -1, -1, -1]
	closed_nodes_map = [] # map of closed (tried-out) nodes
	open_nodes_map = [] # map of open (not-yet-tried) nodes
	dir_map = [] # map of dirs
	row = [0] * n
	for i in range(m): # create 2d arrays
	  closed_nodes_map.append(list(row))
	  open_nodes_map.append(list(row))
	  dir_map.append(list(row))

	pq = [[], []] # priority queues of open (not-yet-tried) nodes
	pqi = 0 # priority queue index
	# create the start node and push into list of open nodes
	n0 = node(xA, yA, 0, 0)
	n0.updatePriority(xB, yB)
	heappush(pq[pqi], n0)
	open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

	# A* search
	while len(pq[pqi]) > 0:
	  # get the current node w/ the highest priority
	  # from the list of open nodes
	  n1 = pq[pqi][0] # top node
	  n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
	  x = n0.xPos
	  y = n0.yPos
	  heappop(pq[pqi]) # remove the node from the open list
	  open_nodes_map[y][x] = 0
	  closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

	  # quit searching when the goal is reached
	  # if n0.estimate(xB, yB) == 0:
	  if x == xB and y == yB:
		   # generate the path from finish to start
		   # by following the dirs
		   path = ''
		   while not (x == xA and y == yA):
		       j = dir_map[y][x]
		       c = str((j + num_of_directions / 2) % num_of_directions)
		       path = c + path
		       x += dx[j]
		       y += dy[j]
		   return path

	  # generate moves (child nodes) in all possible dirs
	  for i in range(num_of_directions):
		   xdx = x + dx[i]
		   ydy = y + dy[i]
		   if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
		           or the_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):
		       # generate a child node
		       m0 = node(xdx, ydy, n0.distance, n0.priority)
		       m0.nextMove(num_of_directions, i)
		       m0.updatePriority(xB, yB)
		       # if it is not in the open list then add into that
		       if open_nodes_map[ydy][xdx] == 0:
		           open_nodes_map[ydy][xdx] = m0.priority
		           heappush(pq[pqi], m0)
		           # mark its parent node direction
		           dir_map[ydy][xdx] = (i + num_of_directions / 2) % num_of_directions
		       elif open_nodes_map[ydy][xdx] > m0.priority:
		           # update the priority
		           open_nodes_map[ydy][xdx] = m0.priority
		           # update the parent direction
		           dir_map[ydy][xdx] = (i + num_of_directions / 2) % num_of_directions
		           # replace the node
		           # by emptying one pq to the other one
		           # except the node to be replaced will be ignored
		           # and the new node will be pushed in instead
		           while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
		               heappush(pq[1 - pqi], pq[pqi][0])
		               heappop(pq[pqi])
		           heappop(pq[pqi]) # remove the target node
		           # empty the larger size priority queue to the smaller one
		           if len(pq[pqi]) > len(pq[1 - pqi]):
		               pqi = 1 - pqi
		           while len(pq[pqi]) > 0:
		               heappush(pq[1-pqi], pq[pqi][0])
		               heappop(pq[pqi])       
		           pqi = 1 - pqi
		           heappush(pq[pqi], m0) # add the better node instead
	return '' # if no route found



def create_map(length, width, starting_pos):
	#starting_pos = lat, lon
	#n = 30 # horizontal size of the map
	#m = 30 # vertical size of the map
	the_map = []
	row = [[0,0]] * length
	for i in range(width): # create empty map
		the_map.append(list(row))

	#xB, yB = 4, 4 # destination
	#mobot starts in center of map
	xA, yA = int(width / 2), int(length / 2)
	lat1 = starting_pos[0]
	lon1 = starting_pos[1]
	the_map[xA][yA] = lat1, lon1
	print 'Map size (X,Y): ', width, length
	print 'Start: ', xA, yA, the_map[xA][yA]
	#print 'Finish: ', xB, yB
	#print the_map
	meters_left = int(width/2)
	meters_up = int(length / 2)
	pos_left = []
	pos_left =  destination_coordinates(lat1, lon1, 270, meters_left)
	print pos_left
	print lldistance((lat1, lon1), pos_left)
	pos_up = []
	pos_up = destination_coordinates(pos_left[0], pos_left[1], 0, meters_up)
	print pos_up
	print lldistance((lat1, lon1), pos_up)
	the_map[0][0] = pos_up
	#print the_map

	
	kml = simplekml.Kml()
	data_filename = "mobot_local_map.kml"
	f_handle = open(data_filename, 'w')
	f_handle.write('')
	f_handle.close()
	for y in range(width):
		for x in range(length):
			temp_posx = destination_coordinates(pos_up[0], pos_up[1], 90 , x)
			temp_posy = destination_coordinates(temp_posx[0], temp_posx[1], 180,y)
			the_map[y][x] = temp_posy
			name_str = "mobot" + str(x) + " " + str(y)
			kml.newpoint(name=(name_str), coords=[(temp_posy[1], temp_posy[0])])
			kml.save(data_filename)
	return the_map


	
def print_map(the_map, width, length):

		# display the map with the route added
		print 'Map:'
		for y in range(width):
			for x in range(length):
				xy = the_map[y][x]
				if xy == 0:
					 print '.', # space
				elif xy == 1:
					 print 'O', # obstacle
				elif xy == 2:
					 print 'S', # start
				elif xy == 3:
					 print 'R', # route
				elif xy == 4:
					 print 'F', # finish
			print



if __name__== "__main__":

	'''
	# fillout the map with a '+' pattern
	for x in range(width / 8, width * 7 / 8):
		 the_map[length / 2][x] = 1
	for y in range(length/8, length * 7 / 8):
		 the_map[y][width / 2] = 1
	'''

	#create map
	length = 10
	width = 10
	the_map = create_map(length, width, (33.5, -86.5))

	print the_map

	sys.exit(-1)


	#until current location = destination location
	currentx = xA
	currenty = yA
	#update map with starting and destination position
	the_map[yA][xA] = 2
	the_map[yB][xB] = 4
	arrived = False

	num_of_directions = 8 # number of possible directions to move on the map
	if num_of_directions == 4:
		 dx = [1, 0, -1, 0]
		 dy = [0, 1, 0, -1]
	elif num_of_directions == 8:
		 dx = [1, 1, 0, -1, -1, -1, 0, 1]
		 dy = [0, 1, 1, 1, 0, -1, -1, -1]

	while arrived == False:
	
		#place random obstacles
		for i in range(5):
			randx =random.randint(1,length-1)
			randy =random.randint(1,width-1)
			if the_map[randy][randx] == 0:
				#print "randx,randy", randx,randy
				the_map[randy][randx] = 1
		the_route = pathFind(the_map, length, width, num_of_directions, currentx, currenty, xB, yB)
		if len(the_route) > 0:
			print "route:", the_route
			j = int(the_route[0])
			currentx += dx[j]
			currenty += dy[j]
			the_map[currenty][currentx] = 3
		
			print_map(the_map, width, length)
		else:
			print "I have arrived..."
			arrived = True	

		raw_input('Press Enter...')




	'''
					self.latitude = (avg_latitude / (x*len(all_gps_list)))
					self.longitude = (avg_longitude / (x*len(all_gps_list)))
					#print "total sats:", self.active_satellites
					self.active_satellites = ( avg_active_satellites / (x*len(all_gps_list)))
					#time.sleep(1)
						print 'Avg latitude : ' , self.latitude, "   ", abs(self.latitude - gpss[n].fix.latitude)
						print 'Avg longitude: ' , self.longitude, "    ", abs(self.longitude - gpss[n].fix.longitude) 				
					print 'Avg Active Satellites: ' , self.active_satellites
			
					print "Distance: ", round((lldistance((self.latitude, self.longitude), (gpss[n].fix.latitude, gpss[n].fix.longitude)) * 3.28084), 4), " feet"
'''
