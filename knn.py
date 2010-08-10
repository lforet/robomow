#!/usr/bin/env python

import os
from PIL import Image
import sys
from optparse import OptionParser
import numpy as np
from numpy import *
from mvpa.clfs.knn import kNN
from mvpa.datasets import Dataset


#pymvpa stuff				
	f_handle = open("classdatafile.txt", 'r')
	f_handle2 = open("classidfile.txt", 'r')
	f_handle3 = open("predictdata.txt", 'r')
	features = genfromtxt(f_handle, dtype = float)
	classes = genfromtxt(f_handle2, dtype = int)
	predictdata = genfromtxt(f_handle3, dtype = float)
	predictdata = np.expand_dims(predictdata, axis=0)
	print np.shape(features), features.ndim
	print np.shape(classes), classes.ndim
	print np.shape(predictdata), predictdata.ndim, predictdata.dtype
	f_handle.close()
	f_handle2.close()
	f_handle3.close()

 	training = Dataset(samples=features,labels=classes)
	clf = kNN(k=2)
	print clf
	clf.train(training)
	#print np.mean(clf.predict(training.samples) == training.labels)
	print clf.predict(predictdata)
	print clf.trained_labels

