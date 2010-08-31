
"""
Python provides a standard module called ‘pickle’. This is an amazing module that can take almost any Python object (even some forms of Python code!), and convert it to a string representation; this process is called pickling. Reconstructing the object from the string representation is called unpickling. Between pickling and unpickling, the string representing the object may have been stored in a file or data, or sent over a network connection to some distant machine. 
"""

import pickle

# We'll pickle a list of numbers:
someList = [ 1, 2, 7, 9, 0, 1, 2,9, 2 ]
print someList
pickledList = pickle.dumps ( someList )
print "the pickled lists = ", pickledList
print "the unpickled list = ",  pickle.loads(pickledList)
