# coding=utf-8
__author__ = 'tianchuang'

import os
print os.getcwd()
#os.chdir('./alidata')
import pandas as pd
from pandas import  DataFrame
import time
import pylab as pl

#将原始数据整合成LR可预测的格式(没有groupby)
def data_to_predict():
    user_data=pd.read_csv('./data/separated/12_03_12_04/12_03_12_04.csv')
    print user_data.describe()

    item=pd.read_csv('./data/separated/item_only_category_drop_duplicates.csv')
    print item.describe()
    user_data_merge=pd.merge(user_data,item,on=['item_category'],how='inner',sort=True)
    print user_data_merge.describe()

    cols_final = ['user_id','item_id','item_category','behavior_type_1','behavior_type_2','behavior_type_3']
    user_data_ok=user_data_merge[cols_final]

    print user_data_ok.head()
    print user_data_ok.describe()
    #user_data_ok.to_csv('./data/separated/11_24_11_27/user_11_24_11_27_item_subset.csv',index=False,index_label='index')
    user_data_merge.to_csv('./data/separated/12_03_12_04/user_12_03_12_04_item_subset.csv',index=False,index_label='index')

#data_to_predict()



#LR可预测的格式进行groupby  初始有18 2523个数据---->7 5688个数据
def data_predict_to_groupby():

    user_data=pd.read_csv('./data/separated/12_03_12_04/12_03_12_04.csv')
    print user_data.describe()
    group=user_data.groupby(['user_id','item_id','item_category'],as_index=False).sum()
    #group=group.drop_duplicates()
    print group.describe()
    group.to_csv('./data/separated/12_03_12_04/12_03_12_04_group.csv',index=False,index_label='index')

#data_predict_to_groupby()

#将前两天数据和第三天数据进行标号
def data_to_label():
    user_data=pd.read_csv('./data/separated/11_26_11_27/user_11_26_11_27_item_subset_merge_separate_a_day.csv')
    print '前两天的数据',user_data.describe()

    data2=pd.read_csv('./data/separated/11_28/11_28.csv')
    data2=data2[['behavior_type_4','item_category']]
    data2=data2.groupby(['item_category'],as_index=False).sum()
    data2=data2.drop_duplicates()
    print '标号当天的数据',data2.describe()

    user_data_merge=pd.merge(user_data,data2,on=['item_category'],how='outer',sort=True)
    user_data_merge=user_data_merge.fillna(0)

    print 'merge后的数据',user_data_merge.describe()

    cols_final = ['behavior_type_4','user_id','item_category','d1_1_1','d1_1_2','d1_1_3','d1_1_4','d1_2_1','d1_2_2',
                  'd1_2_3','d1_2_4','d1_3_1','d1_3_2','d1_3_3','d1_3_4','d1_4_1','d1_4_2','d1_4_3','d1_4_4','d1_5_1',
                  'd1_5_2','d1_5_3','d1_5_4','d2_1_1','d2_1_2','d2_1_3','d2_1_4','d2_2_1','d2_2_2','d2_2_3','d2_2_4'
        ,'d2_3_1','d2_3_2','d2_3_3','d2_3_4','d2_4_1','d2_4_2','d2_4_3','d2_4_4','d2_5_1','d2_5_2','d2_5_3','d2_5_4']
    user_data_ok=user_data_merge[cols_final]
    #user_data_ok=user_data_ok.groupby(['user_id','item_category'],as_index=False).sum()
    user_data_ok=user_data_ok.drop_duplicates()
    user_data_ok=user_data_ok.sort_index(by='user_id')
    '''
    print '在对于用户，商品groupby之前，有可能label值同时出现了0，1，导致出现重复数据（实际为购买），' \
          'label前总数量：',user_data_ok['item_category'].count()
    user_data_ok=user_data_ok.groupby(['item_category'],as_index=False).sum()
    print '在对于用户，商品groupby之后，label总数量：',user_data_ok[['item_category','1b1','1b2','1b3','1b4','2b1',
              '2b2','2b3','2b4','3b1','3b2','3b3','3b4','4b1','4b2','4b3','4b4']].count()
    #cols_final = ['behavior_type_4','user_id','item_category','behavior_type_1','behavior_type_2','behavior_type_3']
    user_data_ok=user_data_ok[cols_final]
    print user_data_ok.head()
    print user_data_ok.describe()
    #user_data_ok.to_csv('./data/separated/11_24_11_28/user_11_24_11_28_item_subset_label_buy_0_1_2.csv',index=False,index_label='index')
    user_data_ok[user_data_ok['behavior_type_4']>1]=1
    '''
    print user_data_ok.describe()
    user_data_ok.to_csv('./data/separated/11_26_11_28/11_26_11_28.csv',index=False,index_label='index')

data_to_label()
