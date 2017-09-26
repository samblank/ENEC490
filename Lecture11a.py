# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

df_training = pd.read_excel('temp_demand.xlsx',sheetname='training',header=0)
df_training.columns =('temp','day','demand')
df_validation = pd.read_excel('temp_demand.xlsx',sheetname='validation',header=0)
df_validation.columns =('temp','day','demand')

t_CDD = np.zeros((len(df_training),1))
t_HDD = np.zeros((len(df_training),1))
v_CDD = np.zeros((len(df_validation),1))
v_HDD = np.zeros((len(df_validation),1))

for i in range(0,len(df_training)):
    t_CDD[i] = np.max([df_training.loc[i,'temp'] - 65,0])
    t_HDD[i] = np.max([65-df_training.loc[i,'temp'],0])
    v_CDD[i] = np.max([df_validation.loc[i,'temp'] - 65,0])
    v_HDD[i] = np.max([65-df_validation.loc[i,'temp'],0])

# Create linear regression object
regr_training = linear_model.LinearRegression()

inter = np.ones((len(t_CDD),1))
X = np.column_stack((inter,t_CDD,t_HDD))
y = df_training.loc[:,'demand']

# Train the model using the training sets
regr_training.fit(X,y)

# fit the validation data to regression
inter2 = np.ones((len(v_CDD),1))
X_vals = np.column_stack((inter2,v_CDD,v_HDD))
y_vals = regr_training.predict(X_vals)

#plotting actual vs. simulated
demand = df_validation.loc[:,'demand']
plt.figure()
plt.scatter(y_vals,demand)
plt.xlabel('Actual Electricity Demand (MWh)')
plt.ylabel('Predicted Electricity Demand (MWh)')

#calculating R^2
Rsq = r2_score(demand,y_vals)

#calculating mean square error
number5 = mse(demand,y_vals)

#scatterplot of actual demand vs. residuals
residuals = y_vals - demand
plt.figure()
plt.scatter(demand,residuals)
plt.xlabel('Actual Demand (MWh)')
plt.ylabel('Residuals (MWh)')
