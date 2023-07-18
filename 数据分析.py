# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:23:30 2021

@author: 89344
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

'''
1 加载数据
'''
import os
os.chdir(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计')
df = pd.read_csv('data3.csv')
df.dropna(inplace = True)

'''
2 计算指标
'''

data_sale = df[['小区名称','lat','lng']].groupby(by = '小区名称').mean()
data_sale.reset_index(inplace = True)

'''
3 导出数据
'''
data_sale.columns = ['name','price','lat','lng']
data_sale['name'] = data_sale['name'] + " "
data_sale.to_csv('pro10data.csv')