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


user_data=pd.read_csv('./data/separated/12_18/user_12_18_geo_item_subset.csv')
user_data2=pd.read_csv('./official_data/tianchi_mobile_recommend_train_item.csv')
print 'Congratulations, load data complete! Took %fs!' % (time.time() - startTime)
print user_data2.head()

#从数据中删除无用的
#user_data= user_data.drop(['time','behavior_type_4','index'],axis=1)
loc_bool=~user_data2['item_geohash'].isnull()   #loc_bool代表有地理信息的数据为true
user_data2=user_data2[loc_bool]

user_data2= user_data2.drop(['item_category','item_geohash'],axis=1)

print user_data.head()
print user_data2.head()

#留着geo信息

user_data_ok=pd.merge(user_data,user_data2,on=['item_id'],how='inner',sort=True)
cols_final = ['user_id','user_geohash','item_id','item_category','behavior_type_1',
              'behavior_type_2','behavior_type_3','behavior_type_4']
user_data_ok=user_data_ok[cols_final]
print user_data_ok.describe()
group=user_data_ok.groupby(['user_id','item_id'],as_index=False).sum()
print group.head()
print group.describe()



group.to_csv('./data/separated/12_18/user_12_18_geo_item_subset_category_geo.csv',
                        index=False,index_label='index')