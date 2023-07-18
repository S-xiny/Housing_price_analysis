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
from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
'''
1 加载数据
'''
import os
os.chdir(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计')
df = pd.read_csv('dataxiaoqu3.csv')
df.dropna(inplace = True)

'''
2 计算指标
'''

data_sale = df[['小区名称','单价','lat','lng']]
data_sale.groupby(by = '小区名称').mean()
data_sale.reset_index(inplace = True)
del data_sale['index']

'''
3 导出数据
'''
data_sale.columns = ['name','price','lat','lng']
data_sale['name'] = data_sale['name'] + " "
data_sale.to_csv('xiaoqudatapro.csv')

'''
4 Qgis处理后加载处理后的数据
'''
data_q3 = pd.read_excel('data_ana.xlsx')
data_q3.fillna(0,inplace = True)

'''
5 标准化处理
'''
def f1(data,col):
    return(data[col]-data[col].min()/(data[col].max()- data[col].min()))

data_q3['路网密度指标'] = f1(data_q3,'长度')
data_q3['离市中心距离'] = ((data_q3['lng'] - (-2224))**2 + (data_q3['lat']- 4342200)**2)**0.5
#计算市中心距离

data_q3_test = data_q3[['路网密度指标','离市中心距离','price_均值']]
data_q3_test = data_q3_test[data_q3_test['price_均值']>0].reset_index()
del data_q3_test['index']

plt.figure(figsize = (15,6))
plt.scatter(data_q3_test['路网密度指标'],data_q3_test['price_均值'], s = 4, alpha=(0.2))
plt.savefig(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\image\路网密度指标与房价的关系.png')

plt.figure(figsize = (15,6))
plt.scatter(data_q3_test['离市中心距离'],data_q3_test['price_均值'], s = 4, alpha=(0.2),color = 'red')
plt.savefig(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\image\离市中心距离与房价的关系.png')
'''
相关性分析
0.3-0.5较相关
'''
data_q3_test.corr().loc['price_均值']

'''
按照市中心距离来分析指标相关性
'''
dis = []
lwmd_person = []
zxjl_person = []

for distance in range(10000,110000,10000):
    datai = data_q3_test[data_q3_test['离市中心距离']<=distance]
    r_value = datai.corr().loc['price_均值']
#    print(r_value)
    dis.append(distance)
    lwmd_person.append(r_value.loc['路网密度指标'])
    zxjl_person.append(r_value.loc['离市中心距离'])
    #添加列表值
    print('离市中心距离小于等于%i米时: ' %distance)
    print('数据量为%i条' %len(datai))
    print('路网密度指标相关性系数为%.3f' %r_value.loc['路网密度指标'])
    print('离市中心指标相关性系数为%.3f' %r_value.loc['离市中心距离'])
    
    
'''
折线图绘制
'''
df_r = pd.DataFrame({'lwmd_person':lwmd_person,
                     'zxjl_person':zxjl_person},
                    index = dis)

source = ColumnDataSource(df_r)

hover = HoverTool(tooltips = [('离市中心距离','@index'),
                              ('路网密度相关系数','@lwmd_person'),
                              ('离市中心距离相关系数','@zxjl_person')
                              ])
output_file('F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\image\cor.html')
p = figure(plot_width = 900, plot_height = 350,
           title = '随着市中心距离增加,不同指标相关性变化',
           tools = [hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
p.line(x = 'index', y='lwmd_person',source = source,line_alpha = 0.8,line_color = 'green', line_dash = [15,4], 
       legend = '道路密度相关系数')

p.circle(x = 'index', y='lwmd_person',source = source,size = 8,color = 'green', line_dash = [15,4], 
       legend = '道路密度相关系数')
p.line(x = 'index', y='zxjl_person',source = source,line_alpha = 0.8,line_color = 'blue', line_dash = [15,4], 
       legend = '中心距离相关系数')

p.circle(x = 'index', y='zxjl_person',source = source,size = 8,color = 'blue', line_dash = [15,4], 
       legend = '中心距离相关系数')


p.legend.location = 'center_right'
show(p)

print('finished!')