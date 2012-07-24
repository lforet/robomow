"""
Computing the distance between two locations on Earth from coordinates

The following code returns the distance between to locations based on each point's longitude and latitude. The distance returned is relative to Earth's radius. To get the distance in miles, multiply by 3960. To get the distance in kilometers, multiply by 6373.

Latitude is measured in degrees north of the equator; southern locations have negative latitude. Similarly, longitude is measured in degrees east of the Prime Meridian. A location 10 west of the Prime Meridian, for example, could be expressed as either 350 east or as -10 east.
"""

import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc


print distance_on_unit_sphere(33.5206, 86.8025, 30.2139, 92.0294) * 3960


