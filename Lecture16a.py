# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:55:03 2017

@author: jdkern
"""

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from statsmodels.tsa.stattools import acf

df_data = pd.read_excel('Data/natgas.xls')
df_data.columns = ('month','year','price')
data = df_data.loc[:,'price'].as_matrix()

# plot
plt.figure() 
plt.plot(data)
plt.ylabel('Natural Gas Price ($/MMBtu)',fontsize=24)
plt.xlabel('Month',fontsize=24)

# Data transformation and pre-processing
plt.figure() 
plt.hist(data)
plt.xlabel('Natural Gas Price ($/MMBtu)',fontsize=24)
plt.ylabel('Frequency',fontsize=24)

# Log transformation
log_data = np.log(data)
plt.figure() 
plt.hist(log_data)
plt.xlabel('Log Transformed Natural Gas Price ($/MMBtu)',fontsize=24)
plt.ylabel('Frequency',fontsize=24)

#%% Differencing
differenced_data = np.zeros((len(log_data)-1,1))

for i in range(0,len(log_data)-1):
    differenced_data[i] = log_data[i+1] - log_data[i]

plt.figure() 
plt.plot(differenced_data)
plt.ylabel('Differenced Gas Price ($/MMBtu)',fontsize=24)
plt.xlabel('Month',fontsize=24)

# Time series characterization
acf_d = acf(differenced_data)
plt.figure() 
plt.plot(acf_d)
plt.xlabel('Months',fontsize=24)
plt.ylabel('Autocorrelation',fontsize=24)



#%% Orenstein Uhlenbeck

x = np.log(data)
#x = np.log(data[150:])

#%% Differencing
differenced_data = np.zeros((len(log_data)-1,1))

for i in range(0,len(log_data)-1):
    differenced_data[i] = log_data[i+1] - log_data[i]

dx = differenced_data

#ensure same length
x = np.delete(x, (-1), axis=0)

# Time in years (12 observations per year)
dt = 1/12
dxdt = dx/dt

# Fit a linear trend to estimate mean reversion parameters
coeff = np.polyfit(x,dxdt,1)
res = dxdt - np.polyval(coeff, x)

revRate   = -coeff[0]
meanLevel = coeff[1]/revRate
vol       = np.std(res) * np.sqrt(dt)

t = range(0,120) #Time vector
x_new = np.zeros((len(t),10)) #Allocate output vector, set initial condition

# initialize
x_new[0,:] = x[-1]

for j in range(0,10):

    for i in range(0,len(t)-1):

        x_new[i+1,j]= x_new[i,j]+revRate*(meanLevel-x_new[i,j])*dt+vol*(dt**.5)*np.random.randn()


plt.figure()
plt.plot(x_new)
plt.show()

#%%
'''historical = np.zeros((len(log_data),10))

for i in range(0,10):
    historical[:,i] = ,synthetic]'''

composite = np.vstack((historical,x_new))
backtransformed = np.exp(composite)

#Plot
plt.figure()
plt.plot(backtransformed)
plt.title('OU',fontsize=24)
plt.xlabel('Month',fontsize=24)
plt.ylabel('Natural Gas Price ($/MMBtu)',fontsize=24)
