__author__ = 'tianchuang'
# coding=utf-8

import os

print os.getcwd()
# os.chdir('./alidata')
import pandas as pd
from pandas import DataFrame
import time

time_initial = time.time()

startTime = time.time()
#得出 只含交易行为的user_id,item_id
def data_to_user_and_item():
    #user_data=pd.read_csv('./data/old/data_pd_final.csv')
    user_data=pd.read_csv('./data/separated/11_18_12_04/user_11_08_12_04.csv')
    print 'Congratulations, load data complete! Took %fs!' % (time.time() - startTime)

    group=user_data.groupby(['user_id','item_id','item_category'],as_index=False).sum() #471 9002
    print group.head()
    data_buy=group[group['behavior_type_4']>0]  #10 3464
    data_user=data_buy[['user_id']]
    print 'user_id before duplicating' ,data_user['user_id'].count()#10 3464  51322
    data_user=data_user.drop_duplicates()
    print 'user_id after duplicating' ,data_user['user_id'].count()#8867  7630
    data_item=data_buy[['item_id']]
    print 'item_id before duplicating' , data_item['item_id'].count()#10 3464  51322
    data_item=data_item.drop_duplicates()
    print 'item_id after duplicating' , data_item['item_id'].count()#93397  47733

    data_user.to_csv('./data/separated/11_18_12_04/user_only_drop_duplicates.csv',index=False,index_label='index')

    data_item.to_csv('./data/separated/11_18_12_04/item_only_drop_duplicates.csv',index=False,index_label='index')

#data_to_user_and_item()

#和最终的预测进行user_id,item_id交集运算
def merge_user_or_item_or_both():
    data_pre = pd.read_csv('./data/separated/predict_by_cart/12_04_by_cart_del_1094.csv')

    data_user = pd.read_csv('./data/separated/11_18_12_04/user_only_drop_duplicates.csv')
    data_item = pd.read_csv('./data/separated/11_18_12_04/item_only_drop_duplicates.csv')
    print data_pre.describe()
    print 'before merging,data_pre:', data_pre['user_id'].count()
    data_pre_by_user = pd.merge(data_pre, data_user, on=['user_id'], how='inner', sort=True)
    print 'after duplicating by user_id ,data_pre:', data_pre_by_user['user_id'].count()
    data_pre_by_item = pd.merge(data_pre, data_item, on=['item_id'], how='inner', sort=True)
    print 'after duplicating by item_id ,data_pre:', data_pre_by_item['user_id'].count()

    data_pre_by_item_user = pd.merge(data_pre_by_user, data_item, on=['item_id'], how='inner', sort=True)
    print 'after duplicating by item_id and item_id ,data_pre:', data_pre_by_item_user['user_id'].count()

    data_pre_by_user.to_csv('./data/separated/predict_by_cart/merge/1205/data_pre_by_user_1205.csv',
                            index=False, index_label='index')
    data_pre_by_item.to_csv('./data/separated/predict_by_cart/merge/1205/data_pre_by_item_1205.csv',
                            index=False, index_label='index')
    data_pre_by_item_user.to_csv('./data/separated/predict_by_cart/merge/1205/data_pre_by_item_user_1205_253.csv',
                                 index=False, index_label='index')
#merge_user_or_item_or_both()

#提取30天内有过交易行为的商品和用户
def item_and_user():
    data_raw=pd.read_csv('./data/old/data_final_itemset.csv')
    data=data_raw[['user_id','item_id','behavior_type_4']]
    data_user=data[['user_id','behavior_type_4']]
    data_user=data_user.groupby(['user_id'],as_index=False).sum()
    buy=data_user['behavior_type_4']>0
    data_user=data_user[buy]
    print 'data_user :',data_user['user_id'].count()

    data_item=data[['item_id','behavior_type_4']]
    data_item=data_item.groupby(['item_id'],as_index=False).sum()
    buy=data_item['behavior_type_4']>0
    data_item=data_item[buy]
    print 'data_item :',data_item['item_id'].count()

    data_user=data_user.drop_duplicates()
    data_item=data_item.drop_duplicates()
    print 'after drop duplicates: \n data_user :',data_user['user_id'].count()
    print 'data_item :',data_item['item_id'].count()

    data_user.to_csv('./data/separated/user_only_drop_duplicates.csv', index=False,index_label='index')
    data_item.to_csv('./data/separated/item_only_drop_duplicates.csv', index=False,index_label='index')

