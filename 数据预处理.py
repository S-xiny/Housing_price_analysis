# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 09:28:06 2021

@author: 89344
"""
import time
import pandas as pd
import numpy as np
import json
import requests
import re
from bs4 import BeautifulSoup
def data_cleaning1():
    data = pd.read_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataroom.xlsx')
    data['挂牌时间'] = data['挂牌时间'].str.split('间').str[1]
    data['挂牌时间'] = pd.to_datetime(data['挂牌时间']).dt.date

    location = pd.read_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataxiaoqu2.xlsx')
    #去除\xa0
    data_loc = pd.merge(data,location[['小区名称','lng','lat']],on = '小区名称')
    data['总价'] = data['总价'].str.split('万').str[0].astype('float')
    data['单价'] = data['单价'].str.split('元').str[0].astype('int')
    data['面积'] = data['面积'].str.split('平').str[0].astype('float')
    '''
    m = data['所在区域']
    mresu = []
    for mi in m:
        mi = ''.join(mi.split())
        mresu.append(mi)
    data['所在区域'] = mresu
    data['经纬度'] = get_loc(data)   
    data['lng'] = data['经纬度'].str.split(',').str[0]
    data['lat'] = data['经纬度'].str.split(',').str[1]
    '''
    data.to_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataroom2.xlsx')

'''
def get_loc(data):
    mc = data['所在区域']+ data['小区名称']
    location1 = '天津' + mc
    loc = []
    bases = r"https://restapi.amap.com/v3/geocode/geo?address="+location1+"&output=XML&key=a2d86849d5be62148caf5fd6cce5bf7d"
    for base in bases:
        try:
            response = requests.get(base)
            soupi = BeautifulSoup(response.text,'lxml')
            loc.append(soupi.find('location').text)
            print('成功采集一条位置数据')
        except:
            try:
                response = requests.get(base)
                soupi = BeautifulSoup(response.text,'lxml')
                loc.append(soupi.find('location').text)
                print('成功采集一条位置数据')
            except:
                print('未成功采集两次，未成功采集的网址为',base)
                loc.append(np.nan)
    return loc
'''
if __name__ == "__main__":

    data_cleaning1()