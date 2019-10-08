# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:54:31 2019

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import csv

def get_info(url,headers,start_page,crawl_page):
    #创建一个空的csv文件
    with open(r'E:\python\Crossin编程教室\Crossincode.v2\GetRentInfo.csv','w',newline='') as f:
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