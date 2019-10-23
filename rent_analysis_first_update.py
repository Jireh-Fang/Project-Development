# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:21:21 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import csv

def get_info(url,headers,start_page,crawl_page):
    #创建一个空的csv文件
    with open(r'E:\python\Crossin编程教室\项目开发\GetRentInfo.csv','w',newline='') as f:
        f.write('')
    #寻找租房信息
    while start_page <= crawl_page:
        html = requests.get(url,headers = headers,timeout = 5 ).text
        soup = BeautifulSoup(html,'lxml')
        info_all = soup.find_all('div',attrs={"class":"content__list--item--main"})
        
        GetRentInfo = []
        for info in info_all:
            infos_p = info.find('p')    #返回p标签下的Tag对象
            zufang_roughlyinfo = infos_p.get_text(strip=True)   #提取p标签下的所有文字 ，租房、地址、房型、方位
            infos_1 = info.find('p',class_="content__list--item--des")
            zufang_type = infos_1.get_text(strip=True)
            infos_span = info.find('span',class_="content__list--item-price")   #返回span标签下的Tag对象
            zufang_price = infos_span.get_text()                        #提取房租价格
            info_2 = info.find('p',class_='content__list--item--bottom oneline').get_text()
            zufang_time = ''
            for i in info_2.split():
                zufang_time += i+'/'            
            title = [zufang_roughlyinfo,zufang_type,zufang_price,zufang_time]
            GetRentInfo.append(title)
        #将数据保存到csv文件中
        with open(r'E:\python\Crossin编程教室\项目开发\GetRentInfo.csv','a+',newline='') as f:
            writer = csv.writer(f)
            for row in GetRentInfo:
                writer.writerow(row)
        start_page += 1

if __name__ == "__main__":
    start_page = 1
    crawl_page = 10
    url = 'https://sh.lianjia.com/zufang/pg{}/#contentList'.format(start_page)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
          'Cookie':'lianjia_uuid=ad0f4a89-aac8-4d37-b3cb-499b9c1310f5; lianjia_ssid=abdb4ceb-fa9c-4e02-8816-8a00dbc7ca08; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjI0NmQyYTIxMGNkMDEzYTBkNzIzNTJhMDU3ZmVmZDZmYjQ2MTMxMDNiNzNlNDVkZDQ2ZDgzMzdmMTRkNzQ3OTViYzlhMzZkZGZmYzMyMWI4MWRjZTgzNDI1ZGRkZDQwYTU4NTE1MmJiNGU4MmU5ZTEyMWNjNDZlMjNlNTdiNzU0OWM3NDkxOWZkY2ExOTFjMmFmYWY3ZjE3ZDcwZjZmYTIyMThkZjM2ODkzYmRjMTQ1ODYwNzg1MGExYzRlZThjNTY4MzAxYzRkZmZhNDI2ZDk0MjBlOGE2ODc2NjhiMjExOGQyZDdjZjQzMTZhZTdhZGVjYzQzYmI3OTc3NDFjZGQ3YzRiNmE1NTRhZDNmYzY0NGVjOGQyMjkyM2M3MDA2NjU1ZjczZTU1MGJkYjRmMTQ1MmYxYzU5ODkzNDUyNDk2MzhiZDY4NmFlMWIzNjZkZGRiNzgzMTQxNmFkZjU2YVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIxNTFkZWQyNVwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL3p1ZmFuZy9wZzEvI2NvbnRlbnRMaXN0Iiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0='}
    get_info(url,headers,start_page,crawl_page)


#数据清洗
import numpy as np
import pandas as pd
names = ['a','b','房价','d']
#文件名有中文，需分两步打开文件
file = open(r'E:\python\Crossin编程教室\项目开发\GetRentInfo.csv')
res = pd.read_csv(file,sep = ',',names = names)

#提取楼层信息
res['楼层'] = res['b'].str.split().str.get(-1)
row_1 = 0
for i in res['楼层']:
    louceng = i[1:-2]
    res['楼层'][row_1]=louceng     #DataFrame是二维数组
    row_1 += 1
#提取面积
row_2 = 0
res['面积'] = res['b'].str.split().str.get(0)
for j in res['面积']:
    sub_res = j.split('/')
    areas = sub_res[1]
    res['面积'][row_2]=areas
    row_2 += 1
#位置优势转换，数值越大表示条件越好
res['位置优势'] = 0
row_3 = 0
for k in res['d']:
    superiority = k.split('/')
    for l in superiority:
        if l == '':
            superiority.remove(l)
    res['位置优势'][row_3] = len(superiority)
    row_3 += 1
#提取朝向
row_4 = 0
res['朝向'] = res['b'].str.split().str.get(0)
for m in res['朝向']:
    sub_res = m.split('/')
    direction = sub_res[2]
    res['朝向'][row_4]=direction
    row_4 += 1
#提取厅室数量
row_5 = 0
res['厅室数量'] = res['b'].str.split().str.get(0)
for n in res['厅室数量']:
    sub_res = n.split('/')
    #有些样本没有厅室信息
    if len(sub_res) <= 3:
        rooms_sum = 0
    else:
        rooms_sum = 0
        rooms = sub_res[3]
        for room in rooms:
            if room.isdigit():       #判断是否为数字
                rooms_sum += int(room)
    res['厅室数量'][row_5] = rooms_sum
    row_5 += 1

# 删除某些不需要的列
res.drop(['a','b','d','朝向'],axis=1,inplace=True)  #去掉列加axis=1，加inplace=True是将删除操作得到的结果赋值给原df本身

#去掉单位
#面积栏
row_6 = 0
for o in res['面积']:
    area_str = ''
    for p in o:
        if p.isdigit():
            area_str += p
            area = int(area_str)
    res['面积'][row_6] = area
    row_6 += 1

#房价栏
row_7 = 0
for q in res['房价']:
    sub_res = q.split('/')
    price_sum = sub_res[0]
    price_str = ''
    for r in price_sum:
        if r.isdigit():
            price_str += r
            price = int(price_str)
    res['房价'][row_7]=price
    row_7 += 1

#把res中所有数据都转换成数值类型
res = res.astype('int')
print(res)