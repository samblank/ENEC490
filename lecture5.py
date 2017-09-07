#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:15:11 2017

@author: SamBlank
"""
# %% cell 1
import pandas as pd
import numpy as np


#%% cell 2
#read 2015 electricity demand data
data = pd.read_csv('hourlybid2015.csv',skiprows = [0,4])
bizarreData = pd.read_csv('bizarre_data.csv')
print(np.shape(bizarreData))

