# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url ='''https://tj.lianjia.com/ershoufang/heping/ 100,
https://tj.lianjia.com/ershoufang/nankai/ 100,
https://tj.lianjia.com/ershoufang/hexi/ 100,
https://tj.lianjia.com/ershoufang/hongqiao/ 100,
https://tj.lianjia.com/ershoufang/xiqing/ 100,
https://tj.lianjia.com/ershoufang/beichen/ 100,
https://tj.lianjia.com/ershoufang/dongli/ 100,
https://tj.lianjia.com/ershoufang/jinnan/ 100,
https://tj.lianjia.com/ershoufang/tanggu/ 100,
https://tj.lianjia.com/ershoufang/kaifaqutj/ 52,
https://tj.lianjia.com/ershoufang/wuqing/ 100,
https://tj.lianjia.com/ershoufang/binhaixinqu/ 100,
https://tj.lianjia.com/ershoufang/baodi/ 100,
https://tj.lianjia.com/ershoufang/jizhou/ 69,
https://tj.lianjia.com/ershoufang/haihejiaoyuyuanqu/ 43,
https://tj.lianjia.com/ershoufang/jinghai/ 26
'''


    
    
def get_urls(urli,n):
    '''
    功能：分页网址url采集
    n:页面参数
    urli:网址
    结果：得到分页网址list
    '''
    lst = []
    for page in range(1,n):
        ui = urli+'pg'+'%i'%page
        lst.append(ui)
    return lst



    

#解析页面
def get_dataurls(ui,d_h,d_c,ips):
    '''

    Parameters
    ----------
    ui :    分页网址.
    d_h :  user-agent信息.
    d_c :  cookies信息

    Returns
    -------
    列表网址.

    '''
    try:
        ri = requests.get(url=ui,headers = d_h, cookies = d_c,proxies=ips,timeout = 3)
    except:
        try:
            ri = requests.get(url=ui,headers = d_h, cookies = d_c,proxies=ips,timeout = 3)
        except:
            print('request failed 2 times')
    #访问页面
    soupi = BeautifulSoup(ri.text,'lxml')
    ul = soupi.find('ul',class_="sellListContent")
    lis = ul.find_all('li')
    lst = []
    for li in lis:
        lst.append(li.find('a')['href'])
    return lst

def get_data(ui,d_h,d_c,ips):
    '''
    

 Parameters
    ----------
    ui :    分页网址.
    d_h :  user-agent信息.
    d_c :  cookies信息


    '''
    try:
        proxies = None
        ri = requests.get(url = ui, headers = d_h, cookies = d_c, verify=False, proxies=ips, timeout=3)
    except:
    # logdebug('requests failed one time')
        try:
            proxies = None
            ri = requests.get(url = ui, headers = d_h, cookies = d_c, verify=False, proxies=ips, timeout=3)
        except:
            # logdebug('requests failed two time')
            print('requests failed two time')
    

        
    
    
    
    soupi = BeautifulSoup(ri.text,'lxml')
    dic = {}#空字典存储数据
    dic['房名'] = soupi.find('div',class_="title").h1.text   
    dic['总价'] = soupi.find('span',class_="total").text + soupi.find('span',class_="unit").text
    dic['单价'] = soupi.find('span',class_="unitPriceValue").text
    dic['户型'] = soupi.find('div', class_="room").div.text
    dic['朝向'] = soupi.find('div',class_="type").div.text
    dic['面积'] = soupi.find('div',class_="area").div.text
    dic['小区名称'] = soupi.find('div',class_="communityName").a.text
    dic['所在区域'] = soupi.find('span',class_="info").text
    infors = soupi.find('div',class_="introContent").text
    
    s = re.sub(r' +','',infors)
    dic['挂牌时间'] = re.search(r'挂牌时间\d+-\d+-\d+', s).group(0)
    position = re.search(r"resblockPosition:'([\d.]+),([\d.]+)'",ri.text)
    
    return dic
   
   


def get_proxies(p_User,p_Pass,p_Host,p_Port):
    '''
    生成动态ip函数
    Parameters
    ----------
    p_Usermp_Pass :
        设置代理服务器.
    p_Host,p_Port : 
        代理服务器验证信息

    Returns
    -------
    ip
    
    '''
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host" : p_Host,
        "port" : p_Port,
        "user" : p_User,
        "pass" : p_Pass,
    }
    ips = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return ips

    

    
if __name__ == "__main__":
    #设置爬取多少页
    
    url_lst = url.strip().split(',')
    url_u = []
    for str in url_lst:
        url_u.append(str.split(' '))
    ip_dic = None
    #设置代理ip
#    ip_dic = get_proxies('123',
#                         '123',
#                         'http-dyn.abuyun.com',
#                         '9020') 

    urllst1 = []
    for url_p in url_u:
        lst_test = get_urls(url_p[0],int(url_p[1]))
        urllst1.extend(lst_test)

    #u1 = urllst1[0]
    dic_h = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'}
    dic_c = {}
    cookies = '''lianjia_uuid=76645c73-49a1-438c-95c2-ee28cb500d5d; UM_distinctid=177eb577f602a6-024a3d39254076-7a667166-144000-177eb577f61680; _smt_uid=603c3f5c.25536a6d; _jzqy=1.1614561116.1614561116.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _ga=GA1.2.1136075548.1614561118; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177eb5781e6324-03916fdd886ac6-7a667166-1327104-177eb5781e73ab%22%2C%22%24device_id%22%3A%22177eb5781e6324-03916fdd886ac6-7a667166-1327104-177eb5781e73ab%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wybeijing%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; _gid=GA1.2.867559070.1614651456; _jzqx=1.1614653279.1614675326.3.jzqsr=tj%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=tj%2Elianjia%2Ecom|jzqct=/ershoufang/; select_city=120000; lianjia_ssid=4b565a7f-28f0-4920-a381-69def72e8786; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1614561141,1614651453,1614739422; CNZZDATA1253477585=1713710079-1614651050-%7C1614737852; CNZZDATA1254525948=1116885174-1614649764-%7C1614736165; CNZZDATA1255633284=80640280-1614649701-%7C1614736106; _jzqa=1.4025737189718715000.1614561116.1614675326.1614739423.6; _jzqc=1; _jzqckmp=1; _qzjc=1; CNZZDATA1255604082=979779749-1614649773-%7C1614739533; login_ucid=2000000156212651; lianjia_token=2.0012573cfd739dccba03fa15ccc218d43b; lianjia_token_secure=2.0012573cfd739dccba03fa15ccc218d43b; security_ticket=q9C8qQhDhwnSb/CQpsneR1kbrQqZ9Az/xHp18h5SKeO7F1TOViWP6fJbYJOQkNrdBitCypzmMOHL9doPLErTpqO74eiF1a9m4Xg6oWUdT6ZzqoWcKlh/fetCxElWI2CqQwVVimhItINdBuCDsuZbKbolon7R18ED0mWUHQ/O0P0=; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1614740786; _jzqb=1.6.10.1614739423.1; _qzja=1.693703322.1614651453707.1614675326242.1614739422909.1614740190787.1614740785929.0.0.0.21.5; _qzjb=1.1614739422909.6.0.0.0; _qzjto=6.1.0; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYmQ0NjJmNjU1NjZmNzE0ODczOGIzZDgwYzFiYTg2YmE0YzI1Y2E3MjRiZWE0ODkyNWE2M2FiOGNiNTRiZjQ1YTMwMzkwYTk4M2Y1YzI1YmFhMDM2YTUxNzk5OWVjOGRhMDhjYWMyODk4NDAzMzI4OTFjNjhkNTk1ZGRkZTIxMzRkYWRkZDdkNWZjZTUyMWYyOWZlMDM3ODhlNjhiMzVlMTE2MzhlZGEyYjA2ZjA5ZjE1NzMxYjFjMTQzNTM1NzZmZDQ4YjZmOTc1YmVjNmRiODNiYmE3MGU0MTdlZTkxMzJmZDI0NTYyOTg0Njc1YmQyMGI0NDRhYmM5ZThhOGE0MTQ2ZTU5MTMzMjc3N2E4MTcxZmQ5NDZlOWM3NTJkZGM1MDFhZmU3OGNhY2ZiYTk0MWY2MjdkMDYyZDAwMjU0YzcwODBlYjYwYWViYTgxZWEwZTIxZDc4ZTQzN2E0Mjk2M1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJmYzQ0ZWNmNVwifSIsInIiOiJodHRwczovL3RqLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcGcxLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'''
    for i in cookies.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
        #获取agent cookies
        
    urllst2 = []

#得到每个房子的网址
    for u in urllst1:
        try:
            urllst2.extend(get_dataurls(u, dic_h, dic_c,ip_dic))
            print('成功采集页面信息，成功采集%i条数据' %(len(urllst2)))
        except:
            print('获取页面信息失败，分页网址位:',u)
       # print(urllst2)  
      
#获取信息  
    errorlst = []    
    datalst = []
    for u in urllst2:
        try:
            datalst.append(get_data(u,dic_h,dic_c,ip_dic))
            print('数据采集成功，总共采集%i条数据' %len(datalst))
        except:
            errorlst.append(u)
            print('采集数据失败，失败网址为',u)


    for u in errorlst:
        try:
            datalst.append(get_data(u,dic_h,dic_c,ip_dic))
            print('数据采集成功，总共采集%i条数据' %len(datalst))
        except:
            errorlst.append(u)
            print('采集数据失败，失败网址为',u)

    data = datalst
    print(12345)    
    datadf = pd.DataFrame(datalst)

    datadf.to_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataultra.xlsx')
 #   pd.DataFrame(errorlst).to_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\errorlst.xlsx')
 #   data_room.to_excel(r'F:\I_love_learning\junior\数据挖掘与数据仓库\课程设计\dataroom.xlsx')
'''
ui = 'https://tj.lianjia.com/ershoufang'
ri = requests.get(url=ui,headers = dic_h, cookies = dic_c)
position = re.search(r"resblockPosition",ri.text)
'''