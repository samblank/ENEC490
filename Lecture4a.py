# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:56:28 2017

@author: jdkern
"""

import matplotlib.pyplot as plt
import pandas as pd 
from pandas.tools.plotting import autocorrelation_plot
import numpy as np

# load data
df_data = pd.read_excel('monthly_demandNC.xlsx',header=None)
df_data.columns = ['demand']

# annual profile
def annual_profile(df_data):
    
    #number of years in record
    num_years = int(len(df_data)/12)
    
    #output matrix of zeros
    output = np.zeros((12,num_years))
    
    #nested for loops
    for i in range(0,num_years):
        for j in range(0,12):
            output[j,i] = df_data.loc[i*12+j,'demand']

    return output

#call annual profile function
x = annual_profile(df_data)


#year on year differences
[months,years] = np.shape(x)

#output 
differences = np.zeros((months,years-1))

# % change by month
for i in range(0,12):
    for j in range(0,years-1):
        differences[i,j] = (x[i,j+1] - x[i,j])/x[i,j]*100
        

#create new figure
plt.figure()
labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

#plot function within for loop
for i in range(0,12):
    plt.plot(differences[i,:],c=np.random.rand(3,1),label=labels[i])
    
plt.xlabel('Years',fontsize=30)
plt.ylabel('% Change',fontsize=30)
ticklabels = ['1998','2000','2002','2004','2006','2008','2010','2012','2014']
plt.xticks(range(0,years,2), ticklabels)
plt.legend(prop={'size': 20})
plt.rc('xtick', labelsize=24)
plt.rc('ytick', labelsize=24)


#annual demand percentages
totals = np.sum(x,axis=0)
monthly_fractions = np.zeros((months,years));

for i in range(0,years):
    monthly_fractions[:,i] = x[:,i]/totals[i]*100;

#create new figure
plt.figure() 

#plot function within for loop
for i  in range(0,12):
    plt.plot(monthly_fractions[i,:],c=np.random.rand(3,1),label=labels[i])

plt.xlabel('Years',fontsize=30)
plt.ylabel('% of Total',fontsize=30)
plt.xticks(range(0,years,2), ticklabels)
plt.legend(prop={'size': 20})
plt.rc('xtick', labelsize=24)
plt.rc('ytick', labelsize=24)


#Simulation

#bootstrapping
sim_years = 10
bootstrap_sample = np.zeros((12*sim_years,1))
for i in range(0,sim_years):
    for j in range(0,12):
        s = int(np.ceil(sim_years*np.random.uniform()))
        bootstrap_sample[i*12+j] = x[j,s]

plt.figure()
#bootstrap sample
plt.plot(bootstrap_sample)
plt.xlabel('Months',fontsize=30)
plt.ylabel('Demand (MWh)',fontsize=30)

plt.figure()
#autocorrelation
autocorrelation_plot(x,c=np.random.rand(3,1))
plt.xlabel('Months',fontsize= 30)
plt.ylabel('Autocorrelation',fontsize=30)

#monte carlo
sim_years = 10
bootstrap_sample = np.zeros((12*sim_years,1))
for i in range(0,sim_years):
    for j in range(0,12):
        s = int(np.ceil(sim_years*np.random.normal()))
        bootstrap_sample[i*12+j] = x[j,s]
#RIGHT ABOVE HERE JORDAN

plt.figure()
#bootstrap sample
plt.plot(bootstrap_sample)
plt.xlabel('Months',fontsize=30)
plt.ylabel('Demand (MWh)',fontsize=30)
