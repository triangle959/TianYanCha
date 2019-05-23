#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/5/16 12:36
# @Filename :crawl_url.py
import json
import time
import random

import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient



headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
}
# 不带上Cookie就访问不了这个页面
cookie = "aliyungf_tc=AQAAAIub1w4uFgcAikIYdAQzI8dY9mjU; ssuid=6115264187; bannerFlag=undefined; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1558404890; _ga=GA1.2.418827579.1558404891; _gid=GA1.2.1891485528.1558404891; csrfToken=lpQFxeRdjmGjcXoLdq3aGZsV; TYCID=46901ee07b6e11e9be27abfcc402465e; undefined=46901ee07b6e11e9be27abfcc402465e; RTYCID=3893429da45240babd4ebcf58969d8c0; CT_TYCID=4135fc93e4a744efb4baa63d20fbf539; _gat_gtag_UA_123487620_1=1; token=a2e453b73bdb483689cb1e653afc9501; _utm=ec1d80bc6b174ee0b1244b21be75a067; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E7%2599%25BD%25E8%25B5%25B7%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25224%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzQyMjgyMDcyMSIsImlhdCI6MTU1ODU3NDEyMSwiZXhwIjoxNTkwMTEwMTIxfQ.QtfsbeQnO7hclIN8u91-lGGjpA9IAnGD7oV6iUT6X3L-9MASeA2_sg6n3HY1CMuuEs9sXHQibat0Ovm2WGbgkA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213422820721%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzQyMjgyMDcyMSIsImlhdCI6MTU1ODU3NDEyMSwiZXhwIjoxNTkwMTEwMTIxfQ.QtfsbeQnO7hclIN8u91-lGGjpA9IAnGD7oV6iUT6X3L-9MASeA2_sg6n3HY1CMuuEs9sXHQibat0Ovm2WGbgkA; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1558574102; cloud_token=33904acac4d444f694a3f0512fb7ca64; cloud_utm=c9a3948de7934cd9b148c0fca7ddcac3"
# 将上面哪个cookie转化成字典类型
cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}
conn = MongoClient("localhost", 27017)
db = conn['tianyancha']


def get_url(keyword,page):
    global count
    res = requests.get('http://106.13.9.45:8007/pop')
    proxy = json.loads(res.text)
    url= "https://www.tianyancha.com/search/p{}?key={}".format(page, keyword)
    response = requests.get(url, headers=headers, cookies=cookie_dict, proxies=proxy)
    if response.status_code == 200:
        doc = pq(response.text)
        items = doc("#web-content > div > div.container-left > div.search-block.header-block-container > div.result-list.sv-search-container > div").items()
        data = {}
        for item in items:
            #利用图片的填充文本获取公司名字
            img = item("div > div.left-item > div > div.logo.-w88 > img")
            data['name'] = img.attr("alt").replace("<em>", "").replace("</em>", "")
            # 获取公司url
            a = item("div > div.content > div.header > a")
            data['url'] = a.attr("href")
            count = count + 1
            print(data, count)
            yield data
            # 北京知乎科技有限责任公司 https: // www.tianyancha.com / company / 32656967
    else:
        return None

#此方法废除
# def get_page(url):
#     res = requests.get('http://106.13.9.45:8007/pop')
#     proxy = json.loads(res.text)
#     response = requests.get(url, cookies=cookie_dict, proxies=proxy)
#     if response.status_code == 200:
#         doc = pq(response.text)
#         str1 = doc('.tyc-num').text()
#         if str1:
#             print(str1)
#             str2 = fontchange(str1)
#             print(str2)
#         else:
#             text = doc("_container_baseInfo > table.table.-striped-col.-border-top-none.-breakall").text()



def savetomongo(keyword, data):

    dataset = db[keyword]
    dataset.update_one({"name": data['name']},{'$set':data}, True)


if __name__ == "__main__":
    count = 0
    keyword = input("请输入要查找的公司关键字：")
    #没有vip只允许查5页内容，第四页只有18条,其余四页有20条
    page = input("请输入需要爬取的页数：")
    for i in range(1,int(page)+1):
        for data in get_url(keyword,i):
            time.sleep(3)
            savetomongo(keyword,data)



