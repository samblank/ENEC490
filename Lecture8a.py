

from __future__ import division
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df_data = pd.read_excel('N3045US3m.xls', sheetname='Data 1', header=2)
df_data.columns = ['date', 'price']

# extract 2002-2016 gas price data
s = df_data.date[df_data.date == '1/15/2002 00:00:00'].index
s = s[0]

e = df_data.date[df_data.date == '12/15/2016 00:00:00'].index
e = e[0]

data = []
for i in range(s, e + 1):
    data = np.append(data, df_data.loc[i, 'price'])

# histogram
plt.figure()
plt.hist(data)
plt.xlabel('Natural Gas Price ($/MMBtu)', fontsize=10)
plt.ylabel('Frequency', fontsize=10)

# log transformation
transformed_data = np.log(data)

# histogram of log transformed data
plt.figure()
plt.hist(transformed_data)
plt.xlabel('log Natural Gas Price ($/MMBtu)', fontsize=10)
plt.ylabel('Frequency', fontsize=10)
#
# number of years in dataset
years = int(len(transformed_data) / 12)


#
# convert to 12 x N matrix
# annual profile
def vec2mat(d, rows):
    # number of years in record
    columns = int(len(d) / rows)

    # output matrix of zeros
    output = np.zeros((rows, columns))

    # nested for loops
    for i in range(0, columns):
        for j in range(0, rows):
            output[j, i] = d[i * rows + j]

    return output


# call annual profile function
x = vec2mat(transformed_data, 12)


# monthly stats function
def monthly_stats(x):
    output = np.zeros((12, 2))
    for j in range(0, 12):
        output[j, 0] = np.average(x[j, :])
        output[j, 1] = np.std(x[j, :])

    return output


s = monthly_stats(x)

# months
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

##########################################
# identify month highest mean
h = s[:, 0] == np.max(s[:, 0])
mu = s[h, 0]
std = s[h, 1]
sample1 = mu + std * np.random.randn(1000, 1)
back_transformed1 = np.exp(sample1)

# month name
idx = []
names = []
for i in range(0, len(h)):
    if h[i] == True:
        idx = i
name1 = months[idx]

names.append(name1)
###########################################
# identify month with lowest mean
g = s[:, 0] == np.min(s[:, 0])
mu2 = s[g, 0]
std2 = s[g, 1]
sample2 = mu2 + std2 * np.random.randn(1000, 1)
back_transformed2 = np.exp(sample2)

# month name
idx = []

for i in range(0, len(g)):
    if g[i] == True:
        idx = i
name2 = months[idx]
names.append(name2)

# identify month with highest std dev
j = s[:, 1] == np.max(s[:, 1])
mu3 = s[j, 0]
std3 = s[j, 1]
sample3 = mu3 + std3 * np.random.randn(1000, 1)
back_transformed3 = np.exp(sample3)

# month name
idx = []

for i in range(0, len(j)):
    if j[i] == True:
        idx = i
name3 = months[idx]
names.append(name3)

# identify month with lowest std dev
k = s[:, 1] == np.min(s[:, 1])
mu4 = s[k, 0]
std4 = s[k, 1]
sample4 = mu4 + std4 * np.random.randn(1000, 1)
back_transformed4 = np.exp(sample4)

# month name
idx = []

for i in range(0, len(k)):
    if k[i] == True:
        idx = i
name4 = months[idx]
names.append(name4)

plt.figure()
bins = np.histogram(np.hstack((back_transformed1, back_transformed2, back_transformed3, back_transformed4)), bins=100)[1]
plt.hist(back_transformed1, bins)
plt.hist(back_transformed2, bins)
plt.hist(back_transformed3, bins)
plt.hist(back_transformed4, bins)
plt.legend(names)

# use the boxplot fnt to plot log transformed data
log_data = [sample1, sample2, sample3, sample4]

plt.figure()
plt.boxplot(log_data)
