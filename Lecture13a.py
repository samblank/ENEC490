# -*- coding: utf-8 -*-
'''
Created on Wed Sep 06 21:15:20 2017

@author: jdkern
'''

from __future__ import division
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

df_data = pd.read_csv('hourlybid2015.csv',header=4)
# get rid of 'date' column in data
del df_data['Date']
m = df_data.as_matrix()

# convert data matrix to vector
def mat2vec(df_data):
    [rows,columns] = np.shape(df_data)
    vector = []
    d = df_data.as_matrix()
    for i in range(0,rows):
        vector = np.append(vector,d[i,:])
     
    return vector

# call function®
v = mat2vec(df_data)

#winter
plt.figure()
plt.subplot(2,2,1)
acf_winter = acf(v[0:1200],nlags=72)
plt.plot(acf_winter)
plt.xlabel('Hours',fontsize=24)
plt.ylabel('Autocorrelation',fontsize=24)
plt.title('Winter',fontsize=24)
plt.show()

#summer
plt.subplot(2,2,2)
acf_summer = acf(v[3999:5199],nlags=72)
plt.plot(acf_winter)
plt.xlabel('Hours',fontsize=24)
plt.ylabel('Autocorrelation',fontsize=24)
plt.title('Summer',fontsize=24)
plt.show()

#fall
plt.subplot(2,2,3)
acf_fall = acf(v[5999:7199],nlags=72)
plt.plot(acf_winter)
plt.xlabel('Hours',fontsize=24)
plt.ylabel('Autocorrelation',fontsize=24)
plt.title('Fall',fontsize=24)
plt.show()

peak_hours = np.zeros((365, 1))
for i in range(0, 365):
    peak_hours[i] = np.max(m[i, :])
    if np.isnan(peak_hours[i]) > 0:
        peak_hours[i] = np.mean([peak_hours[i - 1], peak_hours[i + 1]])

# what
plt.figure()
acf_peak = acf(peak_hours, nlags=60)
plt.plot(acf_peak)

##difference data for volatility
inter = np.ones(len((peak_hours) - 1))

difference = np.ones(len((peak_hours) - 1))

for i in range(0, 364):
    difference[i] = peak_hours[i + 1] - peak_hours[i]

plt.figure()
plt.plot(difference[0:363])

#moving avg smoothing

movingAvg = np.zeros((335,1))
peakMask = peak_hours[14:350]

for i in range(15,350):
    movingAvg[i-15] = np.mean(peak_hours[i-15:i+15])

plt.figure()
plt.subplot(2,2,1)
plt.plot(movingAvg)
plt.title('Moving Average',fontsize=24)
plt.subplot(2,2,2)
plt.plot(peakMask)
plt.title('Peak Comparison',fontsize=24)
plt.show()


#remove smoothed trend from the original time series
residual_timeSeries = peakMask - movingAvg ##replace smoothed_trend w/ number 6 vector name

#^^^^I think we can just subtract "movingAvg" from "peakMask" since they're the same dim

#plot autocorrelation of residual
acf_residuals = acf(residual_timeSeries, nlags=60) #I don't think nlags needs to be changed from earlier?
residuals_vec = mat2vec(acf_residuals)
plt.figure()
plt.plot(acf_residuals[0:363])


