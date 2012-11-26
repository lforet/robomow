import geopy
from geopy.distance import VincentyDistance

# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
lat1 = 33.466582
#lat2 = 53.31861111111111
lon1 = -86.824076
#lon2 = -1.6997222222222223

b=90
d=.001 # 1 meter

origin = geopy.Point(lat1, lon1)

destination = VincentyDistance(kilometers=d).destination(origin, b)

lat2, lon2 = destination.latitude, destination.longitude
print "new lat long:", lat2,lon2

