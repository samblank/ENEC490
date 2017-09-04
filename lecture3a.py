#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 15:35:27 2017

@author: SamBlank
"""


import csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# load data, specify sheet and number of rows to skip
df_data = pd.read_excel('HenryHub.xls',sheetname ='Data 1',skiprows = [0,1])

# renaming the very long price column name
df_data.columns = ['date','price']

def annual_profile(df_data):
    
    #number of years in record
    num_years = int(len(df_data)/12)
    
    #output matrix of zeros
    output = np.zeros((12,num_years))
    
    #nested for loops
    for i in range(0,num_years):
        for j in range(0,12):
            output[j,i] = df_data.loc[i*12+j,'price']
    
    #years considered    
    years = range(1997,2017)
    
    #index of 2008
    a = years.index(2008)
    
    #select data from 2008-present
    m = output[:,a:]
    
    return m

#call annual profile function
x = annual_profile(df_data)

#plotting

#plot function within for loop
new_years = range(2008,2017)
num_new_years = len(new_years)

#assigns random color to each new year
for i in range(0,num_new_years):
    plt.plot(x[:,i],label=str(new_years[i]))

plt.xlabel('Months',fontsize=30)
plt.ylabel('Natural Gas Price ($/MMBtu)',fontsize=30)
labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.xticks(range(0,12), labels)
plt.legend(prop={'size': 20})
plt.rc('xtick', labelsize=24)
plt.rc('ytick', labelsize=24)

