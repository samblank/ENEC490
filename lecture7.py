# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# load data
df_2012 = pd.read_excel('coal860_data.xlsx', sheetname='2012_coal', header=0)
df_2015 = pd.read_excel('coal860_data.xlsx', sheetname='2015_coal', header=0)
df_2012.columns = ('ID', 'P_Code', 'Capacity', 'Year')
df_2015.columns = ('ID', 'P_Code', 'Capacity', 'Year')

# total years under consideration
years = range(1925, 2016)

# creates bins for the histogram
bins = np.zeros((len(years), 1))

for i in range(0, len(df_2012)):
    # identifies the year
    yr = df_2012.loc[i, 'Year']

    # %locates the correct 'bin'
    bin_number = years.index(yr)

    # adds capacity to correct 'bin'
    bins[bin_number] = bins[bin_number] + df_2012.loc[i, 'Capacity']

# plot histogram

y_pos = np.arange(len(years))

plt.bar(y_pos, bins, align='center', alpha=0.5, color='0.8', edgecolor='0.5')
tick_range = range(0, len(years), 5)
year_ticks = range(1925, 2013, 5)
plt.xticks(tick_range, year_ticks)
plt.xlabel('Year', fontsize=24)
plt.ylabel('Capacity (MW)', fontsize=24)

# Identify unique rows that are different

d_2012 = set([tuple(line) for line in df_2012.values.tolist()])
d_2015 = set([tuple(line) for line in df_2015.values.tolist()])



# a is a 'set'
a = d_2012.difference(d_2015)

retired = np.array(list(a))

bins2 = np.zeros((len(years), 1))


#repeat for 2015
for i in range(0, len(retired)):
    # identifies the year
    yr = retired[i,3]

    # %locates the correct 'bin'
    bin_number = years.index(yr)

    # adds capacity to correct 'bin'
    bins2[bin_number] = bins2[bin_number] + retired[i,2]

ypos=np.arange(len(years))
plt.figure()
plt.bar(ypos,bins)
plt.bar(ypos,bins2)
tick_range = range(0, len(years), 5)
year_ticks = range(1925, 2013, 5)
plt.xticks(tick_range, year_ticks)
plt.xlabel('Year', fontsize=24)
plt.ylabel('Capacity (MW)', fontsize=24)
plt.title('Existing coal capacity by operating year')
plt.show()
