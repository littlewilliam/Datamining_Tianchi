# coding=utf-8
__author__ = 'tianchuang'

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np


train = pd.read_csv('../res/user_11_26_11_28_RF.csv')
test = pd.read_csv('../res/user_12_03_12_04_item_subset_merge_separate_a_day.csv')

cols_final =['behavior_type_4','user_id','item_category','d1_1_3',
                  'd1_2_3','d1_3_3','d1_4_3',
                  'd1_5_3','d2_1_3','d2_2_3'
        ,'d2_3_3','d2_4_3','d2_5_3']
train=train[cols_final]
print '原始的训练集行为：',train['user_id'].count()
train=train.groupby(['user_id','item_category'],as_index=False).sum()
train=train[cols_final]
train=train.drop_duplicates()
print '选取特征后，groupby的训练集行为：',train['user_id'].count()

#print train.describe()
cols_test=['item_id','user_id','item_category','d1_1_3',
                  'd1_2_3','d1_3_3','d1_4_3',
                  'd1_5_3','d2_1_3','d2_2_3'
        ,'d2_3_3','d2_4_3','d2_5_3']
test=test[cols_test]
print '原始的测试集行为：',test['item_id'].count()
test=test.groupby(['item_id','user_id','item_category'],as_index=False).sum()
test=test[cols_test]
test=test.drop_duplicates()
print '选取特征后，groupby的测试集行为：',test['item_id'].count()

#test=test[['item_id','user_id','item_category','1b1','1b2','1b3','1b4','2b1',
#              '2b2','2b3','2b4','3b1','3b2','3b3','3b4','4b1','4b2','4b3','4b4']]
#train 只用3个行为
#features = train.columns[2:5]
#train 除了3个行为外，加上item_category
features = train.columns[1:]
#print 'features:', features

clf = RandomForestClassifier(n_jobs=2)
y, _ = pd.factorize(train['behavior_type_4'])
clf.fit(train[features], y)
#print 'y:', y
#test 只用3个行为
#t_features = test.columns[3:6]
#test 除了3个行为外，加上item_category
t_features = test.columns[1:]
#print 'test features:', test[t_features].head()


pre = clf.predict(test[t_features])
#print 'clf.predict(test[features])', pre

# 数组-> 序列->DataFrame
df_pre = pd.Series(pre)
df_pre = pd.DataFrame(df_pre, columns=['predict'])
print 'predict中的值分布',df_pre['predict'].value_counts()
n=0
num_1 = df_pre[df_pre['predict'] > n].count()
num_all = df_pre['predict'].count()
print 'predict > %d,numbers:'%n, num_1
print 'predict = 0,numbers:', num_all - num_1

test['predict'] = df_pre

data_out = test[test['predict'] > n]
data_ok = data_out[['user_id', 'item_id']]
#print data_ok.head()
data_ok = data_ok.drop_duplicates()
print 'after duplicates , predict > %d,numbers:'%n, num_1
data_ok.to_csv('../out/user_12_05_RF.csv', index=False, index_label='index')

#F值计算

def caculate_F_function():
    data_raw = pd.read_csv('../out/user_12_05_RF.csv')
    #data_raw = pd.read_csv('../res/user_12_01_12_04_item_subset_merge.csv')
    #data_raw=data_raw[['user_id','item_id']]

    data_true = pd.read_csv('../res/true/user_12_05_true_drop_duplicates.csv')
    num_raw = float(data_raw['user_id'].count())
    num_true = float(data_true['user_id'].count())

    magic = pd.merge(data_raw, data_true, on=['user_id', 'item_id'], how='inner')
    num_pre = magic['user_id'].count()
    p = num_pre / num_raw
    r = num_pre / num_true
    f = (2 * p * r) / (p + r)
    print 'Number of hits: %d' % num_pre
    print 'Number of submitting: %d' % num_raw
    print 'Really data: %d' % num_true
    print 'f: %f%% p:%f%%  r:%f%%' % (f * 100, p * 100, r * 100 )


caculate_F_function()

