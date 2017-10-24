# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 18:04:20 2017

@author: jdkern
"""

from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import scipy
import scipy.stats as st
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm

df_data = pd.read_excel('winddata.xlsx',header=None)
data = df_data.as_matrix()

## separate data into months
hours = len(data)
days = int(hours/24)
years = int(days/365)

jan = np.zeros((years*31*24,1))
feb = np.zeros((years*28*24,1))
mar = np.zeros((years*31*24,1))
apr = np.zeros((years*30*24,1))
may = np.zeros((years*31*24,1))
jun = np.zeros((years*30*24,1))
jul = np.zeros((years*31*24,1))
aug = np.zeros((years*31*24,1))
sep = np.zeros((years*30*24,1))
oct = np.zeros((years*31*24,1))
nov = np.zeros((years*30*24,1))
dec = np.zeros((years*31*24,1))

for i in range(0,years):
#   
    jan[i*744:i*744 + 743] = data[i*8760 :i*8760+ 743]
    feb[i*672:i*672 + 671] = data[i*8760 + 744:i*8760+ 1415]
    mar[i*744:i*744 + 743] = data[i*8760 + 1416:i*8760+ 2159]
    apr[i*720:i*720 + 719] = data[i*8760 + 2160:i*8760+ 2879]
    may[i*744:i*744 + 743] = data[i*8760 + 2880:i*8760+ 3623]
    jun[i*720:i*720 + 719] = data[i*8760 + 3624:i*8760+ 4343]
    jul[i*744:i*744 + 743] = data[i*8760 + 4344:i*8760+ 5087]
    aug[i*744:i*744 + 743] = data[i*8760 + 5088:i*8760+ 5831]
    sep[i*720:i*720 + 719] = data[i*8760 + 5832:i*8760+ 6551]
    oct[i*744:i*744 + 743] = data[i*8760 + 6552:i*8760+ 7295]
    nov[i*720:i*720 + 719] = data[i*8760 + 7296:i*8760+ 8015]
    dec[i*744:i*744 + 744] = data[i*8760 + 8016:i*8760+ 8760] 
    
jan_days = int(len(jan)/24)
feb_days = int(len(feb)/24)
apr_days = int(len(apr)/24)

# calcuate mean for each m,h
m_diurnal = np.zeros((24,12))
s_diurnal = np.zeros((24,12))

# calculate std for each m,h
x=np.reshape(jan,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,0] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,0] = np.transpose(std_x)

x=np.reshape(feb,(24,feb_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,1] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,1] = np.transpose(std_x)

x=np.reshape(mar,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,2] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,2] = np.transpose(std_x)

x=np.reshape(apr,(24,apr_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,3] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,3] = np.transpose(std_x)

x=np.reshape(may,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,4] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,4] = np.transpose(std_x)

x=np.reshape(jun,(24,apr_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,5] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,5] = np.transpose(std_x)

x=np.reshape(jul,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,6] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,6] = np.transpose(std_x)

x=np.reshape(aug,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,7] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,7] = np.transpose(std_x)

x=np.reshape(sep,(24,apr_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,8] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,8] = np.transpose(std_x)

x=np.reshape(oct,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,9] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,9] = np.transpose(std_x)

x=np.reshape(nov,(24,apr_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,10] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,10] = np.transpose(std_x)

x=np.reshape(dec,(24,jan_days))
mu_x = np.mean(np.transpose(x))
m_diurnal[:,11] = np.transpose(mu_x)
std_x = np.std(np.transpose(x))
s_diurnal[:,11] = np.transpose(std_x)

N = np.zeros((len(data),1))

# remove seasonality and diurnal effects
for i in range(0,years):
    for j in range(0,31):
        for k in range(0,24):
            N[i*8760 +j*24+k] = np.divide(data[i*8760 + j*24+k]-m_diurnal[k,0],s_diurnal[k,0])
            N[i*8760 + j*24 + 1416+k] =np.divide(data[i*8760 + j*24 + 1416+k] -m_diurnal[k,2],s_diurnal[k,2])
            N[i*8760 + j*24 + 2880+k] =np.divide(data[i*8760 + j*24 + 2880+k] -m_diurnal[k,4],s_diurnal[k,4])
            N[i*8760 + j*24 + 4344+k] =np.divide(data[i*8760 + j*24 + 4344+k] -m_diurnal[k,6],s_diurnal[k,6])
            N[i*8760 + j*24 + 5088+k] =np.divide(data[i*8760 + j*24 + 5088+k] -m_diurnal[k,7],s_diurnal[k,7])
            N[i*8760 + j*24 + 6552+k] =np.divide(data[i*8760 + j*24 + 6552+k] -m_diurnal[k,9],s_diurnal[k,9])
            N[i*8760 + j*24 + 8016+k] =np.divide(data[i*8760 + j*24 + 8016+k] -m_diurnal[k,11],s_diurnal[k,11])

    for j in range(0,30):
        for k in range(0,24):
            N[i*8760 +j*24+2160+k] = np.divide(data[i*8760 + j*24+2160+k]-m_diurnal[k,3],s_diurnal[k,3])
            N[i*8760 + j*24 + 3624+k] =np.divide(data[i*8760 + j*24 + 3624+k] -m_diurnal[k,5],s_diurnal[k,5])
            N[i*8760 + j*24 + 5832+k] =np.divide(data[i*8760 + j*24 + 5832+k] -m_diurnal[k,8],s_diurnal[k,8])
            N[i*8760 + j*24 + 7296+k] =np.divide(data[i*8760 + j*24 + 7296+k] -m_diurnal[k,10],s_diurnal[k,10])
            
#
    for j in range(0,28):
        for k in range(0,24):
            N[i*8760 + j*24 + 744+k] =np.divide(data[i*8760 + j*24 + 744+k] -m_diurnal[k,1],s_diurnal[k,1])

# Convert to Gaussian
N = N + 2
IG_params = st.invgauss.fit(N)
mu = 2
lmbda = 7.78448
cdf_IG = st.invgauss.cdf(N,mu/lmbda,scale = lmbda)
cdf_N = st.norm.ppf(cdf_IG)

# autocorrelation
b = acf(cdf_N,nlags=48)
plt.figure()
plt.plot(b)

# partial autocorrelation
c = pacf(cdf_N,nlags=48)
plt.figure()
plt.plot(c)

#Fit the model to the existing time series, In my model the AIC shows best model is AR4 MA2
arma_mod = sm.tsa.ARMA(cdf_N,(4,2)).fit()

#Using the model to genrate simulated data. 1,744 means that we want to generate 744 data points. 
sim=arma_mod.predict(1,10000)


#A single synthetic year
new = sim[1000:9760]

# Convert back to non-Gaussian
new_N = st.norm.cdf(new)
new_IG = st.invgauss.ppf(new_N,mu/lmbda,scale = lmbda)
new_ds = new_IG - 2


#Add seasonality and diurnal effects
new_final = np.zeros((8760,1))

for j in range(0,31):
    for k in range(0,24):

        new_final[j*24+k] = new_ds[j*24+k]*s_diurnal[k,0] + m_diurnal[k,0]
        new_final[j*24+1416+k] = new_ds[j*24+1416+k]*s_diurnal[k,2] + m_diurnal[k,2]
        new_final[j*24+2880+k] = new_ds[j*24+2880+k]*s_diurnal[k,4] + m_diurnal[k,4]
        new_final[j*24+4344+k] = new_ds[j*24+4344+k]*s_diurnal[k,6] + m_diurnal[k,6]
        new_final[j*24+5088+k] = new_ds[j*24+5088+k]*s_diurnal[k,7] + m_diurnal[k,7]
        new_final[j*24+6552+k] = new_ds[j*24+6552+k]*s_diurnal[k,9] + m_diurnal[k,9]
        new_final[j*24+8016+k] = new_ds[j*24+8016+k]*s_diurnal[k,11] + m_diurnal[k,11]

for j in range(0,30):
    for k in range(0,24):
        new_final[j*24+2160+k] = new_ds[j*24+2160+k]*s_diurnal[k,3] + m_diurnal[k,3]
        new_final[j*24+3624+k] = new_ds[j*24+3624+k]*s_diurnal[k,5] + m_diurnal[k,5]
        new_final[j*24+5832+k] = new_ds[j*24+5832+k]*s_diurnal[k,8] + m_diurnal[k,8]
        new_final[j*24+7296+k] = new_ds[j*24+7296+k]*s_diurnal[k,10] + m_diurnal[k,10]
   
for j in range(0,28):
    for k in range(0,24):
        new_final[j*24+744+k] = new_ds[j*24+744+k]*s_diurnal[k,1] + m_diurnal[k,1]

# Logical Bounds

for i in range(0,len(new_final)):
    if new_final[i] > np.max(data):
        new_final[i] = np.max(data)
    elif new_final[i] < np.min(data):
        new_final[i] = np.min(data)

 