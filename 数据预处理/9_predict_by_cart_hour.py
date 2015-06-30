__author__ = 'tianchuang'
# coding=utf-8

import os
print os.getcwd()
import pandas as pd



user_data=pd.read_csv('./data/separated/12_18/12_18.csv')
print '总共的数据:',user_data['user_id'].count()
after_15=user_data['time']>='2014-12-18 20'
before_17=user_data['time']<='2014-12-18 20'

user_data=user_data[after_15 & before_17]
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

data_final.to_csv('./data/separated/predict_by_cart/12_18_by_cart_20_125.csv',index=False,index_label='index')
