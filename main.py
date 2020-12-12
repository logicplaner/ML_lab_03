from _csv import writer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
from datetime import date
import csv

# importing data
df = pd.read_csv('employees.csv', sep=',')
# replace empty rows
df = df.replace('', np.nan)
# print invalid data
print('invalid data:\n',df[df.isna().any(axis='columns')])
# drop invalid rows
df = df.dropna()
print('Describe salary: \n', df.describe())
print('\nAll salary: ',df['Salary'].sum())
print('\nMean salary:\n', df.mean())
print('\nMedian salary:\n', df.median())
print('\nMin salary:\n',df.min())
print('\nMax salary:\n',df.max())
# grouping rows
var = df.groupby(['Senior Management']).median()
print('\nGrouping by senior management:\n',var)
# sorting by new row Experience
def getExperience(row):
    data1 = row['Start Date']
    dataList = data1.split('/')
    data = date(int(dataList[2]), int(dataList[0]), int(dataList[1]))
    today = date.today()
    salary = row['Salary']
    delta = today - data
    return delta.days/365*salary
exp = df.apply(getExperience, axis = 1)
df['Experience'] = exp
res = df.sort_values(by=['Experience'])
print('\nExperience:\n', res)
# show grafs by Experiene and salary for gender
res = res.groupby(['Gender']).plot(x='Experience', y='Salary')
plt.show()
# take a new row
def getBonus(row):
    data1 = row['Salary']
    data2 = row['Bonus %']
    return data1/100*data2
df['Bonus usd'] = df.apply(getBonus, axis = 1)
print('\nnew data:\n',df.head())
# add a row for merging data
df['uid'] = df.apply(lambda _: uuid.uuid1(), axis=1)
# merging right
info = df[['uid','First Name', 'Last Login Time', 'Senior Management', 'Team']]
print('\nInfo:\n', info.head())
personal = df[['uid','First Name', 'Start Date', 'Salary', 'Bonus %', 'Bonus usd']]
print('\nPersonal info:\n', personal.head())
newData = pd.merge(personal, info, on='uid', how='right')
print('Mergin right:', newData.head())
# mergin right join
newData = pd.merge(personal, info, on='uid', how='right')
print('\nMergin inner join:\n', newData.head())
# mergin inner join
newData = pd.merge(personal, info, on='uid', how='inner')
print('\nMergin inner join:\n', newData.head())
# mergin left join
newData = pd.merge(personal, info, on='uid', how='left')
print('\nMergin left join:\n', newData.head())
# export merged data to excell file
newData.to_csv(index=False)
with pd.ExcelWriter('result.xlsx') as writer:
    newData.to_excel(writer, sheet_name='Sheet 1')