# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 00:05:43 2017

@author: jdkern
"""

from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from statsmodels.tsa.stattools import acf

df_data = pd.read_excel('winddata.xlsx',header=None)
data = df_data.as_matrix()

plt.figure()
plt.hist(data)
plt.xlabel('Wind Power Production (MWh)',fontsize=24)
plt.ylabel('Frequency',fontsize=24)

plt.figure()
log_data = np.log(data+1)
plt.hist(log_data)
plt.xlabel('Log Transformed Wind Power Production (MWh)',fontsize=24)
plt.ylabel('Frequency',fontsize=24)

#calculate monthly statistics 
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


## separate data into months
for i in range(0,years):
#   
    jan[i*744:i*744 + 743] = log_data[i*8760 :i*8760+ 743]
    feb[i*672:i*672 + 671] = log_data[i*8760 + 744:i*8760+ 1415]
    mar[i*744:i*744 + 743] = log_data[i*8760 + 1416:i*8760+ 2159]
    apr[i*720:i*720 + 719] = log_data[i*8760 + 2160:i*8760+ 2879]
    may[i*744:i*744 + 743] = log_data[i*8760 + 2880:i*8760+ 3623]
    jun[i*720:i*720 + 719] = log_data[i*8760 + 3624:i*8760+ 4343]
    jul[i*744:i*744 + 743] = log_data[i*8760 + 4344:i*8760+ 5087]
    aug[i*744:i*744 + 743] = log_data[i*8760 + 5088:i*8760+ 5831]
    sep[i*720:i*720 + 719] = log_data[i*8760 + 5832:i*8760+ 6551]
    oct[i*744:i*744 + 743] = log_data[i*8760 + 6552:i*8760+ 7295]
    nov[i*720:i*720 + 719] = log_data[i*8760 + 7296:i*8760+ 8015]
    dec[i*744:i*744 + 744] = log_data[i*8760 + 8016:i*8760+ 8760]   

# mean for each month 
mu_jan = np.mean(jan)
mu_feb = np.mean(feb)
mu_mar = np.mean(mar)
mu_apr = np.mean(apr)
mu_may = np.mean(may)
mu_jun = np.mean(jun)
mu_jul = np.mean(jul)
mu_aug = np.mean(aug)
mu_sep = np.mean(sep)
mu_oct = np.mean(oct)
mu_nov = np.mean(nov)
mu_dec = np.mean(dec)

mus = [mu_jan,mu_feb, mu_mar, mu_apr, mu_may, mu_jun, mu_jul ,mu_aug, mu_sep, mu_oct, mu_nov, mu_dec]

plt.figure()
plt.bar(range(1,13),mus)
plt.xlabel('Month',fontsize=24)
plt.ylabel('Mean Log Wind Power',fontsize=14)
labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.xticks(range(1,13), labels)
#
# std deviation for each month
std_jan = np.std(jan)
std_feb = np.std(feb)
std_mar = np.std(mar)
std_apr = np.std(apr)
std_may = np.std(may)
std_jun = np.std(jun)
std_jul = np.std(jul)
std_aug = np.std(aug)
std_sep = np.std(sep)
std_oct = np.std(oct)
std_nov = np.std(nov)
std_dec = np.std(dec)
#

N = np.zeros((len(data),1))
#
# remove seasonality
for i in range(0,years):
#    
    N[i*8760 :i*8760+ 743] = (log_data[i*8760:i*8760+ 743]-mu_jan)/std_jan 
    N[i*8760 + 744:i*8760+ 1415] = (log_data[i*8760 + 744:i*8760+ 1415]-mu_feb)/std_feb 
    N[i*8760 + 1416:i*8760+ 2159] = (log_data[i*8760 + 1416:i*8760+ 2159] - mu_mar)/std_mar
    N[i*8760 + 2160:i*8760+ 2879] = (log_data[i*8760 + 2160:i*8760+ 2879]-mu_apr)/std_apr
    N[i*8760 + 2880:i*8760+ 3623] = (log_data[i*8760 + 2880:i*8760+ 3623]-mu_may)/std_may
    N[i*8760 + 3624:i*8760+ 4343] = (log_data[i*8760 + 3624:i*8760+ 4343]-mu_jun)/std_jun
    N[i*8760 + 4344:i*8760+ 5087] = (log_data[i*8760 + 4344:i*8760+ 5087]-mu_jul)/std_jul
    N[i*8760 + 5088:i*8760+ 5831] = (log_data[i*8760 + 5088:i*8760+ 5831]-mu_aug)/std_aug
    N[i*8760 + 5832:i*8760+ 6551] = (log_data[i*8760 + 5832:i*8760+ 6551]-mu_sep)/std_sep
    N[i*8760 + 6552:i*8760+ 7295] = (log_data[i*8760 + 6552:i*8760+ 7295]-mu_oct)/std_oct
    N[i*8760 + 7296:i*8760+ 8015] = (log_data[i*8760 + 7296:i*8760+ 8015]-mu_nov)/std_nov
    N[i*8760 + 8016:i*8760+ 8759] = (log_data[i*8760 + 8016:i*8760+ 8759]-mu_dec)/std_dec 


#plot de-seasoned
plt.figure()
plt.plot(N)
plt.xlabel('Hours',fontsize=24)
plt.ylabel('De-Seasoned, Log Transformed Wind',fontsize=14)

# convert to daily mean
jan_days = int(len(jan)/24)
feb_days = int(len(feb)/24)
mar_days = int(len(mar)/24)
apr_days = int(len(apr)/24)
may_days = int(len(may)/24)
jun_days = int(len(jun)/24)
jul_days = int(len(jul)/24)
aug_days = int(len(aug)/24)
sep_days = int(len(sep)/24)
oct_days = int(len(oct)/24)
nov_days = int(len(nov)/24)
dec_days = int(len(dec)/24)

daily_jan = np.zeros((jan_days,1))
daily_feb = np.zeros((feb_days,1))
daily_mar = np.zeros((mar_days,1))
daily_apr = np.zeros((apr_days,1))
daily_may = np.zeros((may_days,1))
daily_jun = np.zeros((jun_days,1))
daily_jul = np.zeros((jul_days,1))
daily_aug = np.zeros((aug_days,1))
daily_sep = np.zeros((sep_days,1))
daily_oct = np.zeros((oct_days,1))
daily_nov = np.zeros((nov_days,1))
daily_dec = np.zeros((dec_days,1))

for i in range(0,jan_days): 
    daily_jan[i] = np.mean(jan[i*24:i*24+23])
    daily_mar[i] = np.mean(mar[i*24:i*24+23])
    daily_may[i] = np.mean(may[i*24:i*24+23])
    daily_jul[i] = np.mean(jul[i*24:i*24+23])
    daily_aug[i] = np.mean(aug[i*24:i*24+23])
    daily_oct[i] = np.mean(oct[i*24:i*24+23])
    daily_dec[i] = np.mean(dec[i*24:i*24+23])

for i in range(0,feb_days): 
    daily_feb[i] = np.mean(feb[i*24:i*24+23])
    
for i in range(0,apr_days): 
    daily_apr[i] = np.mean(apr[i*24:i*24+23])
    daily_jun[i] = np.mean(jun[i*24:i*24+23])
    daily_sep[i] = np.mean(sep[i*24:i*24+23])
    daily_nov[i] = np.mean(nov[i*24:i*24+23])
   
a = np.zeros((22,12))

b = acf(daily_jan,nlags=21)
c = acf(daily_feb,nlags=21)
d = acf(daily_mar,nlags=21)
e = acf(daily_apr,nlags=21)
f = acf(daily_may,nlags=21)
g = acf(daily_jun,nlags=21)
h = acf(daily_jul,nlags=21)
x = acf(daily_aug,nlags=21)
j = acf(daily_sep,nlags=21)
k = acf(daily_oct,nlags=21)
l = acf(daily_nov,nlags=21)
m = acf(daily_dec,nlags=21)

for i in range(0,22):
    a[i,0] = b[i]
    a[i,1] = c[i]
    a[i,2] = d[i]
    a[i,3] = e[i]
    a[i,4] = f[i]
    a[i,5] = g[i]
    a[i,6] = h[i]
    a[i,7] = x[i]
    a[i,8] = j[i]
    a[i,9] = k[i]
    a[i,10] = l[i]
    a[i,11] = m[i]

# plot daily autocorrelation
plt.figure()
for i in range(0,12):
  
    plt.plot(a[:,i],label = labels[i])

plt.legend()
plt.xlabel('Lags (days)',fontsize=24)
plt.ylabel('Autocorrelation',fontsize=14)

##################################################
# START HERE: Remove daily means and find diurnal 
#signal. Create [24x12] matrix called 'diurnal' that stores 
#the signal for each month




##################################################
# smooth the data with a moving avg maybe, or you can calc mean for each 24 hr period and clip it
plt.figure()

for i in range(0,12):
  
    plt.plot(diurnal[:,i],label = labels[i])

plt.legend()
plt.xlabel('Hours',fontsize=24)
plt.ylabel('Zero Centered Signal',fontsize=14)

# remove diurnal signal to find hourly noise 
hnoise_jan = np.zeros((len(jan),1))
hnoise_feb = np.zeros((len(feb),1))
hnoise_mar = np.zeros((len(mar),1))
hnoise_apr = np.zeros((len(apr),1))
hnoise_may = np.zeros((len(may),1))
hnoise_jun = np.zeros((len(jun),1))
hnoise_jul = np.zeros((len(jul),1))
hnoise_aug = np.zeros((len(aug),1))
hnoise_sep = np.zeros((len(sep),1))
hnoise_oct = np.zeros((len(oct),1))
hnoise_nov = np.zeros((len(nov),1))
hnoise_dec = np.zeros((len(dec),1))
#
#
for i in range(0,jan_days):
    for j in range(0,24):     
        hnoise_jan[i*24+j] = jan[i*24+j] - diurnal[j,0]
        hnoise_mar[i*24+j] = mar[i*24+j] - diurnal[j,2]
        hnoise_may[i*24+j] = may[i*24+j] - diurnal[j,4]
        hnoise_jul[i*24+j] = jul[i*24+j] - diurnal[j,6]
        hnoise_aug[i*24+j] = aug[i*24+j] - diurnal[j,7]
        hnoise_oct[i*24+j] = oct[i*24+j] - diurnal[j,9]
        hnoise_dec[i*24+j] = dec[i*24+j] - diurnal[j,11]
#
for i in range(0,apr_days):
    for j in range(0,24):        
        hnoise_apr[i*24+j] = apr[i*24+j] - diurnal[j,3]
        hnoise_jun[i*24+j] = jun[i*24+j] - diurnal[j,5]
        hnoise_sep[i*24+j] = sep[i*24+j] - diurnal[j,8]
        hnoise_nov[i*24+j] = nov[i*24+j] - diurnal[j,10]
    
for i in range(0,feb_days):
    for j in range(0,24):     
        hnoise_feb[i*24+j] = feb[i*24+j] - diurnal[j,1]
#
# Hourly noise
plt.figure()
plt.plot(hnoise_jan)
plt.xlabel('Hours',fontsize=24)
plt.ylabel('Residuals',fontsize=24)


a = np.zeros((49,12))

b = acf(hnoise_jan,nlags=48)
c = acf(hnoise_feb,nlags=48)
d = acf(hnoise_mar,nlags=48)
e = acf(hnoise_apr,nlags=48)
f = acf(hnoise_may,nlags=48)
g = acf(hnoise_jun,nlags=48)
h = acf(hnoise_jul,nlags=48)
x = acf(hnoise_aug,nlags=48)
j = acf(hnoise_sep,nlags=48)
k = acf(hnoise_oct,nlags=48)
l = acf(hnoise_nov,nlags=48)
m = acf(hnoise_dec,nlags=48)

for i in range(0,49):
    a[i,0] = b[i]
    a[i,1] = c[i]
    a[i,2] = d[i]
    a[i,3] = e[i]
    a[i,4] = f[i]
    a[i,5] = g[i]
    a[i,6] = h[i]
    a[i,7] = x[i]
    a[i,8] = j[i]
    a[i,9] = k[i]
    a[i,10] = l[i]
    a[i,11] = m[i]

# plot hourly autocorrelation
plt.figure()
for i in range(0,12):
  
    plt.plot(a[:,i],label = labels[i])

plt.legend()
plt.xlabel('Lags (hours)',fontsize=24)
plt.ylabel('Autocorrelation',fontsize=14)

