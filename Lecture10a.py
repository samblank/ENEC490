# -*- coding: utf-8 -*-

from __future__ import division
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df_data = pd.read_excel('catawba_data.xlsx',header=0)
df_data.columns = ['year','month','day','temp','inflow']

#temps = data(:,4);
#flows = data(:,5);

days=len(df_data)

W = []
losses = []

for i in range(0,days):
    
    v = 33.3/(1+np.exp(.15*(16.9-df_data.loc[i,'temp']))) + 127/df_data.loc[i,'inflow']
    W = np.append(W,v)
    
    if v > 37 and v <= 40:
        a = .25*2000*24
        losses = np.append(losses,a)
    elif v > 40 and v <= 42:
        b = .50*2000*24
        losses = np.append(losses,b)
    elif v > 42:
        c = 2000*24
        losses = np.append(losses,c)
    else:
        losses = np.append(losses,0)
  
        
losses_dollars = losses*.10
years = int(days/365)
annual_losses = np.zeros((years,1))

for i in range(0,years):
    annual_losses[i] = np.sum(losses_dollars[i*365:i*365+364])

edges = range(0,300000,10000)

sorted_losses = np.sort(annual_losses)
idx = int(np.round(.95*years))
CVar = sorted_losses[idx]

plt.figure()
plt.hist(annual_losses,bins=100)
plt.show()

##

# transform the stream flow values

flows = np.log(df_data['inflow'])

originalmean = np.mean(flows)
originaldev = np.std(flows)

Normalized_flows = (flows - originalmean) / originaldev
# 10% mean reduction
climate_mean = 0.9 * originalmean
# 20% increase in std of daily flows
climate_dev = 1.2 * originaldev

New_flows = (Normalized_flows * climate_dev) + climate_mean

Climate_flows = np.exp(New_flows)

# transform temp values
Climate_temp = 2 + df_data['temp']

W2 = []
losses2 = []

for i in range(0, days):

    v2 = 33.3 / (1 + np.exp(.15 * (16.9 - Climate_temp[i]))) + 127 / Climate_flows[i]
    W2 = np.append(W2, v2)

    if v2 > 37 and v2 <= 40:
        a = .25 * 2000 * 24
        losses2 = np.append(losses2, a)
    elif v2 > 40 and v2 <= 42:
        b = .50 * 2000 * 24
        losses2 = np.append(losses2, b)
    elif v2 > 42:
        c = 2000 * 24
        losses2 = np.append(losses2, c)
    else:
        losses2 = np.append(losses2, 0)



plt.hist(annual_losses)