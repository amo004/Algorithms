import numpy as np
a = np.genfromtxt("test.txt",delimiter  =",")
x1 = np.sum(a[:,0])/a.shape[0]
x2 = np.sum(a[:,1])/a.shape[0]
x3 = np.sum(a[:,2])/a.shape[0]
print(a)
print(x1)
print(x2)
print(x3)
# this is fucking nonsense 
