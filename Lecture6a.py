# -*- coding: utf-8 -*-

from __future__ import division
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

df_temps=pd.read_csv('tempdata.csv',header=None)
df_temps.columns = ('Date','Temp')
temps = df_temps.loc[:,'Temp'].as_matrix().astype(np.float)

#Read electricity demand data
df_demand = pd.read_csv('hourlybid2014.csv',header=4)
# get rid of 'date' column in data
del df_demand['Date']
demand = df_demand.as_matrix().astype(np.float)

#convert to a vector
def mat2vec(data):
    [rows,columns] = np.shape(data)
    vector = []
    for i in range(0,rows):
        vector = np.append(vector,data[i,:])

    return vector

vector_demand = mat2vec(demand)

#convert to peak demand vector
peaks = []

for i in range(0,365):
    peak_hourly = np.max(demand[i,:])
    peaks = np.append(peaks,peak_hourly)

peaks = peaks/1000

# forms 2-column matrix
combined = np.column_stack((temps,peaks))

#look for NaNs
for i in range(0,len(combined)):
    if np.isnan(combined[i,1]) > 0:
        combined[i,1] = np.mean([combined[i-1,1],combined[i+1,1]])

#clusters for each row
IDX = KMeans(n_clusters=3, random_state=0).fit_predict(combined)

#forms 3-column matrix
clustered_data = np.column_stack((combined,IDX))


plt.figure()
plt.scatter(combined[:,0],combined[:,1],c=IDX+1)
plt.xlabel('Temps (F)',fontsize=24)
plt.ylabel('Electricity Demand (MWh)',fontsize=24)


# january average
Jan_Avg = np.zeros((24, 1))

for i in range(0, 24):
    Jan_Avg[i] = np.mean(demand[0:30, i])

plt.figure()
hours = np.arange(1, 25)
plt.scatter(hours, Jan_Avg)

# july average
July_Avg = np.zeros((24, 1))

for i in range(0, 24):
    July_Avg[i] = np.mean(demand[181:211, i])

plt.figure()
hours = np.arange(1, 25)
plt.scatter(hours, July_Avg)

'''change nans to zeros - this is okay because averaging 
surrounding values to find a morea ccurate guess would not
 yield a new max'''



boxData = [[combined[4::7,1]],
           [combined[5::7,1]],
           [combined[6::7,1]],
           [combined[7::7,1]],
           [combined[1::7,1]],
           [combined[2::7,1]],
           [combined[3::7,1]]]

#%% plot of max of each day by day of week
plt.figure()
plt.boxplot(boxData)
plt.show()