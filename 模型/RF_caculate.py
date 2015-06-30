# coding=utf-8
__author__ = 'tianchuang'
import pandas as pd
import statsmodels.api as sm
import pylab as pl

#F值计算

def caculate_F_function():
    #data_raw = pd.read_csv('../out/user_12_05_RF.csv')
    data_raw = pd.read_csv('../res/user_12_03_12_04_item_subset_merge_separate_a_day.csv')
    data_raw=data_raw[['user_id','item_id']]

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


#caculate_F_function()



def caculate_F(submit_number):
    number_12_19 = 461.0
    submit = submit_number
    correct = 48.0
    P = correct / submit
    R = correct / number_12_19
    F = (2 * P * R) / (P + R)
    print 'Number of hits: %d' % correct
    print 'Number of submitting: %d' % submit
    print 'Really data: %d' % number_12_19
    print 'f: %f%% p:%f%%  r:%f%%' % (F * 100, P * 100, R * 100 )

caculate_F(628)

'''
def caculate_F(submit_number):
    number_12_19=461.0
    submit=submit_number
    correct=30.0
    P=correct/submit
    R=correct/number_12_19
    F=(2*P*R)/(P+R)
    print F

caculate_F(40)
'''
