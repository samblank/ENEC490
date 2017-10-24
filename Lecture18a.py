# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:18:45 2017

@author: jdkern
"""
from __future__ import division
import numpy as np

#Define state vector
# 1 - sunny; 2 - rainy

x = np.array([0,1])
P = np.array(([.9,.1],[.5,.5]))
a = np.array([0,0])

# Probability of weather 10 days from now
x_n = np.zeros((10,2))

for i in range(1,11):
    for j in range(1,i):
        if j<2:
            a = np.dot(x,P)
        else: 
            a = np.dot(a,P)
    
    x_n[i-1,:] = a


# Steady state probability

# q (P - I) = 0

P_I = P - np.array(([1,0],[0,1]))

# Solve system of equations 
# -.1(q1) + .5(q2) = 0
#  .1(q1) - .5(q2) = 0
#   q1 + q2 = 1

#% .1(q1) - .5(1-q1) = 0; -->
#% .6(q1)  = .5

q1 = .5/.6
q2 = 1-q1

sunny = q1*365
rainy = q2*365


