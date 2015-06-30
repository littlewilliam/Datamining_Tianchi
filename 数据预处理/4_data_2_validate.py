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


#单天处理成user_id,item_id

user_data=pd.read_csv('./data/separated/user_12_05.csv')
user_data2=pd.read_csv('./data/separated/item_only_category_drop_duplicates.csv')
data_ok=user_data[user_data['behavior_type_4']==1]
user_data_ok=pd.merge(data_ok,user_data2,on=['item_category'],how='inner',sort=True)
user_data_ok= user_data_ok.drop(['time','behavior_type_1','behavior_type_2','item_category',
                           'behavior_type_3','behavior_type_4','index','index.1'],axis=1)

#去重！！
user_data_ok=user_data_ok.drop_duplicates()

num_raw = user_data_ok['user_id'].count()


print user_data_ok.head()
print user_data_ok.describe()
print num_raw

user_data_ok.to_csv('./data/separated/user_12_05_true_drop_duplicates.csv', index=False,index_label='index')
