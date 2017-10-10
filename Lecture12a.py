# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 18:04:20 2017

@author: jdkern
"""

from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error as mse

df_data = pd.read_excel('peak_forecasting.xlsx', sheetname='RegressionData')
df_data.columns = ('year', 'demand', 'econ', 'pop', 'eff', 'temp')

training = df_data.loc[0:8, :]
validation = df_data.loc[9:, :]

y = training.loc[:, 'demand']
X = training.loc[:, 'econ':'temp']

# Create linear regression object
regr_training = linear_model.LinearRegression()

# Train the model using the training sets
regr_training.fit(X, y)
coeff = regr_training.coef_
inter = regr_training.intercept_

# Make predictions using the testing set

# actual
actual = validation.loc[:, 'demand']

X_val = validation.loc[:, 'econ':'temp']
predicted = regr_training.predict(X_val)

# scatterplot
plt.figure()
plt.scatter(actual, predicted)
plt.xlabel('Actual Peak Demand (MWh)', fontsize=24)
plt.ylabel('Predicted Peak Demand (MWh)', fontsize=24)

# Residuals
residuals = predicted - actual

# RMSE
RMSE = np.sqrt((np.sum((residuals * residuals)) / len(residuals)))

RMSE2 = np.sqrt(mse(actual, predicted))

df_hist_temps = pd.read_excel('peak_forecasting.xlsx', sheetname='Predictions')
df_hist_temps.columns = ('date', 'temp')
years = int(np.floor(len(df_hist_tempts) / 365))

# grab hottest temps per year
annual_peak = []
for i in range(0, years):
    annual = df_hist_temps.loc[i * 365:i * 365 + 364, 'temp']
annual_peak = np.append(annual_peak, np.max(annual))

# est parameters of
mu_hist = np.mean(annual_peak)
std_hist = np.std(annual_peak)

random_temps = np.random.normal(mu_hist,std_hist,1000)
demand_simulation = inter + coeff[0]*1.8 + coeff[1]*5.32 + coeff[2]*0.87 + coeff[3]*random_temps

plt.figure()
plt.hist(demand_simulation)
plt.show()