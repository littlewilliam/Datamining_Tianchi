# coding=utf-8
__author__ = 'tianchuang'

import os
print os.getcwd()
#os.chdir('./patent/final')
import pandas as pd
from pandas import  DataFrame
import time

time_initial = time.time()

#读取数据
startTime = time.time()
user_data=pd.read_csv('./data/official_data/tianchi_mobile_recommend_train_user.csv')
print user_data.head()
print 'Congratulations, load data complete! Took %fs!' % (time.time() - startTime)

#虚拟变量
startTime = time.time()
dummy_ok = pd.get_dummies(user_data['behavior_type'], prefix='behavior_type')
print dummy_ok.head()
print 'Congratulations, get dummies complete! Took %fs!' % (time.time() - startTime)

#重整数据
startTime = time.time()
#cols_to_keep = ['user_id','item_id','time','item_category','user_geohash']
cols_to_keep = ['user_id','item_id','time','item_category']

#data = user_data[cols_to_keep].join(dummy_ok.ix[:, 'behavior_type_1':])
data_join = user_data[cols_to_keep].join(dummy_ok.ix[:, 0:])
cols_final = ['time','behavior_type_4','user_id','item_id','item_category',
              'behavior_type_1','behavior_type_2','behavior_type_3']
data_final=data_join[cols_final]
data_final=data_final.sort_index(by=['item_id','user_id','time'])
print data_final.head()
print 'Congratulations, sort data complete! Took %fs!' % (time.time() - startTime)

#写出数据
startTime = time.time()
data_final.to_csv('./data/old/data_final.csv', index=False,index_label='index')
print 'Congratulations, save data complete! Took %fs!' % (time.time() - startTime)

print 'Total time: %fs!' % (time.time() - time_initial)

#商品子集
item_raw=pd.read_csv('./data/official_data/tianchi_mobile_recommend_train_item.csv')
item=item_raw[['item_id']]

user_data_ok=pd.merge(data_final,item,on=['item_id'],how='inner',sort=True)
user_data_ok.to_csv('./data/old/data_final_itemset.csv', index=False,index_label='index')