#item_and_user()

#提取商品子集中的category
def category():
    data_raw=pd.read_csv('./data/official_data/tianchi_mobile_recommend_train_item.csv')
    data=data_raw[['item_category']]
    print 'data_category :',data['item_category'].count()

    data=data.drop_duplicates()
    print 'after drop duplicates: \n data_category :',data['item_category'].count()

    data.to_csv('./data/separated/item_only_category_drop_duplicates.csv', index=False,index_label='index')

#category()

def delete_15_17_often():
    user_15_17=pd.read_csv('./data/separated/predict_by_cart/12_18_by_cart_15_17_130.csv')
    user_after_15=pd.read_csv('./data/separated/predict_by_cart/12_18_by_cart_after_15_658.csv')
    user=pd.read_csv('./data/separated/user_only_drop_duplicates.csv')
    item=pd.read_csv('./data/separated/item_only_drop_duplicates.csv')
    print '原数据有：',user_after_15['user_id'].count()
    print '15点-17点数据：',user_15_17['user_id'].count()

    user_15_17=pd.merge(user_15_17,user,on='user_id',how='inner')
    print '15点-17点的老用户有：',user_15_17['user_id'].count()

    #user_15_17=pd.merge(user_15_17,item,on='item_id',how='inner')
    #print '15点-17点的老用户+老商品有：',user_15_17['user_id'].count()

    sub = ['user_id', 'item_id']
    mask = user_after_15[sub].isin(user_15_17[sub].to_dict(outtype='list')).all(axis=1)
    #取差集
    by_cart_data = user_after_15[~mask]

    print '去除掉刚刚那些15点-17点比较无聊随意点击不购买的数量，现在有：',by_cart_data['user_id'].count()
    by_cart_data.to_csv('./data/separated/predict_by_cart/12_18_by_cart_after_15_658_del_boring_user_580.csv', index=False, index_label='index')

#delete_15_17_often()

def delete_17_23_often():
    user_17_23=pd.read_csv('./data/separated/predict_by_cart/12_18_by_cart_23_70.csv')
    user_after_17=pd.read_csv('./data/separated/predict_by_cart/0421/2_12_18_by_cart_after_15_658_del_boring_user_580_del_all_boring_user_item_544.csv')
    user=pd.read_csv('./data/separated/user_only_drop_duplicates.csv')
    item=pd.read_csv('./data/separated/item_only_drop_duplicates.csv')
    print '原数据有：',user_after_17['user_id'].count()
    print '15点-17点数据：',user_17_23['user_id'].count()

    user_17_23=pd.merge(user_17_23,user,on='user_id',how='inner')
    print '15点-17点的老用户有：',user_17_23['user_id'].count()

    #user_17_23=pd.merge(user_17_23,item,on='item_id',how='inner')
    #print '15点-17点的老用户+老商品有：',user_17_23['user_id'].count()

    sub = ['user_id', 'item_id']
    mask = user_after_17[sub].isin(user_17_23[sub].to_dict(outtype='list')).all(axis=1)
    #取差集
    by_cart_data = user_after_17[~mask]

    print '去除掉刚刚那些15点-17点比较无聊随意点击不购买的数量，现在有：',by_cart_data['user_id'].count()
    by_cart_data.to_csv('./data/separated/predict_by_cart/0422/2_12_18_by_cart_after_15_658_del_boring_user_580_del_all_boring_user_item_544_del23_493.csv', index=False, index_label='index')

delete_17_23_often()
print 'Total time : %fs!' % (time.time() - time_initial)
