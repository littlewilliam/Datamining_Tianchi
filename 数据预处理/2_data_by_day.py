__author__ = 'tianchuang'
# coding=utf-8
import os
print os.getcwd()
import pandas as pd
from pandas import  DataFrame
import time
import pylab as pl

time_initial = time.time()


startTime = time.time()
#无地理位置
user_data=pd.read_csv('./data/old/data_final_itemset.csv')
#有地理位置
#user_data=pd.read_csv('./data/old/data_contain_geo_final.csv')

print 'Congratulations, load data complete! Took %fs!' % (time.time() - startTime)

#print ((user_data['time'] < '2014-11-20') or (user_data['time'] >= '2014-11-19'))
user_validate=user_data[user_data['time'] < '2014-11-29']
user_validate=user_validate[user_data['time'] >= '2014-11-28']
#elegant way (and)
#user_validate=user_data[((user_data['time'] < '2014-12-05')+(user_data['time'] >= '2014-11-18'))>1]


#user_validate=user_data

print user_validate.head()
print user_validate['behavior_type_4'].value_counts()
print user_validate['time'].value_counts()
print user_validate.describe()
'''
# 频率表，表示behavior_type_3与behavior_type_4的值相应的数量关系
print pd.crosstab(user_validate['behavior_type_4'], user_validate['behavior_type_3'], rownames=['behavior_type_4'])
print pd.crosstab(user_validate['behavior_type_4'], user_validate['behavior_type_2'], rownames=['behavior_type_4'])
print pd.crosstab(user_validate['behavior_type_4'], user_validate['behavior_type_1'], rownames=['behavior_type_4'])
'''
print 'Total time: %fs!' % (time.time() - time_initial)


'''
user_validate.hist()
pl.show()
'''
user_validate.to_csv('./data/separated/11_28/11_28.csv',index=False,index_label='index')



'''

user_1=user_data[user_data['behavior_type']==1]
user_1_0=user_data[user_data['behavior_type']!=1]
user_1_0.loc[:, 'behavior_type'] = 0
user1=user_1_0.append(user_1)
user1=user1.sort_index()
user1=user1.rename(columns = {'behavior_type':'behavior_type_click'})

a=-1
for row in user_data.values:
    a +=1

    if row[2] == 1:
        print row

    if a == 10:
        break

#print user_data
'''