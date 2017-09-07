# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 21:01:34 2017

@author: jdkern
"""
from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy.stats as stats



df_data = pd.read_csv('hourlybid2015.csv',header=4)
# get rid of 'date' column in data
del df_data['Date']

#############################################################################
# convert data matrix to vector
def mat2vec(df_data):
    [rows,columns] = np.shape(df_data)
    vector = []
    d = df_data.as_matrix()
    for i in range(0,rows):
        vector = np.append(vector,d[i,:])
     
    return vector

vector = mat2vec(df_data)


# Read 2014 electricity demand data
df_bizarre_data = pd.read_csv('bizarre_data.csv',header=None)
bizarre_data = df_bizarre_data.as_matrix()

############################################################################
#Pre-process Data
def pre_processor(bizarre_data):
    #find and correct missing data
    for i in range(0,len(bizarre_data)):
    
    # looks for 0s and -999s
        if bizarre_data[i] < 1:
            
            #looks for incidence of 2 consecutive 0s or -999s
            if bizarre_data[i+1] < 1:
          
                # linear interpolation
                bizarre_data[i] = np.mean([bizarre_data[i-1],bizarre_data[i+2]])
            
            # linear interpolation
            else:
                bizarre_data[i] = np.mean([bizarre_data[i-1],bizarre_data[i+1]])
                
        # looks for really big numbers
        elif bizarre_data[i] > 200000:
        
            #linear interpolation
            bizarre_data[i] = np.mean([bizarre_data[i-1],bizarre_data[i+1]])
               
    return bizarre_data
#############################################################################
    
# call pre_processor function
processed_data = pre_processor(bizarre_data)

# find date of weird remaining point
weird_point = [index for index,value in enumerate(processed_data) if value > 130000 and index > 7000]
weird_point = weird_point[0]

day = np.floor(weird_point/24)
hour = weird_point%24 + 1 #to make up for zero index
answer = [day,hour]

plt.figure()
plt.hist(processed_data)
plt.xlabel('Demand (MWh)',fontsize=30)
plt.ylabel('Frequency',fontsize=30)
plt.title('Pre-processed 2014 Data', fontsize=30)

#qqplot
plt.figure()
plt.subplot(1,2,1)
whitened_data = (processed_data - np.mean(processed_data))/np.std(processed_data)
stats.probplot(whitened_data[:,0],dist="norm",plot=plt)
plt.xlabel('Theoretical Normal Quantiles',fontsize=30)
plt.ylabel('Empirical Data Normal Quantiles',fontsize=30)
plt.title('QQ Plot of Demand Data',fontsize=30)
#
#log transformation
transformed_data = np.log(processed_data) 
#
plt.subplot(1,2,2)
whitened_data = (transformed_data - np.mean(transformed_data))/np.std(transformed_data)
stats.probplot(whitened_data[:,0],dist="norm",plot=plt)
plt.xlabel('Theoretical Normal Quantiles',fontsize=30)
plt.ylabel('Empirical Data Normal Quantiles',fontsize=30)
plt.title('QQ Plot of Log-Transformed Demand Data',fontsize=30)


#mean
mu = np.mean(transformed_data)
dev = np.std(transformed_data)

#number of standard deviations weird point is away from mean
number_stds = (transformed_data[weird_point] - mu)/dev


#moving window assessment
num_hours = len(transformed_data)
window = 700

#ouput
outliers = np.zeros((num_hours,1))

# for i = 251 to i = 8510
for i in range(7321,7322):#range(int(window/2) + 1,num_hours-int(window/2)):
    
    # calculate the mean for every point in transformed data from (i-250)
    # to (i + 250) (a 501 point window)
    window_mean = np.mean()
    
    #calculate the std. deviation for every point in transformed data from
    #(i-250) to (i + 250) (a 501 point window)
    window_std = np.std()
    
    #test whether points 251:8510 in transformed data are outliers
    if transformed_data[i] >= window_mean + 2*window_std or transformed_data[i] <= window_mean - 2*window_std:
        outliers[i] = 1
    else:
        outliers[i] = 0

list_outliers = outliers[:,0].tolist()
list_outliers.index(1)





