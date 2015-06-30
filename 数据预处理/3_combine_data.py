# coding=utf-8
__author__ = 'tianchuang'

import os
print os.getcwd()
#os.chdir('./alidata')
import pandas as pd
from pandas import  DataFrame
import time
import pylab as pl

time_initial = time.time()

startTime = time.time()


user_data=pd.read_csv('./data/separated/12_18/user_12_18.csv')
print user_data.head()
print 'Congratulations, load data complete! Took %fs!' % (time.time() - startTime)


#!!!原始数据多了一个index,新数据应该不需要!!!
def drop_index1(u):
    global user_data
    user_data=u.sort_index(by=['index.1','time'])
    user_data= user_data.drop(['index'],axis=1)
    user_data=user_data.rename(columns = {'index.1':'index'})
    return user_data
#drop_index1(user_data)

#从数据中删除无用的time,index,behavior4
#user_data= user_data.drop(['time','behavior_type_4','index'],axis=1)
user_data= user_data.drop(['time','index'],axis=1)

print user_data.head()

#一些分析的代码分析 item_category
'''
print user_data['item_category'].value_counts()
print user_data2['item_category'].value_counts()

user_data2.hist()
pl.show()
'''

#整合为4天检验集的格式
'''
user_data_ok=pd.merge(user_data,user_data2,on=['item_category'],how='inner',sort=True)
cols_final = ['user_id','item_id','item_category','behavior_type_1','behavior_type_2','behavior_type_3']
user_data_ok=user_data_ok[cols_final]
group=user_data_ok.groupby(['user_id','item_id','item_category'],as_index=False).sum()
print group.head()
print group.describe()
user_data_ok.to_csv('./data/separated/user_12_01_12_04_group_user_item_category.csv',
                        index=False,index_label='index')
'''

#整合为4天训练集的初始格式
'''
user_data_ok=pd.merge(user_data,user_data2,on=['user_id','item_id','item_category'],how='inner',sort=True)
cols_final = ['item_category','behavior_type_1','behavior_type_2','behavior_type_3']
user_data_ok=user_data_ok[cols_final]
'''

#留着geo信息
'''
user_data_ok=pd.merge(user_data,user_data2,on=['item_category'],how='inner',sort=True)
cols_final = ['user_id','user_geohash','item_id','item_category','behavior_type_1',
              'behavior_type_2','behavior_type_3','behavior_type_4']
user_data_ok=user_data_ok[cols_final]
group=user_data_ok.groupby(['user_id','user_geohash','item_id','item_category'],as_index=False).sum()
print group.head()
print group.describe()
group.to_csv('./data/separated/12_18/user_12_18_geo_item_subset.csv',
                        index=False,index_label='index')

'''