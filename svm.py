import numpy as np
import mlpy
#from numpy import *
#from mlpy import *



xtr = np.array([[7.0, 2.0, 3.0, 1.0],  # first sample
                 [1.0, 2.0, 3.0, 2.0],  # second sample
                 [2.0, 2.0, 2.0, 1.0], # third sample
					  [2.0, 4.0, 2.0, 6.0],
                 [2.0, 2.0, 7.0, 9.0]])
print xtr
print np.size(xtr), np.shape(xtr), np.ndim(xtr)

ytr = np.array([1, 2, 3, 1, 2])             # classes
print ytr 
print np.size(ytr), np.shape(ytr), np.ndim(ytr)

#Save and read data from disk
print mlpy.data_tofile('data_example.dat', xtr, ytr, sep='	')
x, y = mlpy.data_fromfile('data_example.dat')
print x
print y

print "mlpy.data_normalize(x) = ", mlpy.data_normalize(x)

#mysvm = mlpy.Svm()                     # initialize Svm class
myknn = mlpy.Knn(k = 1)                # initialize knn class

## initialize fda class
myfda = mlpy.Fda()

#print mysvm.compute(xtr, ytr)     # compute SVM
print myknn.compute(xtr, ytr)      # compute knn
print myfda.compute(xtr, ytr)      # compute fda

#print mysvm.predict(xtr)     # predict SVM model on training 
print myknn.predict(xtr)      # predict knn model on training data
print myfda.predict(xtr)      # predict fda model on training data


xts = np.array([2.0, 2.0, 7.0, 1.0])   # test point
#print mysvm.predict(xts)    # predict SVM model on test point
print myknn.predict(xts)     # predict knn model on test point
print myfda.predict(xts)     # predict fda model on test point

#print mysvm.realpred      # real-valued prediction
print myknn.realpred      # real-valued prediction
print myfda.realpred      # real-valued prediction

#print mysvm.weights(xtr, ytr)                # compute weights on training data
#print myfda.weights(xtr, ytr) # compute weights on training data


