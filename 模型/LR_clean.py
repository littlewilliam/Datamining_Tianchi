# coding=utf-8
__author__ = 'tianchuang'

# coding=utf-8
__author__ = 'tianchuang, sunsibai'

import pandas as pd
import statsmodels.api as sm
import pylab as pl

import time

startTime = time.time()
time_initial = time.time()

data = pd.read_csv('../out/validate/predict_1205_raw.csv')
data_frame = {'F': [], 'P': [], 'R': [], 'HIT': [], 'PREDICT': []}
print 'Congratulations, load data complete! Took %fs!' % (time.time() - startTime)

# 是否和购物车数据取交集,效果不好
def merge_cart_data():
    global data
    data_fool = pd.read_csv('../res/by_cart/12_04_by_cart.csv')
    print 'initial numbers of data', data['user_id'].count()
    magic = pd.merge(data, data_fool, on=['user_id', 'item_id'], how='inner')
    print 'after merging,the numbers of data', magic['user_id'].count()
    data = magic
    return data

# merge_cart_data()

#print data.describe()
#print data.head()

'''
            user_id       item_id     prediction
count  1.779970e+05  1.779970e+05  177997.000000
mean   7.269845e+07  2.036460e+08       0.044878
std    4.091619e+07  1.171656e+08       0.008038
min    1.415200e+04  2.966000e+03       0.027092
25%    3.627651e+07  1.026887e+08       0.043822
50%    7.373717e+07  2.029349e+08       0.043822
75%    1.078088e+08  3.068612e+08       0.043822
max    1.424281e+08  4.045487e+08       0.090402
'''
#循环判断F最大值
'''
def loop():
    global data

    def f_add(a1,a2,a3,a4,a5):
        global data_frame
        data_frame.setdefault('F').append(a1)
        data_frame.setdefault('P').append(a2)
        data_frame.setdefault('R').append(a3)
        data_frame.setdefault('HIT').append(a4)
        data_frame.setdefault('PREDICT').append(a5)


    #predict 从最小到最大
    predict=0.027092
    while predict<0.090402:
        data['prediction_ok'] = data['prediction'].map(lambda x: 1 if x >= predict else 0)

        data_ok=data[data['prediction_ok']==1]
        #print data_ok.describe()
        result=data_ok[['user_id','item_id']]
        result=result.drop_duplicates()
        data_raw= result
        data_true=pd.read_csv('../out/validate/true/user_12_05_true_drop_duplicates.csv')
        num_raw = float(data_raw['user_id'].count())
        num_true = float(data_true['user_id'].count())

        magic=pd.merge(data_raw,data_true,on=['user_id','item_id'],how='inner')
        num_pre = magic['user_id'].count()
        p=num_pre/num_raw
        r=num_pre/num_true
        f=(2*p*r)/(p+r)
        print 'Number of hits: %d'%num_pre
        print 'Number of submitting: %d'%num_raw
        #print 'Really data: %d'%num_true
        print 'f: %f%% p:%f%%  r:%f%%  predict:%f' %(f*100,p*100,r*100 ,predict)
        f_add(f,p,r,num_pre,predict)
        predict+=0.001

loop()
print 'total time: %fs!' % (time.time() - time_initial)

frame = pd.DataFrame(data_frame,columns=['F','P','R','HIT','PREDICT'])
print frame.describe()
'''



#用以输出文件
predict = 0.039092

data['prediction_ok'] = data['prediction'].map(lambda x: 1 if x >= predict else 0)
data_ok = data[data['prediction_ok'] == 1]
#print data_ok.describe()
result = data_ok[['user_id', 'item_id']]
result = result.drop_duplicates()

data_fool = pd.read_csv('../res/by_cart/12_04_by_cart.csv')
data_LR = result
print 'initial numbers of data', data_LR['user_id'].count()
merge_cart = pd.merge(data_fool, data_LR, on=['user_id', 'item_id'], how='inner')
print 'after merging,the numbers of data', merge_cart['user_id'].count()

data_raw = merge_cart
data_true = pd.read_csv('../out/validate/true/user_12_05_true_drop_duplicates.csv')
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
print 'f: %f%% p:%f%%  r:%f%%  predict:%f' % (f * 100, p * 100, r * 100, predict)






#merge_cart.to_csv('../out/validate/predict_1205_large.csv',index=None)

