#!/usr/bin/env python

import os
from img_processing_tools import *
import Image 
import time
import csv
import numpy as np
import milk
from mvpa.clfs.knn import kNN
from mvpa.datasets import Dataset
import mlpy
import matplotlib.pyplot as plt # required for plotting

ifile  = open('mower_image_data.csv', "rb")
reader = csv.reader(ifile)

classID = []
features = []
lbp= []
lbp_temp_array = []
i3_histo_temp_array = []
i3_histo = []
rgb_histo_temp_array = []
rgb_histo = []

#read data from file into arrays
for row in reader:
    features.append(row)
'''
I3_sum =    ImageStat.Stat(image).sum
		I3_sum2 =   ImageStat.Stat(image).sum2
		I3_median = ImageStat.Stat(image).median
		I3_mean =   ImageStat.Stat(image).mean
		I3_var =    ImageStat.Stat(image).var
		I3_stddev = ImageStat.Stat(image).stddev
		I3_rms =    ImageStat.Stat(image).rms
'''

#print features[1][1]
#stop


for row in range(1, len(features)):
	#print features[row][1]
	classID.append(int(features[row][0]))
	lbp_temp_array.append(features[row][1].split(" "))
	i3_histo_temp_array.append(features[row][2].split(" "))
	rgb_histo_temp_array.append(features[row][3].split(" "))


#removes ending element which is a space
for x in range(len(lbp_temp_array)):
		lbp_temp_array[x].pop()
		lbp_temp_array[x].pop(0)
		i3_histo_temp_array[x].pop()
		i3_histo_temp_array[x].pop(0)
		rgb_histo_temp_array[x].pop()
		rgb_histo_temp_array[x].pop(0)

#print lbp_temp_array
#convert all strings in array to numbers
temp_array = []
for x in range(len(lbp_temp_array)):
	temp_array = [ float(s) for s in lbp_temp_array[x] ]
	lbp.append(temp_array)
	temp_array = [ float(s) for s in i3_histo_temp_array[x] ]
	i3_histo.append(temp_array)
	temp_array = [ float(s) for s in rgb_histo_temp_array[x] ]
	rgb_histo.append(temp_array)

#make numpy arrays
lbp = np.asarray(lbp)
i3_histo = np.asarray(i3_histo)
rgb_histo = np.asarray(rgb_histo)

id_index = 15
lbp_predictdata = lbp[[id_index]]
i3_histo_predictdata = lbp[[id_index]]

print
#print predictdata
print classID[id_index]
#print "len lbp:", len(lbp)
#print "shape:", lbp.shape

#mvpa
lbp_training = Dataset(samples=lbp,labels=classID)
i3_histo_training = Dataset(samples=lbp,labels=classID)
clf = kNN(k=1, voting='majority')
print "clf = ", clf
clf.train(lbp_training)
lbp_predicted_classID =  clf.predict(lbp_predictdata)
clf.train(i3_histo_training)
i3_histo_predicted_classID =  clf.predict(i3_histo_predictdata)



print "lbp_predicted_classID: ", lbp_predicted_classID 
print "i3_histo__predicted_classID :", i3_histo_predicted_classID
#if predicted_classID[0]  == 1.0: print "Image is of class: GRASS"
#if predicted_classID[0]  == 2.0: print "Image is of class: DIRT/GRAVEL"
#if predicted_classID[0]  == 3.0: print "Image is of class: CEMENT/ASPHALT"

#mlpy
#Diagonal Linear Discriminant Analysis.
from numpy import *
from mlpy import *
xtr2 = np.array([[1.1, 2.4, 3.1, 1.0],  # first sample
             [1.2, 2.3, 3.0, 2.0],  # second sample
             [1.3, 2.2, 3.5, 1.0],  # third sample
             [1.4, 2.1, 3.2, 2.0]]) # fourth sample

ytr2 = np.array([1, -1, 1, -1])
xts2 = np.array([[4.0, 5.0, 6.0, 7.0]])   # test point


#ytr = array([1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
xtr = lbp
ytr = np.array(classID)
print 
print "----------------------------"
print
#print xtr2.shape, xtr.shape
#print ytr2.shape, ytr.shape

#ytr = classID         # classes
#print lbp
print classID
#print xtr
print 
print "----------------------------"
print
print ytr

#print xtr2
#print type(lbp_predictdata[0][0])
#print type(xtr2[0][0])

xts = np.array([lbp_predictdata[0]])   # test point
print "np.shape(xts), xts.ndim, xts.dtype:", np.shape(xts), xts.ndim, xts.dtype

print 
print "----------------------------"
print

myknn = mlpy.Knn(k=1)
myknn.compute(xtr,ytr)
print "knn: ", myknn.predict(xts)
print "correct class:", classID[id_index]

mypda = mlpy.Pda()
mypda.compute(xtr,ytr)
print "pda: ", mypda.predict(xts)
print "correct class:", classID[id_index]


#print np.shape(xtr), xtr.ndim, xtr.dtype
#print np.shape(ytr), ytr.ndim, ytr.dtype
#print np.shape(xts), xts.ndim, xts.dtype

#milk
#Help on function feature_selection_simple in module milk.supervised.defaultlearner:

#selector = feature_selection_simple()

learner = milk.defaultclassifier(mode='medium', multi_strategy='1-vs-1', expanded=False)
model = learner.train(xtr, ytr)
print "milk: ", model.apply(xts[0])


from sklearn.externals import joblib
joblib.dump(model, 'saved_model.pkl') 
model2 = joblib.load('saved_model.pkl') 
print "milk: ", model2.apply(xts[0])

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(leaf_size=30, n_neighbors=5, p=2,
           warn_on_equidistant=True, weights='distance')

model3 = knn.fit(xtr, ytr)
print "knn sclearn: ", model3.predict(xts)
joblib.dump(model3, 'lbp_knn_clf.pkl')

#print" feature ranking"
#myrank = Ranking()                 # initialize ranking class
#mysvm = Svm()                      # initialize svm class
#print myrank.compute(xtr, ytr, mysvm) 

