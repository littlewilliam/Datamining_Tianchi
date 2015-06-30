# coding=utf-8
__author__ = 'tianchuang'

import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import time


# 加载数据
df = pd.read_csv("../res/user_11_26_11_28_RF.csv")

# 浏览数据集
print df.head()
'''
df.hist()
pl.show()
'''

# 需要自行添加逻辑回归所需的intercept变量
df['intercept'] = 1.0

print df.head()

# 指定作为训练变量的列，不含目标列`behavior_type_4`
train_cols = df.columns[1:]
print train_cols

logit = sm.Logit(df['behavior_type_4'], df[train_cols])
# 拟合模型
result = logit.fit()

# 查看数据的要点,1、coefficient 系数 2、

print result.summary()


# 预测数据
startTime = time.time()
combos = pd.read_csv('../res/user_12_01_12_04_group_user_item_category.csv')
print 'Congratulations, load last day data complete! Took %fs!' % (time.time() - startTime)
combos['intercept'] = 1.0
print combos.head()

startTime = time.time()
train_cols = combos.columns[2:]  # index,user_id,item_id,item_category,behavior_type_1,behavior_type_2,behavior_type_3
print train_cols
combos['prediction'] = result.predict(combos[train_cols])  # 为每组特征进行预测打分，存储在一个新的prediction列，这里是第五列
print 'Congratulations, predict complete! Took %fs!' % (time.time() - startTime)

# print combos
#frame = pd.DataFrame(combos)

#result=combos.columns['user_id','item_id','prediction']
result = combos[['user_id', 'item_id', 'prediction']]
print result.head()

result.to_csv('../out/validate/predict_1205_raw.csv', index=None)

