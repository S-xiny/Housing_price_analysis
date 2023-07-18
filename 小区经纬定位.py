import time
import pandas as pd
import numpy as np
import json
import requests
import re
from bs4 import BeautifulSoup


def get_loc(data):
    mc = data['小区名称']
    location1 = '天津' + mc
    loc = []
    bases = r"https://restapi.amap.com/v3/geocode/geo?address="+location1+"&output=XML&key=a2d86849d5be62148caf5fd6cce5bf7d"
    for base in bases:
        try:
            response = requests.get(base)
            soupi = BeautifulSoup(response.text,'lxml')
            loc.append(soupi.find('location').text)
            print('成功采集一条位置数据,共采集%i'%(len(loc)))
        except:
            try:
                response = requests.get(base)
                soupi = BeautifulSoup(response.text,'lxml')
                loc.append(soupi.find('location').text)
                print('成功采集一条位置数据,共采集%i'%(len(loc)))
            except:
                print('未成功采集两次，未成功采集的网址为',base)
                loc.append(np.nan)
    return loc

#locationplus = get_loc(data)
#data = pd.DataFrame()
#data['小区名称'] = ['市政府']
#data_use = data
if __name__ == "__main__":
    data = pd.read_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataxiaoqu.xlsx')
    data = data[['单价','小区名称']]
    data_use = data
    locationplus = get_loc(data_use)
    data_use['经纬度'] = locationplus
    data_use['lng'] = data_use['经纬度'].str.split(',').str[0]
    data_use['lat'] = data_use['经纬度'].str.split(',').str[1]
    data_use.to_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataxiaoqu2.xlsx')
    