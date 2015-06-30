__author__ = 'tianchuang'
# coding=utf-8

import os
print os.getcwd()
#os.chdir('./alidata')
import pandas as pd
from pandas import  DataFrame
import time
import pylab as pl


user_data=pd.read_csv('./data/separated/12_18/12_18.csv')
#user_data2=pd.read_csv('./data/separated/item_only_category_drop_duplicates.csv')
#非购买
#user_data=pd.merge(user_data,user_data2,on='item_category')
#print '和商品子集merge后的数据:\n',user_data.head()
#不管有没有购买，添加则为考虑没购买
print '总共的数据:',user_data['user_id'].count()
user_data=user_data[['user_id','item_id','item_category','behavior_type_3','behavior_type_4']]
user_data=user_data.groupby(['user_id','item_id','item_category'],as_index=False).sum()
print 'groupby之后的数据:',user_data['user_id'].count()

not_buy=user_data['behavior_type_4']==0
add_cart=user_data['behavior_type_3']>0
data_cart=user_data[not_buy & add_cart]
print '加入购物车且没有购买的数据:',data_cart['user_id'].count()


'''
#商品item_category>13200剔除，根据可视化
data_cart=data_cart[data_cart['item_category']<13185]
print '删除item_category >13185, 数据:',data_cart['user_id'].count()
'''

cols_final = ['user_id','item_id']
data_final=data_cart[cols_final]
data_final=data_final.drop_duplicates()
print '去重后, 数据:',data_final['user_id'].count()

print data_final.describe()

data_final.to_csv('./data/separated/predict_by_cart/12_18_by_cart_1033.csv',index=False,index_label='index')

'''
user_item=pd.read_csv('./official_data/tianchi_mobile_recommend_train_item.csv')
user_item= user_item.drop(['item_geohash','item_category'],axis=1)
user_item['be']=1
print user_item.head()
user_data=pd.read_csv('./data/separated/predict_by_cart/12_18.csv')

user_data_ok=pd.merge(user_data,user_item,on='item_id')
print user_data.describe()
print user_data_ok.describe()

cols_final = ['user_id','item_id']
data_final=user_data_ok[cols_final]
print data_final
data_final.to_csv('./data/separated/predict_by_cart/12_18_item.csv',index=False,index_label='index')


'''
