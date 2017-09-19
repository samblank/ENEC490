from __future__ import division
import pandas as pd 
import numpy as np


data = pd.read_excel('state_fuel_cf.xlsx',header=0)
data.columns = ['state','fuel','cf']

state = 'NC'
fuel = 'SUN'
cf = .20

## state probabilities
a = data.loc[data['state'] == state]
state_prob = len(a)/len(data)

## fuel probabilities
b = data.loc[data['fuel'] == fuel]
fuel_prob = len(b)/len(data)

## capacity factor probability: > 0.2
c = data.loc[data['cf']> cf]
cf_prob = len(c)/len(data)

# probability of selecting a plant in NC among US pop of solar plants
d = a.loc[a['fuel'] == fuel]
both_prob = len(d) / len(data)
ncgivensun = both_prob / fuel_prob

# solar given NC
e = b.loc[b['state'] == state]
both_probe = len(e) / len(data)
sungivennc = both_probe / state_prob

# capacity>cf and solar and NC
f = d.loc[d['cf'] > cf]
f_prob = len(f) / len(data)
q = state_prob * fuel_prob * cf_prob
# probability of capacity>cf given NC solar
g_prob = f_prob/both_prob